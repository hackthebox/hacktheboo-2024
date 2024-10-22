def julius_decrypt(enc, shift):
    pt = ''
    for c in enc:
        if c == '0':
            pt += ' '
        elif not ord('A') <= ord(c) <= ord('Z'):
            pt += c
        else:
            o = ord(c) - 65
            pt += chr(65 + (o - shift) % 26)
    return pt

enc = open('output.txt').read()

for i in range(1, 26):
    print(f'{i = } | {julius_decrypt(enc, i)}')
