#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# pinos pcf8591: pin 1 - AIN0           pin 16 - VCC - 5V
#                pin 2 - AIN1           pin 15 - LED RED
#                pin 3 - AIN2           pin 14 - LED GREEN
#                pin 4 - AIN3           pin 13 - VCC
#                pin 5 - gnd            pin 12 - gnd
#                pin 6 - gnd            pin 11 - x
#                pin 7 - gnd            pin 10 - SCL 
#                pin 8 - gnd            pin 9  - SDA
#
# Pinos RPI -  pin 3 - SDA
#              pin 5 - SCL
#              pin 2 - VCC 5V
#              pin 6 - gnd
import smbus
import time

address = 0x48

A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

bus = smbus.SMBus(1)

def value2():
	bus.write_byte(address, A2)
	value = bus.read_byte(address)
#	print ("AOUT:%1.3f " %(value))
	time.sleep(0.1)
	return value


sensorValue = 0

buf = [0]*10
while(1):
    for i in list(range(10)):
            Ain = value2()
            buf[i] = Ain
            time.sleep(0.01)

    for i in list(range(9)):
            for j in list(range(i+1,9)):
                if buf[i] >buf[j]:
                    temp = buf[i]
                    buf[i] = buf[j]
                    buf[j]=temp

    avgValue = 0

    for i in list(range(2,8)):
        avgValue += buf[i]
        pHVol = avgValue*5.0/256/6
        phValue =  - 5.6628*pHVol + 21.399
        time.sleep(0.2)    
      
    print(phValue)	
    time.sleep(0.2)






