import os
import math
from collections import Counter

gather_counts = __import__('2task').gather_counts

def read_tokens(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]

def read_lemmas(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]

def compute_tf(term_counts, total_terms):
    return {term: count / total_terms for term, count in term_counts.items()}

def compute_idf(doc_term_counts, num_docs):
    idf = {}
    for term, doc_count in doc_term_counts.items():
        # Добавляем epsilon, чтобы избежать деления на ноль
        idf[term] = math.log(num_docs / (1 + doc_count)) if doc_count > 0 else 0
    return idf

def process_files():
    tokens_dir = "tokens"
    lemmas_dir = "lemmas"
    output_tokens_dir = "output_tokens"
    output_lemmas_dir = "output_lemmas"
    os.makedirs(output_tokens_dir, exist_ok=True)
    os.makedirs(output_lemmas_dir, exist_ok=True)

    num_docs = 100
    doc_term_counts = Counter()
    doc_lemma_counts = Counter()
    term_frequencies = {}
    lemma_frequencies = {}
    token_counts, lemma_counts = gather_counts()

    for i in range(num_docs):
        doc_term_counts.update(token_counts[i])
        doc_lemma_counts.update(lemma_counts[i])

        total_terms = sum(token_counts[i].values())
        total_lemmas = sum(lemma_counts[i].values())

        if total_terms > 0:
            term_frequencies[i] = compute_tf(token_counts[i], total_terms)
        if total_lemmas > 0:
            lemma_frequencies[i] = compute_tf(lemma_counts[i], total_lemmas)

    idf_terms = compute_idf(doc_term_counts, num_docs)
    idf_lemmas = compute_idf(doc_lemma_counts, num_docs)

    for i in range(num_docs):
        token_output_file = os.path.join(output_tokens_dir, f"page_{i}_tfidf.txt")
        lemma_output_file = os.path.join(output_lemmas_dir, f"page_{i}_tfidf.txt")

        with open(token_output_file, "w", encoding="utf-8") as f:
            for term, tf in term_frequencies.get(i, {}).items():
                tfidf = tf * idf_terms[term]
                f.write(f"{term} {idf_terms[term]:.6f} {tfidf:.6f}\n")

        with open(lemma_output_file, "w", encoding="utf-8") as f:
            for lemma, tf in lemma_frequencies.get(i, {}).items():
                tfidf = tf * idf_lemmas[lemma]
                f.write(f"{lemma} {idf_lemmas[lemma]:.6f} {tfidf:.6f}\n")
    return lemma_counts, doc_lemma_counts

if __name__ == "__main__":
    process_files()
