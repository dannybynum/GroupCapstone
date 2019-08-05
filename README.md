[//]: # (Image References)

[image3]: ./writeup/Veerback-Aug5.PNG "Veerback screenshot"
[image2]: ./writeup/Veeroff-Aug5.PNG "Veeroff screenshot"
[image1]: ./writeup/Waypoints_In_Front_Of_Car.PNG "Simulator Screenshot with code updates from first walk-thru video"

# Group Capstone Project
From Self-Driving Car Engineer Nanodegree Program

---

## Update Aug-5.  Updated the dbw_node.py and twist_controller.py files under /twist_controller

Now when I unclick the "manual" button the car accelerates but it veers off of the line pretty quickly - see picture below
![alt text][image2]

Eventually the car does try to steer back towards the trajectory, but way overshoots it.  Could be several errors.  For starters I'm going to go research why the trajectory isn't getting updated - the path should only show points in FRONT of the vehicle and for some reason this path is static and doesn't get updated.  I'm going to go back to the "waypoint_updater.py" file and walk-through and see what I missed.  May be tomorrow morning, Tues Aug-6 at ~9am EDT (Detroit time) before my next update.
![alt text][image3]


Veerback-Aug5

## Initial update -- updated the "waypoint_updater.py" with the suggestions from the walk-through video.  Here is a screenshot of the simulator with the waypoints now being published and shown there.
![alt text][image1]
