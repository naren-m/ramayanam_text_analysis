from database import Database

import pickle

class AttrDict(dict):
    def __setattr__(self, attr, value):
        self[attr] = value

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr) from None

    def __delattr__(self, attr):
        try:
            del self[attr]
        except KeyError:
            raise AttributeError(attr) from None

    def __dir__(self):
        return list(self) + dir(dict)


class Ramayana:
    kandaDetails = dict({
            1: {
                'id': 1,
                'name': "BalaKanda",
                'sargas': 77
            },
            2: {
                'id': 2,
                'name': "AyodhyaKanda",
                'sargas': 119
            },
            3: {
                'id': 3,
                'name': "AranyaKanda",
                'sargas': 75
            },
            4: {
                'id': 4,
                'name': "KishkindaKanda",
                'sargas': 67
            },
            5: {
                'id': 5,
                'name': "SundaraKanda",
                'sargas': 68
            }
        })

    def __init__(self):
        self.kandas = dict()

    def addKanda(self, kanda):
        self.kandas[kanda.number] = kanda

    @classmethod
    def load(cls, dbName='./ramayanam.db', pickleFile='./ramayanam.pkl'):
        if os.path.exists(pickleFile):
            with open(pickleFile, 'rb') as f:
                r = pickle.load(f)
                return r
        else:
            r = cls()
            db = Database(dbName)

            for k, v in r.kandaDetails.items():
                kanda = Kanda.createKandaFromDict(v, db=db)
                r.addKanda(kanda)

            db.close()

            return r


class Kanda:
    def __init__(self, name, number, totalSargas):
        self.name = name
        self.number = number
        self.totalSargas = totalSargas
        self.sargas = dict()

    def addSarga(self, sarga):
        self.sargas[sarga.number] = sarga

    def __str__(self):
        return '{} has {} sargas'.format(self.name, self.totalSargas)

    @classmethod
    def createKandaFromDict(cls, kandaMetadata, db):
        kanda = cls(name=kandaMetadata['name'], number=kandaMetadata['id'], totalSargas=kandaMetadata['sargas'])
        for s in range(kanda.totalSargas):
            sarga = Sarga.loadFromDB(number=s, kanda=kanda, db=db)
            kanda.addSarga(sarga)
        return kanda

class Sarga:
    def __init__(self, number, kanda):
        self.number = number
        self.kanda = kanda
        self.slokas = dict()

    def addSloka(self, sloka):
        self.slokas[sloka.number] = sloka

    def __str__(self):
        return 'Sarga {} of {} has {} slokas'.format(self.number, self.kanda.name, len(self.slokas))

    @classmethod
    def loadFromDB(cls, number, kanda, db):
        sarga = cls(number=number, kanda=kanda)
        columns = 'kanda_id, sarga_id, sloka_id, sloka, meaning, translation'
        where = 'kanda_id={} and sarga_id={}'.format(kanda.number, sarga.number)
        rows = db.get(table='slokas', columns=columns, where=where)
    
        for row in rows:
            row = AttrDict(row)
            sloka = Sloka(sarga, row.sloka_id, row.sloka, row.meaning, row.translation)
            sarga.addSloka(sloka)
        return sarga


class Sloka:
    def __init__(self, sarga, number, text, meaning, translation):
        self.number = number
        self.sarga = sarga

        self._text = text
        self._meaning = meaning
        self._translation = translation


    @property
    def kanda(self):
        return self.sarga.kanda

    @property
    def meaning(self):
        return self._meaning

    @property
    def translation(self):
        return self._translation

    @property
    def text(self):
        return self._text

    def __str__(self):
        if not self.text:
            return 'Something went wrong. Debug'
        return self.text

    @classmethod
    def loadFromData(cls, sarga, number, text, meaning, translation):
        sloka = Sloka(sarga, number, text, meaning, translation)
        return sloka

if __name__ == "__main__":
    r = Ramayana.load()

    s = r.kandas[1].sargas[8].slokas[20]

    len(r.kandas[1].sargas[8].slokas)
    print(s)
    print(s.meaning)
    print(s.translation)