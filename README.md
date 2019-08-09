[//]: # (Image References)
[image5]: ./writeup/SimStopsAtRedLights.PNG "Sim Car Now Stops at Red Lights"
[image4]: ./writeup/SimLagFixed.PNG "Sim Lag Fixed Screenshot"
[image3]: ./writeup/Veerback-Aug5.PNG "Veerback screenshot"
[image2]: ./writeup/Veeroff-Aug5.PNG "Veeroff screenshot"
[image1]: ./writeup/Waypoints_In_Front_Of_Car.PNG "Simulator Screenshot with code updates from first walk-thru video"



# Group Capstone Project
From Self-Driving Car Engineer Nanodegree Program

---

## Notes regarding changes from suggestions in walk-thru
If we make changes away from what was recommended in the video walk-thru then suggest we list them here so that team members can easily follow the code and changes or additions we may make from the suggestions.

Aug-5, I removed the "fuel_capacity" from the files twist_controller.py and dbw_node.py -- this was not used and decided it would help me learn by making a small modification from suggestions in the video


## Update Aug-9, 615pm ET - Car now stops at traffic lights (in simulator) 

It Works (see image below)!!!! I finally fixed the error(s) in `waypoint_updater.py` and now the car stops at traffic lights.  I tested using a modified `tl_detector.py` file on my local copy so that only uses the ground-truth information (does not use the classifier) -- I did this because processing images in the sim is very laggy with my setup.  In the repo this file is `tl_detector_danny_testonly.py`.

Bob - please update to the latest waypoint_updater.py on your system and let me know if it works end2end now for you when using the traffic classifier.

I haven't checked out anything on the second track yet but I plan to do that this weekend (Sunday) and maybe we'll be ready to submit by then.

![alt text][image5]


## Update Aug-8 10 PT - merged ROS folder and added traffic classifier 

* Classifier and trained inference model for simulation environment added. 
* Arranged folder structure follow Udacity provided template.
* Copied waypoint_updater_Aug8_Fullwalkthru_NotWorking.py to waypoint_updater.py and launch folder
* A few minor changes to tl_detector.py to match newly added code
* Added traffic light classifier, freeze inference model and verified in local PC(TF-GPU 1.4) 
* Real site model will take another day to be trained and merged.


## Update Aug-8.  Thanks to Bob I found out the "bug" was really just a lag issue - changed number of waypoints to 25 and reduced rospy update frequency to 31 and works now!!  

Very minor code change made to waypoint_updater.py - and now works in the simulator - screenshot below!  Now on to work on the traffic light recognition part and will tie that back into the waypoint_updater later (possibly this weekend)
![alt text][image4]


## Update Aug-5.  Updated the dbw_node.py and twist_controller.py files under /twist_controller


Now when I unclick the "manual" button the car accelerates but it veers off of the line pretty quickly - see picture below
![alt text][image2]

Eventually the car does try to steer back towards the trajectory, but way overshoots it.  Could be several errors.  For starters I'm going to go research why the trajectory isn't getting updated - the path should only show points in FRONT of the vehicle and for some reason this path is static and doesn't get updated.  I'm going to go back to the "waypoint_updater.py" file and walk-through and see what I missed.  May be tomorrow morning, Tues Aug-6 at ~9am EDT (Detroit time) before my next update.
![alt text][image3]


Veerback-Aug5

## Initial update -- updated the "waypoint_updater.py" with the suggestions from the walk-through video.  Here is a screenshot of the simulator with the waypoints now being published and shown there.
![alt text][image1]
