from fuzzysearch import find_near_matches

from ramayanam import Ramayanam


r = Ramayanam.load()

s = r.kandas[1].sargas[8].slokas[20]
print(len(r.kandas[1].sargas[8].slokas))
print(s)

print(r.kandas[5].sargas[4].slokas[14].id)

print(find_near_matches('PATTERN', 'aaa PTTEaaa', max_l_dist=3))
