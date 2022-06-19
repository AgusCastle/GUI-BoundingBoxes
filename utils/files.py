import glob
import os
import shutil


def returnAllfilesbyType(path, tfile):
    path_full = path + '/*' + tfile
    return glob.glob(path_full)


def imagenInapropiada(root, path_img, path_xml, name_img, name_xml):
    full_path = root + '/inappropiate/ImagesJPGs'
    os.makedirs(full_path, exist_ok=True)

    source = r'' + path_img
    destination = r'' + full_path + '/' + name_img

    shutil.move(source, destination)

    full_path = root + '/inappropiate/annotations'
    os.makedirs(full_path, exist_ok=True)
    source = r'' + path_xml
    destination = r'' + full_path + '/' + name_xml

    shutil.move(source, destination)


def imagenSinObjetos(root, path_img, path_xml, name_img, name_xml):
    full_path = root + '/empty/ImagesJPGs'
    os.makedirs(full_path, exist_ok=True)

    source = r'' + path_img
    destination = r'' + full_path + '/' + name_img

    shutil.move(source, destination)

    full_path = root + '/empty/annotations'
    os.makedirs(full_path, exist_ok=True)
    source = r'' + path_xml
    destination = r'' + full_path + '/' + name_xml

    shutil.move(source, destination)
