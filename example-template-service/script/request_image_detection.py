
import requests
import uuid

import json

import time
import os
import datetime
import cv2
import pkg_resources

path = "/home/anustup/Pictures/Animals"

classes = 'all'
veichels = 'bicycle,car,motorbike,aeroplane,bus,train,truck,boat'
animals = 'bird,cat,dog,horse,sheep,cow,elephant,bear,zebra,giraffe'
sports_equipments = 'frisbee,skis,snowboard,sports ball,kite,baseball bat,baseball glove,skateboard,surfboard,tennis racket'
kitchen_utensils = 'bottle,wine glass,cup,fork,knife,spoon,bowl,microwave,oven,toaster,sink,refrigerator'
fruits_and_veggies = 'banana,apple,sandwich,orange,broccoli,carrot'
fast_food = 'hot dog,pizza,donut,cake'
misclenious = 'traffic light,fire hydrant,stop sign,parking meter,bench,backpack,umbrella,handbag,tie,suitcase,chair,sofa,potted plant,bed,dining table,toilet,tvmonitor,laptop,mouse,remote,keyboard,cell phone,book,clock,vase,scissors,teddy bear,hair drier,toothbrush'


for pic in os.listdir(path):
    print(pic)
    if pic != "hold":
        frame = os.path.join(path, pic)
        data = open(frame,'rb').read()
        rq = {'frame':data,'claases_to_detect': animals,
              'id_': str(uuid.uuid4())}

        res = requests.post(f'http://localhost:5000/api/1/example/detect?claases_to_detect={classes}', files=rq)
        response_dict = res.content


        print(response_dict)

