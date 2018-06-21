import os
import Adafruit_DHT 
import RPi.GPIO as GPIO
import time
from nameko.standalone.rpc import ClusterRpcProxy

sensor = Adafruit_DHT.DHT22

pin = 23
cooler =24

GPIO.setmode(GPIO.BCM)
GPIO.setup(cooler, GPIO.OUT)
print "Reading values"

config = {'AMQP_URI': os.environ.get('RABBIT_URL')}

while(True):
    with ClusterRpcProxy(config) as cluster_rpc:
        print "opening connection"
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin);
        if humidity is not None and temperature is not None:
            print "Temperature = {}  Humidity = {}".format(temperature, humidity)
            # print "sending to humidity"
            # cluster_rpc.humidity_server.receive_humidity(humidity)
            print "sending to temperature"
            cluster_rpc.temperature_server.receive_temperature(temperature)
            time.sleep(0.5)

        else:
            print "Failed to read data"

        if temperature > 25:
            GPIO.output(cooler, GPIO.LOW)
        else:
            GPIO.output(cooler, GPIO.HIGH)
