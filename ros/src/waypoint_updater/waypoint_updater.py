#!/usr/bin/env python

#################################################
# File/Revision History
# Modified by Danny Bynum, Aug-4 at 11am ET
# Updated by Danny Bynum, Aug-9 at 522pm ET
# Updated DB Aug-11 at 7am ET
##################################################

import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint
import math

#New libraries added from Walk-Thru-Video
import numpy as np
from scipy.spatial import KDTree
from std_msgs.msg import Int32

'''
This node will publish waypoints from the car's current position to some `x` distance ahead.

As mentioned in the doc, you should ideally first implement a version which does not care
about traffic lights or obstacles.

Once you have created dbw_node, you will update this node to use the status of traffic lights too.

Please note that our simulator also provides the exact location of traffic lights and their
current status in `/vehicle/traffic_lights` message. You can use this message to build this node
as well as to verify your TL classifier.

TODO (for Yousuf and Aaron): Stopline location for each traffic light.
'''

LOOKAHEAD_WPS = 50 # Number of waypoints we will publish. You can change this number
MAX_DECEL = .5 #added from Full Waypoint walkthru Aug-7

'''
From walk-thru video - Waypoint Updater Partial Walkthrough
Note for part 1 the whole goal is to "take a chunk of the base waypoints and use the first 200
of them that are in front of the car as reference
'''


class WaypointUpdater(object):
    def __init__(self):
        rospy.init_node('waypoint_updater')

        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)
        rospy.Subscriber('/traffic_waypoint', Int32, self.traffic_cb)

        # TODO: Add a subscriber for /traffic_waypoint and /obstacle_waypoint below


        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)

        # TODO: Add other member variables you need below
        # Added from walk-thru
        self.pose = None
        self.stopline_wp_idx = -1
        self.base_waypoints = None
        self.waypoints_2d = None
        self.waypoint_tree = None

        self.loop()
        #rospy.spin()
    
    #added from walkthru
    def loop(self):
        rate = rospy.Rate(35)
        while not rospy.is_shutdown():
            #modified on Aug-19
            if self.pose and self.base_waypoints and self.waypoint_tree:
                #Get closest waypoint
                #closest_waypoint_idx = self.get_closest_waypoint_idx()
                self.publish_waypoints()
            rate.sleep()
    
    #added from walk_thru        
    def get_closest_waypoint_idx(self):
        x = self.pose.pose.position.x
        y = self.pose.pose.position.y
        #modified on Aug-19
        #if not None in (self.waypoint_tree):
        #if not self.waypoint_tree:
        #	closest_idx = self.waypoint_tree.query([x,y], 1)[1]
        #else:
        #	closest_idx = 0

        closest_idx = self.waypoint_tree.query([x,y], 1)[1]
        
        #Check if closest is ahead or behind vehicle
        closest_coord = self.waypoints_2d[closest_idx]
        prev_coord = self.waypoints_2d[closest_idx-1]
        
        #Equation for hyperplane through closest_coords
        cl_vect = np.array(closest_coord)
        prev_vect = np.array(prev_coord)
        pos_vect = np.array([x,y])
        
        #dot product between two vectors
        #figuring out of the wapoint coordinate is in front of the vehicle or behind the vehicle
        val = np.dot(cl_vect-prev_vect, pos_vect-cl_vect)
        
        if val > 0:
            closest_idx = (closest_idx +1) % len(self.waypoints_2d)
        
        return closest_idx

    #added from Full video walk-thru Aug-7
    def decelerate_waypoints(self, waypoints, closest_idx):
        temp_waypoints = []  #note - preserving base_waypoints
        for i, wp in enumerate(waypoints):
            p = Waypoint()
            p.pose = wp.pose
            
            stop_idx = max(self.stopline_wp_idx - closest_idx - 3,0) #video says 2, I'm using 3
            dist = self.distance(waypoints, i, stop_idx)
            vel = math.sqrt(2*MAX_DECEL*dist)  #FIXME, video indicates this could be imporoved
            if vel < 1.:
                vel = 0.
            
            p.twist.twist.linear.x = min(vel, wp.twist.twist.linear.x)
            temp_waypoints.append(p)
        
        return temp_waypoints

    
    def generate_lane(self):
        lane = Lane()
        closest_idx = self.get_closest_waypoint_idx()
        # using Python slicing to publish the points in front of us - 
        # starting with the index we determined plus the number of points we want to use
        #lane.waypoints = self.base_waypoints.waypoints[closest_idx:closest_idx + LOOKAHEAD_WPS]

        base_waypoints = self.base_waypoints.waypoints[closest_idx:closest_idx + LOOKAHEAD_WPS]

        if (self.stopline_wp_idx == -1) or (self.stopline_wp_idx>= closest_idx + LOOKAHEAD_WPS):
            lane.waypoints = base_waypoints
            #lane.waypoints = self.base_waypoints.waypoints[closest_idx:closest_idx + LOOKAHEAD_WPS]
        else:
            lane.waypoints = self.decelerate_waypoints(base_waypoints, closest_idx)
            #lane.waypoints = base_waypoints
            #lane.waypoints = self.base_waypoints.waypoints[closest_idx:closest_idx + LOOKAHEAD_WPS]
            #lane.waypoints = self.decelerate_waypoints(base_waypoints, closest_idx)
   

        return lane

    

    #added from walk-thru
    def publish_waypoints(self):

        final_lane = self.generate_lane()
        #lane = Lane()
        #making the header the same - comment that maybe this isn't even needed
        #lane.header = self.base_waypoints.header
        final_lane.header = self.base_waypoints.header
        
        # using Python slicing to publish the points in front of us - 
        # starting with the index we determined plus the number of points we want to use
        #lane.waypoints = self.base_waypoints.waypoints[closest_idx:closest_idx + LOOKAHEAD_WPS]
        self.final_waypoints_pub.publish(final_lane)



    def pose_cb(self, msg):
        # TODO: Implement
        self.pose = msg   #added from walk-thru
        # pass

    #Note - from walk-thru - This is a latched subscriber - so this is only sent once
    def waypoints_cb(self, waypoints):
        # TODO: Implement
        self.base_waypoints = waypoints
        #making sure self.waypoints_2d is initialized
        if not self.waypoints_2d:
            self.waypoints_2d = [[waypoint.pose.pose.position.x, waypoint.pose.pose.position.y] for waypoint in waypoints.waypoints]  #FIXME not sure how this line ends, was cutoff in video :-)
            self.waypoint_tree = KDTree(self.waypoints_2d)
                              
        #pass

    def traffic_cb(self, msg):
        # TODO: Callback for /traffic_waypoint message. Implement
        #pass
        self.stopline_wp_idx = msg.data

    def obstacle_cb(self, msg):
        # TODO: Callback for /obstacle_waypoint message. We will implement it later
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist


if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')
