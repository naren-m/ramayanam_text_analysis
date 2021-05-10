from fuzzysearch import find_near_matches
from ramayanam import Ramayanam
from pyfiglet import Figlet
from wcwidth import wcswidth
from prompt_toolkit import prompt
import ftfy

f = Figlet(font='slant')

print(f.renderText('Sri Ramayanam'))

r = Ramayanam.load()

s = r.kanda(1).sarga(8).sloka(20)

print(s, s.id)
print(wcswidth('コンニチハ'))

print('------------------------------------')
print(ftfy.fix_text(s._text))
print('------------------------------------')


print(find_near_matches('PATTERN', 'aaa PATERN', max_l_dist=3))



# if __name__ == '__main__':
#     answer = prompt('Give me some input: ')
#     print('You said: %s' % answer)