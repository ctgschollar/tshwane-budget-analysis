"""Moya-era rows (2024/25 adjustments budget, 2025/26 MTREF, 2025/26 adjustments budget, 2026/27 MTREF) with Option A
ward attribution, in the same row format as output/projects.csv so part2_attribute.allocate() can be reused.

Option A:
  2024/25adj : ward from the SAME year's Appendix O, via the WBS-linked 2024/25 MTREF row (no carry-forward needed);
               otherwise region from the 2024/25 SA36 tag of the same WBS.
  2025/26+   : ward CARRIED FORWARD from the most recent earlier row with an Appendix O ward (2024/25 MTREF row, then
               2023/24 adjustments-budget row), linked by WBS without the funding segment + name check (flagged);
               otherwise the City's 'Regions' column of the same document (Region N -> region-only;
               'Tshwane Wide' -> city-wide; 'Administrative' -> administrative-hq; blank -> unmatched)."""
import re
import pandas as pd
from match import norm, score
from analyze import p as P  # output/projects.csv
from ex_annex_new import norm_region

BULK_RE = re.compile(r"substation|infeed|sub station|wwtw|power line|network control|reservoir|bulk|canal|feeder|"
                     r"outfall|water treatment|purification", re.I)
SCOPE_RE = re.compile(r"city ?wide|all regions|various|regions? \d[^)]*?(,| and |&)\s*\d|area[- ]?[a-e]\b", re.I)
DOC_LABEL = {
    "2024/25adj": ("2024/25", "adjusted_budget", "07.-Proposed-2024-2025-Adjustment-Budget.pdf"),
    "2025/26": ("2025/26", "original_budget", "02.-2025-2026-MTREF-for-the-City-of-Tshwane-Special-Council-29-05-2025.pdf"),
    "2025/26adj": ("2025/26", "adjusted_budget", "10.-2025-2026-Adjustment-Budget.pdf"),
    "2026/27": ("2026/27", "original_budget", "02.-2026-2027-MTREF-for-CoT-Final-1.pdf"),
}
# Overprinted names in the new PDFs: (doc, page, wbs or None, amount in the doc's value column or None) -> (name, evidence)
NAME_OVERRIDES = [
    ("2026/27", 71, None, 52047480, "(710026C) Replacement Of Critical Worn-Out Water Network Pipes (Area C - Region 4,5,6&7)",
     "overprint decoded: raw text p71 shows '(710026C)' and '(Area C- Region 4,5,6&7)' on the wrapped lines; Regions column 'Multiple regions'"),
    ("2026/27", 71, None, 9812793, "(710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B - Region 3)",
     "overprint decoded: raw text p71 '(710026B)' / '(Area B- Region 3)'; Regions column 'Region 3'"),
    ("2026/27", 69, "9.804016.1.B.RE.02.W", None, "Rehabilitation of Existing Infrastructure (BRT)",
     "overprint decoded: WBS sub-code RE under BRT programme 9.804016; raw text p69 '... of Existing Infrastructure'"),
    ("2026/27", 71, "9.804713.1.W.EK.24.7", None, "Ekangala WWTW: Upgrade of existing infrastructure",
     "overprint decoded: WBS sub-code EK (Ekangala WWTW in earlier years); overprint is '(City wide)'"),
    ("2026/27", 71, "9.804710.1.C.LA.16.6", None, "Contributions: La Montagne",
     "overprint decoded: 'Contributions: La Montagne' overprinted with '(City Wide)'; Regions column 'Region 6'"),
    ("2026/27", 69, "9.804016.1.B.BE.02.3", None, "Belle Ombre - Phase 2 (Overflow car park, Electric Fencing etc)",
     "overprint decoded: WBS sub-code BE (as in 2023/24); overprint is AFC tail"),
    ("2024/25adj", 136, "9.805201.1.S.SH.05.1", None, "Chantelle detail design and bulk infrastructure upgrade",
     "overprint decoded: WBS 9.805201 is Chantelle in the 2023/24 adjustments budget; overprint is the Sunnyside row"),
]

# manual cross-year links (2025/26+ WBS -> earlier WBS), each with evidence. Filled after review of unlinked rows.
MANUAL_LINKS: dict[str, tuple[str, str]] = {
    "9.804721.1.S.SE.05.7": ("9.804713.1.W.EK.05.7",
                             "Ekangala Block A - F sewer reticulation and toilets: the 2024/25 MTREF (Annexure A) carried it under the "
                             "Ekangala WWTW code EK.05.7; the 2024/25 adjustments budget (p139) lists it under 9.804721.1.S.SE.05.7 with the "
                             "identical original amount R32,379,635"),
}


