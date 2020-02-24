import os

root_dir = os.getcwd() + "/"
sloka_root = os.path.join(root_dir, "Slokas")
print(root_dir, sloka_root)


def readSlokaFile(fname):
    if not fileExists(fname):
        raise Exception('File not found. File {}'.format(fname))

    with open(fname, 'r') as f:
        for line in f.readlines():
            print(line)
            print(line.split('::'))


# readSlokaFile(fileName)

from database import Database

db = Database('./ramayanam.db')
columns = 'kanda_id, sarga_id, sloka_id, sloka, meaning, translation'
with db:
    rows = db.get(table='slokas', columns=columns, limit=2, where='kanda_id=1 and sarga_id=1')


for r in rows:
    print(r)

from ramayana import Sloka
from ramayana import Ramayana

r = Ramayana()
print(r)
r.loadFromDB()
for _, k in r.kandas.items():
    print(k)
    for _, s  in k.sargas.items():
        print(s)
        for num, sloka in s.slokas.items():
            print(num, len(s.slokas), sloka)

print(r.kandas[1].sargas[8].slokas[21])
len(r.kandas[1].sargas[8].slokas)

