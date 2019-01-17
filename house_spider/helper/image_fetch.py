import requests
from PIL import Image
from io import BytesIO
import os
from time import sleep


def imfetch(arr, folder_name):
    path = "images/"+folder_name+"/"
    if not os.path.exists(path):
        os.makedirs(path)

    for index, im in enumerate(arr):
        # print(im)
        name = "{}.jpg".format(index)

        r = requests.get(im, stream=True)
        if r.status_code != 200:
            continue

        with open(path+name, "wb") as fout:
            for chunk in r.iter_content():
                fout.write(chunk)

        sleep(3)

        """i = Image.open(BytesIO(r.content))
        i.save(path+name, "JPEG")
        sleep(1)"""
