"""Markdown for summary.md section 8 (follow-up 2). Re-runs the scenarios so figures are current."""
import pandas as pd
import analyze as A
import part2_attribute as Q
import ward_region as WRm

F = ",.1f"
ORDER = [m[0] for m in A.MEASURES]


def scenarios() -> dict:
    res = {}
    for basis in ("location", "service"):
        for mode in "ab":
            Q.INCLUDE_TITLES = False
            res[(basis, mode)] = Q.run(basis, mode).set_index("measure")
    Q.INCLUDE_TITLES = True
    for mode in "ab":
        res[("service+titles", mode)] = Q.run("service", mode).set_index("measure")
    Q.INCLUDE_TITLES = False
    return res


def markdown_section() -> str:
    t, e = WRm.build()
    res = scenarios()
    ben = pd.read_csv("work/bulk_beneficiaries_final.csv")
    notu = pd.read_csv("work/bulk_beneficiaries_not_used.csv")
    src = pd.read_csv("work/part2_region_only_sources.csv")

    basis_counts = t.assignment_basis.value_counts()
    conflicts = t[t.step1_conflict][["ward", "step1_city_documents", "step2_rekord_2021", "step3_official_egis", "region_final"]]
    rek_dis = t[t.disagree_step1_vs_rekord][["ward", "step1_city_documents", "step2_rekord_2021", "step3_official_egis"]]
    overrides = t[t.disagree_final_vs_egis][["ward", "step1_city_documents", "step3_official_egis", "region_final"]]
    ev_counts = e.evidence_type.value_counts().rename_axis("Evidence type").reset_index(name="Rows")
    per_region = t.groupby("region_final").ward.apply(lambda s: ", ".join(str(x) for x in sorted(s))).rename_axis("Region").reset_index(name="Wards")

    # results table: Black-ward share, (a) vs (b), both bases
    rows = []
    for m in ORDER:
        la, lb = res[("location", "a")].loc[m], res[("location", "b")].loc[m]
        sa, sb = res[("service", "a")].loc[m], res[("service", "b")].loc[m]
        tb = res[("service+titles", "b")].loc[m]
        rows.append({"Measure": m,
                     "Location (a)": la.black_share, "Location (b)": lb.black_share, "Location (c) = b − a": lb.black_share - la.black_share,
                     "Service area (a)": sa.black_share, "Service area (b)": sb.black_share, "Service (c) = b − a": sb.black_share - sa.black_share,
                     "Service + titles (b)": tb.black_share})
    share_tbl = pd.DataFrame(rows).to_markdown(index=False, floatfmt=F)
    rows = []
    for m in ORDER:
        rows.append({"Measure": m,
                     "Location (a)": res[("location", "a")].loc[m].percap_ratio, "Location (b)": res[("location", "b")].loc[m].percap_ratio,
                     "Service area (a)": res[("service", "a")].loc[m].percap_ratio, "Service area (b)": res[("service", "b")].loc[m].percap_ratio})
    pc_tbl = pd.DataFrame(rows).to_markdown(index=False, floatfmt=",.2f")

    def unatt(key: tuple) -> str:
        d = res[key].copy()
        cols = [c for c in d.columns if c.startswith("un_")]
        out = d[["total_Rm", "attributed_pct", "multiward_Rm"] + cols + ["unattributed_pct"]].copy()
        out = out.rename(columns={c: c.replace("un_", "").replace("_Rm", " (R m)") for c in cols})
        out = out.rename(columns={"total_Rm": "Total (R m)", "attributed_pct": "Ward-attributed %", "multiward_Rm": "Multi-ward (R m)",
                                  "unattributed_pct": "Unattributed %"})
        return out.to_markdown(floatfmt=F)

    srcp = (src.pivot_table(index=["basis", "src"], columns="measure", values="v", aggfunc="sum").reindex(columns=ORDER)
            .to_markdown(floatfmt=F))
    sub3 = (src[src["sub"].fillna("") != ""].pivot_table(index="basis", columns="measure", values="v", aggfunc="sum")
            .reindex(columns=ORDER).to_markdown(floatfmt=F))
    ben_tbl = ben.assign(**{"Page": ben.pdf_page.fillna("").astype(str).str.replace(r"\.0$", "", regex=True)})[
        ["project_key", "basis", "kind", "target", "source_file", "Page", "quote", "note"]].rename(columns={
            "project_key": "Project", "basis": "Basis", "kind": "Attributed to", "target": "Target", "source_file": "Source", "quote": "Quote", "note": "Decision note"}
    ).to_markdown(index=False)
    notu_tbl = notu.rename(columns={"project": "Project", "statement": "Statement", "why_not_used": "Why not used"}).to_markdown(index=False)

    L, Sv = res[("location", "b")], res[("service", "b")]
    return f"""## 8. Follow-up 2 — bulk infrastructure by service area, and region-only money

### 8.1 Ward → region table

Built in the order you specified; the result is in `ward_classification.csv` (`region`, `region_basis`, and the evidence columns).

1. **City documents.** These are every row in the City's documents that gives both a ward and a region:
   - narrative statements in the annual reports (each quoted, with its page, in `work/ward_region_evidence.csv`);
   - Appendix O rows whose project name states a region, e.g. "Region 5 (Public Lighting)" → ward 99;
   - project rows whose Appendix O ward and SA36/SB19 region tag share a WBS code. These are joined across two documents, so they are weaker evidence.

   Four public submissions reproduced in the MTREF appendices also state a ward and region. They are written by residents, not the City, so they are reported but not used.

{ev_counts.to_markdown(index=False)}

2. **Rekord cross-check.** The City-supplied list published by Rekord (18 Oct 2021) was compared ward by ward. Ward 89 is listed under both Region 1 and Region 5, so it is treated as ambiguous.
3. **Official boundary file.** City of Tshwane e-GIS "Tshwane Regions" layer: https://e-gis001.tshwane.gov.za/server/rest/services/Other_WS/Regions/MapServer/2 (ArcGIS Online item 373aab0ab11b4acf93064338ceea828e, owner `Tshwane_Web_GIS`, retrieved 18 Nov 2026). Overlaid on the MDB 2020 wards, **every ward falls 100% inside one region by both area and 2011 population**; the region polygons are built from whole 2020 wards. The layer has Regions 1–7 only, with no 3A/3B split.

Assignment rule:
- One region across all step-1 rows: use it.
- Step-1 rows disagree: use the e-GIS layer as tie-break.
- No step-1 evidence: use the e-GIS layer.

{basis_counts.rename_axis("Basis").reset_index(name="Wards").to_markdown(index=False)}

**Wards the City assigns to different regions in different rows** ({len(conflicts)}). Most are one stray joined row against a clear majority:

{conflicts.to_markdown(index=False)}

**Step 1 vs Rekord disagreements** ({len(rek_dis)}):

{rek_dis.to_markdown(index=False)}

The Rekord list and the e-GIS layer agree on every ward except ward 89, which Rekord lists under both Regions 1 and 5 (e-GIS: Region 1). All four public submissions agree with the final table.

**Where City documents override the e-GIS layer** (unanimous step-1 evidence, per your order of evidence). Ward 107 rests only on the 2023/24 Bronkhorstbaai narrative, which the 2022/23 report places in ward 102, so treat it with caution.

{overrides.to_markdown(index=False)}

Final assignment:

{per_region.to_markdown(index=False)}

**Region 3A/3B.** The budget tables tag some projects "Region 3A" or "Region 3B"; no source lists which wards belong to each half. That money is split across all of Region 3.

### 8.2 Bulk infrastructure: stated beneficiaries

The 84 bulk-infrastructure project names (name-based flag; see §6) were searched across all nine documents for an explicit statement of the area served. Every quote below was checked against the PDF text. Rules for turning a statement into ward weights:
- A stated **ward** goes to that ward.
- A stated **township** goes to its wards, weighted by each ward's share of the township's 2011 population (Census 2011 Main Place mapping).
- A stated **region**, or a statement whose ward conflicts with its own stated region, counts as **region-only money**.
- Anything without a stated beneficiary is **unattributed**, even when Appendix O gives the plant's ward.

The primary run uses narrative and table statements only. Project titles with a service verb ("Water provision – Winterveldt …") are added as a separate variant.

{ben_tbl}

Statements found but not used:

{notu_tbl}

Most bulk projects have **no stated beneficiary**. None was found for Waltloo–Nyala lines, Temba/Babelegi, Ekangala and Baviaanspoort WWTWs, Bronkhorstspruit WPP, the Booysens, Fort West, Refilwe Manor, Babelegi, Magalies, Garsfontein and Klapperkop reservoirs, Salvokop, the Network Control Centre, Ifafi, Kentron, Pyramid, the Olievenhoutbosch X60 bulk line, Bulk Sewer Line – Winterveldt, or the canals. All of those are unattributed on the service-area basis.

### 8.3 Results: Black-ward share (≥80%) of ward-attributed capex

- **Location:** the earlier method (Appendix O ward). Two exceptions: titles naming more than one region (the "Critical Worn-Out Water Pipes" areas), and titles naming a region that doesn't contain the Appendix O ward (Areas B and D in 2023/24), are treated as region-only.
- **Service area:** bulk rows attributed only through a stated beneficiary (§8.2); all other rows as under location.
- **(a):** region-only money left unattributed.
- **(b):** region-only money split across that region's wards in proportion to 2022 population. **This assumes every resident of the region benefits equally; it is an assumption, not a fact from the documents.**
- **(c):** (b) minus (a), in percentage points.

{share_tbl}

Per-capita ratio (R per resident in Black wards ÷ R per resident in other wards):

{pc_tbl}

### 8.4 What remains unattributed

After (b), the unattributed share of each measure's capex is **{L.unattributed_pct.min():.0f}–{L.unattributed_pct.max():.0f}%** on the location basis and **{Sv.unattributed_pct.min():.0f}–{Sv.unattributed_pct.max():.0f}%** on the service-area basis. On top of that, multi-ward projects (shown separately) are not split across wards.

Location basis, (b):

{unatt(("location", "b"))}

Service-area basis, (b):

{unatt(("service", "b"))}

Where the region-only money comes from (R m, split in (b)):

{srcp}

Of which tagged "Region 3A/3B" and therefore spread over all of Region 3 (R m):

{sub3}

### 8.5 Reading

- **Service area.** Re-attributing bulk infrastructure by stated service area mainly removes it from the ward analysis, because only a handful of plants have a documented beneficiary. On that basis the Black-ward share is roughly flat between 2022/23 and 2023/24 ({Sv.black_share.iloc[0]:.1f}% → {Sv.black_share.iloc[2]:.1f}% original; {Sv.black_share.iloc[1]:.1f}% → {Sv.black_share.iloc[3]:.1f}% adjusted, under (b)). It is lower in all three 2024/25 measures ({Sv.black_share.iloc[4]:.1f}% original, {Sv.black_share.iloc[5]:.1f}% adjusted, {Sv.black_share.iloc[6]:.1f}% actual).
- **Rooiwal.** Under the location basis, Rooiwal counts against Black wards because the plant sits in ward 96. Under the service-area basis it counts for Temba and Hammanskraal, as the City's annual reports state. Because so much other bulk spending drops out, the service-area shares rest on 33–49% of the budget.
- **Region-only split.** Population-splitting region-only money moves the Black-ward share by at most {max(abs(res[('location','b')].black_share - res[('location','a')].black_share).max(), abs(res[('service','b')].black_share - res[('service','a')].black_share).max()):.1f} points in any year. It raises ward-attributed coverage by 0–14 points on the location basis and 4–13 points on the service-area basis, depending on the year, but leaves the year-to-year pattern unchanged.
- **Overall.** The 2022/23 → 2023/24 fall in §3 depends on counting bulk plants by location; it doesn't survive service-area attribution. The 2024/25 fall (Brink-era original budget, and the adjusted budget and actual spend executed mostly afterwards) survives every variant here, though a third of that step is ward labelling (§7).
"""
