"""Assemble output/projects.csv from extracted tables + match decisions."""
import re
import pandas as pd
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

W = "work/"
OUT = ROOT + "/output/"

a = pd.read_csv(W + "annexB_clean.csv")
o = pd.read_csv(W + "appO_used.csv", index_col=0)
dec_b = pd.read_csv(W + "match_decisions_budget.csv")
dec_n = pd.read_csv(W + "match_decisions_appN.csv")
n = pd.read_csv(W + "appN_2425.csv")
reg = pd.read_csv(W + "regions.csv").fillna({"region": ""})

REGION_SRC = {"2022/23": ["SB_2223adj", "SA36_2223"], "2023/24": ["SB19_2324adj", "SA36_2425", "SA36_2324"],
              "2024/25": ["SA36_2425"]}
SCOPE_RE = re.compile(r"city ?wide|all regions|various|regions? \d[^)]*?(,| and |&)\s*\d|area[- ]?[a-e]\b", re.I)
BULK_RE = re.compile(r"substation|infeed|sub station|wwtw|power line|network control|reservoir|bulk|canal|feeder|"
                     r"outfall|water treatment|purification", re.I)


def ward_fields(ao_row: float | None) -> dict:
    if ao_row is None or pd.isna(ao_row):
        return dict(wards_raw="", wards="", ward_category="unmatched", ward_source="")
    r = o.loc[int(ao_row)]
    return dict(wards_raw=r.wards_raw, wards=r.wards if isinstance(r.wards, str) else "",
                ward_category=r.ward_category,
                ward_source=f"{r.source_file} p{r.page} (Appendix O: '{r.project_name}')")


def region_for(year: str, wbs: str) -> tuple[str, str]:
    if not isinstance(wbs, str):
        return "", ""
    for t in REGION_SRC[year]:
        h = reg[(reg.table == t) & (reg.code == wbs) & (reg.region != "")]
        if len(h):
            return h.region.iloc[0], f"{h.source_file.iloc[0]} p{h.page.iloc[0]} ({t})"
    return "", ""


rows = []
# --- budget rows: 2022/23 & 2023/24 Annexure B (orig+adj), 2024/25 Annexure A (orig only)
dec_b = dec_b.set_index("left_index")
for i, r in a[a.use_row].iterrows():
    d = dec_b.loc[i]
    assert d.budget_name == r.project_name, (i, d.budget_name, r.project_name)
    acc = d.status.startswith("accept")
    wf = ward_fields(d.appO_row if acc else None)
    rg, rgs = region_for(r.year, r.wbs)
    rows.append(dict(
        year=r.year, record_type="budget (Annexure B, adjustments budget)" if r.year != "2024/25" else "budget (Annexure A, MTREF)",
        source_file=r.source_file, page=r.page, project_name=r.project_name, department=r.department,
        wbs=r.wbs if isinstance(r.wbs, str) else "", **wf, dominant_ward_appN="",
        region=rg, region_source=rgs,
        original_budget=r.original_budget, adjusted_budget=r.adjusted_budget if r.year != "2024/25" else None,
        actual_spend=None, match_status=d.status, match_score=d.score, match_reason=d.reason if isinstance(d.reason, str) else "",
        name_note=r.name_note if isinstance(r.name_note, str) else "",
        note=r.note if isinstance(r.note, str) else ""))
# --- 2024/25 Appendix N rows (adjusted + actual)
dec_n = dec_n.set_index("appN_index")
for i, r in n.iterrows():
    d = dec_n.loc[i]
    acc = d.status.startswith("accept")
    wf = ward_fields(d.appO_row if acc else None)
    rows.append(dict(
        year="2024/25", record_type="adjusted+actual (Annual Report Appendix N)",
        source_file="22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.pdf", page=r.page,
        project_name=r.project_name, department=r.department, wbs="", **wf, dominant_ward_appN=r.dominant_ward,
        region="", region_source="", original_budget=None, adjusted_budget=r.adjusted_budget, actual_spend=r.actual_spend,
        match_status=d.status, match_score=d.score, match_reason=d.reason if isinstance(d.reason, str) else "",
        name_note="", note=""))
p = pd.DataFrame(rows)
p["scope_flag_multi_region_name"] = p.project_name.fillna("").str.contains(SCOPE_RE) & (p.ward_category == "single-ward")
p["bulk_infrastructure_name_flag"] = p.project_name.fillna("").str.contains(BULK_RE)
p.to_csv(OUT + "projects.csv", index=False)
print(p.groupby(["year", "record_type"]).agg(rows=("project_name", "size"), orig=("original_budget", "sum"),
                                             adj=("adjusted_budget", "sum"), act=("actual_spend", "sum")).to_string())
print(p.groupby(["year", "record_type", "ward_category"]).size().unstack(fill_value=0).to_string())
