import os
import time
import requests
from datetime import datetime

url = "http://172.20.10.4:8000/picture"

while True:
    print "taking picture"
    filename = str(datetime.now()).replace(" ", "")
    string = "fswebcam --no-banner -r 640x480 " + filename + ".jpg --skip 10"
    os.system(string)
    files = {"picture": open(filename +".jpg", "rb")}
    response = requests.post(url, files=files)

    if response.ok:
        print "Upload complete"
        os.system("rm " + filename + ".jpg")
    else:
        print response.text
        print "Upload failed"

    print "sleeping"
    time.sleep(20) 
