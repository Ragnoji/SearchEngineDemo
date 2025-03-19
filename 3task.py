from collections import defaultdict
from boolmatch import make_parse_tree

inverted_index = defaultdict(set)

for i in range(100):
    with open(f'lemmas/lemmas{i}.txt', 'r', encoding='utf-8') as lemmas:
        for l in lemmas.readlines():
            inverted_index[l.strip('\n').split()[0]].add(i)
with open('inverted_index.txt', 'w', encoding='utf-8') as f:
    f.writelines([f"{i[0]}: {', '.join(map(str, i[1]))}\n" for i in inverted_index.items()])


while True:
    query = input()
    if query == 'q':
        break
    tree = make_parse_tree(query)
    result = tree.matches(inverted_index)
    print([f'lemmas{i}.txt' for i in sorted(list(result))])