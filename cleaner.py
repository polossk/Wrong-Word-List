import glob

import configuration

txt_files = glob.glob(configuration.WORDLIST_PATTERN)

for text in txt_files:
    data = []
    with open(text, 'r', encoding='utf-8') as fin:
        data = fin.readlines()
    for i, elem in enumerate(data):
        elem = elem.strip()
        if elem.find(u"’") != -1:
            print(text, i, elem)
        elem = elem.replace(u"’", "'")
        data[i] = elem + '\n'
    with open(text, 'w', encoding='utf-8') as fout:
        fout.writelines(data)
