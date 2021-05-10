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
        sloka = r.kandas[kanda_id].sargas[sarga_id].slokas[sloka_id]
        print(sloka, sloka.id)

        self.assertEqual(sloka.id, expected_sloka_id)
