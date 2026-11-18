"""Minimal stdlib xlsx reader: dumps each sheet as rows (tab-separated) to stdout."""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def col_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_sheets(path: str) -> dict[str, list[list[str]]]:
    z = zipfile.ZipFile(path)
    shared: list[str] = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    relmap = {r.get("Id"): r.get("Target") for r in rels}
    out: dict[str, list[list[str]]] = {}
    for s in wb.find("m:sheets", NS):
        name = s.get("name")
        target = relmap[s.get("{%s}id" % NS["r"])].lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        root = ET.fromstring(z.read(target))
        rows: list[list[str]] = []
        for row in root.iter("{%s}row" % NS["m"]):
            vals: dict[int, str] = {}
            for c in row.findall("m:c", NS):
                v = c.find("m:v", NS)
                t = c.get("t")
                if t == "s" and v is not None:
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                else:
                    val = v.text if v is not None else ""
                vals[col_index(c.get("r"))] = val
            if vals:
                rows.append([vals.get(i, "") for i in range(max(vals) + 1)])
        out[name] = rows
    return out


if __name__ == "__main__":
    sheets = read_sheets(sys.argv[1])
    for name, rows in sheets.items():
        print(f"### SHEET {name} rows={len(rows)}")
        for r in rows:
            print("\t".join(r))
