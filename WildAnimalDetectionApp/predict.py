import numpy as np
from keras.preprocessing import image
from tensorflow.keras.models import load_model

from os import getcwd
import cv2 as cv
import imutils

animal = ['Bear', 'Chinkara', 'Elephant', 'Lion', 'Tiger']

def process():

    imagetest = cv.imread(getcwd() + '/media/test.png')
    # test_image = image.img_to_array(test_image)
    # test_image = np.expand_dims(test_image, axis=0)
    classifier = load_model(getcwd() + '\\trained_model_wild.h5')

    gray = cv.cvtColor(imagetest, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=2)
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv.contourArea)

    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    new_image = imagetest[extTop[1]:extBot[1], extLeft[0]:extRight[0]]

    image = cv.resize(new_image, dsize=(150,150), interpolation=cv.INTER_CUBIC)
    image = image / 255.

    image = image.reshape((1, 150, 150, 3))

    result = classifier.predict(image)

    # training_set.class_indices
    print(result[0][0])
    print(result[0][1])
    print(result[0][2])
    # print(result[0][3])
    index=result[0].tolist().index(max(result[0]))
    print(index)
    print(animal[index])

    # if index== 0:
    #     prediction = animal[0]
    # elif index==1:
    #     prediction = animal[1]    
    # else:
    #     prediction=animal[2]

    # print("Result : " + prediction)

    return animal[index]
