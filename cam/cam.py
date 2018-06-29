import os
import time
import requests
from datetime import datetime
from nameko.standalone.rpc import ClusterRpcProxy

url = "http://172.20.10.4:8000/picture"

config = {'AMQP_URI': os.environ.get('RABBIT_URL')}

while True:
    try:
        with ClusterRpcProxy(config) as cluster_rpc:
            print "taking picture"
            filename = str(datetime.now()).replace(" ", "")
            string = "fswebcam --no-banner -r 640x480 " + filename + ".jpg --skip 10"
            os.system(string)
            files = {"picture": open(filename +".jpg", "rb")}
            response = requests.post(url, files=files)
            cluster_rpc.image_server.receive_image(filename)
            print "Sending to server"
            
            if response.ok:
                print "Upload complete"
                os.system("rm " + filename + ".jpg")
            else:
                print response.text
                print "Upload failed"

            print "sleeping"
            time.sleep(20) 

    except:
        pass