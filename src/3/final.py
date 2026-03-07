#!/usr/bin/env python3
with open("../../result/3/iteration8.dec", "r") as f:
    final = f.read().strip()
    f.close()

final = final.upper()
print(final)

with open("../../result/3/3.dec", "w") as f:
    f.write(final)
    f.close()