import xml.etree.ElementTree as ET
import operator

labels = {'other': -1, 'cloth': 1, 'other': 2, 'none': 3,
          'respirator': 4, 'surgical': 5, 'valve': 6}


def xml_annotation(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    boxes = list()
    labels = list()
    faces = int(root.find("faces").text)
    for object in root.iter('object'):
        label = object.find('label').text
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
        labels.append(int(label))
    return {'name': root.find('filename').text, 'boxes': boxes, 'labels': labels, 'faces': faces}


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
    if aux != None:
        root.remove(aux)
    tree.write(xml_path)


def xml_get_name(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    return root.find('filename').text


def xml_update_faces(xml_path, op):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    if op:
        root.find('faces').text = str(-1)
    else:
        root.find('faces').text = str(0)

    tree.write(xml_path)


def xml_get_faces(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    return root.find('faces').text


def xml_sort(xml_paths, img_paths):

    # Las listas llegan ordenadas
    labels_list = {}
    for idx, path_xml in enumerate(xml_paths):
        tree = ET.parse(path_xml)
        root = tree.getroot()
        labels_list[idx] = int(root.find('object').find('label').text)

    sort = sorted(labels_list.items(),
                  key=operator.itemgetter(1), reverse=True)

    xml = []
    img = []
    for i in sort.values():
        xml.append(xml_paths[i])
        img.append(img_paths[i])

    return xml, img
