import os

from .ramayana import Sloka

root_dir = os.getcwd() + "/"
sloka_root = os.path.join(root_dir, "Slokas")
print(root_dir, sloka_root)

def fileExists(fileName):
    if os.path.isfile(fileName):
        return True

    return False

fileNameFormat = '{kandaName}_sarga_{sargaNum}_{fileType}.txt'

typesOfFiles = ['sloka', 'translation', 'meaning']

for k in KandaList:
    p = os.path.join(sloka_root, k['name'])
    for t in typesOfFiles:
        f = fileNameFormat.format(kandaName=k['name'], sargaNum=k['sargas'], fileType=t)


fileName = '/Users/nmudivar/Projects/personal/ramayanam_text_analysis/Slokas/KishkindaKanda/KishkindaKanda_sarga_67_sloka.txt'


def readSlokaFile(fname):
    if not fileExists(fname):
        raise Exception('File not found. File {}'.format(fname))

    with open(fname, 'r') as f:
        for line in f.readlines():
            print(line)
            print(line.split('::'))



readSlokaFile(fileName)




