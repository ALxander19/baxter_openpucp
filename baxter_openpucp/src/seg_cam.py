#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from opencv_apps.msg import FaceArrayStamped

global pos_x, pos_y

pos_x = pos_y = 0

def face_position(msg):
  
  global pos_x, pos_y

  try:
    pos_x = msg.faces[0].face.x
    pos_y = msg.faces[0].face.y
    #rospy.loginfo("Position x: "+str(pos_x))
    #rospy.loginfo("Position y: "+str(pos_y))
  except:
    pos_x = 0
    pos_y = 0

if __name__ == '__main__':

  rospy.init_node("seg_cam")
  
  rospy.Subscriber('face_detection/faces',FaceArrayStamped,face_position)
  pub = rospy.Publisher('person_near', String, queue_size=1)
  #rospy.loginfo("hola")

  rate = rospy.Rate(5)

  while not rospy.is_shutdown():
    
    if(pos_x>250 and pos_x<350 and pos_y>370 and pos_y<480):
    
      pub.publish('detected')
      rospy.loginfo("A person is near")
    else:
      pub.publish('nodetected')
    rate.sleep()
