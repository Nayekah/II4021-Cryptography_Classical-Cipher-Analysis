#!/usr/bin/env python3
from collections import Counter

def readc(path):
    with open(path, "r") as f:
        s = f.read()

    return s

def main():
    ct = readc("../../chall/1.enc")
    keylen = 8
    groups = [""] * keylen
    
    for i, char in enumerate(ct):
        groups[i % keylen] += char
        
    print(f"{'Most frequent letter'}")

    for i in range(keylen):
        count = Counter(groups[i])
        if groups[i]:
            comm, count = count.most_common(1)[0]
        else:
            comm, count = "-", 0

        msg = groups[i]
        print(f"{i+1} | {msg} | {comm} ({count} times)")

if __name__ == "__main__":
    main()