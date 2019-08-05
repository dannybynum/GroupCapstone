[//]: # (Image References)

[image3]: ./writeup/Veerback-Aug5.PNG "Veerback screenshot"
[image2]: ./writeup/Veeroff-Aug5.PNG "Veeroff screenshot"
[image1]: ./writeup/Waypoints_In_Front_Of_Car.PNG "Simulator Screenshot with code updates from first walk-thru video"

# Group Capstone Project
From Self-Driving Car Engineer Nanodegree Program

---

## Notes regarding changes from suggestions in walk-thru
If we make changes away from what was recommended in the video walk-thru then suggest we list them here so that team members can easily follow the code and changes or additions we may make from the suggestions.

Aug-5, I removed the "fuel_capacity" from the files twist_controller.py and dbw_node.py -- this was not used and decided it would help me learn by making a small modification from suggestions in the video


## Update Aug-5.  Updated the dbw_node.py and twist_controller.py files under /twist_controller

Now when I unclick the "manual" button the car accelerates but it veers off of the line pretty quickly - see picture below
![alt text][image2]

Eventually the car does try to steer back towards the trajectory, but way overshoots it.  Could be several errors.  For starters I'm going to go research why the trajectory isn't getting updated - the path should only show points in FRONT of the vehicle and for some reason this path is static and doesn't get updated.  I'm going to go back to the "waypoint_updater.py" file and walk-through and see what I missed.  May be tomorrow morning, Tues Aug-6 at ~9am EDT (Detroit time) before my next update.
![alt text][image3]


Veerback-Aug5

## Initial update -- updated the "waypoint_updater.py" with the suggestions from the walk-through video.  Here is a screenshot of the simulator with the waypoints now being published and shown there.
![alt text][image1]
