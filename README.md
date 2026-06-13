# UCSD ECEMAE148 Team 10 Final Project 

<img src="READMEassets/ucsd_ros2_logos.png">

<div>

<div id="top"></div>

<h1 align="center">OakDLite Gimble Camera & Detection Method Comparisons</h1>
<h4 align="center"></h4>
<!-- PROJECT LOGO -->:
<br />
<div align="center">

<h3>ECE/MAE 148 Final Project</h3>
<p>
Team 10 Winter 2025
</p>

<img src="robocar.jpg">

</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#team-members">Team Members</a></li>
    <li><a href="#final-project">Final Project</a></li>
      <ul>
        <li><a href="#original-goals">Original Goals</a></li>
          <ul>
            <li><a href="#goals-we-met">Goals We Met</a></li>
            <li><a href="#our-hopes-and-dreams">If We Have Another Week...</a></li>
              <ul>
                <li><a href="#stretch-goal-1">Stretch Goal 1</a></li>
                <li><a href="#stretch-goal-2">Stretch Goal 2</a></li>
              </ul>
          </ul>
        <li><a href="#final-project-documentation">Final Project Documentation</a></li>
      </ul>
    <li><a href="#robot-design">Robot Design </a></li>
      <ul>
        <li><a href="#cad-parts">CAD Parts</a></li>
          <ul>
            <li><a href="#final-assembly">Final Assembly</a></li>
            <li><a href="#custom-designed-parts">Custom Designed Parts</a></li>
            <li><a href="#open-source-parts">Open Source Parts</a></li>
          </ul>
        <li><a href="#electronic-hardware">Electronic Hardware</a></li>
          <ul>
            <li><a href="#embedded-systems">Embedded Systems</a></li>
            <li><a href="#ros2">ROS2</a></li>
            <li><a href="#donkeycar-ai">DonkeyCar AI</a></li>
          </ul>
      </ul>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- TEAM MEMBERS -->
## Team Members

<h4>Team Member Major and Class </h4>
<ul>
  <li>Melvin Y - Mechanical Engineering - Class of 2028</li>
  <li>Youngyen L - Mechanical Engineering - Class of 2026</li>
  <li>Yuxian X - Electrical Engineering - Class of 2026</li>
</ul>

<!-- Final Project -->
## Final Project
<!-- put stuff here -->

<!-- Original Goals -->
### Original Goals
Team 10’s project focuses on the integration of a gimbaled OAK-D Lite to the basic MAE/ECE 148 robot car platform. This would enable a source of vision that is independent of the car’s chassis or direction of travel. Furthermore, we also wanted to compare the computer vision detection options between RGB video, RBG video w/ depth perception (RGB-D), ArUco Markers/AprilTags, and a combination of these three.
   
<!-- End Results -->
### Goals We Met
<p>
 We were able to get the gimbal working, as well as having the camera and gimbal communicate with each other, and tracking the AprilTags. We were also able to test between RGB video and AprilTags and were able to compare their Mean Absolute Error, Root Mean Squared Error, and Jitter.
</p>

<p>
  temp
  <img src="oakD_detection.png">
</p>
<p>
  temp
</p>


### If We Have Another Week...
#### Goal 1
temp
#### Goal 2
temp
## Final Project Documentation

<!-- Early Quarter -->
### Robot Design CAD and Parts
<!--<img src="/media/full%20car%20cad.png" width="400" height="300" />-->

#### Modeled Ourselves
| Part | CAD Model |
|------|--------|
| Servo Mount | <a href="CAD/ServoMount.stl"> ServoMount.stl |
| Lidar Mount | <a href="CAD/LidarMount.stl"> LidarMount.stl |
| BasePlate | <a href="CAD/BasePlateMount.stl"> BasePlateMount.stl |

#### Open Source Parts
| Part | CAD Model | Source |
|------|--------|-----------|
| Gimbal | <img src="" /> | [RobotShop](https://www.robotshop.com/products/lynxmotion-pan-and-tilt-kit-aluminium?pr_prod_strat=e5_desc&pr_rec_id=165fcfb55&pr_rec_pid=7487360368801&pr_ref_pid=7487361974433&pr_seq=uniform)|
| Servo | <img src="" /> | [Amazon](https://www.amazon.com/Digital-Waterproof-Compatible-Crawler-Control/dp/B0C6LVX73M?th=1) |

### Software


### How to Run


Slides are also published onto this repository.

<!-- Authors -->
## Authors

Melvin Yu, Yushan X, Youngyen L


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

*Big thanks to Professor Jack Silberman, our TA Jose and Winston Chou, and thank you Jose and Winston for the ReadMe Templates!


<!-- CONTACT -->
## Contact

* Melvin Yu | mey009@ucsd.edu
* Yushan X | y1xian@ucsd.edu@ucsd.edu 
* Youngyen L | yol064@ucsd.edu@ucsd.edu
