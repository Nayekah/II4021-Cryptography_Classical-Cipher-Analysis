#!/usr/bin/env python3
from collections import Counter

with open("../../chall/2.enc", "r") as f:
    ct = f.read().strip()

def freq(text, n, topk):
    freq = Counter(text[i:i+n] for i in range(len(text) - n + 1))
    return freq.most_common(topk)

def show(title, items):
    print(f"\n{title}")
    for i, (k, v) in enumerate(items, 1):
        print(f"{i:2d}. {k} : {v}")

show("Monograms:", freq(ct, 1, 10))
show("Bigrams:", freq(ct, 2, 10))
show("Trigrams:", freq(ct, 3, 10))
show("Quadgrams:", freq(ct, 4, 10))