
# coding: utf-8


from bs4 import BeautifulSoup
import requests
import os
import codecs


# Ramayanam metadata

KandaList = []

KandaDetails = {'num': 1, 'name': "BalaKanda", 'sargas': 77}
KandaList.append(KandaDetails)
KandaDetails = {'num': 2, 'name': "AyodhyaKanda", 'sargas': 119}
KandaList.append(KandaDetails)
KandaDetails = {'num': 3, 'name': "AranyaKanda", 'sargas': 75}
KandaList.append(KandaDetails)
KandaDetails = {'num': 4, 'name': "KishkindaKanda", 'sargas': 67}
KandaList.append(KandaDetails)
KandaDetails = {'num': 5, 'name': "SundaraKanda", 'sargas': 68}
KandaList.append(KandaDetails)
KandaDetails = {'num': 6, 'name': "YuddhaKanda", 'sargas': 128}
KandaList.append(KandaDetails)


def clean_text(text):
    text = text.replace("\n", "")
    text = text.replace("\"", "")

    return text


def generate_url(kanda, sarga, language="dv"):
    url = "https://www.valmiki.iitk.ac.in/sloka?field_kanda_tid=" + \
        kanda + "&language=" + language + "&field_sarga_value=" + sarga
    return url


def generate_filename(kanda_name, sarga_num, kind):
    if kind is None:
        kind = ""
    else:
        kind = "_" + kind

    file_name = kanda_name + "_" + "sarga_" + sarga_num + kind + ".txt"
    return file_name


def readSlokasFromUrlAndWriteToFile(kanda_name, kanda_num, sarga_num,
                                    folder_path):
    url = generate_url(kanda=kanda_num, sarga=sarga_num, language="dv")
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    mydivs = soup.findAll("div", {"class": "view-content"})
    mydivs = soup.find_all("div", class_="view-content")
    div_string = ""

    for a in mydivs:
        div_string = div_string + str(a)

    div_contents = BeautifulSoup(div_string)
    sloka_divs = div_contents.findAll("div", {"class": "field-content"})

    lines = []

    for a in sloka_divs:
        temp = str(a).strip()
        line = temp[temp.find('>') + 1:]
        line = line.replace('</div>', '')
        line = line.replace('<br/>', '')

        lines.append(line)

    slokas = []
    word_meaning = []
    translation = []
    for i in range(0, len(lines)):
        if(i % 3 == 0):
            slokas.append(lines[i])  # .replace('।','।\n',1)#
        if(i % 3 == 1):
            word_meaning.append(lines[i])
        if(i % 3 == 2):
            translation.append(lines[i])

    sloka_fn = os.path.join(folder_path,
                            generate_filename(kanda_name=kanda_name,
                                              sarga_num=sarga_num,
                                              kind="sloka"))
    mean_fn = os.path.join(folder_path,
                           generate_filename(kanda_name=kanda_name,
                                             sarga_num=sarga_num,
                                             kind="meaning"))
    trans_fn = os.path.join(folder_path,
                            generate_filename(kanda_name=kanda_name,
                                              sarga_num=sarga_num,
                                              kind="translation"))

    f_sloka = codecs.open(sloka_fn, encoding='utf-8', mode='w+')
    f_meaning = codecs.open(mean_fn, encoding='utf-8', mode='w+')
    f_translation = codecs.open(trans_fn, encoding='utf-8', mode='w+')

    delimiter = "::"

    for i in range(0, len(slokas)):
        sloka_num = str(i + 1)
        prefix = kanda_num + delimiter + sarga_num + delimiter + sloka_num
        f_sloka.write(prefix + delimiter + clean_text(slokas[i]) + "\n")
        f_meaning.write(prefix + delimiter +
                        clean_text(word_meaning[i]) + "\n")
        f_translation.write(prefix + delimiter +
                            clean_text(translation[i]) + "\n")

    return (slokas, word_meaning, translation)


# fp = "/Users/nmudivar/go/src/github.com/naren-m/ramayanam/Slokas"
# s, m, t = readSlokasFromUrlAndWriteToFile("BalaKanda", "1", "1", fp)
# s, m, t = readSlokasFromUrlAndWriteToFile("BalaKanda", "1", "2", fp)


def main():
    sloka_root = os.path.join(os.getcwd(), "Slokas/")

    for kand in KandaList:
        # print(kand, kand['name'])
        kanda_folder = os.path.join(sloka_root + kand['name'] + os.path.sep)

        if not os.path.exists(kanda_folder):
            os.makedirs(kanda_folder)

        for sarga in range(1, kand['sargas'] + 1):
            s, m, t = readSlokasFromUrlAndWriteToFile(
                kand['name'], str(kand['num']), str(sarga), kanda_folder)

        print("Downladed", kand['name'],  "data to", kanda_folder)


if __name__ == '__main__':
    main()
