import cv2

def setBoxesToImage(path, boxes=[408,135,249,331]):
    image = cv2.imread(path)

    image = cv2.rectangle(image, (boxes[3], boxes[2]), (boxes[1], boxes[0]), (255, 0, 0), 2)

    return image


