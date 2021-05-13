import unittest

# from .ramayanam import Ramayanam
from ramayanam import Ramayanam


class TestRamayanam(unittest.TestCase):
    def test__init(self):
        pass

    def test_id(self):
        r = Ramayanam.load()

        kanda_id = 1
        sarga_id = 9
        sloka_id = 2
        expected_sloka_id = '{}.{}.{}'.format(kanda_id, sarga_id, sloka_id)

        sloka = r.kanda(kanda_id).sarga(sarga_id).sloka(sloka_id)
        # print(sloka, sloka.id)
        # print(sloka.meaning)
        # print(sloka.translation)
        self.assertEqual(sloka.id, expected_sloka_id)

    def test_all(self):
        r = Ramayanam.load()
        t = r.all()
        print(t)