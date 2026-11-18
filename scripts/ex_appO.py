"""Extract Appendix O (capital programmes by ward: project -> ward list, no rand values) from the three annual reports."""
import re
import sys
import pdfplumber
import pandas as pd
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

D = ROOT + "/"
DOCS = {
    "2022/23": ("City-of-Tshwane-Audited-Annual-Report-for-2022_23-FY.pdf", range(385, 394)),
    "2023/24": ("13.-The-Consolidated-Annual-Report-for-the-City-of-Tshwane_2023_24.pdf", range(405, 412)),
    "2024/25": ("22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.pdf", range(516, 526)),
}
HEADER = re.compile(r"^(Department|Division|Capital Programmes|Yes/No|Complete|Project complete)", re.I)


def clean(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\n", " ")).strip()


def extract(year: str) -> pd.DataFrame:
    f, pages = DOCS[year]
    pdf = pdfplumber.open(D + f)
    rows = []
    for pn in pages:
        for t in pdf.pages[pn - 1].extract_tables():
            for r in t:
                cells = [clean(c) for c in r]
                nonempty = [c for c in cells if c]
                if not nonempty or HEADER.match(nonempty[0]) or len(nonempty) < 2:
                    continue
                dept, proj = cells[0], cells[1]
                rest = [c for c in cells[2:] if c]
                if not proj:
                    continue
                ward = rest[0] if rest else ""
                complete = rest[1] if len(rest) > 1 else ""
                m = re.match(r"\(\s*(\d{6})\s*\)\s*(.*)", proj)
                rows.append(dict(year=year, source_file=f, page=pn, department=dept,
                                 idp_number=m.group(1) if m else "", project_name=m.group(2) if m else proj,
                                 wards_raw=ward, complete=complete))
    df = pd.DataFrame(rows)
    df["department"] = df["department"].replace("", pd.NA).ffill()
    return df


def ward_list(raw: str) -> list[int]:
    return [int(x) for x in re.findall(r"\b(\d{1,3})\b", raw) if 1 <= int(x) <= 107]


def ward_category(raw: str) -> str:
    w = ward_list(raw)
    r = raw.lower()
    if "city wide" in r or "citywide" in r or "all regions" in r or "various" in r:
        return "city-wide"
    if "intersect" in r:
        return "no-intersect"
    if "admin" in r or "hq" in r:
        return "administrative-hq"
    if len(w) == 1:
        return "single-ward"
    if len(w) > 1:
        return "multi-ward"
    return "unspecified"


if __name__ == "__main__":
    out = []
    for y in DOCS:
        df = extract(y)
        df["ward_category"] = df.wards_raw.map(ward_category)
        df["wards"] = df.wards_raw.map(lambda s: ";".join(str(x) for x in ward_list(s)))
        print(y, len(df), df.ward_category.value_counts().to_dict())
        out.append(df)
    pd.concat(out).to_csv(sys.argv[1], index=False)
