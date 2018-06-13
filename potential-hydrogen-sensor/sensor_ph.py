import smbus
import time
from nameko.standalone.rpc import ClusterRpcProxy

address = 0x48

A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

bus = smbus.SMBus(1)

def value2():
	bus.write_byte(address, A1)
	value = bus.read_byte(address)
	time.sleep(0.1)
	return value


sensorValue = 0

config = {'AMQP_URI':'amqp://52.67.189.254:80'}

buf = [0]*10
while(1):
    with ClusterRpcProxy(config) as cluster_rpc:
        print "opening connection"
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
          
        print "ph: {}".format(phValue)
        cluster_rpc.ph_server.receive_ph(phValue)
        time.sleep(0.2)
