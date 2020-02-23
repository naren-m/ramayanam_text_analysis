import os

root_dir = os.getcwd() + "/"
sloka_root = os.path.join(root_dir, "Slokas")
print(root_dir, sloka_root)


def fileExists(fileName):
    if os.path.isfile(fileName):
        return True

    return False


fileNameFormat = '{kandaName}_sarga_{sargaNum}_{fileType}.txt'

typesOfFiles = ['sloka', 'translation', 'meaning']

# for k in KandaList:
#     p = os.path.join(sloka_root, k['name'])
#     for t in typesOfFiles:
#         f = fileNameFormat.format(kandaName=k['name'],
#                                   sargaNum=k['sargas'],
#                                   fileType=t)

fileName = '/Users/nmudivar/Projects/personal/ramayanam_text_analysis/Slokas/KishkindaKanda/KishkindaKanda_sarga_67_sloka.txt'


def readSlokaFile(fname):
    if not fileExists(fname):
        raise Exception('File not found. File {}'.format(fname))

    with open(fname, 'r') as f:
        for line in f.readlines():
            print(line)
            print(line.split('::'))


readSlokaFile(fileName)

from database import Database

db = Database('./ramayanam.db')
columns = 'kanda_id, sarga_id, sloka_id, sloka, meaning, translation'
with db:
    rows = db.get(table='slokas', columns=columns, limit=4)

from ramayana import Sloka

for row in rows:
    print('kanda {}, sarga {}, sloka {}'.format(row[0], row[1], row[2]))
    print('meaning {}, translation {}, sloka {}'.format(
        row[4], row[5], row[3]))
    s = Sloka(kanda=row[0],
              sarga=row[1],
              number=row[2],
              text=row[3],
              meaning=row[4],
              translation=row[5])

print(s)

from ramayana import Ramayana

r = Ramayana()
print(r)
r._loadFromDB()