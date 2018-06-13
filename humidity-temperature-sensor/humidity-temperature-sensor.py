import Adafruit_DHT 
import RPi.GPIO as GPIO
import time
from nameko.standalone.rpc import ClusterRpcProxy

sensor = Adafruit_DHT.DHT22

pin = 23

print "Reading values"

config = {'AMQP_URI':'amqp://52.67.189.254:80'}


while(True):
    with ClusterRpcProxy(config) as cluster_rpc:
        print "opening connection"
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin);
        if humidity is not None and temperature is not None:
            print "Temperature = {}  Humidity = {}".format(temperature, humidity);
            cluster_rpc.humidity_server.receive_humidity(humidity)
            cluster_rpc.temperature_server.receive_temperature(temperature)
            time.sleep(0.5)
        else:
            print "Failed to read data"
