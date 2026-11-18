"""Moya-era extension: headline shares (Option A, both bases, (a)/(b)), Option B region-level series, carry-forward
checks, composition, step decompositions, and tracing of the four 2024/25 cuts."""
import re
import pandas as pd
import analyze as A
import part2_attribute as Q
from moya_build import link_key, sa36_2425
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

T = 80
M = pd.read_csv("work/moya_rows.csv")
for c in ("wards", "wards_raw", "ward_source", "region", "region_source", "region_city_column", "linked_prior_wbs", "name_note"):
    M[c] = M[c].fillna("")
WR = pd.read_csv("work/ward_region_table.csv")
EGIS = dict(zip(WR.ward, WR.step3_official_egis))
BLACK = {w for w, v in A.pct22.items() if v >= T}
POP = A.pop22
BPOP = sum(POP[w] for w in BLACK)
OPOP = sum(v for w, v in POP.items() if w not in BLACK)

# administration that adopted each budget (from the documents; mayoral tenure dates as given in the brief)
NEW_MEASURES = [  # label, doc, value column, adopted by / document date
    ("2024/25 adjusted (adj. budget)", "2024/25adj", "adjusted_budget",
     "Moya-era Council (adjustments budget after Oct 2024; adoption date not stated in the document)"),
    ("2025/26 original", "2025/26", "original_budget", "Moya-era Council (MTREF, Special Council 29 May 2025 per file title)"),
    ("2025/26 adjusted", "2025/26adj", "adjusted_budget", "Moya-era Council (2025/26 adjustments budget; adoption date not stated)"),
    ("2026/27 original (Mayco draft, reconciles to adopted SDBIP)", "2026/27", "original_budget",
     "Moya-era; document is the version for the Mayoral Committee of 21 May 2026 (p65)"),
]
OLD_ADOPTION = {
    "2022/23 original budget": "pre-Brink (MTREF approved 26 May 2022)",
    "2022/23 adjusted budget": "pre-Brink (adjustments budget prepared before 2–3 Mar 2023)",
    "2023/24 original budget": "Brink (MTREF approved 31 May 2023)",
    "2023/24 adjusted budget": "Brink (adjustments budget, early 2024)",
    "2024/25 original budget": "Brink (MTREF tabled May 2024)",
    "2024/25 adjusted budget": "App N adjusted (final, incl. later amendments) — Moya-era",
    "2024/25 actual spend": "spent Jul 2024–Jun 2025 (≈3 months Brink, 9 months Moya)",
}


def run_df(d: pd.DataFrame, col: str, basis: str, mode: str, excl_conflict: bool = False) -> dict:
    B = O = Mw = 0.0
    un: dict[str, float] = {}
    for _, r in d.iterrows():
        v = r[col]
        if pd.isna(v) or v == 0:
            continue
        if excl_conflict and r.get("carry_conflict", False):
            r = r.copy()
            g = r.region_city_column
            r["ward_category"] = {"Tshwane Wide": "city-wide", "Administrative": "administrative-hq"}.get(g, "unmatched")
            r["wards"], r["region"], r["ward_source"] = "", (g if g.startswith("Region") else ""), f"'{r.project_name}'"
        a, _ = Q.allocate(r, basis, mode)
        if isinstance(a, dict):
            for w, x in a.items():
                if w in BLACK:
                    B += v * x
                else:
                    O += v * x
        elif a == "multi-ward":
            Mw += v
        else:
            un[a] = un.get(a, 0) + v
    tot = d[col].sum()
    return dict(total_Rm=tot / 1e6, black_Rm=B / 1e6, other_Rm=O / 1e6, multiward_Rm=Mw / 1e6,
                attributed_pct=(B + O) / tot * 100, black_share=B / (B + O) * 100 if B + O else float("nan"),
                percap_ratio=(B / BPOP) / (O / OPOP) if O else float("nan"), unattributed_pct=sum(un.values()) / tot * 100)


def carry_checks() -> pd.DataFrame:
    """Check 1: Regions column vs e-GIS region of the carried-forward ward (2025/26+ single-ward carried rows)."""
    c = M[(M.attribution == "carried-forward ward") & (M.ward_category == "single-ward") & (M.doc != "2024/25adj")].copy()
    c["carried_ward"] = c.wards.str.split(";").str[0].astype(int)
    c["egis_region"] = c.carried_ward.map(EGIS)
    c["value"] = c[["original_budget", "adjusted_budget"]].max(axis=1)

    def verdict(r: pd.Series) -> str:
        g = r.region_city_column
        if not g:
            return "no Regions value"
        if g in ("Tshwane Wide", "Administrative", "Multiple regions"):
            return f"column says {g}"
        return "agree" if r.egis_region in g.split(";") else "conflict"
    c["check"] = c.apply(verdict, axis=1)
    return c


