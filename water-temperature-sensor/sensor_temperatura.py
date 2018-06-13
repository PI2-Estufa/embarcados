#/usr/bin/env python
import os
import time
from nameko.standalone.rpc import ClusterRpcProxy

def sensor(): 
    ds18b20 = None
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
        else:
            print("not yet")

    return ds18b20

def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return celsius, farenheit


config = {'AMQP_URI':'amqp://52.67.189.254:80'}

def loop(ds18b20):
    while True:
        with ClusterRpcProxy(config) as cluster_rpc:
            if read(ds18b20) != None:
                temperature = read(ds18b20)[0]
                print "Connecting. Please, wait"
                cluster_rpc.temperature_server.receive_temperature(temperature)
                print "connected"
                time.sleep(2)
                print "Current temperature : %0.3f C" % temperature

def kill():
    quit()

if __name__ == '__main__':
    try:
        serialNum = sensor()
        loop(serialNum)
    except KeyboardInterrupt:
        kill()
    except:
        print "I tried. Did not succeed. Now I'm leaving"


