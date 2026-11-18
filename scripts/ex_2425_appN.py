"""Extract 2024/25 Annual Report Appendix N (Dominant Ward / Department / Project; adjusted budget, actual)."""
import re
import sys
import pdfplumber
import pandas as pd
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

PDF = ROOT + "/22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.pdf"
FIRST, LAST = 503, 515
AMT = re.compile(r"^(?P<name>.*?)\s*R\s*(?P<a>[\d ,]+\d|-)\s+R\s*(?P<b>[\d ,]+\d|-)\s*$")


def to_num(s: str) -> float:
    s = s.replace(" ", "").replace(",", "")
    return 0.0 if s == "-" else float(s)


def level(x0: float) -> str:
    if x0 < 42:
        return "ward"
    if x0 < 53:
        return "dept"
    return "project"


def extract() -> tuple[pd.DataFrame, list[dict]]:
    pdf = pdfplumber.open(PDF)
    rows: list[dict] = []
    subtotals: list[dict] = []
    started = False
    ward = dept = None
    pending: tuple[str, float] | None = None
    for pn in range(FIRST, LAST + 1):
        for ln in pdf.pages[pn - 1].extract_text_lines():
            t = ln["text"].strip()
            if not started:
                if t.startswith("Dominant Ward"):
                    started = True
                continue
            if re.fullmatch(r"\d+( \| Page)?", t) or t.startswith("Adjustment Budget") or t.startswith("Dominant Ward"):
                continue
            m = AMT.match(t)
            if not m:
                pending = (t if pending is None else pending[0] + " " + t, pending[1] if pending else ln["x0"])
                continue
            name = m["name"].strip()
            x0 = ln["x0"]
            if pending is not None:
                name = (pending[0] + " " + name).strip()
                x0 = pending[1]
                pending = None
            a, b = to_num(m["a"]), to_num(m["b"])
            if name.startswith("Grand Total"):
                subtotals.append(dict(kind="grand", name=name, adj=a, act=b, page=pn))
                continue
            lv = level(x0)
            if lv == "ward":
                ward = name
                dept = None
                subtotals.append(dict(kind="ward", name=name, adj=a, act=b, page=pn))
            elif lv == "dept":
                dept = name
                subtotals.append(dict(kind="dept", ward=ward, name=name, adj=a, act=b, page=pn))
            else:
                rows.append(dict(dominant_ward=ward, department=dept, project_name=name,
                                 adjusted_budget=a, actual_spend=b, page=pn))
    return pd.DataFrame(rows), subtotals


if __name__ == "__main__":
    df, sub = extract()
    # reconciliation checks: projects vs dept subtotals vs ward subtotals vs grand total
    errs = 0
    for s in sub:
        if s["kind"] == "dept":
            g = df[(df.dominant_ward == s["ward"]) & (df.department == s["name"])]
            for c, k in (("adjusted_budget", "adj"), ("actual_spend", "act")):
                if abs(g[c].sum() - s[k]) > 2:
                    errs += 1
                    print("DEPT MISMATCH", s, c, g[c].sum())
        elif s["kind"] == "ward":
            g = df[df.dominant_ward == s["name"]]
            for c, k in (("adjusted_budget", "adj"), ("actual_spend", "act")):
                if abs(g[c].sum() - s[k]) > 2:
                    errs += 1
                    print("WARD MISMATCH", s, c, g[c].sum())
        elif s["kind"] == "grand":
            print("GRAND", s, "| extracted:", df.adjusted_budget.sum(), df.actual_spend.sum())
    print("rows", len(df), "wards/groups", df.dominant_ward.nunique(), "mismatches", errs)
    df.to_csv(sys.argv[1], index=False)
