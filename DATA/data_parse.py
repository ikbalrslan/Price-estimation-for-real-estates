import sqlite3 as sq
import os
import shutil
import math as m
import random
import csv

DATA_PATH = 'scraped'
# DATA_PATH = 'ready_to_use'

LABEL_COUNT = 10


def parse_into_labels(label_count, validation_train_split=0.15):
    if DATA_PATH == 'scraped':
        con = sq.connect('parsed.db')
        curse = con.cursor()

        curse.execute("SELECT ilan_no, price FROM hurriyet ORDER BY price ASC")
        labels = curse.fetchall()

    else:
        labels = []
        for row in csv.DictReader(open('HousesInfo.csv', 'r')):
            labels.append((row['id'], int(row['price'])))

    dicthead = {}
    headdict = {i: [] for i in range(1, label_count + 1)}
    pmin, pmax = min(labels, key=lambda x: x[1])[1], max(labels, key=lambda x: x[1])[1]
    # diff = (pmax - pmin) / label_count
    diff = round(2000000 / label_count)
    for house in labels:
        # dicthead[house[0]] = m.ceil(((house[1] - pmin) / (pmax - pmin)) * label_count)
        dicthead[house[0]] = m.ceil(house[1] / diff) if m.ceil(house[1] / diff) <= label_count else label_count
        headdict[dicthead[house[0]]].append(house[0])

    data_root = 'data_'+DATA_PATH
    validation_root = 'validation_'+DATA_PATH
    types = ['bathroom', 'kitchen', 'bedroom']
    types = list(map(lambda x: data_root + '/' + x, types)) + list(map(lambda x: validation_root + '/' + x, types))

    if not os.path.isdir(data_root):
        os.mkdir(data_root)

    if not os.path.isdir(validation_root):
        os.mkdir(validation_root)

    if not os.path.isdir(DATA_PATH):
        raise FileNotFoundError('There is no data folder called {}. You need that'.format(DATA_PATH))

    for t in types:
        # recreate directories if they exists
        folder_name = t+'_data'
        if os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
        os.mkdir(folder_name)

        # create labels
        for i in range(1, label_count + 1):
            if not os.path.isdir(folder_name + '/' + str(i)):
                os.mkdir(folder_name + '/' + str(i))

    folders = [i for i in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH, i))]
    random.shuffle(folders)
    validation = folders[0:int(len(folders) * validation_train_split)]

    if DATA_PATH == 'scraped':
        # if scraped dataset
        for subdir, dirs, files in os.walk(DATA_PATH):
            folders = subdir.split('/')
            if len(folders) == 3:
                ilan_no = folders[1]
                t = folders[2]

                if ilan_no in validation:
                    current_dir = validation_root
                else:
                    current_dir = data_root

                for file in files:
                    fpath = os.path.join(subdir, file)
                    shutil.copyfile(fpath,
                                    current_dir + '/' + t + "_data/" + str(dicthead[ilan_no]) + '/' + ilan_no + file)
    else:
        # if ready to use dataset
        for subdir, dirs, files in os.walk(DATA_PATH):
            folders = subdir.split('/')
            if len(folders) == 2:
                ilan_no = folders[1]

                if ilan_no in validation:
                    current_dir = validation_root
                else:
                    current_dir = data_root

                for file in files:
                    t = file.split('_')[-1].split('.')[0]
                    if t not in ['bedroom', 'bathroom', 'kitchen']:
                        continue

                    fpath = os.path.join(subdir, file)
                    shutil.copyfile(fpath,
                                    current_dir + '/' + t + "_data/" + str(dicthead[ilan_no]) + '/' + file)


if __name__ == "__main__":
    # DEBUG
    parse_into_labels(LABEL_COUNT)

    print("done")
