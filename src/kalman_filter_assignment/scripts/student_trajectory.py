#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import math

def get_trajectory(student_name):
    name_hash = sum(ord(c) for c in student_name) % 3

    if name_hash == 0:
        # Circle
        def circle():
            rate = rospy.Rate(10)
            while not rospy.is_shutdown():
                yield (0.2, 0.2)
                rate.sleep()
        return circle()
    elif name_hash == 1:
        # Square
        def square():
            rate = rospy.Rate(10)
            t0 = rospy.Time.now().to_sec()
            while not rospy.is_shutdown():
                t = rospy.Time.now().to_sec() - t0
                # Every 5 seconds, turn 90 deg in 1 second
                if int(t) % 5 == 0:
                    angular = math.pi/2
                else:
                    angular = 0.0
                yield (0.2, angular)
                rate.sleep()
        return square()
    else:
        # Figure 8
        def figure8():
            rate = rospy.Rate(10)
            t0 = rospy.Time.now().to_sec()
            while not rospy.is_shutdown():
                t = rospy.Time.now().to_sec() - t0
                yield (0.2, 0.4 * math.sin(0.5 * t))
                rate.sleep()
        return figure8()

if __name__ == "__main__":
    rospy.init_node("student_trajectory_node")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    student_name = rospy.get_param("~student_name", "student")
    traj_gen = get_trajectory(student_name)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        linear_vel, angular_vel = next(traj_gen)
        msg = Twist()
        msg.linear.x = linear_vel
        msg.angular.z = angular_vel
        pub.publish(msg)
        rate.sleep()

