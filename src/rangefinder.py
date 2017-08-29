#!/usr/bin/env python
import roslib
#; roslib.load_manifest('numpy_tutorials') #not sure why I need this
import rospy
from sensor_msgs.msg import Range
import serial
import std_msgs.msg

# For this sensor it only sees certain size objects at certain distances
# We have covered from the datasheet Beam patten B and C which should
# cover distances 0.3 to 3.0 metres. The size of the objects will be
# from 2.54cm to 8.89cm

# psuedo constants
DEFAULT_FIELD_OF_VIEW_IN_RAD = 0.488692
DEFAULT_MIN_RANGE_METRES = 0.3
DEFAULT_MAX_RANGE_METRES = 3.0

ser = serial.Serial('/dev/ttyUSB0', 57600)

def talker():
    while not rospy.is_shutdown():
        buffer = ""
        stillReading = True
        while stillReading:
            one_byte = ser.read(1)
            if one_byte == 'R':
                buffer += one_byte
                four_bytes = ser.read(4)
                buffer += four_bytes
                stillReading = False
        data = buffer
        data_int = int(data[1:])
        data_metres = data_int/1000.0
        range = Range()
        header = std_msgs.msg.Header()
        header.stamp = rospy.Time.now()
        header.frame_id = 'rangefinder'
        range.header = header
        range.radiation_type = Range.ULTRASOUND
        range.field_of_view = DEFAULT_FIELD_OF_VIEW_IN_RAD
        range.min_range = DEFAULT_MIN_RANGE_METRES
        range.max_range = DEFAULT_MAX_RANGE_METRES
        range.range = data_metres
        rospy.loginfo(data)
        rospy.loginfo(range)
        pub.publish(range)
        rospy.sleep(1.0)
    pass

if __name__ == '__main__':
    try:
        pub = rospy.Publisher('rangefinder', Range, queue_size=10)
        rospy.init_node('rangefinder_pub')
        rate = rospy.Rate(10)
        talker()
    except rospy.ROSInterruptException:
        pass            
