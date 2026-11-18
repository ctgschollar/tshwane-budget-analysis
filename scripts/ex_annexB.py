"""Extract Annexure B (adjusted capital budget, project level, rands) from the 2022/23 and 2023/24 adjustments budgets."""
import re
import sys
import pdfplumber
import pandas as pd
from bands import page_lines, bucket, money
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

DOCS = {
    "2022/23": dict(
        file="26.-Proposed-2022-2023-Adjustment-Budget.pdf", pages=range(141, 149),
        bands=dict(dept=(40, 218), name=(218, 455), projno=(455, 495), wbs=(495, 560), fund=(560, 598),
                   orig=(598, 658), adjm=(658, 720), adjd=(720, 800)),
        stated=(2793105151, 2816190047)),
    "2023/24": dict(
        file="12.-Proposed-2023-2024-Adjustments-Budget.pdf", pages=range(132, 139),
        bands=dict(dept=(40, 205), name=(205, 370), wbs=(370, 444), fund=(444, 502),
                   orig=(502, 557), adjm=(557, 612), adjd=(612, 666), b1=(666, 724), b2=(724, 800)),
        stated=(2347686908, 2112614368)),
    # 2024/25 MTREF Annexure A: original budget only (adjusted band deliberately empty)
    "2024/25": dict(
        file="02.-2024-2025-MTREF-for-the-City-of-Tshwane.pdf", pages=range(58, 66),
        bands=dict(dept=(40, 147), name=(147, 388), projno=(388, 440), wbs=(440, 532), fund=(532, 600),
                   orig=(600, 652), adjm=(9998, 9999), adjd=(9998, 9999), b1=(652, 720), b2=(720, 800)),
        stated=(2347552576, 0)),
}
WBS_RE = re.compile(r"^9\.\d{6}")


def extract(year: str, d: dict | None = None) -> tuple[pd.DataFrame, list[dict]]:
    """d: document config (defaults to DOCS[year]). Optional keys: 'fy' (fiscal-year label written to the 'year' column),
    a 'region' band (City 'Regions' column; wrapped region text on the next line is appended), 'skip' (regex of lines to ignore)."""
    d = d or DOCS[year]
    fy = d.get("fy", year)
    pdf = pdfplumber.open(ROOT + "/" + d["file"])
    rows: list[dict] = []
    totals: list[dict] = []
    seen_rows = set()
    for pn in d["pages"]:
        for line in page_lines(pdf.pages[pn - 1]):
            c = bucket(line, d["bands"])
            txt = " ".join(w["text"] for w in line)
            if d.get("skip") and re.search(d["skip"], txt):
                continue
            if "ANNEXURE" in txt or c["dept"].startswith("Department") or txt.strip() in ("Number Code 2022/23 2022/23", "Mask) Code Code") or re.fullmatch(r"(ANNEXURE B )?\d+", txt.strip()) or re.match(r"^(Mask\)|Code|ng Code)", txt.strip()):
                continue
            has_num = any(c[k] for k in ("orig", "adjd"))
            if c["dept"].startswith("Total"):
                totals.append(dict(label=c["dept"], orig=money(c["orig"]), adjd=money(c["adjd"]), page=pn))
                continue
            if not WBS_RE.match(c["wbs"] or "") and not has_num:
                # continuation line of a wrapped description/department
                if rows:
                    if c.get("region"):
                        rows[-1]["region_raw"] = (rows[-1].get("region_raw", "") + " " + c["region"]).strip()
                    if c["name"]:
                        rows[-1]["project_name"] += " " + c["name"]
                    if c["dept"] and rows[-1]["is_head"]:
                        rows[-1]["department"] += " " + c["dept"]
                continue
            if not c["name"].strip() and not c["wbs"].strip() and not c["dept"].strip():
                continue  # bare number with no description/code: page artefact (e.g. rotated margin text)
            key = (c["wbs"], c["name"], c["orig"], c["adjd"])
            if key in seen_rows and pn == d["pages"][-1]:
                continue  # duplicated overlay page
            seen_rows.add(key)
            rows.append(dict(year=fy, doc=year, source_file=d["file"], page=pn, department=c["dept"], region_raw=c.get("region", ""),
                             project_name=c["name"], project_number=c.get("projno", ""), wbs=c["wbs"],
                             is_head=bool(c["dept"]),
                             original_budget=money(c["orig"]) or 0.0, adjusted_budget=money(c["adjd"]) or 0.0,
                             adjustment_raw=c["adjm"]))
    df = pd.DataFrame(rows)
    # inherit department for indented child rows
    df["department"] = df["department"].replace("", pd.NA).ffill()
    # Positional parent/child: rows after a head row (until the next head) are its sub-projects.
    # Use sub-project rows when they reconcile to the head on both columns; otherwise use the head row.
    df["use_row"] = False
    df["note"] = ""
    heads = df.index[df.is_head].tolist() + [len(df)]
    for a, b in zip(heads[:-1], heads[1:]):
        kids = df.loc[a + 1:b - 1]
        if len(kids) == 0:
            df.at[a, "use_row"] = True
            continue
        ok = all(abs(kids[c].sum() - df.at[a, c]) <= 2 for c in ("original_budget", "adjusted_budget"))
        if ok:
            df.loc[kids.index, "use_row"] = True
            df.loc[kids.index, "note"] = "sub-project of " + df.at[a, "wbs"]
        else:
            df.at[a, "use_row"] = True
            df.at[a, "note"] = "head row used: sub-project rows in source do not sum to head"
    return df, totals


if __name__ == "__main__":
    out = []
    for y in DOCS:
        df, totals = extract(y)
        leaf = df[df.use_row]
        stated = DOCS[y]["stated"]
        gt = [t for t in totals if t["label"].startswith("Total Capex")]
        print(f"{y}: rows {len(df)} used rows {len(leaf)} head-fallbacks {(df.note.str.startswith('head row')).sum()}")
        print(f"   leaf sums  orig {leaf.original_budget.sum():,.0f}  adj {leaf.adjusted_budget.sum():,.0f}")
        print(f"   stated     orig {stated[0]:,.0f}  adj {stated[1]:,.0f}   printed grand total row: {gt}")
        dept_totals = [t for t in totals if t["label"] == "Total"]
        print(f"   sum of dept 'Total' rows: orig {sum(t['orig'] or 0 for t in dept_totals):,.0f} adj {sum(t['adjd'] or 0 for t in dept_totals):,.0f}")
        out.append(df)
    pd.concat(out).to_csv(sys.argv[1], index=False)
