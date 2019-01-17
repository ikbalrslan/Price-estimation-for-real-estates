"""
Model wrapper
"""
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.preprocessing.image import load_img, img_to_array
import pickle
import random
import csv
import numpy as np
from matplotlib import pyplot as plt


class Model:
    """ 4 NN together """

    def __init__(self,
                 kpath,
                 btpath,
                 bdpath,
                 input_shape=(244, 224, 3),
                 layers=None,
                 activations=None
                 ):

        if layers is None:
            layers = [4, 10]

        if activations is None:
            activations = ['sigmoid', 'softmax']

        self.activations = activations
        self.layers = layers
        self.input_shape = input_shape

        self.last_train = None

        # The image classification models
        self.kitchen = self.create_model(kpath)
        self.bathroom = self.create_model(btpath)
        self.bedroom = self.create_model(bdpath)

        # fully connected model, combines all the above
        self.fully_connected = Sequential()
        self.fully_connected.add(Dropout(0.2, input_shape=(9,)))
        self.fully_connected.add(Dense(10, activation='relu'))
        self.fully_connected.add(Dropout(0.5))
        self.fully_connected.add(Dense(10, activation='relu'))
        self.fully_connected.add(Dropout(0.5))
        self.fully_connected.add(Dense(1, activation='sigmoid'))

        self.fully_connected.compile(optimizer='SGD', loss='mean_absolute_error', metrics=['acc', 'mse'])

    def create_model(self, path):
        model = Sequential()

        model.add(Flatten(input_shape=self.input_shape))
        for index in range(len(self.layers)):
            model.add(Dense(self.layers[index], activation=self.activations[index]))

        model.load_weights(path)

        return model

    def train(self, x, y):
        """ Train the fully connected layer with a dataset(no images just labels) """
        history = self.fully_connected.fit(
            x,
            y,
            epochs=2,
            batch_size=1,
            shuffle=True,
            validation_split=0.1,
            verbose=1
        )

        self.last_train = history

        return history

    def test(self, mi, bti, bdi, data):
        """ Make predictions on trained model """
        kitchen = load_img(mi, target_size=(300, 300))
        kimage = img_to_array(kitchen)
        bathroom = load_img(bti, target_size=(300, 300))
        btimage = img_to_array(bathroom)
        bedroom = load_img(bdi, target_size=(300, 300))
        bdimage = img_to_array(bedroom)

        kimage /= 255
        kimage = np.expand_dims(kimage, axis=0)
        btimage /= 255
        btimage = np.expand_dims(btimage, axis=0)
        bdimage /= 255
        bdimage = np.expand_dims(bdimage, axis=0)

        k = self.kitchen.predict(kimage)
        bt = self.bathroom.predict(btimage)
        bd = self.bedroom.predict(bdimage)

        k = np.argmax(k) + 1
        bt = np.argmax(bt) + 1
        bd = np.argmax(bd) + 1

        print(k, bt, bd)

        dataset = np.array(
            [
                k,
                bt,
                bd,
                data['place'],
                data['age'],
                data['bathrooms'],
                data['size'],
                data['rooms'],
                data['floor']
            ]
        ).reshape(1, -1)

        return self.fully_connected.predict(dataset)

    def save(self, file_name=None):
        """ Save model to a pickle file """
        if file_name is None:
            file_name = str(random.randint(1, 1e20)) + '.pkl'

        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    def graph(self):
        if self.last_train is None:
            raise ValueError('You must train at least once')

        fig, axs = plt.subplots(2, 1)
        axs[0].plot(self.last_train.history['acc'])
        axs[0].plot(self.last_train.history['val_acc'])
        axs[0].set_title('model accuracy')
        axs[0].set(ylabel='accuracy', xlabel='epoch')

        axs[1].plot(self.last_train.history['loss'])
        axs[1].plot(self.last_train.history['val_loss'])
        axs[1].set_title('model loss')
        axs[1].set(ylabel='loss', xlabel='epoch')

        plt.show()


def load_model(fname):
    """ load a module from file """
    return pickle.load(open(fname, 'rb'))


if __name__ == '__main__':
    kpath = 'trained_models/kitchen_CT-rgb_HNC-4_HA-sigmoid_E-10_A-0.4073170731707317_35312172520306354189.h5'
    btpath = 'trained_models/bathroom_CT-rgb_HNC-4_HA-sigmoid_E-10_A-0.45_84921715989644490494.h5'
    bdpath = 'trained_models/bedroom_CT-rgb_HNC-4_HA-sigmoid_E-10_A-0.3620253164556962_27382087226522127698.h5'

    train_datapath = 'DATA/labeled_hurriyet.csv'
    train_dataset = [dict(data) for data in csv.DictReader(open(train_datapath, 'r'), delimiter='\t')]

    with open('DATA/main_hurriyet_place_index.csv', 'r') as index_file:
        indexify = {i['place']: i['id'] for i in csv.DictReader(index_file)}

    dataset = np.array([
        np.array(
            [
                int(data['label']),
                int(data['label']),
                int(data['label']),
                int(indexify[data['yer']]),
                int(data['bina_yasi']),
                int(data['banyo']),
                int(data['metrekare']),
                int(data['oda']),
                int(data['kat'])
            ]
        )
        for data in train_dataset
    ])

    # dataset = (dataset - dataset.min(axis=0)) / (dataset.max(axis=0) - dataset.min(axis=0))
    dataset = dataset / dataset.max(axis=0)

    prices = [float(i['price']) for i in train_dataset]
    pmin, pmax = min(prices), max(prices)
    expected = list(map(lambda x: x / pmax, prices))
    # expected = list(map(lambda x: (x - pmin) / (pmax - pmin), prices))

    model = Model(kpath, btpath, bdpath, input_shape=(300, 300, 3))
    results = model.train(dataset, np.array(expected))

    model.graph()

    model.save(file_name='test.pkl')
    print("done")
