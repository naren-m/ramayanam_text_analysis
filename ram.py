
# from ramayanam import Ramayanam
import ramayanam

r = ramayanam.Ramayanam.load()

s = r.kandas[1].sargas[8].slokas[20]
print(len(r.kandas[1].sargas[8].slokas))
print(s)
