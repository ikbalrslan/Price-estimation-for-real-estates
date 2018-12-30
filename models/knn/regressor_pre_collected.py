import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.svm import SVR, LinearSVR
import sqlite3 as sq


def join(val):
    return "/".join(val.split('/')[:2])


# fetching data
con = sq.connect('../../house_spider/usa_kaggle.db')
con.row_factory = sq.Row
cursor = con.cursor()
# cursor.execute('SELECT * FROM hurriyet WHERE yer IN (SELECT yer FROM hurriyet GROUP BY yer HAVING count(yer) > 0)')
cursor.execute("SELECT * FROM HOUSE_DATA")
data = cursor.fetchall()
cursor.close()