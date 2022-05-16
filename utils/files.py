import glob

def returnAllfilesbyType(path, tfile):
    path_full = path + '/*' + tfile
    return glob.glob(path_full)

    


