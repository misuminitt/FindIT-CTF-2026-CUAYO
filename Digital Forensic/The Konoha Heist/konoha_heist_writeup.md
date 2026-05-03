# The Konoha Heist - Writeup

**Category:** Miscellaneous  
**Author:** dnday  
**Files:** [metadata.bson](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/CTF-FIND-IT%20Day%202/Digital%20Forensic/The%20Konoha%20Heist/metadata.bson), [blockchain_export.json](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/CTF-FIND-IT%20Day%202/Digital%20Forensic/The%20Konoha%20Heist/blockchain_export.json), [server_log.txt](https://github.com/misuminitt/FindIT-CTF-2026-CUAYO/blob/main/CTF-FIND-IT%20Day%202/Digital%20Forensic/The%20Konoha%20Heist/server_log.txt)

## Ringkasan
Challenge ini menggabungkan blockchain trace, memory/log artifacts, dan metadata encoding bertingkat. Objective akhirnya menyusun empat komponen menjadi satu flag lengkap.

## Recon
Sumber data yang dianalisis:
- `blockchain_export.json` -> transaksi mencurigakan + calldata
- `server_log.txt` -> decimal fragments dari process anomali
- `metadata.bson` -> nilai base64/hex tersembunyi

## Step-by-step
1. Dari `blockchain_export.json`, identifikasi calldata mencurigakan.
2. Parse selector `0xa9059cbb` -> `transfer(address,uint256)`.
3. Ambil address tujuan transfer:
`0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad`
4. Decode fragment decimal di server log (decimal -> hex -> ASCII):
- `26852480951005303` -> `_f0ll0w`
- `1601464371` -> `_th3`
5. Decode metadata bertingkat:
- Base64 -> hex -> ASCII
- hasil: `_m0n3y_d40_h4ck3r`
6. Gabungkan sesuai format:
`FindITCTF{<address><message1><message2><message3>}`

## Flag
`FindITCTF{0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad_f0ll0w_th3_m0n3y_d40_h4ck3r}`

## Inti Pelajaran
- Banyak challenge forensics modern berbentuk correlation challenge antar format data berbeda.
