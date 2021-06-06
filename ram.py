from fuzzysearch import find_near_matches
from ramayanam import Ramayanam
from pyfiglet import Figlet
from prompt_toolkit import prompt
from iterfzf import iterfzf

f = Figlet(font='slant')
print(f.renderText('Sri Ramayanam'))
print()

r = Ramayanam.load()

s = r.kanda(1).sarga(8).sloka(20)

for k in r:
    print(k)
    for s in k:
        print(s)
        for sl in s:
            print(sl)
