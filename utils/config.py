import configparser
import os


def initConfigFile():

    configuracion = configparser.ConfigParser()
    if not os.path.exists('./gui_config.cfg'):
        configuracion['workspace'] = {
            'last_folder': 'empty', 'last_index': '-1'}
        with open('./gui_config.cfg', 'w') as archivoconfig:
            configuracion.write(archivoconfig)


def getConfig():

    configuracion = configparser.ConfigParser()

    configuracion.read('./gui_config.cfg')
    workspace = configuracion['workspace']

    return str(workspace['last_folder']), int(workspace['last_index'])


def setConfig(folder, index):

    configuracion = configparser.ConfigParser()

    configuracion['workspace'] = {
        'last_folder': folder, 'last_index': '{}'.format(index)}
    with open('./gui_config.cfg', 'w') as archivoconfig:
        configuracion.write(archivoconfig)
