# Did You Find IT? - Writeup

**Category:** Miscellaneous  
**Author:** Find IT! 2026  
**Source:** `https://www.instagram.com/p/DUVBD06kipI/`

## Ringkasan
Challenge ini termasuk misc/OSINT ringan. Flag disisipkan di caption Instagram dalam bentuk Base64, jadi solve path utamanya adalah identifikasi encoding lalu decode.

## Recon
Caption post berisi string mencurigakan berikut:

```text
RmluZElUQ1RGe2phbmdhbl9sdXBhX2ZvbGxvd19pZ19maW5kaXR9
```

Karakter dan panjang string konsisten dengan pola Base64 (`A-Za-z0-9+/=`).

## Source Artifact
Caption asli:

```text
Find IT! 2026 introduces a series of competitive categories built to test your IT skills, logic, and innovation. Each challenge is designed to break limits and push you toward the future beyond time and space.

Brace yourself for what’s ahead.
More details coming soon. 🚀

RmluZElUQ1RGe2phbmdhbl9sdXBhX2ZvbGxvd19pZ19maW5kaXR9
```

## Step-by-step
1. Ambil string Base64 dari caption.
2. Decode dengan Python.
3. Validasi hasil decode sudah format `FindITCTF{...}`.

```bash
python3 - << 'PY'
import base64
s = 'RmluZElUQ1RGe2phbmdhbl9sdXBhX2ZvbGxvd19pZ19maW5kaXR9'
print(base64.b64decode(s).decode())
PY
```

## Flag
`FindITCTF{jangan_lupa_follow_ig_findit}`

## Inti Pelajaran
- Base64 bukan enkripsi, hanya encoding reversibel.
- Data sensitif di channel publik tetap bisa diekstrak walau di-encode.
