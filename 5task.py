from flask import Flask, render_template, request, send_from_directory
from numpy import dot
from numpy.linalg import norm
import pymorphy3
from collections import defaultdict

lemma_counts, doc_lemma_counts = __import__('4task').process_files()

compute_idf = __import__('4task').compute_idf
compute_tf = __import__('4task').compute_tf

for i in lemma_counts:
    for w in doc_lemma_counts.keys():
        i[w] += 0


app = Flask(__name__)

def parse_query(text):
    global lemma_counts
    global doc_lemma_counts
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    words = ' '.join(chunks).split()

    morph = pymorphy3.MorphAnalyzer()
    lemma_counts.append(defaultdict(int))
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

        lemma_counts[-1][parsed.normal_form] += 1
    doc_lemma_counts.update(lemma_counts[-1])

    tf_f = compute_tf(lemma_counts[-1], sum(lemma_counts[-1].values()))
    idf_f = compute_idf(doc_lemma_counts, len(lemma_counts))
    q_vector = defaultdict(int)
    for lemma, tf in tf_f.items():
        tfidf = tf * idf_f[lemma]
        q_vector[lemma] = tfidf
    cosine_similarities = []
    vectors = []
    for i in range(len(lemma_counts)):
        tf_f = compute_tf(lemma_counts[i], sum(lemma_counts[i].values()))
        vector = defaultdict(int)
        for lemma, tf in tf_f.items():
            tfidf = tf * idf_f[lemma]
            vector[lemma] = tfidf
        for w in q_vector.keys():
            vector[w] += 0
        vectors.append([i[1] for i in sorted(vector.items(), key=lambda x: x[0])])
    for w in doc_lemma_counts.keys():
        q_vector[w] += 0
    q_vector = [i[1] for i in sorted(q_vector.items(), key=lambda x: x[0])]

    for i in range(len(lemma_counts) - 1):
        v = vectors[i]
        cos_sim = dot(q_vector, v) / (norm(q_vector) * norm(v))
        cosine_similarities.append((i, cos_sim))
    cosine_similarities.sort(key=lambda x: x[1], reverse=True)
    relevant = [i[0] for i in cosine_similarities[:10]]

    for k, v in lemma_counts[-1].items():
        doc_lemma_counts[k] -= v
        if doc_lemma_counts[k] == 0:
            del doc_lemma_counts[k]
    del lemma_counts[-1]
    return relevant

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/page/<int:page_number>.html')
def page(page_number):
    return send_from_directory('htmls', f'{page_number}.html')

@app.route("/search", methods=["POST"])
def search():
    query = request.form["query"]
    top_indices = parse_query(query)

    results = [(f'page/{i}.html', f'{i}.html') for i in top_indices]

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)

