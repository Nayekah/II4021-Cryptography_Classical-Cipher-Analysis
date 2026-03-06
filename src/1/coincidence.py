#!/usr/bin/env python3
from collections import Counter

def readc(path):
    with open(path, "r") as f:
        s = f.read()
        
    return s

def calc(text):
    n = len(text)
    
    freq = Counter(text)
    num = 0
    for f in freq.values():
        num += f * (f - 1)
        
    den = n * (n - 1)
    return num / den

def check(ct, keylen):
    cols = [""] * keylen
    for i, char in enumerate(ct):
        cols[i % keylen] += char
        
    total = 0
    for col in cols:
        total += calc(col)
        
    return total / keylen

def main():
    ct = readc("../../chall/1.enc")
    cand = [2, 3, 4, 8, 16]
    
    res = []
    for k in cand:
        avg = check(ct, k)
        res.append((avg, k))

    res.sort(reverse=True)
    for avg, k in res:
        print(f"Keylen: {k} | IC: {avg:.4f}")

if __name__ == "__main__":
    main()