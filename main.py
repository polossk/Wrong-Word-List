import os
import glob
import pickle
from operator import itemgetter

GROUP_BY = ["ABCDEFG", "HIJKLMN", "OPQRST", "UVWXYZ"]


def markdown2wordlist(filename):
    data = None
    with open(filename, 'r', encoding='utf-8') as fin:
        hoge = map(str.strip, fin.readlines())
        hoge = filter(lambda x: len(x) > 0, hoge)
        hoge = filter(lambda x: x[0] != '#', hoge)
        data = sorted(hoge)
    return data


def wordlists2frqdict(wordlists):
    frq = {}
    for data in wordlists:
        for elem in data:
            if elem in frq:
                frq[elem] += 1
            else:
                frq[elem] = 1
    return frq


def frqdict2frqlist(frq_dict):
    wordlist = [item for item in frq_dict.items()]
    wordlist.sort(key=itemgetter(0))
    wordlist.sort(key=itemgetter(1), reverse=True)
    return wordlist


def count(frq_list):
    values = list(range(frq_list[0][1] + 1, 0, -1))
    for value in values[::-1]:
        cnt = sum([1 for _ in frq_list if _[1] == value])
        # print(f"record {value:2d} time(s): {cnt:4d} word(s).")
        print(cnt, end='|')
        # print(value, cnt)
    # print()
    return values


def frqlist2markdown(export, cnt, frq_list):
    cnt = cnt[:-1]
    value_and_prefix = [(v, g) for v in cnt for g in GROUP_BY]
    frq_list = list(filter(lambda x: x[1] > 1, frq_list))
    with open(export, 'w', encoding='utf-8') as fout:
        for value, prefix in value_and_prefix:
            p0, p1 = prefix[0], prefix[-1]
            data = [
                _0 + '\n' for _0, _1 in frq_list
                if _1 == value and p0 <= _0[0].upper() <= p1
            ]
            if len(data) == 0: continue
            print(f"#{value} {prefix} ({len(data)})")
            print(f"#{value} {prefix} ({len(data)})", file=fout)
            fout.writelines(data)
            print("", file=fout)


def frqlist2markdown_rank(export, cnt, frq_list, _data):
    cnt = cnt[:-1]
    byrank_, phrase_ = [[] for value in cnt], [[] for value in cnt]
    for lemma, frq in frq_list:
        if frq < 2: continue
        if lemma.find(' ') == -1:
            rank = _data[lemma.upper()]
            byrank_[frq - 2].append((lemma + '\n', rank))
        else:
            phrase_[frq - 2].append(lemma + '\n')
    with open(export, 'w', encoding='utf-8') as fout:
        value = cnt[0]
        total = 0
        for byrank, phrase in zip(byrank_[::-1], phrase_[::-1]):
            phrase = sorted(phrase)
            byrank.sort(key=itemgetter(0))
            byrank.sort(key=itemgetter(1), reverse=True)
            if len(byrank) != 0:
                print(f"#{value} byrank ({len(byrank)})")
                print(f"#{value} byrank ({len(byrank)})", file=fout)
                fout.writelines([_[0] for _ in byrank])
                print("", file=fout)
                total += len(byrank)
            if len(phrase) != 0:
                print(f"#{value} phrase ({len(phrase)})")
                print(f"#{value} phrase ({len(phrase)})", file=fout)
                fout.writelines(phrase)
                print("", file=fout)
                total += len(phrase)
            value -= 1
        print(f"total {total} word(s).")


def readRank():
    filename = "60000RANK.txt"
    data = []
    with open(filename, 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            rank, word = line.strip().split()
            rank = int(rank)
            word = word.replace('(', '').replace(')', '')
            data.append((rank, word))
    data_dict = {word: rank for rank, word in data}
    pickle.dump(data_dict, open('data_dict.bin', 'wb'))
    return data_dict


# def readRank():
#     return pickle.load(open('data_dict.bin', 'rb'))


def main():
    readRank()
    worklist_pattern = r".\data\????-??-??-*.txt"
    worklist = glob.glob(worklist_pattern)
    wordlists = [markdown2wordlist(_) for _ in worklist]
    frq_dict = wordlists2frqdict(wordlists)
    frq_list = frqdict2frqlist(frq_dict)
    cnt = count(frq_list)
    frqlist2markdown("Wrong-Word-List-Group-by-Error-Frequency.txt", cnt,
                     frq_list)
    frqlist2markdown_rank("Wrong-Word-List-Group-by-Using-Frequency.txt", cnt,
                          frq_list, readRank())


if __name__ == "__main__":
    main()