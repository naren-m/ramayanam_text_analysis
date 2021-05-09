
from ramayanam import Ramayanam

r = Ramayanam.load()
# for _, k in r.kandas.items():
#     print(k)
#     for _, s  in k.sargas.items():
#         print(s)
#         for num, sloka in s.slokas.items():
#             print(num, len(s.slokas), sloka)

s = str(r.kandas[1].sargas[8].slokas[20])
len(r.kandas[1].sargas[8].slokas)
print(s)
print(s.encode('utf-8').decode('utf-8'))


if __name__ == "__main__":
    r = Ramayanam.load()

    s = r.kandas[1].sargas[1].slokas[1]

    len(r.kandas[1].sargas[8].slokas)
    print(s)
    print(s.meaning)
    print(s.translation)
