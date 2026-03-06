#!/usr/bin/env python3
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def imod(a):
    a %= 26
    _, x, _ = egcd(a, 26)
    return x % 26

def num(s): return [ord(ch.upper()) - 65 for ch in s if ch.isalpha()]
def txt(ns): return "".join(chr((n % 26) + 65) for n in ns)

def multp(A, B):
    r, k = len(A), len(A[0])
    c = len(B[0])
    out = [[0] * c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            s = sum(A[i][t] * B[t][j] for t in range(k))
            out[i][j] = s % 26
    return out

def det(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return det % 26

def adjs(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    adj = [
        [(e * i - f * h), -(b * i - c * h),  (b * f - c * e)],
        [-(d * i - f * g), (a * i - c * g), -(a * f - c * d)],
        [(d * h - e * g), -(a * h - b * g),  (a * e - b * d)]
    ]
    return [[x % 26 for x in row] for row in adj]

def inv(M):
    d = det(M)
    dinv = imod(d)
    adj = adjs(M)
    return [[(dinv * adj[i][j]) % 26 for j in range(3)] for i in range(3)]

def mat(nums): return [[nums[c * 3 + r] for c in range(3)] for r in range(3)]

def decrypt(ct_nums, Kinv):
    out = []
    for i in range(0, len(ct_nums), 3):
        block = ct_nums[i:i+3]
        for r in range(3):
            s = sum(Kinv[r][t] * block[t] for t in range(3))
            out.append(s % 26)
    return out

def main():
    with open("../../chall/4.enc", "r") as f:
        ct = f.read().strip()

    known = "ROYALGUARD"[:9]
    ctn = num(ct)
    kpn = num(known)

    pmat = mat(kpn)
    cmat = mat(ctn[:9])
    
    pinv = inv(pmat)
    key = multp(cmat, pinv)
    kinv = inv(key)

    pt = decrypt(ctn, kinv)
    print(txt(pt))

if __name__ == "__main__":
    main()