#!/usr/bin/env python
import sys
import rospy
import baxter_interface
from std_msgs.msg import Bool
from std_msgs.msg import String
from baxter_interface import CHECK_VERSION

global button_state

def press_button1(msg):
  
  global button_state
  button_state = msg.data
  

def try_float(x):
  try:
    return float(x)
  except ValueError:
    return None


def clean_line(line, names):

  line = [try_float(x) for x in line.rstrip().split(',')]
  combined = zip(names[1:], line[1:])
  cleaned = [x for x in combined if x[1] is not None]
  command = dict(cleaned)
  left_command = dict((key, command[key]) for key in command.keys() if key[:-2] == 'left_')
  right_command = dict((key, command[key]) for key in command.keys() if key[:-2] == 'right_')
  return (command, left_command, right_command, line)


def map_file(filename, loops=1):

    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')
    grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
    grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
    rate = rospy.Rate(1000)

    if grip_left.error():
        grip_left.reset()
    if grip_right.error():
        grip_right.reset()
    if (not grip_left.calibrated() and
        grip_left.type() != 'custom'):
        grip_left.calibrate()
    if (not grip_right.calibrated() and
        grip_right.type() != 'custom'):
        grip_right.calibrate()

    print("Playing back: %s" % (filename,))
    with open(filename, 'r') as f:
        lines = f.readlines()
    keys = lines[0].rstrip().split(',')

    l = 0
    while loops < 1 or l < loops:
        i = 0
        l += 1
        print("Moving to start position...")

        _cmd, lcmd_start, rcmd_start, _raw = clean_line(lines[1], keys)
        left.move_to_joint_positions(lcmd_start)
        right.move_to_joint_positions(rcmd_start)
        start_time = rospy.get_time()
        for values in lines[1:]:
            i += 1
            loopstr = str(loops) if loops > 0 else "forever"
            sys.stdout.write("\r Record %d of %d, loop %d of %s" %
                             (i, len(lines) - 1, l, loopstr))
            sys.stdout.flush()

            cmd, lcmd, rcmd, values = clean_line(values, keys)
            while (rospy.get_time() - start_time) < values[0]:
                if rospy.is_shutdown():
                    print("\n Aborting - ROS shutdown")
                    return False
                if len(lcmd):
                    left.set_joint_positions(lcmd)
                if len(rcmd):
                    right.set_joint_positions(rcmd)
                if ('left_gripper' in cmd and
                    grip_left.type() != 'custom'):
                    grip_left.command_position(cmd['left_gripper'])
                if ('right_gripper' in cmd and
                    grip_right.type() != 'custom'):
                    grip_right.command_position(cmd['right_gripper'])
                rate.sleep()
        print
    return True


if __name__ == '__main__':

  rospy.init_node("Hug_control")

  pub_life = rospy.Publisher('/life', String, queue_size=1)
  rospy.Subscriber("pushed1", String, press_button1)
  #rospy.Subscriber("pushed2", Bool, press_button2)
  rate = rospy.Rate(10)

  rs = baxter_interface.RobotEnable(CHECK_VERSION)
  init_state = rs.state().enabled

  def clean_shutdown():
    print("\nExiting example...")
    if not init_state:
      print("Disabling robot...")
      rs.disable()
  
  rospy.on_shutdown(clean_shutdown)
  rs.enable()

  last_button_state = button_state = 'notpushed'
  pub_life.publish("notalive")
  rospy.sleep(1)
  pub_life.publish("alive")

  while not rospy.is_shutdown():
    
    if(last_button_state == 'pushed' and button_state == 'notpushed'):
      rospy.loginfo("Release Button")
      map_file("/home/alex/tryout_ws/src/baxter_openpucp/hugh",1)
      rospy.sleep(1)
      map_file("/home/alex/tryout_ws/src/baxter_openpucp/open_arms",1)
      pub_life.publish("alive")
      rospy.loginfo("Autonomos life back")

    elif(last_button_state == 'notpushed' and button_state == 'pushed'):
      rospy.loginfo("Pushed button")
      pub_life.publish("notalive")

    last_button_state = button_state
    rate.sleep()