def link_key(w: str) -> str:
    if not isinstance(w, str) or not w.strip():
        return ""
    parts = w.strip().split(".")
    return ".".join(parts[:5] + parts[6:]) if len(parts) >= 7 else w.strip()


def prior_index() -> dict[str, list[pd.Series]]:
    """link key -> earlier budget rows (2024/25 MTREF first, then 2023/24 adj budget) that carry an Appendix O attribution."""
    idx: dict[str, list] = {}
    for y in ("2024/25", "2023/24"):
        b = P[(P.year == y) & P.record_type.str.startswith("budget")]
        for _, r in b.iterrows():
            k = link_key(r.wbs)
            if k:
                idx.setdefault(k, []).append(r)
    return idx


def sa36_2425() -> dict[str, tuple[str, str]]:
    reg = pd.read_csv("work/regions.csv").fillna({"region": ""})
    r = reg[(reg.table == "SA36_2425") & (reg.region != "")]
    return {c: (g, f"{f} p{pg} (SA36_2425)") for c, g, f, pg in zip(r.code, r.region, r.source_file, r.page)}


def build() -> pd.DataFrame:
    a = pd.read_csv("work/annex_new.csv")
    a = a[a.use_row].copy()
    a["name_note"] = ""
    for d_, pg, w, amt, nm, why in NAME_OVERRIDES:
        col_ = "adjusted_budget" if DOC_LABEL[d_][1] == "adjusted_budget" else "original_budget"
        msk = (a.doc == d_) & (a.page == pg)
        msk &= (a.wbs == w) if w else (a[col_].round() == amt)
        assert msk.sum() >= 1, (d_, pg, w, amt)
        a.loc[msk, "project_name"] = nm
        a.loc[msk, "name_note"] = why
    # canonical titles for the worn-out pipe programme (overprinted in several new PDFs): titles per 2025/26 MTREF p69
    AREA = {"A": "Area A - Region 1-2", "B": "Area B - Region 3", "C": "Area C - Region 4,5,6&7"}
    for i, r in a.iterrows():
        mw = re.match(r"9\.804700\.1\.W\.A([ABC])\.", str(r.wbs))
        mn = re.search(r"\(710026([ABC])\)", str(r.project_name))
        L = (mw.group(1) if mw else None) or (mn.group(1) if mn and "Worn" in str(r.project_name) else None)
        if L:
            a.at[i, "project_name"] = f"(710026{L}) Replacement Of Critical Worn-Out Water Network Pipes ({AREA[L]})"
            a.at[i, "name_note"] = ("canonical title from 2025/26 MTREF Annexure A p69 by area letter "
                                    f"({'WBS sub-code A' + L if mw else 'project code 710026' + L}); source text overprinted/wrapped")
    a["region_city"] = a.region_city.fillna("")
    a["lk"] = a.wbs.map(link_key)
    a["region_filled_from_sibling"] = False
    for (d, k), g in a[a.lk != ""].groupby(["doc", "lk"]):
        regs = set(g.region_city) - {""}
        if len(regs) == 1:
            m_ = g.index[g.region_city == ""]
            a.loc[m_, "region_city"] = regs.pop()
            a.loc[m_, "region_filled_from_sibling"] = True
    idx = prior_index()
    sa = sa36_2425()
    out = []
    for _, r in a.iterrows():
        fy, col, f = DOC_LABEL[r.doc]
        val = r.adjusted_budget if col == "adjusted_budget" else r.original_budget
        k = link_key(r.wbs)
        if r.wbs in MANUAL_LINKS:
            k = link_key(MANUAL_LINKS[r.wbs][0])
        cands = idx.get(k, [])
        # same-year (2024/25adj) may only link to 2024/25 rows; later years take 2024/25 first, then 2023/24
        if r.doc == "2024/25adj":
            cands = [c for c in cands if c.year == "2024/25"]
        cands = [c for c in cands if score(norm(c.project_name), norm(r.project_name)) >= 60 or r.wbs in MANUAL_LINKS]
        cands = sorted(cands, key=lambda c: -score(norm(c.project_name), norm(r.project_name)))
        link_basis = "manual" if r.wbs in MANUAL_LINKS else "WBS (excl. funding segment) + name check"
        if not cands and isinstance(r.wbs, str) and r.wbs.count(".") >= 2:
            prog = ".".join(r.wbs.split(".")[:2])
            pool = [c for k2, cs in idx.items() if k2.startswith(prog + ".") for c in cs
                    if (r.doc != "2024/25adj" or c.year == "2024/25")]
            from run_match import conflict, PLACES
            nr = norm(r.project_name)

            def ok(c: pd.Series) -> bool:
                pn_ = norm(c.project_name)
                extra_places = (set(nr.split()) - set(pn_.split())) & PLACES
                contained = len(pn_) > 15 and pn_ in nr and not extra_places
                return (score(pn_, nr) >= 95 or contained) and not conflict(c.project_name, r.project_name)
            scored = sorted(((score(norm(c.project_name), nr), c) for c in pool if ok(c)), key=lambda t: -t[0])
            if scored:
                best = scored[0][0]
                cands = [c for sc, c in scored if sc == best]
                link_basis = f"same WBS programme ({prog}) + name match {best:.0f} (sub-code renamed)"
        attrib = [c for c in cands if c.ward_category in ("single-ward", "multi-ward", "city-wide", "administrative-hq", "no-intersect")]
        row = dict(year=fy, doc=r.doc, record_type=f"budget ({r.doc})", source_file=f, page=r.page,
                   project_name=r.project_name, department=r.department, wbs=r.wbs,
                   original_budget=None, adjusted_budget=None, actual_spend=None,
                   region_city_column=r.get("region_city", "") if isinstance(r.get("region_city", ""), str) else "",
                   linked_prior_year="", linked_prior_name="", linked_prior_page="", linked_prior_wbs="",
                   region_filled_from_sibling=bool(r.region_filled_from_sibling), name_note=r.name_note)
        row[col] = val
        if attrib:
            c = attrib[0]
            row.update(ward_category=c.ward_category, wards=c.wards, wards_raw=c.wards_raw,
                       ward_source=("same-year App O via 2024/25 MTREF row; " if r.doc == "2024/25adj" else
                                    f"CARRIED FORWARD from {c.year}: ") + str(c.ward_source),
                       attribution=("same-year Appendix O" if r.doc == "2024/25adj" else "carried-forward ward"),
                       region=c.region if isinstance(c.region, str) else "",
                       region_source=c.region_source if isinstance(c.region_source, str) else "",
                       linked_prior_year=c.year, linked_prior_name=c.project_name, linked_prior_page=c.page,
                       linked_prior_wbs=c.wbs,
                       link_basis=("manual: " + MANUAL_LINKS[r.wbs][1]) if r.wbs in MANUAL_LINKS else link_basis)
        else:
            if r.doc == "2024/25adj":
                g, src = sa.get(r.wbs, ("", ""))
                cat = "unmatched"
                attr = "region-only (SA36 tag)" if g else "no ward or region"
            else:
                g = row["region_city_column"]
                src = f"{f} p{r.page} (Regions column)"
                cat = {"Tshwane Wide": "city-wide", "Administrative": "administrative-hq"}.get(g, "unmatched")
                attr = {"Tshwane Wide": "Tshwane Wide", "Administrative": "Administrative",
                        "Multiple regions": "Multiple regions (unspecified)"}.get(g, "region-only (Regions column)" if g else "no ward or region")
                if ";" in str(g):
                    g = g  # multiple regions in the column -> handled by regions_in_text via ward_source
            row.update(ward_category=cat, wards="", wards_raw="", ward_source=f"'{r.project_name}'" if g else "",
                       attribution=attr, region=g if str(g).startswith("Region") else "", region_source=src if g else "",
                       link_basis="")
        row["bulk_infrastructure_name_flag"] = bool(BULK_RE.search(str(r.project_name)))
        row["scope_flag_multi_region_name"] = bool(SCOPE_RE.search(str(r.project_name))) and row["ward_category"] == "single-ward"
        out.append(row)
    return pd.DataFrame(out)


if __name__ == "__main__":
    m = build()
    m.to_csv("work/moya_rows.csv", index=False)
    for d, g in m.groupby("doc", sort=False):
        col = "adjusted_budget" if DOC_LABEL[d][1] == "adjusted_budget" else "original_budget"
        print(d, f"total R{g[col].sum()/1e6:,.1f}m", (g.groupby("attribution")[col].sum() / 1e6).round(1).to_dict())
