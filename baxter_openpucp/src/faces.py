#!/usr/bin/env python
import os
import sys
import cv2
import rospy
import cv_bridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

def display_image(msg):
  image = msg.data  
  
  if(image=="normal"):
    pub.publish(normal)
    rospy.loginfo("Showing normal eyes")
    rospy.sleep(1)
  elif(image=="rwink"):
    pub.publish(rwink)
    rospy.loginfo("Showing right eye wink")
    rospy.sleep(1)
  elif(image=="lwink"):
    pub.publish(lwink)
    rospy.loginfo("Showing left eye wink")
    rospy.sleep(1)
  elif(image=="blink"):
    pub.publish(blink)
    rospy.loginfo("Showing blink eyes")
    rospy.sleep(1)
  elif(image=="flushed"):
    pub.publish(flushed)
    rospy.loginfo("Showing flushed face")
    rospy.sleep(1)
  else:
    rospy.loginfo("Image's name not valid")

if __name__ == '__main__':
  rospy.init_node('Display_controller')
  rospy.Subscriber('faces', String, display_image)
  pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
  
  img = cv2.imread('/home/alex/tryout_ws/src/baxter_openpucp/images/normal.png')
  normal = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
  img = cv2.imread('/home/alex/tryout_ws/src/baxter_openpucp/images/rwink.png')
  rwink = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
  img = cv2.imread('/home/alex/tryout_ws/src/baxter_openpucp/images/lwink.png')
  lwink = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
  img = cv2.imread('/home/alex/tryout_ws/src/baxter_openpucp/images/blink.png')
  blink = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
  img = cv2.imread('/home/alex/tryout_ws/src/baxter_openpucp/images/flushed.png')
  flushed = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
  
  rospy.spin()
