# I Forgor - Writeup

**Category:** Cryptography  
**Author:** imios  
**File:** [Release.txt](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/CTF-FIND-IT%20Day%202/Cryptography/I%20Forgor/Release.txt)

## Ringkasan
Challenge RSA ini menggunakan modulus yang sama (`n`) untuk dua ciphertext berbeda eksponen (`e1=3`, `e2=65537`). Karena `gcd(e1,e2)=1`, plaintext dapat dipulihkan dengan Common Modulus Attack tanpa faktorisasi `n`.

## Recon
Temuan kunci dari file challenge:
- ada satu modulus `n`
- ada dua pasangan `(e1,c1)` dan `(e2,c2)`
- plaintext yang sama terenkripsi dengan dua eksponen

## Step-by-step
1. Hitung koefisien Bézout `a,b` sehingga `a*e1 + b*e2 = 1`.
2. Jika `a`/`b` negatif, gunakan modular inverse ciphertext terkait.
3. Hitung `m = c1^a * c2^b (mod n)`.
4. Decode hasil ke string Base64 lalu decode lagi ke flag plaintext.

```bash
python3 - << 'PY'
import base64

n = 65621244306653319670872009812479216556253539637757012684247326929337446029691949229830476009336324085576381980962409932835777704841875948755620309035826526718252935851707644029182010811923912024332263063320474435206957030905287233900554131266746644303012869033868346154962019095877474062849704039936163171519
e1, c1 = 3, 4105931817714585546497262196126228765774747581873311887305453434266838391287108553391387157504909553136096865866521360681945219809348271859677395206127927734410477669438652581050897860699569762295858375013954260208805208594575707901219384284893069846994938217
e2, c2 = 65537, 5243776788607977912607186503410037199569145142332695425831937859544540040996262696184528670956624577919073391021809450507327272297435046801815065538981326146894350676101027549009511804525444015269785480390765263800156021463103944845372299272838235762577979029844373619729965521134404669451262632798052638846

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

g, a, b = egcd(e1, e2)
if a < 0:
    c1 = pow(c1, -1, n)
    a = -a
if b < 0:
    c2 = pow(c2, -1, n)
    b = -b

m = (pow(c1, a, n) * pow(c2, b, n)) % n
encoded = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
print(base64.b64decode(encoded).decode())
PY
```

## Flag
`FindITCTF{PA5SW0RDNY4_1234}`

## Inti Pelajaran
- Reuse modulus pada RSA adalah kesalahan fatal saat plaintext sama dipakai di banyak eksponen.
