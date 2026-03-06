#!/usr/bin/env python3
from sympy import divisors
from collections import defaultdict, Counter

def readc(path):
    with open(path, "r") as f:
        s = f.read()
        
    return s

def factors(n): return set(divisors(n))
def frepeated(ct, nmin, nmax):
    occ = defaultdict(list)
    L = len(ct)

    for n in range(nmin, nmax + 1):
        for i in range(0, L - n + 1):
            gram = ct[i:i+n]
            occ[(n, gram)].append(i)

    rep = {}
    for key, pos in occ.items():
        if len(pos) >= 2:
            rep[key] = pos
    return rep

def main():
    ct = readc("../../chall/1.enc")
    repeated = frepeated(ct, 3, 999)
    
    distances = []
    
    for _, pos in repeated.items():
        for i in range(len(pos) - 1):
            distances.append(pos[i+1] - pos[i])

    facs = []
    for d in distances:
        fs = factors(d)
        fs.discard(1)
        facs.extend(fs)

    count = Counter(facs)
    topn = count.most_common(5)
    
    for cand, count in topn:
        print(f"Keylen: {cand}")

if __name__ == "__main__":
    main()