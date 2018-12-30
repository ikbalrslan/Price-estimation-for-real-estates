import sqlite3
import os
import csv

#print(os.getcwd())
conn = sqlite3.connect('usa_kaggle.db')
curr = conn.cursor()
print("Opened database successfully")

curr.execute('''CREATE TABLE if NOT EXISTS HOUSE_DATA
        (UNIQUE_ID PRIMARY KEY NOT NULL,
        ID INT NOT NULL,
        DATE_TIME CHAR(50) NOT NULL,
        PRICE REAL NOT NULL,
        BEDROOMS INT NOT NULL,
        BATHROOMS INT NOT NULL,
        SQFT_LIVING INT NOT NULL,
        SQFT_LOT INT NOT NULL,
        FLOORS INT NOT NULL,
        WATERFRONT INT NOT NULL,
        VIEW_COUNT INT NOT NULL,
        CONDITION  INT NOT NULL,
        GRADE INT NOT NULL,
        SQFT_ABOVE INT NOT NULL,
        SQFT_BASEMENT INT NOT NULL,
        YR_BUILT INT NOT NULL,
        YR_RENOVATED INT NOT NULL,
        ZIPCODE INT NOT NULL,
        LAT REAL NOT NULL,
        LONG REAL NOT NULL,
        SQFT_LIVING15 INT NOT NULL,
        SQFT_LOT15 INT NOT NULL);''')
        

print("Table created successfully")

with open('kc_house_data.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = []
    count = 0
    for i in dr:
        count += 1
        to_db.append((count, i['id'], i['date'],i['price'],i['bedrooms'],i['bathrooms'],i['sqft_living'],i['sqft_lot'],i['floors'],i['waterfront'],i['view'],i['condition'],i['grade'],i['sqft_above'],i['sqft_basement'],i['yr_built'],i['yr_renovated'],i['zipcode'],i['lat'],i['long'],i['sqft_living15'],i['sqft_lot15']))
    #to_db = [(i['id'], i['date'],i['price'],i['bedrooms'],i['bathrooms'],i['sqft_living'],i['sqft_lot'],i['floors'],i['waterfront'],i['view'],i['condition'],i['grade'],i['sqft_above'],i['sqft_basement'],i['yr_built'],i['yr_renovated'],i['zipcode'],i['lat'],i['long'],i['sqft_living15'],i['sqft_lot15']) for i in dr]

curr.executemany("INSERT INTO HOUSE_DATA (UNIQUE_ID, ID, DATE_TIME, PRICE, BEDROOMS, BATHROOMS, SQFT_LIVING, SQFT_LOT, FLOORS, WATERFRONT, VIEW_COUNT, CONDITION, GRADE, SQFT_ABOVE, SQFT_BASEMENT, YR_BUILT, YR_RENOVATED, ZIPCODE, LAT, LONG, SQFT_LIVING15, SQFT_LOT15) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()
conn.close()
