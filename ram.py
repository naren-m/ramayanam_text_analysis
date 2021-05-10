from fuzzysearch import find_near_matches

from ramayanam import Ramayanam


r = Ramayanam.load()

s = r.kanda(1).sarga(8).sloka(20)

print(s, s.id)

print(r.kandas[5].sargas[4].slokas[14].id)

print(find_near_matches('PATTERN', 'aaa PTTEaaa', max_l_dist=3))
