from time import sleep

analogPin = 10
sensorValue = 0

buf = []*10

def setup():
    for i in range(10):
        buf[i] = analogPin
        sleep(10)
    
    for i in range(9):
        for j in range(i+1,9)
            if buf[i] >buf[j]:
                temp = buf[i]
                buf[i] = buf[j]
                buf[j]=temp

avgValue = 0

for i in range(2,8):
    avgValue += buf[i]
    pHVol = avgValune*5.0/256/6
    phValue =  - 5.6628*pHVol + 21.399

sleep(200)





