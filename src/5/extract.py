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

    outputs = {"R": ("lsb_r.bin", 0), "G": ("lsb_g.bin", 1), "B": ("lsb_b.bin", 2)}

    for name, (out, idx) in outputs.items():
        data = extract(arr, idx)
        with open(out, "wb") as f:
            f.write(data)
        print(f"{name}: wrote {len(data)} bytes to {out}")

if __name__ == "__main__":
    main()