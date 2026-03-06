#!/usr/bin/env python3
from collections import Counter

def readc(path):
    with open(path, "r") as f:
        s = f.read()
        
    return s

def topn(text, n, topn):
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    return Counter(ngrams).most_common(topn)

def main():
    ct = readc("../../chall/1.enc")

    print("Monograms:")
    mons = topn(ct, 1, 10)
    for rank, (gram, count) in enumerate(mons, 1):
        print(f"{rank}. {gram}: {count} times")


    print("\nBigrams:")
    bigs = topn(ct, 2, 10)
    for rank, (gram, count) in enumerate(bigs, 1):
        print(f"{rank}. {gram}: {count} times")

    print("\nTrigrams:")
    trigs = topn(ct, 3, 10)
    for rank, (gram, count) in enumerate(trigs, 1):
        print(f"{rank}. {gram}: {count} times")

if __name__ == "__main__":
    main()