import rclpy
import re
from rclpy.node import Node
from geometry_msgs.msg import Point
import cv2
import depthai as dai
from pupil_apriltags import Detector

# EVALUATION_NODE = "APRILTAG" or "RGB_FACE"
# former is AprilTag detection, latter is RGB w/o depth
EVALUATION_MODE = "APRILTAG" 

class MasterVisionNode(Node):
    def __init__(self):
        super().__init__('master_vision_node')
        self.error_pub = self.create_publisher(Point, '/gimbal_error', 10)
        
        # tools
        self.at_detector = Detector(families='tag36h11')
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # pipeline for RGB vision - runs on DepthAI V3
        self.pipeline = dai.Pipeline()
        
        # unified camera node
        camRgb = self.pipeline.create(dai.node.Camera).build()
        
        # request 640x480 BGR Interleaved output for OpenCV
        cam_out = camRgb.requestOutput((640, 480), type=dai.ImgFrame.Type.BGR888i)

        self.get_logger().info(f"Booting OAK-D Lite in {EVALUATION_MODE} mode...")
        
        # OCV3 creates the USB bridge directly from the output !!! NOT like V2
        self.qRgb = cam_out.createOutputQueue(maxSize=4, blocking=False)
        
        # start pipeline directly (Replaces "with dai.Device()")
        self.pipeline.start()
        
        self.timer = self.create_timer(0.05, self.process_frame)

    def process_frame(self):
        if not self.pipeline.isRunning(): return
        
        inRgb = self.qRgb.tryGet()
        if inRgb is None: return
        
        frame = inRgb.getCvFrame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        screen_center_x, screen_center_y = 320.0, 240.0 
        target_found = False
        error_x, error_y = 0.0, 0.0
        
        # ------------------------------------------
        # MODALITY 1: APRILTAG
        # ------------------------------------------
        if EVALUATION_MODE == "APRILTAG":
            tags = self.at_detector.detect(gray)
            if len(tags) > 0:
                try:
                    # 1. regex ctrl+f for frame center
                    # dump raw memory into a string
                    raw_memory_dump = str(tags)
                    
                    # regex search: Find "center = [...", grab two numbers, ignore else
                    match = re.search(r'center\s*=\s*\[\s*([\d\.\-]+)\s*,?\s*([\d\.\-]+)\s*\]', raw_memory_dump)
                    
                    if match:
                        tag_center_x = float(match.group(1))
                        tag_center_y = float(match.group(2))
                    else:
                        raise ValueError("Regex failed to find center coordinates.")

                    # 2. gimbal calcs
                    # set screen center
                    screen_center_x = 320.0
                    screen_center_y = 240.0
                    
                    #calc diff from screen center
                    error_x = screen_center_x - tag_center_x
                    error_y = screen_center_y - tag_center_y
                    target_found = True
                    
                    # 3. visual rep
                    cv2.circle(frame, (int(tag_center_x), int(tag_center_y)), 5, (0, 0, 255), -1)
                    cv2.line(frame, (int(screen_center_x), int(screen_center_y)), (int(tag_center_x), int(tag_center_y)), (0, 255, 0), 2)
                    cv2.putText(frame, "AprilTag Locked", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                except Exception as e:
                    self.get_logger().error(f"Failsafe Triggered: {e}")

        # ------------------------------------------
        # MODALITY 2: RGB
        # ------------------------------------------
        elif EVALUATION_MODE == "RGB_FACE":
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(faces) > 0:
                #if face, extract pos
                (x, y, w, h) = faces[0] 
                face_center_x = x + (w / 2.0)
                face_center_y = y + (h / 2.0)
                
                error_x = screen_center_x - face_center_x
                error_y = screen_center_y - face_center_y
                target_found = True
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.line(frame, (int(screen_center_x), int(screen_center_y)), (int(face_center_x), int(face_center_y)), (0, 255, 0), 2)
                cv2.putText(frame, "RGB Face Locked", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # ------------------------------------------
        # PUBLISH/RENDER
        # ------------------------------------------
        if target_found:
            msg = Point()
            msg.x = error_x
            msg.y = error_y
            self.error_pub.publish(msg)

        # !!! MUST be completely unindented from the IF above
        cv2.imshow("OAK-D Master Vision", frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(MasterVisionNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()