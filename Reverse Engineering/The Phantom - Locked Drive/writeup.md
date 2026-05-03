# The Phantom - Locked Drive - Writeup

**Category:** Reverse Engineering  
**Author:** vvry  
**File:** [flash_drive](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/Reverse%20Engineering/The%20Phantom%20-%20Locked%20Drive/flash_drive)

## Ringkasan
Binary Linux x86-64 ini memakai anti-debug check, state machine, dan tiga validator input. Setelah ketiga input valid, binary melakukan dekripsi final berbasis hash FNV-1a dengan layout buffer overlap.

## Recon
Hal penting dari reversing:
- anti-debug: cek `TracerPid` dari `/proc/self/status`
- ada tiga prompt input terpisah
- validator masing-masing input berbeda (TEA-like, constraint linear, seeded transform)
- blok ciphertext final dirakit dengan overlap stack

## Bug/Logic yang Dieksploitasi
Tidak ada memory corruption klasik; solve murni dari logic recovery:
- inverse algoritma validator untuk recover input valid
- rekonstruksi layout memori final yang tidak linear

## Step-by-step
1. Enumerasi binary dan strings awal.

```bash
file flash_drive
strings -a flash_drive | sed -n '1,120p'
```

2. Analisis flow `main`/state machine di disassembler.

```bash
r2 -q -c 'aaa; s main; pdf' flash_drive
```

3. Reverse validator input pertama (TEA-like) -> `sham`.
4. Reverse validator input kedua (pair constraints) -> `forged`.
5. Reverse validator input ketiga (seeded transform) -> `counterfeits`.
6. Bangun hash FNV-1a dari tiga input.
7. Rekonstruksi ciphertext final dengan memperhatikan overlap stack write (`a0`, `b0`, `ba`).
8. Jalankan dekripsi final.

## Solver

```bash
python3 solve.py
```

## Flag
`FindITCTF{no_appetite_for_glittering_lies}`

## Inti Pelajaran
- Reversing CTF sering menang di dataflow reconstruction, bukan sekadar decompile.
- Detail layout memory bisa menentukan benar/salahnya plaintext akhir.
