"""Banded / threshold-free re-analysis (v2). Reuses the binary_v1 allocation logic unchanged
(part2_attribute.allocate for Option A; moya_analysis.option_b_region for Option B) and records rand per project x ward.

Outputs (work/): v2_alloc.parquet-like CSV of (column, basis, mode, option, project_key, project_name, ward, R)."""
import pandas as pd
import analyze as A
import part2_attribute as Q
import moya_analysis as X
from match import norm

C = pd.read_csv("census_clean/tshwane_ward_popgroup.csv")
PCT = dict(zip(C.ward_no, C.pct_black_african))
POP = dict(zip(C.ward_no, C.total_population))
TOTPOP = sum(POP.values())

BANDS = {  # name -> list of (lo, hi) half-open [lo, hi); 100 included in top band
    "headline": [("0–20", 0, 20), ("20–40", 20, 40), ("40–60", 40, 60), ("60–80", 60, 80), ("80–100", 80, 101)],
    "split_80_100": [("0–20", 0, 20), ("20–40", 20, 40), ("40–60", 40, 60), ("60–80", 60, 80), ("80–90", 80, 90), ("90–100", 90, 101)],
    "merged_40_80": [("0–20", 0, 20), ("20–40", 20, 40), ("40–80 (mixed)", 40, 80), ("80–100", 80, 101)],
}


def band_of(w: int, scheme: str = "headline") -> str:
    for lab, lo, hi in BANDS[scheme]:
        if lo <= PCT[w] < hi:
            return lab
    raise ValueError(w)


# ---- columns: (label, kind, adopted_by, document/date, rows, value column, source of Option-B region)
COLUMNS = [
    ("2022/23 original", "budget", "pre-Brink", "2022/23 MTREF approved 26 May 2022 (2022/23 adj. budget p51)",
     A.rows_for("2022/23", "budget"), "original_budget", "old"),
    ("2022/23 adjusted", "budget", "pre-Brink", "2022/23 adjustments budget, prepared before the 2–3 Mar 2023 NT engagement (p52)",
     A.rows_for("2022/23", "budget"), "adjusted_budget", "old"),
    ("2023/24 original", "budget", "Brink", "2023/24 MTREF approved 31 May 2023 (2023/24 adj. budget p48)",
     A.rows_for("2023/24", "budget"), "original_budget", "old"),
    ("2023/24 adjusted", "budget", "Brink", "2023/24 adjustments budget, based on results to 31 Dec 2023 (p48)",
     A.rows_for("2023/24", "budget"), "adjusted_budget", "old"),
    ("2024/25 original", "budget", "Brink", "2024/25 MTREF, 'tabled for approval by Council in May 2024' (p76)",
     A.rows_for("2024/25", "budget"), "original_budget", "old"),
    ("2024/25 adjusted (adj. budget)", "budget", "Moya", "2024/25 adjustments budget, based on results to 31 Dec 2024 (p47)",
     X.M[X.M.doc == "2024/25adj"], "adjusted_budget", "new"),
    ("2024/25 adjusted (App N, final)", "budget", "Moya", "AR 2024/25 Appendix N pp503–515 (final adjusted incl. later amendments)",
     A.rows_for("2024/25", "adjusted+actual"), "adjusted_budget", "old"),
    ("2025/26 original", "budget", "Moya", "2025/26 MTREF, Special Council 29 May 2025 (file title; p152 'approval in May 2025')",
     X.M[X.M.doc == "2025/26"], "original_budget", "new"),
    ("2025/26 adjusted", "budget", "Moya", "2025/26 adjustments budget, based on results to 31 Dec 2025 (p52)",
     X.M[X.M.doc == "2025/26adj"], "adjusted_budget", "new"),
    ("2026/27 original", "budget", "Moya", "2026/27 MTREF, version for Mayoral Committee 21 May 2026 (p65); total reconciles to SDBIP R2,856,300,538",
     X.M[X.M.doc == "2026/27"], "original_budget", "new"),
    ("2024/25 actual", "actual", "Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025", "AR 2024/25 Appendix N pp503–515 (audited annual report)",
     A.rows_for("2024/25", "adjusted+actual"), "actual_spend", "old"),
]
BUDGET_COLS = [c[0] for c in COLUMNS if c[1] == "budget" and "App N" not in c[0]]


def project_key(r: pd.Series) -> str:
    return X.canon_key(r) if "linked_prior_wbs" in r.index else X.canon_key(pd.concat([r, pd.Series({"linked_prior_wbs": "", "link_basis": ""})]))


def placement(a: dict, ev: str) -> str:
    """How allocate() placed this row: a single ward, a region split by population, or a stated township split over its wards."""
    if len(a) == 1:
        return "named ward"
    if str(ev).startswith("population split"):
        return "region split"
    return "township split"


def allocate_all() -> pd.DataFrame:
    out = []
    for lab, kind, adm, doc, d, col, src in COLUMNS:
        for _, r in d.iterrows():
            v = r[col]
            if pd.isna(v) or v == 0:
                continue
            key = project_key(r)
            for basis in ("service", "location"):
                for mode in "ab":
                    Q.INCLUDE_TITLES = False
                    a, ev = Q.allocate(r, basis, mode)
                    if isinstance(a, dict):
                        pl = placement(a, ev)
                        for w, x in a.items():
                            out.append((lab, "A", basis, mode, key, r.project_name, w, v * x, "", pl))
                    else:
                        out.append((lab, "A", basis, mode, key, r.project_name, -1, v, str(a), "not placed in wards"))
            regs = X.option_b_region(r, src)
            if regs:
                for w, x in Q.region_split(regs).items():
                    out.append((lab, "B", "region", "b", key, r.project_name, w, v * x, "", "region split"))
            else:
                out.append((lab, "B", "region", "b", key, r.project_name, -1, v, "unattributed: no specific region tag", "not placed in wards"))
    return pd.DataFrame(out, columns=["column", "option", "basis", "mode", "key", "project_name", "ward", "R", "unattributed", "placement"])


if __name__ == "__main__":
    import sys
    al = allocate_all()
    al.to_csv(sys.argv[1] if len(sys.argv) > 1 else "work/v2_alloc.csv", index=False)
    chk = al.groupby(["column", "option", "basis", "mode"]).R.sum().unstack(["option", "basis", "mode"]) / 1e6
    print(chk.round(1).to_string())
