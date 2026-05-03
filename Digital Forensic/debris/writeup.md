# debris - Writeup

**Category:** Digital Forensic  
**Author:** gorbaz  
**File:** [chall.img](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/CTF-FIND-IT%20Day%202/Digital%20Forensic/debris/chall.img)

## Ringkasan
Disk image berisi jejak artefak operasional: backup zip ber-password dan payload tersembunyi di file gambar. Solve path: carving image -> recover password -> ekstrak stego payload -> decode Base64.

## Recon
Temuan utama dari artefak:
- ada file zip hasil carving
- ada jejak command/petunjuk password di strings image
- file gambar hasil ekstrak zip mengandung hidden data steghide

## Weakness Utama
- Artefak sensitif tidak dibersihkan dari disk image.
- Password backup tersimpan secara recoverable.
- Media backup masih membawa payload tersembunyi.

## Step-by-step
1. Identifikasi tipe image dan lakukan carving.

```bash
binwalk chall.img
foremost -i chall.img -o /tmp/debris_carve
```

2. Cari clue password dari strings.

```bash
strings chall.img | rg "session_key|zip -P|backup.zip"
```

3. Ekstrak zip dengan password yang ditemukan.

```bash
unzip -P jp3gm4f14 /tmp/debris_carve/zip/00019460.zip -d /tmp/debris_out
```

4. Brute/ekstrak steghide payload dari JPEG.

```bash
stegseek /tmp/debris_out/keep.jpg /tmp/findit_words.txt
cat keep.jpg.out
```

5. Decode hasil Base64.

```bash
echo 'RmluZElUQ1RGe2g0djNfeTB1XzdyMTNkX2M0cnYxbmd9' | base64 -d
```

## Flag
`FindITCTF{h4v3_y0u_7r13d_c4rv1ng}`

## Inti Pelajaran
- Forensics disk image kuat di korelasi multi-artefak (metadata, strings, carved files, stego).
- Operational security failure kecil (history/key leak) bisa membuka seluruh chain.
