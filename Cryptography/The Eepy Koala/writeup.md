# The Eepy Koala - Writeup

**Category:** Cryptography  
**Author:** Dkulkas  
**Files:** [enc.py](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/CTF-FIND-IT%20Day%202/Cryptography/The%20Eepy%20Koala/enc.py), [koala-enc.ppm](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/CTF-FIND-IT%20Day%202/Cryptography/The%20Eepy%20Koala/koala-enc.ppm)

## Ringkasan
Skema enkripsi menggunakan seed 16-bit untuk dua fungsi sekaligus: derivasi key AES-ECB dan permutasi blok ciphertext. Karena keyspace kecil, seed bisa di-bruteforce cepat dengan known-plaintext dari padding PKCS#7.

## Recon
Dari `enc.py` terlihat:
- seed hanya 16-bit (`0..65535`)
- AES mode ECB
- urutan blok diacak pakai seed yang sama
- ukuran data pas blok 16-byte (tidak ada partial block acak)

## Step-by-step
1. Brute-force seed 16-bit.
2. Validasi seed kandidat dengan mencocokkan blok padding (`0x10` x 16) setelah inverse permutation.
3. Gunakan seed valid untuk inverse permutation semua blok.
4. Dekripsi ulang menjadi file PPM original.
5. Render ke PNG untuk membaca flag visual.

```bash
cd "CTF-FIND-IT Day 2/Cryptography"
../../.venv/bin/python solve_koala.py
magick koala-restored.ppm koala-restored.png
```

## Flag
`FindITCTF{w0W_sUch_4n_4W3s0m3_k0aL4}`

## Inti Pelajaran
- Keyspace kecil + ECB + seed reuse membuat skema mudah dipulihkan.
