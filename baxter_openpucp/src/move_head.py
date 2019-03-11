#!/usr/bin/env python
import sys
import rospy
import baxter_interface
from std_msgs.msg import Float64
from baxter_interface import CHECK_VERSION


if __name__ == '__main__':

    rospy.init_node("Head_control")

    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled

    def clean_shutdown():
        print("\nExiting example...")
        if not init_state:
            print("Disabling robot...")
            rs.disable()
    rospy.on_shutdown(clean_shutdown)

    rs.enable()
    rospy.loginfo("Robot enable")

    head = baxter_interface.Head()
    head.set_pan(-1.0, 0.06)


