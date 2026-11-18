"""Extract project -> region ('Ward Location') from MBRR SA36 / SB19 tables (R thousand)."""
import re
import sys
import pdfplumber
import pandas as pd
from bands import page_lines, bucket
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

D = ROOT + "/"
TABLES = {
    "SA36_2223": dict(file="02.-2022-2023-MTREF-for-the-City-of-Tshwane.pdf", pages=range(199, 235), year="2022/23",
                      bands=dict(func=(80, 172), desc=(172, 247), code=(247, 284), region=(522, 592),
                                 cy=(592, 624), by=(624, 652), by1=(652, 680), by2=(680, 712))),
    "SB_2223adj": dict(file="26.-Proposed-2022-2023-Adjustment-Budget.pdf", pages=range(100, 105), year="2022/23",
                       bands=dict(func=(40, 175), desc=(175, 300), code=(300, 344), region=(530, 606),
                                  by=(606, 640), by_adj=(640, 668))),
    "SA36_2324": dict(file="02.-2023-2024-MTREF-for-the-City-of-Tshwane.pdf", pages=range(181, 189), year="2023/24",
                      bands=dict(func=(80, 180), desc=(180, 296), code=(296, 334), region=(598, 642),
                                 by=(642, 668), by1=(668, 690), by2=(690, 720))),
    "SB19_2324adj": dict(file="12.-Proposed-2023-2024-Adjustments-Budget.pdf", pages=range(90, 94), year="2023/24",
                         bands=dict(func=(44, 125), code=(125, 192), region=(485, 553), by=(640, 700), by_adj=(700, 790))),
    "SA36_2425": dict(file="02.-2024-2025-MTREF-for-the-City-of-Tshwane.pdf", pages=range(205, 217), year="2024/25",
                      bands=dict(func=(70, 163), desc=(163, 258), code=(258, 300), region=(638, 664),
                                 cy=(664, 688), by=(688, 708), by1=(708, 730), by2=(730, 760))),
}
CODE_RE = re.compile(r"9\.\d{6}\.\d[\w.,]*")


def norm_region(raw: str) -> str:
    s = re.sub(r"\s+", "", raw)
    m = re.search(r"Region(\d)(A|B)?", s, re.I)
    if m:
        return f"Region {m.group(1)}{m.group(2) or ''}"
    if re.search(r"Wholeof", s, re.I):
        return "Whole of Metro"
    if re.search(r"CityWide", s, re.I):
        return "City Wide"
    if re.search(r"Administrative", s, re.I):
        return "Administrative HQ"
    return ""


def thousands(s: str) -> float | None:
    s = s.strip()
    if not s:
        return None
    dg = re.sub(r"[^\d]", "", s)
    return float(dg) * 1000 if dg else 0.0


def extract(key: str) -> pd.DataFrame:
    t = TABLES[key]
    pdf = pdfplumber.open(D + t["file"])
    rows: list[dict] = []
    for pn in t["pages"]:
        for line in page_lines(pdf.pages[pn - 1]):
            c = bucket(line, t["bands"])
            code_txt = re.sub(r"\s+", "", c["code"])
            m = CODE_RE.search(code_txt)
            if m:
                r = dict(table=key, year=t["year"], source_file=t["file"], page=pn, code=m.group(0).rstrip(".,"),
                         desc=c.get("desc", ""), func=c["func"], region_raw=c["region"])
                for k in ("cy", "by", "by_adj", "by1", "by2"):
                    if k in c:
                        r[k] = thousands(c[k])
                rows.append(r)
            elif rows and rows[-1]["page"] == pn:
                # continuation line (wrapped description / region text)
                if c.get("desc"):
                    rows[-1]["desc"] += " " + c["desc"]
                if c["region"]:
                    rows[-1]["region_raw"] += " " + c["region"]
    df = pd.DataFrame(rows)
    df["region"] = df.region_raw.map(norm_region)
    return df


if __name__ == "__main__":
    out = []
    for k in TABLES:
        df = extract(k)
        print(f"{k}: rows {len(df)}  region found {(df.region != '').sum()}  "
              f"budget-year sum R{df.by.fillna(0).sum()/1e6:,.1f}m  regions: {df.region.value_counts().to_dict()}")
        out.append(df)
    pd.concat(out).to_csv(sys.argv[1], index=False)
