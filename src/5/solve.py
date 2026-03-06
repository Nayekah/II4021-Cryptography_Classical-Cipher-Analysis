#!/usr/bin/env python3
from PIL import Image
import numpy as np

def byt(bits):
    out = bytearray()
    n = (len(bits) // 8) * 8
    for i in range(0, n, 8):
        b = 0
        for bit in bits[i:i+8]:
            b = (b << 1) | int(bit)
        out.append(b)
    return bytes(out)

def extract(arr, idx):
    ch = arr[:, :, idx].reshape(-1)
    bits = (ch & 1).astype(np.uint8)
    return byt(bits)

def main():
    path = "../../chall/1412.png"
    img = Image.open(path).convert("RGB")
    arr = np.array(img)

    stream = extract(arr, 1)

    pos = stream.find(B'1412')
    length = int.from_bytes(stream[pos+4:pos+8], "big")
    start = pos + 8
    end = start + length

    secret = stream[start:end]
    print(secret)

if __name__ == "__main__":
    main()