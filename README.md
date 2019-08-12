[//]: # (Image References)
[image5]: ./writeup/SimStopsAtRedLights.PNG "Sim Car Now Stops at Red Lights"
[image4]: ./writeup/SimLagFixed.PNG "Sim Lag Fixed Screenshot"
[image3]: ./writeup/Veerback-Aug5.PNG "Veerback screenshot"
[image2]: ./writeup/Veeroff-Aug5.PNG "Veeroff screenshot"
[image1]: ./writeup/Waypoints_In_Front_Of_Car.PNG "Simulator Screenshot with code updates from first walk-thru video"



# Group Capstone Project
From Self-Driving Car Engineer Nanodegree Program

## Three team members as follows:
Team Lead:  Danny Bynum: email witheld

Member:  Bob Ding:  email witheld

Member:  Minbo Tan:  email witheld

---


## Update Aug-12, bob, 12 am PT - updates on real model 
* updated the classifier portion for real traffic light detection. Now it can detect both red/green light with the provided bag files. 

## Update Aug-11, DWB, 7am ET - updates on testing and minor code changes
* made minor change in waypoint_updater.py (deleted some code I was using for tshooting)

* I tested that the "velocity" parameter is respected/followed -- changed the launch\waypoint_loader.launch file velocity parameter as follows `<param name="velocity" value="10" />  <!-- DWB Aug-11 change to 10 and 100 for testing purposes -->`

* I tested out the 2nd track in the simulator the "test lot" by swaping which of these lines was commented out in the launch\waypoint_loader.launch file.  The car drove around - but looks to me like it only drove around about half of the track so I will research this some more.
```     
<!--<param name="path" value="$(find styx)../../../data/wp_yaw_const.csv" /> -->
<param name="path" value="$(find styx)../../../data/churchlot_with_cars.csv" /> 
```

* I did a code inspection to make sure I believe the car will reset its PID controllers when run on the real course - added a note to the twist_controller.py file to indicate where this is covered.

* **We're ready to submit from my perspective** - once Bob confirms that the code works in real mode and that he is ready to submit then I will do the submission.  For other members (Minbo and Rakshith) I am currently not able to include you on the team submission, but please see email I sent and respond to that letting me know progress and contribution/plans.


## Update Aug-9, 720 pm PT - add initial real traffic light inference model support

This verion is based on the lastest from origin.  
* real classifier model change when launch with roslaunch launch/site.launch. Added param in tl_detector launch file
* twist_controller launch folder and makefile

In simulation mode this works ok for run(green light) and stop(red light). For real mode this has not been verified yet. So please don't run site launch yet.

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
