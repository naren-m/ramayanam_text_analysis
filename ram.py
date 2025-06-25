from fuzzysearch import find_near_matches
from ramayanam import Ramayanam
from pyfiglet import Figlet
from prompt_toolkit import prompt, print_formatted_text, HTML, ANSI


f = Figlet(font='slant')
print(f.renderText('Sri Ramayanam'))


r = Ramayanam.load()

s = r.kanda(1).sarga(8).sloka(20)





### Sanskrit-parser
def callParser():
    import requests

    url = "https://sanskrit-parser.appspot.com/sanskrit_parser/v1/splits/वाल्मीकिर्मुनिपुङ्गवम्"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

print_formatted_text(ANSI('\x1b[31mhello \x1b[32mworld'))

# x = callParser()
# print_formatted_text(HTML('<aaa fg="ansiwhite" bg="ansigreen">{}</aaa>'.format(x['splits'])))



for k in r:
    for s in k:
        for sl in s:
            trans = str(sl.translation).strip()
            if trans:
                print(trans, type(trans))
                x = find_near_matches(trans, 'ram', max_l_dist=1)
                if x:
                    print(x)