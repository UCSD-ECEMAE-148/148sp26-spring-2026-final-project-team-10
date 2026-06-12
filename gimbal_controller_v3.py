import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point

# 1. THE NEW I2C HARDWARE LIBRARY
import Adafruit_PCA9685

class GimbalNode(Node):
    def __init__(self):
        super().__init__('gimbal_node')
        self.error_sub = self.create_subscription(Point, '/gimbal_error', self.error_callback, 10)
        
        self.current_pan = 0.0
        self.current_tilt = 0.0
        
        # PID Tuning
        self.Kp_pan = 0.02
        self.Kp_tilt = 0.02
        
        # ==========================================
        # 2. I2C HARDWARE SETUP (PCA9685)
        # ==========================================
        try:
            # Initialize the I2C driver on the default address (0x40)
            self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
            
            # Standard hobby servos run at 50Hz (20ms cycles)
            self.pwm.set_pwm_freq(50)
            
            # Move to center on boot (Channel 0 = Pan, Channel 1 = Tilt)
            self.set_servo_angle(0, 0.0)
            self.set_servo_angle(1, 0.0)
            
            self.get_logger().info("Gimbal Controller Online. PCA9685 I2C connected!")
        except Exception as e:
            self.get_logger().error(f"Failed to connect to I2C driver: {e}")

    def set_servo_angle(self, channel, angle):
        """
        Translates a human angle (-90 to +90) into I2C ticks (0 to 4095)
        """
        # --- HARDWARE CALIBRATION ---
        # These numbers define the physical limits of your servos.
        # If your servos grind at the edges, increase the min or decrease the max.
        servo_min = 150  # Tick count for -90 degrees
        servo_max = 600  # Tick count for +90 degrees
        
        # 1. Normalize the angle from (-90 to +90) to (0 to 180)
        norm_angle = angle + 90.0
        
        # 2. Map the 0-180 degree scale to the 150-600 tick scale
        pulse = int(servo_min + (norm_angle / 180.0) * (servo_max - servo_min))
        
        # 3. Send the command over I2C
        self.pwm.set_pwm(channel, 0, pulse)

    def error_callback(self, msg):
        # Convert pixel error to servo degrees
        self.current_pan += (msg.x * self.Kp_pan)
        self.current_tilt += (msg.y * self.Kp_tilt)
        
        # Physical limits (Clamped to +/- 90 degrees)
        self.current_pan = max(min(self.current_pan, 90.0), -90.0)
        self.current_tilt = max(min(self.current_tilt, 90.0), -90.0)
        
        # ==========================================
        # 3. MOVE THE I2C HARDWARE
        # ==========================================
        if hasattr(self, 'pwm'):
            # Assuming Pan servo is plugged into slot 0, Tilt into slot 1
            self.set_servo_angle(0, self.current_pan)
            self.set_servo_angle(1, self.current_tilt)
        
        self.get_logger().info(f"TRACKING -> Pan: {self.current_pan:.2f} deg | Tilt: {self.current_tilt:.2f} deg")

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(GimbalNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()