M = M.merge(carry_checks()[["check"]], left_index=True, right_index=True, how="left")
M["carry_conflict"] = M.check.isin(["conflict", "column says Tshwane Wide", "column says Administrative", "column says Multiple regions"])


def headline() -> pd.DataFrame:
    rows = []
    for basis in ("location", "service"):
        for mode in "ab":
            Q.INCLUDE_TITLES = False
            old = Q.run(basis, mode).set_index("measure")
            for lab in old.index:
                rows.append(dict(measure=lab, adopted=OLD_ADOPTION[lab], basis=basis, mode=mode, **old.loc[lab][
                    ["total_Rm", "black_Rm", "other_Rm", "attributed_pct", "black_share", "percap_ratio", "unattributed_pct"]].to_dict()))
            for lab, doc, col, adopted in NEW_MEASURES:
                r = run_df(M[M.doc == doc], col, basis, mode)
                rows.append(dict(measure=lab, adopted=adopted, basis=basis, mode=mode,
                                 **{k: r[k] for k in ("total_Rm", "black_Rm", "other_Rm", "attributed_pct", "black_share", "percap_ratio", "unattributed_pct")}))
    return pd.DataFrame(rows)


def conflict_sensitivity() -> pd.DataFrame:
    rows = []
    for lab, doc, col, _ in NEW_MEASURES[1:]:
        for excl in (False, True):
            r = run_df(M[M.doc == doc], col, "location", "b", excl_conflict=excl)
            rows.append(dict(measure=lab, carried_conflicts=("Regions column used where it disagrees (incl. Tshwane Wide)" if excl else "carried ward kept (primary)"),
                             black_share=r["black_share"], percap_ratio=r["percap_ratio"], attributed_pct=r["attributed_pct"]))
    return pd.DataFrame(rows)


def composition() -> pd.DataFrame:
    """Check 2: how each Moya-era budget is attributed under Option A."""
    rows = []
    for lab, doc, col, _ in NEW_MEASURES:
        d = M[M.doc == doc]
        tot = d[col].sum()

        def cls(r: pd.Series) -> str:
            if r.attribution in ("carried-forward ward", "same-year Appendix O"):
                pre = "carried-forward" if r.attribution.startswith("carried") else "same-year App O"
                if r.ward_category == "single-ward":
                    return f"(i) {pre}: single ward"
                if r.ward_category == "multi-ward":
                    return f"(i) {pre}: multi-ward"
                return f"(i') {pre}: App O city-wide / HQ / no-intersect"
            if r.attribution.startswith("region-only"):
                return "(ii) region-only (" + ("SA36 tag" if "SA36" in r.attribution else "Regions column") + ")"
            if r.attribution in ("Tshwane Wide", "Administrative"):
                return "(iii) Tshwane Wide / Administrative"
            if r.attribution.startswith("Multiple"):
                return "(iv) 'Multiple regions' (unspecified)"
            return "(v) no ward or region"
        s = d.assign(c=d.apply(cls, axis=1)).groupby("c")[col].sum()
        for k, v in s.items():
            rows.append(dict(measure=lab, category=k, Rm=v / 1e6, pct=v / tot * 100))
    return pd.DataFrame(rows)


# ---------------- Option B: region-level series for every year ----------------
def option_b_region(r: pd.Series, source: str) -> list[str]:
    if source == "new":
        g = r.region_city_column if r.doc != "2024/25adj" else ""
        if r.doc == "2024/25adj":
            g = sa36_2425().get(r.wbs, ("", ""))[0] or (r.region if str(r.region).startswith("Region") else "")
        if not str(g).startswith("Region"):
            return []
        return [re.sub(r"[AB]$", "", x.strip()) for x in str(g).split(";")]
    reg = r.region if isinstance(r.region, str) else ""
    if r.record_type.startswith("adjusted+actual"):
        reg = Q.REGION_BY_NAME_2425.get(Q.norm(r.project_name), "")
    if not reg.startswith("Region"):
        return []
    return [re.sub(r"[AB]$", "", reg)]


