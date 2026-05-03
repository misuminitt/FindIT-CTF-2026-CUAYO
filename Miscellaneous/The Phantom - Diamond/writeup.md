# The Phantom - Diamond - Writeup

**Category:** Miscellaneous  
**Author:** vvry  
**Target:** `https://gemini.google.com/gem/1Zz_3mdXqsSaSFIbIszi9k3JFZ2TmCoyK?usp=sharing`

## Ringkasan
Challenge ini adalah puzzle interogasi AI dengan objective mendapatkan 3-word address untuk format flag. Kunci solve: bypass gate `Signature`, lanjut pivot clue lokasi, lalu konversi ke What3Words.

## Recon
Saat probing awal, AI menolak semua prompt dan mengembalikan hint:
- akses butuh `Signature`
- petunjuk: `My true signature lies hidden in the unseen spaces.`
- code `C0B1C0B1` hanya decoy/hint konteks

Ini mengarah ke karakter invisibel/zero-width pada elemen UI percakapan.

## Bug/Weakness Utama
Mekanisme autentikasi `Signature` bergantung pada artefak teks tak terlihat yang masih bisa dicopy dari UI, sehingga gate dapat dibypass tanpa kredensial rahasia klasik.

## Step-by-step
1. Ekstrak karakter tak terlihat (zero-width/invisible spaces) dari elemen yang terkait signature.
2. Kirim signature tersebut ke chat sampai AI membuka alur clue utama.
3. Ikuti clue berantai:
- `Musashi`
- `roku-hyaku san-juu yon` -> `634`
- lokasi menara tinggi di Tokyo
4. Pivot ke `Tokyo Skytree`.
5. Lanjut clue restoran pada tower -> `Sky Restaurant 634 (Musashi)`.
6. Ambil What3Words titik tersebut -> `watches.caked.land`.

## Flag
`FindITCTF{watches.caked.land}`

## Inti Pelajaran
- Challenge AI puzzle sering punya attack surface di layer presentasi/UI, bukan hanya prompt content.
- Clue linguistik + geospatial pivot efektif untuk narrowing lokasi akhir.
