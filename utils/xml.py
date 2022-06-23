import xml.etree.ElementTree as ET
labels = {'other': 0, 'cloth': 1, 'other': 2, 'none': 3,
          'respirator': 4, 'surgical': 5, 'valve': 6}


def xml_annotation(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    boxes = list()
    labels = list()
    for object in root.iter('object'):
        label = object.find('name').text.lower().strip()
        bbox = object.find('bndbox')

        xmin = int(bbox.find('xmin').text) - 1
        ymin = int(bbox.find('ymin').text) - 1

        if int(bbox.find('xmin').text) - 1 < 0:
            xmin = 0
        if int(bbox.find('ymin').text) - 1 < 0:
            ymin = 0
        xmax = int(bbox.find('xmax').text) - 1
        ymax = int(bbox.find('ymax').text) - 1
        boxes.append([xmin, ymin, xmax, ymax])
        labels.append(label)
    return {'name': root.find('filename').text, 'boxes': boxes, 'labels': labels}


def xml_update(xml_path, index, new_class):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for i, object in enumerate(root.iter('object')):
        if i == index:
            object.find('name').text = new_class
            object.find('label').text = str(labels[new_class])
            object.find('score').text = "2.0"
    tree.write(xml_path)


def xml_delete_bounding(xml_path, index):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    aux = None
    size = 0
    for i, object in enumerate(root.iter('object')):
        if i == index:
            aux = object
        size += 1

    root.find('faces').text = str(size - 1)
    root.remove(aux)
    tree.write(xml_path)


def xml_get_name(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    return root.find('filename').text


def xml_get_faces(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    return root.find('faces').text
