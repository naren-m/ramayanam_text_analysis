
# from ramayanam import Ramayanam
import ramayanam

r = ramayanam.Ramayanam.load()

s = str(r.kandas[1].sargas[8].slokas[20])
len(r.kandas[1].sargas[8].slokas)
print(s)
print(s.encode('utf-8').decode('utf-8'))
