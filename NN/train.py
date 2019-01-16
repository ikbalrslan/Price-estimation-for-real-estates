"""
Train a model
"""
from keras import applications
from keras.layers import Flatten, Dense
from keras.models import Model, Sequential
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot as plt
import random

BATCH_SIZE = 1
SCALE_SIZE_TO = 300
# TF_CPP_MIN_LOG_LEVEL = 2
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

C2N = {'grayscale': 1, 'rgb': 3}

DATA_TYPES = ['scraped', 'ready_to_use']
DATA_TYPE = DATA_TYPES[0]

ROOMS = ['bathroom', 'kitchen', 'bedroom']
SELECTED_ROOM = ROOMS[0]

DATA_PATH = '../DATA/data_' + DATA_TYPE + "/" + SELECTED_ROOM + '_data'
VALIDATION_PATH = '../DATA/validation_' + DATA_TYPE + '/' + SELECTED_ROOM + '_data'

COLOR_TYPE = 'rgb'
HIDDEN_NODE_COUNT = 4
HIDDEN_ACTIVATION = 'sigmoid'
EPOCHS = 10


def train():
    # loader/preprocessor for data
    train_datagen = ImageDataGenerator(
        rescale=1. / SCALE_SIZE_TO,
        shear_range=0.2,  # random application of shearing
        zoom_range=0.2,
        horizontal_flip=True)  # randomly flipping half of the images horizontally

    # loader for test
    test_datagen = ImageDataGenerator(rescale=1. / SCALE_SIZE_TO)

    train_generator = train_datagen.flow_from_directory(
        DATA_PATH,
        target_size=(SCALE_SIZE_TO, SCALE_SIZE_TO),
        color_mode=COLOR_TYPE,
        batch_size=BATCH_SIZE,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        VALIDATION_PATH,
        target_size=(SCALE_SIZE_TO, SCALE_SIZE_TO),
        color_mode=COLOR_TYPE,
        batch_size=BATCH_SIZE,
        class_mode='categorical')

    model = Sequential()

    model.add(Flatten(input_shape=(SCALE_SIZE_TO, SCALE_SIZE_TO, C2N[COLOR_TYPE])))
    model.add(Dense(HIDDEN_NODE_COUNT, activation=HIDDEN_ACTIVATION))
    model.add(Dense(10, activation='softmax'))

    # head_model = Model(input=model.input, output=x)

    model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['acc'])

    history = model.fit_generator(train_generator,
                                  steps_per_epoch=len(train_generator),
                                  epochs=EPOCHS,
                                  )

    tests = model.evaluate_generator(validation_generator,
                                     steps=len(validation_generator),
                                     verbose=1
                                     )

    return model, history, tests


if __name__ == "__main__":

    # gather data
    model, history, tests = train()
    ID = random.randint(1, 1e20)

    FILE_NAME = '{}_CT-{}_HNC-{}_HA-{}_E-{}_A-{}_{}'.format(
        SELECTED_ROOM,
        COLOR_TYPE,
        HIDDEN_NODE_COUNT,
        HIDDEN_ACTIVATION,
        EPOCHS,
        tests[1],
        ID
    )

    model.save_weights("../trained_models/{}.h5".format(FILE_NAME))

    print("ID: {}\nTest accuracy: {}\nTest loss: {}\n".format(ID, tests[1], tests[0]))

    # plot results
    fig, axs = plt.subplots(1, 2)

    axs[0].plot(history.history['acc'])
    axs[0].set_title('model accuracy')
    axs[0].set(ylabel='accuracy', xlabel='epoch')
    axs[0].legend(['train', 'test'])

    axs[1].plot(history.history['loss'])
    axs[1].set_title('model loss')
    axs[1].set(ylabel='loss', xlabel='epoch')
    axs[1].legend(['train', 'test'])

    plt.savefig('../graphs/{}.png'.format(FILE_NAME))
