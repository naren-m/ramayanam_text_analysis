
class Ramayana:
    def __init__(self):
        self._metadata = {1: {'id': 1, 'name': "BalaKanda", 'sargas': 77},
                          2: {'id': 2, 'name': "AyodhyaKanda", 'sargas': 119},
                          3: {'id': 3, 'name': "AranyaKanda", 'sargas': 75},
                          4: {'id': 4, 'name': "KishkindaKanda", 'sargas': 67},
                          5: {'id': 5, 'name': "SundaraKanda", 'sargas': 68}}
        self.kandas = dict()
        self._dbName = './ramayanam.db'

    def addKanda(self, kanda):
        self.kandas[kanda.number] = kanda


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
        self.kanda = kanda
        self.slokas = dict()

    @property
    def slokas(self):
        return self.slokas
    
    def addSloka(self, sloka):
        self.slokas[sloka.number] = sloka


class Sloka:
    def __init__(self, number, kanda, sarga):
        self.number = number
        self.kanda = kanda
        self.sarga = sarga

        self._text = None
        self._meaning = None
        self._translation = None

    @property
    def meaning(self):
        return self._meaning

    @property
    def translation(self):
        return self._translation

    @property
    def text(self):
        return self._text

    @meaning.setter
    def meaning(self, meaning):
        self._meaning = meaning

    @translation.setter
    def translation(self, translation):
        self._translation = translation

    @text.setter
    def text(self, text):
        self._text = text
