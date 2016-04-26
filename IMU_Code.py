#!/usr/bin/python

import smbus
import math
import time

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

stable_x_acc = 0
stable_y_acc = 0
stable_z_acc = 0

stable_x_gyro = 0
stable_y_gyro = 0
stable_z_gyro = 0

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

while True:
	#print "gyro data"
	#print "---------"

	gyro_xout = read_word_2c(0x43)
	gyro_yout = read_word_2c(0x45)
	gyro_zout = read_word_2c(0x47)

        gyro_xout_scaled = gyro_xout/131
        gyro_yout_scaled = gyro_yout/131
        gyro_zout_scaled = gyro_zout/131
    

	#print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
	#print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
	#print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

	#print
	#print "accelerometer data"
	#print "------------------"

	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)

	accel_xout_scaled = accel_xout / 16384.0 * 1000
	accel_yout_scaled = accel_yout / 16384.0 * 1000
	accel_zout_scaled = accel_zout / 16384.0 * 1000

	#print  "accel_xout: ", accel_xout," scaled: ", accel_xout_scaled
	#print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
	#print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

	#print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	#print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	#print str(accel_xout).zfill(6), str(accel_yout).zfill(6), str(accel_zout).zfill(6), str(gyro_xout).zfill(6), str(gyro_yout).zfill(6), str(gyro_zout).zfill(6)
	print str(accel_xout_scaled).zfill(15), str(accel_yout_scaled).zfill(15), str(accel_zout_scaled).zfill(15), str(gyro_xout_scaled).zfill(5), str(gyro_yout_scaled).zfill(5), str(gyro_zout_scaled).zfill(5)
        time.sleep(1/5.0)
