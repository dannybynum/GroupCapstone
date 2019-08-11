#added from video-walk-thru Aug-5
from pid import PID
from lowpass import LowPassFilter
from yaw_controller import YawController
import rospy

GAS_DENSITY = 2.858
ONE_MPH = 0.44704

#modified class Controller per video walk-thru on Aug-5
class Controller(object):
    #def __init__(self, vehicle_mass, fuel_capacity, brake_deadband, decel_limit,  #remove fuel capacity
    def __init__(self, vehicle_mass, brake_deadband, decel_limit,
                 accel_limit, wheel_radius, wheel_base, steer_ratio, max_lat_accel, max_steer_angle):
        # TODO: Implement
        self.yaw_controller = YawController(wheel_base, steer_ratio, 0.1, max_lat_accel, max_steer_angle)
        
        #parameters from video walk-thru, determined experimentally
        kp = 0.3
        ki = 0.1
        kd = 0.
        mn = 0.
        mx = 0.2
        self.throttle_controller = PID(kp, ki, kd, mn, mx)
        
        tau = 0.5  #note says 1/(2pi*tau) = cutoff frequency
        ts = .02   #note says Sample time
        self.vel_lpf = LowPassFilter(tau, ts)
        
        self.vehicle_mass = vehicle_mass
        #self.fuel_capacity = fuel_capacity   #commenting out fuel_capacity, video stated not needed
        self.brake_deadband = brake_deadband
        self.decel_limit = decel_limit
        self.accel_limit = accel_limit
        self.wheel_radius = wheel_radius
        
        self.last_time = rospy.get_time()

    #Added From Video Walk-Thru, DWB Aug-5
    def control(self, current_vel, dbw_enabled, linear_vel, angular_vel):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer

        # Danny Note on Aug-11 - this is just using the code from the video walkthru, and
        # I believe this will properly reset the the PID controller if dbw_enabled is toggled during real testing
        if not dbw_enabled:
            self.throttle_controller.reset()
            return 0., 0., 0.
        
        current_vel = self.vel_lpf.filt(current_vel)
        
        #Some debug comments were inserted here - see video on 8.DBW Walkthrough at 7:42
        
        steering = self.yaw_controller.get_steering(linear_vel, angular_vel, current_vel)
        
        vel_error = linear_vel - current_vel
        self.last_vel = current_vel
        
        current_time = rospy.get_time()
        sample_time = current_time - self.last_time
        self.last_time = current_time
        
        throttle = self.throttle_controller.step(vel_error, sample_time)
        brake = 0
        
        if linear_vel == 0. and current_vel <0.1:
            throttle = 0
            brake = 701  #lesson recommends 700 N*m to prevent roll-forward from stop, video walkthru used 400
        elif throttle < .1 and vel_error <0:
            throttle = 0
            decel = max(vel_error, self.decel_limit)
            brake = abs(decel)*self.vehicle_mass*self.wheel_radius #equation to get Torque in N*m
            
        return throttle, brake, steering
            
        
        
        return 1., 0., 0.
