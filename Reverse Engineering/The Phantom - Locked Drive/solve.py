from pathlib import Path


BINARY = Path(__file__).resolve().parents[1] / "flash_drive"


def fnv1a_parts(parts: list[bytes]) -> int:
    h = 0x811C9DC5
    for part in parts:
        for b in part:
            h ^= b
            h = (h * 0x1000193) & 0xFFFFFFFF
    return h


def solve_input1() -> bytes:
    v0 = 0x528F4DD2
    v1 = 0xEC0DA7E9
    total = 0xC6EF3720
    k0 = 0x50336854
    k1 = 0x746E3468
    k2 = 0x72446D30
    k3 = 0x21337631

    for _ in range(32):
        v1 = (v1 - ((((v0 << 4) & 0xFFFFFFFF) + k2) ^ ((v0 >> 5) + k3) ^ ((v0 + total) & 0xFFFFFFFF))) & 0xFFFFFFFF
        v0 = (v0 - ((((v1 << 4) & 0xFFFFFFFF) + k0) ^ ((v1 >> 5) + k1) ^ ((v1 + total) & 0xFFFFFFFF))) & 0xFFFFFFFF
        total = (total + 0x61C88647) & 0xFFFFFFFF

    return v0.to_bytes(4, "little")


def rol4(x: int) -> int:
    return ((x << 4) & 0xFF) | (x >> 4)


def solve_input2() -> bytes:
    targets = [0xB4, 0x5D, 0xF6, 0x5B, 0x52, 0x68]
    out = bytearray()
    for i in range(0, 6, 2):
        for a in range(32, 127):
            for b in range(32, 127):
                if rol4((5 * a + 3 * b) & 0xFF) == targets[i] and rol4((2 * a + 7 * b) & 0xFF) == targets[i + 1]:
                    out.extend([a, b])
                    break
            else:
                continue
            break
    return bytes(out)


def solve_input3(input1: bytes, input2: bytes) -> bytes:
    seed = sum(input1[:4]) * sum(input2[:6])
    encoded = bytes.fromhex("cedc0c6afab8372724359331")
    out = bytearray()
    cur = seed & 0xFFFFFFFF

    for b in encoded:
        plain = (((b >> 4) | ((b << 4) & 0xFF)) & 0xFF) ^ (cur & 0xFF)
        out.append(plain)
        cur = (cur + 0x13) & 0xFFFFFFFF

    return bytes(out)


def extract_zero_width_clue(data: bytes) -> str:
    off = 0x3080
    length = 0xE7
    key = 0x4B
    decoded = bytearray()
    for b in data[off:off + length]:
        decoded.append(b ^ key)
        key = (key + 0x0D) & 0xFF

    story = decoded.decode("utf-8")
    mapping = {"\u200c": "0", "\u200b": "1"}
    bits = "".join(mapping[ch] for ch in story if ch in mapping)
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)).decode()


def decrypt_flag(data: bytes, hash_value: int) -> str:
    # Rebuild the exact overlapped stack layout used by the binary.
    buf = bytearray(b"\x00" * 0x2A)
    buf[0:16] = data[0x3320:0x3330]
    buf[16:32] = data[0x3330:0x3340]
    buf[26:42] = data[0x3340:0x3350]

    out = bytearray()
    state = hash_value
    for b in buf:
        out.append(b ^ (state & 0xFF))
        state = ((state >> 8) | ((state & 0xFF) << 24)) & 0xFFFFFFFF
        state = (state - 0x61C88647) & 0xFFFFFFFF
    return out.decode()


def main() -> None:
    data = BINARY.read_bytes()
    input1 = solve_input1()
    input2 = solve_input2()
    input3 = solve_input3(input1, input2)
    clue = extract_zero_width_clue(data)
    h = fnv1a_parts([input1, input2, input3])
    flag = decrypt_flag(data, h)

    print(f"Input 1: {input1.decode()}")
    print(f"Input 2: {input2.decode()}")
    print(f"Input 3: {input3.decode()}")
    print(f"Clue   : {clue}")
    print(f"Flag   : {flag}")


if __name__ == "__main__":
    main()
