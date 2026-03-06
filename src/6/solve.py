#!/usr/bin/env python3
with open("../../chall/corrupt.jpg", 'rb') as f:
    encrypted = f.read()

signatures = {
    "jpg": [0xFF, 0xD8, 0xFF],
    "txt": [0xEF, 0xBB, 0xBF],
    "png": [0x89, 0x50, 0x4E, 0x47],
    "gif": [0x47, 0x49, 0x46, 0x38],
    "pdf": [0x25, 0x50, 0x44, 0x46],
    "zip": [0x50, 0x4B, 0x03, 0x04]
}

for ext, magic in signatures.items():
    key = encrypted[0] ^ magic[0]

    is_match = True
    for i in range(1, len(magic)):
        if encrypted[i] ^ key != magic[i]:
            is_match = False
            break
    
    if is_match:
        print(f"Original extension : {ext}")
        print(f"Keys : {hex(key)}")

        print("Recovering...")
        recov = bytearray([byte ^ key for byte in encrypted])

        output = f"original.{ext}"
        with open(output, 'wb') as f:
            f.write(recov)
            print(f"Done :3, check {output}")
        break