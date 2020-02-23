from database import Database


class Ramayana:
    def __init__(self, dbName=None):
        self._kandaDetails = {
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
        }
        self.kandas = dict()

        if dbName is None:
            self._dbName = './ramayanam.db'
        else:
            self._dbName = dbName

        self._db = Database(self._dbName)

    def addKanda(self, kanda):
        self.kandas[kanda.number] = kanda

    def _loadFromDB(self):
        for k, v in self._kandaDetails.items():
            print(k, v)
            kanda = Kanda(name=v['name'], number=k, totalSargas=v['sargas'])


class Kanda:
    def __init__(self, name, number, totalSargas):
        self.name = name
        self.number = number
        self.totalSargas = totalSargas
        self.sargas = dict()

    @property
    def sargas(self):
        return self.sargas

    def addSarga(self, sarga):
        self.sargas[sarga.number] = sarga


class Sarga:
    def __init__(self, number, kanda):
        self.number = number
        self._kanda = kanda
        self.slokas = dict()

    @property
    def slokas(self):
        return self.slokas

    def addSloka(self, sloka):
        self.slokas[sloka.number] = sloka


class Sloka:
    def __init__(self, sarga, number, text, meaning, translation):
        self.number = number
        self.sarga = sarga
        self.kanda = sarga.kanda

        self._text = text
        self._meaning = meaning
        self._translation = translation

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
        return self.text
