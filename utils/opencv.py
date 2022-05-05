import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
size_font = 1
grosor = 2

def setBoxesToImage(path, boxes={}):

    image = cv2.imread(path)
    colors = []
    for box, label in zip(boxes['boxes'], boxes['labels']):
        color = list(np.random.choice(range(256), size=3))
        for x, _ in enumerate(color):
            color[x] = float(color[x])
        colors.append(color)
        image = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), color, 2)
        image = cv2.putText(image, label, (box[0], box[3] + 18), font, size_font, color, grosor)
    return image, colors

def cutImageBox(path, array):
    image = cv2.imread(path)
    image = image[array[1]:array[3], array[0]:array[2]]
    h, w, _ = image.shape
    return h, w, image


