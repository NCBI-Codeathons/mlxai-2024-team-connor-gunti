import argparse
import numpy as np
import pandas as pd

from nltk.metrics.distance import jaccard_distance
from rouge_score import rouge_scorer


def r_score(a):
    rouger1 = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)

    chunk = pd.read_csv(f'../attributes/{a}.entries.tsv', sep = '\t', names=['text'])

    sentences = chunk.text.values.tolist()
    dim = len(sentences)

    rou = np.zeros((dim, dim)).astype(np.float32)

    tokens = [set(s.split()) for s in sentences]

    for i, j in zip(*np.tril_indices(dim, -1)):
        rou[i, j] = rouger1.score(sentences[j], sentences[i])['rouge1'].precision
            
    np.save(f'../scores/{a}.rouge1.scores', rou, allow_pickle = False)

def j_score(a):
    chunk = pd.read_csv(f'../attributes/{a}.entries.tsv', sep = '\t', names=['text'])

    sentences = chunk.text.values.tolist()
    dim = len(sentences)

    jac = np.zeros((dim, dim)).astype(np.float32)

    tokens = [set(s.split()) for s in sentences]

    for i, j in zip(*np.tril_indices(dim, -1)):
        jac[i, j] = 1 - jaccard_distance(tokens[j], tokens[i])
            
    np.save(f'../scores/{a}.jaccard.scores', jac, allow_pickle = False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attr')
    parser.add_argument('--score', choices=['jaccard', 'rouge'])

    args = parser.parse_args()

    if args.score == 'jaccard':
        j_score(args.attr)
    else:
        r_score(args.attr)

if __name__ == '__main__':
    main()
    
