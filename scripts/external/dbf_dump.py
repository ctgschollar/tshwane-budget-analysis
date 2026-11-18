"""Minimal stdlib DBF (dBase III) reader: prints field names then rows matching a prefix filter."""
import struct
import sys


def read_dbf(path: str) -> tuple[list[str], list[list[str]]]:
    with open(path, "rb") as f:
        data = f.read()
    nrec, hlen, rlen = struct.unpack("<IHH", data[4:12])
    fields: list[tuple[str, int]] = []
    pos = 32
    while data[pos] != 0x0D:
        name = data[pos:pos + 11].split(b"\x00")[0].decode("latin-1")
        flen = data[pos + 16]
        fields.append((name, flen))
        pos += 32
    rows: list[list[str]] = []
    for i in range(nrec):
        off = hlen + i * rlen + 1
        vals = []
        for _, flen in fields:
            vals.append(data[off:off + flen].decode("utf-8", "replace").strip())
            off += flen
        rows.append(vals)
    return [n for n, _ in fields], rows


if __name__ == "__main__":
    names, rows = read_dbf(sys.argv[1])
    print("\t".join(names))
    print("total_records", len(rows), file=sys.stderr)
    pat = sys.argv[2] if len(sys.argv) > 2 else ""
    for r in rows:
        if pat in "\t".join(r):
            print("\t".join(r))
