"""
Train a model
"""
from keras import applications
from keras.layers import Flatten, Dense
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot as plt
import os

BATCH_SIZE = 1
# TF_CPP_MIN_LOG_LEVEL = 2
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def train():
    # loader/preprocessor for data
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,  # random application of shearing
        zoom_range=0.2,
        horizontal_flip=True)  # randomly flipping half of the images horizontally

    # loader for test
    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        'data/kitchen_data',
        target_size=(255, 255),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        'validation/kitchen_data',
        target_size=(255, 255),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical')

    model = applications.VGG16(include_top=False, weights=None, input_shape=(255, 255, 1))

    x = Flatten(name='flatten')(model.output)
    x = Dense(100, activation='relu', name='fc1')(x)
    x = Dense(10, activation='softmax', name='predictions')(x)

    head_model = Model(input=model.input, output=x)

    head_model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['acc'])

    history = head_model.fit_generator(train_generator,
                                       epochs=10,
                                       steps_per_epoch=round(train_generator.n / BATCH_SIZE),
                                       validation_data=validation_generator,
                                       validation_steps=round(validation_generator.n / BATCH_SIZE),
                                       verbose=1
                                       )

    return head_model, history


if __name__ == "__main__":
    model, history = train()

    # plot results
    fig, axs = plt.subplots(1, 2)

    axs[0].plot(history.history['acc'])
    axs[0].plot(history.history['val_acc'])
    axs[0].set_title('model accuracy')
    axs[0].set(ylabel='accuracy', xlabel='epoch')
    axs[0].legend(['train', 'test'])

    axs[1].plot(history.history['loss'])
    axs[1].plot(history.history['val_loss'])
    axs[1].set_title('model loss')
    axs[1].set(ylabel='loss', xlabel='epoch')
    axs[1].legend(['train', 'test'])

    plt.savefig('training.png')
    plt.show()

    # forgotten to save the weights you dumb bitch
