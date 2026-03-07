#!/usr/bin/env python3
from collections import Counter

with open("../../chall/3.enc", "r") as f:
    ct = f.read().strip()

def freq(text, n, topk):
    freq = Counter(text[i:i+n] for i in range(len(text) - n + 1))
    return freq.most_common(topk)

def show(title, items):
    print(f"\n{title}")
    for i, (k, v) in enumerate(items, 1):
        print(f"{i:2d}. {k} : {v}")

show("Monograms:", freq(ct, 1, 20))
show("Bigrams:", freq(ct, 2, 20))
show("Trigrams:", freq(ct, 3, 20))