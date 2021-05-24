from fuzzysearch import find_near_matches
from ramayanam import Ramayanam
from pyfiglet import Figlet
from wcwidth import wcswidth
from prompt_toolkit import prompt
import ftfy
import os.path
import time
from iterfzf import iterfzf

# f = Figlet(font='slant')

# print(f.renderText('Sri Ramayanam'))

# print()

r = Ramayanam.load()

s = r.kanda(1).sarga(8).sloka(20)

# print(s, s.id)

# print('------------------------------------')
# print(ftfy.fix_text(s._text))
# print('------------------------------------')


# print(find_near_matches('PATTERN', 'aaa PATERN', max_l_dist=3))



kanda = r.kanda(1)
trans_kanda = kanda.all()

print('------------------------------------')
print(r.details())
print('------------------------------------')

translations = trans_kanda[:100]


def iter_pokemon(slp=0.01):
    for l in translations:
        yield l
        time.sleep(slp)


def main():
    result = iterfzf(iter_pokemon(), multi=True)
    for item in result:
        print(item)
        # print(ftfy.fix_textitem)


# if __name__ == '__main__':
#     main()
