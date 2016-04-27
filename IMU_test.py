
#!/usr/bin/python

import smbus
import math
import time
import sys
import ibmiotf.application
import ibmiotf.device


arrSamples = []
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

stable_x_acc = 0
stable_y_acc = 0
stable_z_acc = 0

stable_x_gyro = 0
stable_y_gyro = 0
stable_z_gyro = 0

flag = 2

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

deviceOptions = ibmiotf.device.ParseConfigFile("/home/pi/Desktop/ProjectDevice.cfg")
try:
  deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
  print("Caught exception connecting device: %s" % str(e))
  sys.exit()

deviceCli.connect()

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

	#print str(accel_xout_scaled).zfill(15), str(accel_yout_scaled).zfill(15), str(accel_zout_scaled).zfill(15), str(gyro_xout_scaled).zfill(5), str(gyro_yout_scaled).zfill(5), str(gyro_zout_scaled).zfill(5)
#       deviceCli.connect()
	if gyro_xout_scaled > 4 or gyro_xout_scaled < -4:
	        flag = 1
		values = str(accel_xout_scaled)+','+str(accel_yout_scaled)+','+ str(accel_zout_scaled)+','+str(gyro_xout_scaled)+','+str(gyro_yout_scaled)+','+str(gyro_zout_scaled)
		#data = values[0] + ", " + values[1] + ", " + values[2] + ", " + values[3] + ", " + values[4] + ", " + values[5]
                arrSamples.append(values)
	#	deviceCli.connect()
		#deviceCli.publishEvent("IMU_Readings", "json", data)
		time.sleep(1/5.0)
	else:
		data = "Stable"
		if flag != 0 and len(arrSamples) >=3:
                        print arrSamples, len(arrSamples)
                        for i in range(len(arrSamples)):
		            deviceCli.publishEvent("IMU_Readings", "json", arrSamples[i])
			deviceCli.publishEvent("Event_Stop", "json", "1")
                        #fp  = open("testfile","a")
                        #for i in range(len(arrSamples)):
                        #    fp.write(str(arrSamples[i]))
                        #    fp.write("\n")
                        #fp.write("event\n")
                        #fp.close()
                        arrSamples = []
			flag = 0
	
#	data = values[0] + ", " + values[1] + ", " + values[2] + ", " + values[3] + ", " + values[4] + ", " + values[5] + ", 1" 
	#deviceCli.publishEvent("Event_Stop", "json", "1")
	#print data
#	deviceCli.disconnect()
        time.sleep(1/10.0)