def option_b() -> pd.DataFrame:
    rows = []
    series = [(lab, A.rows_for(y, rt), col, "old") for lab, y, rt, col in A.MEASURES] + \
             [(lab, M[M.doc == doc], col, "new") for lab, doc, col, _ in NEW_MEASURES]
    for lab, d, col, src in series:
        B = O = 0.0
        for _, r in d.iterrows():
            v = r[col]
            if pd.isna(v) or v == 0:
                continue
            regs = option_b_region(r, src)
            if not regs:
                continue
            for w, x in Q.region_split(regs).items():
                if w in BLACK:
                    B += v * x
                else:
                    O += v * x
        tot = d[col].sum()
        rows.append(dict(measure=lab, attributed_pct=(B + O) / tot * 100, black_share=B / (B + O) * 100,
                         percap_ratio=(B / BPOP) / (O / OPOP)))
    return pd.DataFrame(rows)


# ---------------- Step decompositions (excl. bulk, location basis, (a)) ----------------
def canon_key(r: pd.Series) -> str:
    if "Ekangala Block A" in str(r.project_name):
        return "EKANGALA_BLOCK_A-F"   # carried under three different WBS codes 2023/24-2026/27 (see moya_build.MANUAL_LINKS)
    w = r.linked_prior_wbs if isinstance(r.get("linked_prior_wbs", ""), str) and r.get("linked_prior_wbs", "") and \
        str(r.get("link_basis", "")).startswith(("same WBS", "manual")) else r.wbs
    k = link_key(w) if isinstance(w, str) and w else ""
    return k or "NAME:" + Q.norm(r.project_name)


def grouped(d: pd.DataFrame, col: str) -> pd.DataFrame:
    out = []
    for _, r in d.iterrows():
        v = r[col]
        if pd.isna(v):
            v = 0.0
        if r.bulk_infrastructure_name_flag:
            g = "excluded (bulk)"
        else:
            a, _ = Q.allocate(r, "location", "a")
            if isinstance(a, dict) and len(a) == 1:
                g = "Black" if list(a)[0] in BLACK else "Other"
            else:
                g = "not single-ward"
        out.append(dict(key=canon_key(r), name=r.project_name, wards=r.wards, g=g, val=v,
                        B=v if g == "Black" else 0.0, O=v if g == "Other" else 0.0, page=r.page))
    o = pd.DataFrame(out)
    return o.groupby("key").agg(name=("name", "first"), wards=("wards", "first"), g=("g", lambda s: "/".join(sorted(set(s)))),
                                val=("val", "sum"), B=("B", "sum"), O=("O", "sum"), page=("page", "first"))


STEPS = [
    ("2024/25 original → 2024/25 adjusted", (A.rows_for("2024/25", "budget"), "original_budget"), (M[M.doc == "2024/25adj"], "adjusted_budget")),
    ("2024/25 adjusted → 2025/26 original", (M[M.doc == "2024/25adj"], "adjusted_budget"), (M[M.doc == "2025/26"], "original_budget")),
    ("2025/26 original → 2025/26 adjusted", (M[M.doc == "2025/26"], "original_budget"), (M[M.doc == "2025/26adj"], "adjusted_budget")),
    ("2025/26 adjusted → 2026/27 original", (M[M.doc == "2025/26adj"], "adjusted_budget"), (M[M.doc == "2026/27"], "original_budget")),
]


def decompose(x: tuple, y: tuple) -> tuple[pd.DataFrame, dict]:
    X, Y = grouped(*x), grouped(*y)
    m = X.join(Y, how="outer", lsuffix="_1", rsuffix="_2")
    for c in ("val", "B", "O"):
        for s in ("_1", "_2"):
            m[c + s] = m[c + s].fillna(0.0)
    m["dB"], m["dO"] = m.B_2 - m.B_1, m.O_2 - m.O_1
    for side in ("B", "O"):
        att = []
        for r in m.itertuples():
            x1, x2 = getattr(r, side + "_1"), getattr(r, side + "_2")
            if x1 > 0 and x2 == 0 and r.val_2 > 0:
                att.append(-min(r.val_2, x1))
            elif x1 == 0 and x2 > 0 and r.val_1 > 0:
                att.append(min(r.val_1, x2))
            else:
                att.append(0.0)
        m[f"d{side}_attr"] = att
        m[f"d{side}_budget"] = m[f"d{side}"] - m[f"d{side}_attr"]
    B1, O1, B2, O2 = m.B_1.sum(), m.O_1.sum(), m.B_2.sum(), m.O_2.sum()
    Bb, Ob = B1 + m.dB_budget.sum(), O1 + m.dO_budget.sum()
    m["adverse"] = (-m.dB.clip(upper=0)) + m.dO.clip(lower=0)
    m["favourable"] = m.dB.clip(lower=0) + (-m.dO.clip(upper=0))
    return m, dict(B1=B1, O1=O1, B2=B2, O2=O2, s1=B1 / (B1 + O1) * 100, s2=B2 / (B2 + O2) * 100,
                   s2_budget_only=Bb / (Bb + Ob) * 100)


