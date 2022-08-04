from itertools import count
import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
size_font = 1
grosor = 2

labels = {-1: 'other', 0: 'cloth', -1: 'other', 1: 'unmasked',
          2: 'respirator', 3: 'surgical', 4: 'valved'}


def setBoxesToImage(path, lis={}):

    image = cv2.imread(path)
    colors = []
    # count = 0
    # Grondtruth
    # for box, label in zip(lis['boxes'], lis['labels']):
    #     color = boundingBoxColor(labels[label])
    #     colors.append(color)
    #     cv2.rectangle(image, (box[0], box[1]),
    #                   (box[2], box[3]), (0, 255, 0), 4)
    #     cv2.putText(image, labels[label] + " GT",
    #                 (box[0], box[1] - 18), font, size_font, color, grosor)
    #     count += 1

    count = 0
    for box, label in zip(lis['pred_boxes'], lis['pred_labels']):
        color = boundingBoxColor(labels[label])

        cv2.rectangle(image, (int(box[0]), int(box[1])),
                        (int(box[2]), int(box[3])), color, 2)
        cv2.putText(image, labels[label],
                    (int(box[0]), int(box[1] + 18)), font, size_font, color, grosor)
        count += 1

    cv2.imwrite('./img.jpg', image)
    return colors


def cutImageBox(path, array):
    image = cv2.imread(path)
    image = image[array[1]:array[3], array[0]:array[2]]
    h, w, _ = image.shape

    s_ = 1000 / h
    h_ = int(h * s_)
    w_ = int(w * s_)
    image = cv2.resize(image, (w_, h_), interpolation=cv2.INTER_CUBIC)
    return h_, w_, image


def boundingBoxColor(label):
    if label == 'surgical':  # Color Cian
        return (255, 255, 0)
    elif label == 'valved':  # Color Magenta
        return (255, 0, 255)
    elif label == 'cloth':  # Color lima
        return (255, 0, 0)
    elif label == 'respirator':
        return (0, 165, 255)  # Color amarillo
    elif label == 'other':
        return (0, 165, 255)  # Color rojo
    elif label == 'unmasked':
        return (0, 0, 255)
    return (0, 0, 0)


def test(path):
    img_raw = cv2.imread(path)
    b = [493, 273, 609, 279, 561, 349, 506, 398, 582, 403]
    cv2.circle(img_raw, (b[0], b[1]), 1, (0, 0, 255), 4)
    cv2.circle(img_raw, (b[2], b[3]), 1, (0, 255, 255), 4)
    cv2.circle(img_raw, (b[4], b[5]), 1, (255, 0, 255), 4)
    cv2.circle(img_raw, (b[6], b[7]), 1, (0, 255, 0), 4)
    cv2.circle(img_raw, (b[8], b[9]), 1, (255, 0, 0), 4)
    b2 = [210, 233, 289, 224, 268, 274, 237, 318, 294, 310]
    cv2.circle(img_raw, (b2[0], b2[1]), 1, (0, 0, 255), 4)
    cv2.circle(img_raw, (b2[2], b2[3]), 1, (0, 255, 255), 4)
    cv2.circle(img_raw, (b2[4], b2[5]), 1, (255, 0, 255), 4)
    cv2.circle(img_raw, (b2[6], b2[7]), 1, (0, 255, 0), 4)
    cv2.circle(img_raw, (b2[8], b2[9]), 1, (255, 0, 0), 4)
    b2 = [907, 312, 977, 338, 919, 353, 895, 382, 937, 402]
    cv2.circle(img_raw, (b2[0], b2[1]), 1, (0, 0, 255), 4)
    cv2.circle(img_raw, (b2[2], b2[3]), 1, (0, 255, 255), 4)
    cv2.circle(img_raw, (b2[4], b2[5]), 1, (255, 0, 255), 4)
    cv2.circle(img_raw, (b2[6], b2[7]), 1, (0, 255, 0), 4)
    cv2.circle(img_raw, (b2[8], b2[9]), 1, (255, 0, 0), 4)
    b2 = [753, 201, 753, 199, 763, 226, 757, 262, 760, 261]
    cv2.circle(img_raw, (b2[0], b2[1]), 1, (0, 0, 255), 4)
    cv2.circle(img_raw, (b2[2], b2[3]), 1, (0, 255, 255), 4)
    cv2.circle(img_raw, (b2[4], b2[5]), 1, (255, 0, 255), 4)
    cv2.circle(img_raw, (b2[6], b2[7]), 1, (0, 255, 0), 4)
    cv2.circle(img_raw, (b2[8], b2[9]), 1, (255, 0, 0), 4)

    return img_raw
