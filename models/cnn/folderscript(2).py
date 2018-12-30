import os
import sys
import pandas as pd
import shutil

path = sys.argv[1]
dirs = os.listdir(path)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def getlabel(x):
    if x < 100000:
        return 1

    if 100000 <= x < 200000:
        return 2
    if 200000 <= x < 300000:
        return 3
    if 300000 <= x < 400000:
        return 4
    if 400000 <= x < 500000:
        return 5
    if 500000 <= x < 600000:
        return 6
    if 600000 <= x < 700000:
        return 7
    if 700000 <= x < 800000:
        return 8
    if 800000 <= x < 900000:
        return 9
    if 900000 <= x:
        return 10


data = pd.read_csv(sys.argv[2])
id = data.id.values
price = data.price.values

mydict = dict(zip(id, price))

banyoresimleri = {}
mutfakresimleri = {}
salonresimleri = {}

for i in range(1, 11):
    createFolder("kitchen/train/" + str(i))
    createFolder("kitchen/validation/" + str(i))

    createFolder("bedroom/train/" + str(i))
    createFolder("bedroom/validation/" + str(i))

    createFolder("bathroom/train/" + str(i))
    createFolder("bathroom/validation/" + str(i))

for name in dirs:

    banyoresimleri[name] = list(
        map(lambda x: path + "/" + name + "/bathroom/" + x, os.listdir(path + "/" + name + "/bathroom")))
    mutfakresimleri[name] = list(
        map(lambda x: path + "/" + name + "/kitchen/" + x, os.listdir(path + "/" + name + "/kitchen")))
    salonresimleri[name] = list(
        map(lambda x: path + "/" + name + "/bedroom/" + x, os.listdir(path + "/" + name + "/bedroom")))
    for names in banyoresimleri[name]:
        shutil.copy(names,
                    "bathroom/validation/" + str(getlabel(int(mydict[name]))) + "/" + name + "_" + names.split("/")[3])
        shutil.copy(names,
                    "bathroom/train/" + str(getlabel(int(mydict[name]))) + "/" + name + "_" + names.split("/")[3])
    for names in mutfakresimleri[name]:
        shutil.copy(names,
                    "kitchen/validation/" + str(getlabel(int(mydict[name]))) + "/" + name + "_" + names.split("/")[3])
        shutil.copy(names, "kitchen/train/" + str(getlabel(int(mydict[name]))) + "/" + name + "_" + names.split("/")[3])
    for names in salonresimleri[name]:
        shutil.copy(names,
                    "bedroom/validation/" + str(getlabel(int(mydict[name]))) + "/" + name + "_" + names.split("/")[3])
        shutil.copy(names, "bedroom/train/" + str(getlabel(int(mydict[name]))) + "/" + name + "_" + names.split("/")[3])
