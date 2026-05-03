from hashlib import sha256
from pathlib import Path

from Crypto.Cipher import AES


BLOCK = 16
IN_PATH = Path("koala-enc.ppm")
OUT_PPM = Path("koala-restored.ppm")
OUT_PNG = Path("koala-restored.png")


def permute(n: int, seed: int) -> list[int]:
    indices = list(range(n))
    state = seed
    for i in range(n - 1, 0, -1):
        state = (state * 0x41C64E6D + 12345) & 0xFFFFFFFF
        j = (state ^ (state >> 16)) % (i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    return indices


def parse_ppm(raw: bytes) -> tuple[bytes, bytes]:
    parts = raw.split(b"\n", 3)
    header = b"\n".join(parts[:3]) + b"\n"
    return header, parts[3]


def find_seed(blocks: list[bytes]) -> int:
    block_set = set(blocks)
    pad_block = bytes([16]) * 16
    candidates = []

    for seed in range(65536):
        key = sha256(seed.to_bytes(2, "big")).digest()[:16]
        cpad = AES.new(key, AES.MODE_ECB).encrypt(pad_block)
        if cpad in block_set:
            candidates.append(seed)

    if len(candidates) != 1:
        raise RuntimeError(f"unexpected candidate seeds: {candidates[:10]}")
    return candidates[0]


def main() -> None:
    raw = IN_PATH.read_bytes()
    header, ct = parse_ppm(raw)
    blocks = [ct[i : i + BLOCK] for i in range(0, len(ct), BLOCK)]
    n = len(blocks)

    seed = find_seed(blocks)
    key = sha256(seed.to_bytes(2, "big")).digest()[:16]
    mapping = permute(n, seed)

    # Encryption used: shuffled[pos] = enc_blocks[i]
    # Inverse mapping: enc_blocks[i] = shuffled[mapping[i]]
    enc_blocks = [blocks[pos] for pos in mapping]

    cipher = AES.new(key, AES.MODE_ECB)
    pt = b"".join(cipher.decrypt(b) for b in enc_blocks)

    pad = pt[-1]
    if pt[-pad:] != bytes([pad]) * pad:
        raise RuntimeError("invalid PKCS#7 padding")

    plain = pt[:-pad]
    OUT_PPM.write_bytes(header + plain)

    print(f"[+] seed: {seed}")
    print(f"[+] wrote: {OUT_PPM}")
    print("[*] Convert manually to PNG with:")
    print("    magick koala-restored.ppm koala-restored.png")


if __name__ == "__main__":
    main()
