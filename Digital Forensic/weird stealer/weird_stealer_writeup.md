# Weird Stealer - Writeup

**Category:** Digital Forensic  
**Author:** buwung ap tu man  
**File:** `stealer.zip` (tidak tersedia di folder lokal). Lihat folder: [weird stealer](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/tree/main/CTF-FIND-IT%20Day%202/Digital%20Forensic/weird%20stealer)

## Ringkasan
Challenge memory forensics ini meminta kita mengekstrak artefak stealer dari dump memory, lalu mendekripsi data exfiltrasi. Payload ditemukan pada request `/checksum` dengan format `nonce(12 byte) + ciphertext`, dan key AES-256 berhasil dipulihkan dari memory.

## Recon
Langkah awal:
- ekstrak `stealer.zip`
- `strings stealer.DMP` untuk cari endpoint/protocol artefak
- ditemukan request `POST /checksum`

## Step-by-step
1. Dump string penting dari memory.

```bash
strings stealer.DMP > strings.txt
grep -i "POST\|GET\|checksum\|http" strings.txt
```

2. Ambil body request `/checksum` (72 byte), pecah jadi:
- 12 byte pertama: nonce
- sisa byte: ciphertext

3. Ambil key AES dari artefak memory:
`848e69c1783a4ca1b27d85cbefa785cb0a5e3fc49d3576766985e99189ef7645`

4. Dekripsi payload dengan AES-CTR (counter start `nonce || 00000002`).

```python
from Crypto.Cipher import AES
from Crypto.Util import Counter

key = bytes.fromhex("848e69c1783a4ca1b27d85cbefa785cb0a5e3fc49d3576766985e99189ef7645")
body = bytes.fromhex("<hex_body_checksum>")

nonce = body[:12]
ciphertext = body[12:]
initial_value = int.from_bytes(nonce + b"\x00\x00\x00\x02", "big")
ctr = Counter.new(128, initial_value=initial_value)

pt = AES.new(key, AES.MODE_CTR, counter=ctr).decrypt(ciphertext)
print(pt.decode())
```

## Flag
`FindITCTF{#kita usahakan wfh gaji usd itu!!}`

## Inti Pelajaran
- Memory dump sering menyimpan key material dan artefak C2/exfil secara plaintext atau near-plaintext.
