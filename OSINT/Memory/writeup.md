# Memory - Writeup

**Category:** OSINT  
**Author:** zenapietal  
**File:** [picture11.jpg](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/CTF-FIND-IT%20Day%202/OSINT/Memory/picture11.jpg)

## Ringkasan
Challenge ini adalah geolocation dari satu foto, dengan target koordinat format DMS (`FindITCTF{DD_MM_SS_DIR_DD_MM_SS_DIR}`). Dari clue visual (area aquarium, signage restoran Jepang, dan layout jalan), lokasi dipastikan di area Tokyo Skytree/Solamachi.

## Recon
Clue visual yang paling berguna:
- signage `壱角家 スカイツリー店`
- signage `タワー丼` (業平橋かみむら)
- konteks cerita: pergi ke aquarium + makan soba

Kombinasi ini mengarah ke kawasan Sumida Aquarium / Tokyo Solamachi.

## Step-by-step
1. Enumerasi semua clue teks dari foto.
2. Cari candidate POI di sekitar Tokyo Skytree menggunakan map sources.
3. Cross-check lokasi dengan OSM/Google Maps/GSI agar sudut pandang sesuai.
4. Ambil titik paling cocok dengan posisi kamera.
5. Konversi koordinat ke DMS (detik dibulatkan integer sesuai format flag).

Contoh validasi koordinat via Overpass/GSI:

```python
import requests, urllib.parse

addresses = [
    '東京都墨田区業平1-18-4',
    '東京都墨田区業平1-18-13',
    '東京都墨田区業平1-17-5',
    '東京都墨田区業平1-18-12'
]

for a in addresses:
    u = 'https://msearch.gsi.go.jp/address-search/AddressSearch?q=' + urllib.parse.quote(a)
    data = requests.get(u, timeout=20).json()
    if data:
        c = data[0]['geometry']['coordinates']
        print(a, c[1], c[0])
```

## Koordinat Final
`35°42'35"N 139°48'31"E`

## Flag
`FindITCTF{35_42_35_N_139_48_31_E}`

## Inti Pelajaran
- Geolocation CTF efektif jika menggabungkan visual clue + multi-source validation.
- Akurasi format (DMS integer) sangat krusial karena beda 1 detik bisa gagal submit.
