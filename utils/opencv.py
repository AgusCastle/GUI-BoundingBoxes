from itertools import count
import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
size_font = 1
grosor = 2

def setBoxesToImage(path, lis={}):

    image = cv2.imread(path)
    colors = []
    count = 0
    for box, label in zip(lis['boxes'], lis['labels']):
        color = boundingBoxColor(label)
        colors.append(color)
        image = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), color, 2)
        image = cv2.putText(image, label + " " + str(count + 1), (box[0], box[3] + 18), font, size_font, color, grosor)
        count += 1
    return image, colors

def cutImageBox(path, array):
    image = cv2.imread(path)
    image = image[array[1]:array[3], array[0]:array[2]]
    h, w, _ = image.shape
    return h, w, image

def boundingBoxColor(label):
    if label == 'surgical': # Color Cian
        return (255, 255, 0)
    elif label == 'valve':  # Color Magenta
        return (255, 0, 255)
    elif label == 'cloth': # Color lima
        return (0, 255, 0) 
    elif label == 'respirator':
        return (0, 255, 255) # Color amarillo
    elif label == 'others':
        return (0, 165, 255) # Color rojo
    elif label == 'none':
        return (0, 0, 255)
    return (0, 0, 0)
