import xml.etree.ElementTree as ET

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
        xmax = int(bbox.find('xmax').text) - 1
        ymax = int(bbox.find('ymax').text) - 1
        boxes.append([xmin, ymin, xmax, ymax])
        labels.append(label)
    return {'name': root.find('filename').text, 'boxes': boxes, 'labels': labels}
