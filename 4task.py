import os
import math
from collections import Counter

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

    for i in range(num_docs):
        token_file = os.path.join(tokens_dir, f"tokens{i}.txt")
        lemma_file = os.path.join(lemmas_dir, f"lemmas{i}.txt")

        tokens = read_tokens(token_file)
        lemmas = read_lemmas(lemma_file)

        token_counts = Counter(tokens)
        lemma_counts = Counter(lemmas)

        doc_term_counts.update(token_counts.keys())
        doc_lemma_counts.update(lemma_counts.keys())

        total_terms = sum(token_counts.values())
        total_lemmas = sum(lemma_counts.values())

        if total_terms > 0:
            term_frequencies[i] = compute_tf(token_counts, total_terms)
        if total_lemmas > 0:
            lemma_frequencies[i] = compute_tf(lemma_counts, total_lemmas)

    idf_terms = compute_idf(doc_term_counts, num_docs)
    idf_lemmas = compute_idf(doc_lemma_counts, num_docs)

    for i in range(num_docs):
        token_output_file = os.path.join(output_tokens_dir, f"page_{i}_tfidf.txt")
        lemma_output_file = os.path.join(output_lemmas_dir, f"page_{i}_tfidf.txt")

        with open(token_output_file, "w", encoding="utf-8") as f:
            for term, tf in term_frequencies.get(i, {}).items():
                if tf > 0 and idf_terms.get(term, 0) > 0:
                    tfidf = tf * idf_terms[term]
                    f.write(f"{term} {idf_terms[term]:.6f} {tfidf:.6f}\n")

        with open(lemma_output_file, "w", encoding="utf-8") as f:
            for lemma, tf in lemma_frequencies.get(i, {}).items():
                if tf > 0 and idf_lemmas.get(lemma, 0) > 0:
                    tfidf = tf * idf_lemmas[lemma]
                    f.write(f"{lemma} {idf_lemmas[lemma]:.6f} {tfidf:.6f}\n")

if __name__ == "__main__":
    process_files()