# ---------------- Trace the four 2024/25 cuts ----------------
# matched by WBS programme prefix (catches wrapped names and renamed sub-items) or by name
TRACE = {
    "Thorntree View roads & stormwater": (("9.803306", "9.710865.2.022.N", "9.710865.2.005.N"), r"Thorntree"),
    "Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25)": (("9.801638", "9.801645", "9.714008"), r"Distribution Loss"),
    "Zithobeni X8 sewer provision": (("9.803317",), r"Sewer provision\s*-\s*Zithobeni X8"),
    "Timberlands social housing": (("9.805201.1.S.TI", "9.805202.1.S.SH.CG"), r"Timberlands"),
}


def _hit(d: pd.DataFrame, pref: tuple, pat: str) -> pd.Series:
    w = d.wbs.fillna("").astype(str)
    return w.map(lambda x: any(x.startswith(p_) for p_ in pref)) | d.project_name.str.contains(pat, regex=True, na=False)


def trace() -> pd.DataFrame:
    rows = []
    p = A.p
    meas = [("2023/24 original", p[(p.year == "2023/24") & p.record_type.str.startswith("budget")], "original_budget"),
            ("2023/24 adjusted", p[(p.year == "2023/24") & p.record_type.str.startswith("budget")], "adjusted_budget"),
            ("2024/25 original (Brink)", p[(p.year == "2024/25") & p.record_type.str.startswith("budget")], "original_budget")]
    meas += [(lab, M[M.doc == doc], col) for lab, doc, col, _ in NEW_MEASURES[:1]]
    meas += [("2024/25 adjusted (App N, final)", p[(p.year == "2024/25") & p.record_type.str.startswith("adjusted")], "adjusted_budget"),
             ("2024/25 actual (App N)", p[(p.year == "2024/25") & p.record_type.str.startswith("adjusted")], "actual_spend")]
    meas += [(lab, M[M.doc == doc], col) for lab, doc, col, _ in NEW_MEASURES[1:]]
    for lab, (pref, pat) in TRACE.items():
        for mlab, d, col in meas:
            h = d[_hit(d, pref, pat)]
            rows.append(dict(project=lab, measure=mlab, Rm=h[col].fillna(0).sum() / 1e6 if len(h) else 0.0,
                             listed="yes" if len(h) else "not listed",
                             source=(f"{h.source_file.iloc[0]} p{','.join(str(int(x)) for x in sorted(set(h.page)))}" if len(h) else ""),
                             lines="; ".join(sorted(set(h.project_name.astype(str))))[:160]))
    return pd.DataFrame(rows)


def write_projects_moya(path: str = ROOT + "/output/projects_moya.csv") -> int:
    cols = ["year", "doc", "record_type", "source_file", "page", "project_name", "department", "wbs", "original_budget",
            "adjusted_budget", "attribution", "ward_category", "wards", "ward_source", "region_city_column",
            "region_filled_from_sibling", "region", "region_source", "linked_prior_year", "linked_prior_name",
            "linked_prior_page", "linked_prior_wbs", "link_basis", "check", "carry_conflict",
            "bulk_infrastructure_name_flag", "name_note"]
    M[cols].rename(columns={"check": "regions_column_vs_carried_ward"}).to_csv(path, index=False)
    return len(M)


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    h = headline()
    h.to_csv("work/moya_headline.csv", index=False)
    print(h.pivot_table(index="measure", columns=["basis", "mode"], values="black_share", sort=False).round(1).to_string())
    print(option_b().round(1).to_string(index=False))
    c = carry_checks()
    print(c.groupby("check").agg(n=("value", "size"), Rm=("value", lambda s: s.sum() / 1e6)).round(1))
    print(composition().round(1).to_string(index=False))
    print(conflict_sensitivity().round(1).to_string(index=False))
    for lab, x, y in STEPS:
        m, s = decompose(x, y)
        print(lab, {k: round(v / 1e6 if k in ("B1", "O1", "B2", "O2") else v, 1) for k, v in s.items()})
    print(trace().round(1).to_string(index=False))
