#!/usr/bin/env python3
import os

with open("../../chall/3.enc", "r") as f:
    ct0 = f.read().strip()

os.makedirs("../../result/3", exist_ok=True)

def write(it, buf):
    with open(f"../../result/3/iteration{it}.dec", "w+") as f:
        f.write(buf)

def subs(ct, maps):
    return "".join(maps.get(c, c) for c in ct)

# Iterasi 1
key = {"Z":"t", "J":"h", "S":"e", "G":"a", "R":"n", "M":"d"}
write(1, subs(ct0, key))

# Iterasi 2
key.update({"Z":"t", "J":"h", "S":"e", "U":"m", "O":"o", "X":"l", "G":"i", "M":"g"})
write(2, subs(ct0, key))

# Iterasi 3
key.update({"E":"a", "V":"d"})
write(3, subs(ct0, key))

# Iterasi 4
key.update({"W":"u", "F":"r"})
write(4, subs(ct0, key))

# Iterasi 5
key.update({"Q":"w", "C":"s", "Y":"c", "K":"y"})
write(5, subs(ct0, key))

# Iterasi 6
key.update({"T":"v", "B":"b", "P":"f"})
write(6, subs(ct0, key))

# Iterasi 7
key.update({"L":"p", "I":"q", "H":"z", "A":"k"})
write(7, subs(ct0, key))

# Iterasi 8
key.update({"D":"j", "N":"x"})
write(8, subs(ct0, key))