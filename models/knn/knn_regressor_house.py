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
con = sq.connect('../../house_spider/parsed.db')
con.row_factory = sq.Row
cursor = con.cursor()
cursor.execute("SELECT * FROM hurriyet_ankara")
data = cursor.fetchall()
cursor.close()

cursor = con.cursor()
cursor.execute('SELECT * FROM hurriyet_ankara_place_index')
enumerator = cursor.fetchall()
cursor.close()
enum = {}

for i in enumerator:
    enum[i['yer']] = i['id']


train, test = train_test_split(data, test_size=0.3, shuffle=True)

training_data = {'x': [], 'y': []}
test_data = {'x': [], 'y': []}

for sample in train:
    training_data['x'].append(np.array([sample['metrekare'], sample['oda'], sample['banyo'], enum[sample['yer']]]))
    training_data['y'].append(np.array([sample['price']]))

for sample in test:
    test_data['x'].append(np.array([sample['metrekare'], sample['oda'], sample['banyo'], enum[sample['yer']]]))
    test_data['y'].append(np.array([sample['price']]))


"""training_data['x'] = np.divide(np.array(training_data['x']), np.max(np.array(training_data['x']), axis=0))
training_data['y'] = np.divide(np.array(training_data['y']), np.max(np.array(training_data['y']), axis=0))

test_data['x'] = np.divide(np.array(test_data['x']), np.max(np.array(test_data['x']), axis=0))
test_data['y'] = np.divide(np.array(test_data['y']), np.max(np.array(test_data['y']), axis=0))"""


"""for k in range(1, 100, 2):
    knn = neighbors.KNeighborsRegressor(n_neighbors=k, algorithm='auto', metric='euclidean')
    knn.fit(training_data['x'], training_data['y'])
    print('KNN score is for %d: %f' % (k, knn.score(test_data['x'], test_data['y'])))"""

knn = neighbors.KNeighborsRegressor(n_neighbors=50, algorithm='auto')
knn.fit(training_data['x'], training_data['y'])
print('KNN score is for %d: %f' % (15, knn.score(test_data['x'], test_data['y'])))
print('KNN training score is for %d: %f' % (15, knn.score(training_data['x'], training_data['y'])))
prediction = knn.predict(test_data['x'])
print("-"*20 + "\n")
"""
plt.plot(prediction, label='prediction')
plt.plot(test_data['y'], label='expected')
plt.legend()
plt.show()

"""
reg = LinearRegression(normalize=True)
reg.fit(training_data['x'], training_data['y'])
print('Test accuracy: ', reg.score(test_data['x'], test_data['y']))
print('Training accuracy: ', reg.score(training_data['x'], training_data['y']))
print(reg.coef_)

prediction = reg.predict(test_data['x'])
print("-"*20 + "\n")
"""plt.plot(prediction, label='prediction')
plt.plot(test_data['y'], label='expected')
plt.legend()
plt.show()"""


svm = LinearSVR(C=3.0, epsilon=0.1, max_iter=30000, verbose=True)
svm.fit(training_data['x'], np.array(training_data['y']).flatten())
print("Test score: ", svm.score(test_data['x'], np.array(test_data['y']).flatten()))
print("Training score: ", svm.score(training_data['x'], np.array(training_data['y']).flatten()))
print(svm.coef_)

prediction = svm.predict(test_data['x'])
"""
plt.plot(prediction, label='prediction')
plt.plot(test_data['y'], label='expected')
plt.legend()
plt.show()
"""
print("done")
