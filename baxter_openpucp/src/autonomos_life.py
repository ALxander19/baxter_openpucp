#!/usr/bin/env python
import rospy
import random
import baxter_interface
from std_msgs.msg import String
from baxter_interface import CHECK_VERSION

global state

def autonomos_life(msg):
  
  global state
  state = msg.data


if __name__ == '__main__':
  
  rospy.init_node('autonomos_life')
  
  rospy.Subscriber('life', String, autonomos_life)
  pub = rospy.Publisher('/faces', String, queue_size=1)
  
  pub.publish('normal')
  
  last_state = state = 'notalive'
  change = False
  state_change_time = rospy.Time.now() + rospy.Duration(3600)

  head = baxter_interface.Head()
  rs = baxter_interface.RobotEnable(CHECK_VERSION)
  init_state = rs.state().enabled

  def clean_shutdown():
    print "\nExiting example..."
    if not init_state:
      print "Disabling robot..."
      rs.disable()
  rospy.on_shutdown(clean_shutdown)
  rs.enable()

  while(True):

    if(last_state == 'notalive' and state == 'alive'):
      change = True
      rospy.loginfo("Autonomos life turn on")

    if(change):
      interval = round(random.randint(3,6))
      state_change_time = rospy.Time.now() + rospy.Duration(interval)
      change = False
      pub.publish('blink')
      angle = round(random.uniform(-1,1),1)
      print angle
      head.set_pan(angle, 0.06)
      rospy.sleep(1)
      pub.publish('normal')

    if(rospy.Time.now() > state_change_time):
      change = True

    if((last_state == 'alive' and state == 'notalive') or (last_state == 'notalive' and state == 'notalive')):
      change = False
      state_change_time = rospy.Time.now()
      
    if(last_state == 'alive' and state == 'notalive'):
      rospy.loginfo("Autonomos life turn down")
      head.set_pan(0, 0.06)

    last_state = state



