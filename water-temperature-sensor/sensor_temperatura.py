#/usr/bin/env python
import os
def sensor(): 
   for i in os.listdir('/sys/bus/w1/devices'):
       if i != 'w1_bus_master1':
           temperature_sensor = i
   return temperature_sensor

def read(temperature_sensor):
   location = '/sys/bus/w1/devices/' + temperature_sensor + '/w1_slave'
   tfile = open(location)
   text = tfile.read()
   tfile.close()
   secondline = text.split("\n")[1]
   temperaturedata = secondline.split(" ")[9]
   temperature = float(temperaturedata[2:])
   celsius = temperature / 1000
   farenheit = (celsius * 1.8) + 32
   return celsius, farenheit

def loop(temperature_sensor):
   current_temperature = read(temperature_sensor)
   while True:
       if current_temperature != None:
           print "Current temperature: %0.3f C" % current_temperature[0]
           #print "Current temperature : %0.3f F" % current_temperature[1]

def kill():
   quit()

if __name__ == '__main__':
   try:
       serialNum = sensor()
       loop(serialNum)
   except KeyboardInterrupt:
       kill()
