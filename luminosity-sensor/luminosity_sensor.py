import RPi.GPIO as gpio
import os
import smbus
import time
from nameko.standalone.rpc import ClusterRpcProxy


gpio.setmode(gpio.BOARD)

lamp = 12

gpio.setup(lamp, gpio.OUT)
gpio.output(lamp, gpio.HIGH)

address = 0x48

A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

config = {'AMQP_URI': os.environ.get("RABBIT_URL")}

bus = smbus.SMBus(1)
while True:
    try:
        with ClusterRpcProxy(config) as cluster_rpc:
            print("Opening connection")
            bus.write_byte(address, A0)
            value = bus.read_byte(address)
            if (value >= 150):
                print("lights off")
                cluster_rpc.ilumination_server.receive_ilumination(False)
            else:
                print("lights on")
                cluster_rpc.ilumination_server.receive_ilumination(True)
            time.sleep(1)
    except:
        pass
	
gpio.cleanup()

