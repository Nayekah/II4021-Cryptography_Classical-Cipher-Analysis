#!/usr/bin/env python3
import os, random, math
from collections import defaultdict

alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # J -> I

def prefix(word):
    out = ""
    for ch in word:
        if ch not in out:
            out += ch

    return out

def ngidx(token):
    idx = 0
    for ch in token:
        idx = idx * 25 + alphabet.index(ch)

    return idx

def load():
    tables = []
    for path, n, weight in [("../../misc/bigrams.txt", 2, 0.12), ("../../misc/trigrams.txt", 3, 1.0)]:
        counts = defaultdict(int)
        with open(path, "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) == 2 and len(parts[0]) == n and all(ch in alphabet for ch in parts[0]):
                    counts[parts[0]] += int(parts[1])

        total = sum(counts.values())
        floor = math.log(0.01 / total)
        table = [floor] * (25**n)

        for token, count in counts.items():
            table[ngidx(token)] = math.log(count / total) * weight

        tables.append(table)

    return tables[0], tables[1]

def build(pref):
    base = [-1] * 25
    used = set()

    for i, ch in enumerate(pref):
        v = alphabet.index(ch)
        base[i] = v
        used.add(v)

    freepos = [i for i in range(len(pref), 25)]
    freelet = [i for i in range(25) if i not in used]
    return base, freepos, freelet

def complete(base, freepos, freelet, rng):
    key = base[:]
    lets = freelet[:]
    rng.shuffle(lets)
    for p, l in zip(freepos, lets):
        key[p] = l
    return key

def formatkey(key):
    rows = []
    for r in range(5):
        row = key[r * 5 : (r + 1) * 5]
        rows.append(" ".join(alphabet[v] for v in row))

    return "\n".join(rows)

def dec(ctnum, key):
    inv = [0] * 25
    for pos, sym in enumerate(key):
        inv[sym] = pos

    out = [0] * len(ctnum)
    for i in range(0, len(ctnum), 2):
        l, r = inv[ctnum[i]], inv[ctnum[i + 1]]
        rl, cl = divmod(l, 5)
        rr, cr = divmod(r, 5)

        if rl == rr:
            out[i] = key[rl * 5 + (cl - 1) % 5]
            out[i + 1] = key[rr * 5 + (cr - 1) % 5]
        elif cl == cr:
            out[i] = key[((rl - 1) % 5) * 5 + cl]
            out[i + 1] = key[((rr - 1) % 5) * 5 + cr]
        else:
            out[i] = key[rl * 5 + cr]
            out[i + 1] = key[rr * 5 + cl]

    return out

def decrypt(ctnum, key): return "".join(alphabet[v] for v in dec(ctnum, key))
def score(ctnum, key, bigrams, trigrams):
    plain = dec(ctnum, key)
    sc = 0.0

    for i in range(len(plain) - 1):
        sc += bigrams[plain[i] * 25 + plain[i + 1]]
    for i in range(len(plain) - 2):
        sc += trigrams[(plain[i] * 25 + plain[i + 1]) * 25 + plain[i + 2]]

    return sc

def mutate(key, freepos):
    cand = key[:]
    roll = random.random()

    if roll < 0.80:
        a, b = random.sample(freepos, 2)
        cand[a], cand[b] = cand[b], cand[a]
        return cand

    if roll < 0.90:
        rows = [r for r in range(5) if all(r * 5 + c in freepos for c in range(5))]
        if len(rows) >= 2:
            ra, rb = random.sample(rows, 2)
            for c in range(5):
                ia, ib = ra * 5 + c, rb * 5 + c
                cand[ia], cand[ib] = cand[ib], cand[ia]
            return cand

    if roll < 0.98:
        cols = [c for c in range(5) if all(r * 5 + c in freepos for r in range(5))]
        if len(cols) >= 2:
            ca, cb = random.sample(cols, 2)
            for r in range(5):
                ia, ib = r * 5 + ca, r * 5 + cb
                cand[ia], cand[ib] = cand[ib], cand[ia]
            return cand

    for _ in range(3):
        a, b = random.sample(freepos, 2)
        cand[a], cand[b] = cand[b], cand[a]

    return cand

def refine(ctnum, bigrams, trigrams, key, curr, freepos):
    bkey, bscore = key[:], curr
    improved = True

    while improved:
        improved = False
        for i in range(len(freepos) - 1):
            for j in range(i + 1, len(freepos)):
                l, r = freepos[i], freepos[j]
                cand = bkey[:]
                cand[l], cand[r] = cand[r], cand[l]
                sc = score(ctnum, cand, bigrams, trigrams)
                if sc > bscore:
                    bkey, bscore, improved = cand, sc, True
                    break
            if improved:
                break

    return bkey, bscore

def search(ctnum, bigrams, trigrams, start, freepos, iterations, seed):
    random.seed(seed)
    ckey, bkey = start[:], start[:]
    cscore = bscore = score(ctnum, ckey, bigrams, trigrams)
    temp = 18.0

    for _ in range(iterations):
        cand = mutate(ckey, freepos)
        sc = score(ctnum, cand, bigrams, trigrams)
        if sc >= cscore or random.random() < math.exp((sc - cscore) / temp):
            ckey, cscore = cand, sc
            if sc > bscore:
                bkey, bscore = cand[:], sc
        temp = max(0.20, temp * 0.9995)

    return refine(ctnum, bigrams, trigrams, bkey, bscore, freepos)

keyword = "THERISA"
pref = prefix(keyword)

os.makedirs("../../result/2", exist_ok=True)
with open("../../chall/2.enc", "r") as f:
    ct0 = f.read().strip()

nums = [alphabet.index(ch) for ch in ct0]
bigrams, trigrams = load()

base, freepos, freelet = build(pref)
rng = random.Random(67)

gscore = float("-inf")
gkey = None

for _ in range(30):
    start = complete(base, freepos, freelet, rng)
    key, sc = search(nums, bigrams, trigrams, start, freepos, 900, rng.randrange(1 << 30))
    if sc > gscore:
        gscore, gkey = sc, key[:]

gplain = decrypt(nums, gkey)

with open("../../result/2/key.txt", "w") as f:
    f.write(formatkey(gkey) + "\n")

with open("../../result/2/2.dec", "w") as f:
    f.write(gplain)

print("done :3")
print(formatkey(gkey))