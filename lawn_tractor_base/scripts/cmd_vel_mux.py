#!/usr/bin/python
"""
Source:
https://github.com/danielsnider/URC/blob/master/rosws/src/rover_drive/src/cmd_vel_muxer.py
"""
import rospy
import time
import geometry_msgs.msg

auto_timeout = 0
dt = time.time()

rospy.init_node("cmd_vel_mux")
pub = rospy.Publisher("/cmd_vel_mux/safe_check", geometry_msgs.msg.Twist, queue_size=10)


def on_auto_data(data):
    data = data # type: geometry_msgs.msg.Twist
    global auto_timeout, dt
    dtt = time.time() - dt
    dt = time.time()
    auto_timeout -= dtt
    data.linear.x = data.linear.x
    data.angular.z = data.angular.z
    if auto_timeout <= 0:
        auto_timeout = 0
        pub.publish(data)


def on_twist(data):
    global auto_timeout, dt
    dt = time.time()
    auto_timeout = 5
    pub.publish(data)


rospy.Subscriber("/cmd_vel_mux/move_base", geometry_msgs.msg.Twist, callback=on_auto_data)
rospy.Subscriber("/cmd_vel_mux/teleop", geometry_msgs.msg.Twist, callback=on_twist)
rospy.spin()