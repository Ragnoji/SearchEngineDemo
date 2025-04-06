import os
from collections import defaultdict

import pymorphy3
from bs4 import BeautifulSoup

if not os.path.exists('tokens'):
    os.makedirs('tokens')

if not os.path.exists('lemmas'):
    os.makedirs('lemmas')

def parse_html(file_id):
    with open(f"htmls/{file_id}.html", "r", encoding='utf-8') as f:
        html_string = "".join(f.readlines())
    soup = BeautifulSoup(html_string, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text(separator=" ")
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    words = ' '.join(chunks).split()

    morph = pymorphy3.MorphAnalyzer()
    tokens = set()
    lemmas = defaultdict(set)
    token_counts = defaultdict(int)
    lemma_counts = defaultdict(int)
    for w in words:
        skip_flag = False
        w = w.lower()
        for ch in w:
            if ord(ch) < ord('а') or ord(ch) > ord('я'):
                skip_flag = True
                break

        if skip_flag:
            continue

        parsed = morph.parse(w)[0]
        if parsed.tag.POS not in {'INFN', 'ADJF', 'VERB', 'NOUN'}:
            continue

        tokens.add(w)
        lemmas[parsed.normal_form].add(w)
        token_counts[w] += 1
        lemma_counts[parsed.normal_form] += 1

    with open(f'tokens/tokens{file_id}.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(tokens))

    with open(f'lemmas/lemmas{file_id}.txt', 'w', encoding='utf-8') as file:
        file.writelines([f'{p[0]} {" ".join(p[1])}\n' for p in lemmas.items()])
    return token_counts, lemma_counts


def gather_counts():
    with open('index.txt', 'r') as f:
        file_ids = [line.split()[0] for line in f.readlines()]

    token_counts = []
    lemma_counts = []
    for f_id in file_ids:
        t, l = parse_html(f_id)
        token_counts.append(t)
        lemma_counts.append(l)
    return token_counts, lemma_counts


if __name__ == '__main__':
    with open('index.txt', 'r') as f:
        file_ids = [line.split()[0] for line in f.readlines()]
    
    for f_id in file_ids:
        parse_html(f_id)