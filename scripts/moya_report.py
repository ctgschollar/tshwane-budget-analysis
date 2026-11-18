"""Markdown for summary.md section 9 (Moya-era extension). All figures computed from work/ files."""
import pandas as pd
import moya_analysis as X
import moya_build as MB

F = ",.1f"
ORDER = ["2022/23 original budget", "2022/23 adjusted budget", "2023/24 original budget", "2023/24 adjusted budget",
         "2024/25 original budget", "2024/25 adjusted (adj. budget)", "2025/26 original", "2025/26 adjusted",
         "2026/27 original (Mayco draft, reconciles to adopted SDBIP)"]
EXTRA = ["2024/25 adjusted budget", "2024/25 actual spend"]  # App N (final adjusted / actual)


def ab_compare(h: pd.DataFrame, b: pd.DataFrame) -> tuple[str, str]:
    a = h[(h.basis == "location") & (h["mode"] == "b")].set_index("measure").black_share
    bb = b.set_index("measure").black_share
    rows, agree_n = [], 0
    for x, y in zip(ORDER[:-1], ORDER[1:]):
        da, db = a[y] - a[x], bb[y] - bb[x]
        same = (da > 0) == (db > 0) or (abs(da) < 1 and abs(db) < 1)
        agree_n += same
        size = "similar" if abs(abs(da) - abs(db)) <= max(2.0, 0.5 * max(abs(da), abs(db))) else ("A larger" if abs(da) > abs(db) else "B larger")
        rows.append({"Step": f"{x} → {y}", "Option A Δ (pts)": da, "Option B Δ (pts)": db,
                     "Same direction?": "yes" if same else "NO", "Size": size})
    return pd.DataFrame(rows).to_markdown(index=False, floatfmt="+.1f"), f"{agree_n} of {len(ORDER) - 1}"


def section() -> str:
    h = pd.read_csv("work/moya_headline.csv") if False else X.headline()
    b = X.option_b()
    comp = X.composition()
    cc = X.carry_checks()
    sens = X.conflict_sensitivity()
    tr = X.trace()

    # ---- headline
    piv = {}
    for basis in ("location", "service"):
        for mode in "ab":
            piv[(basis, mode)] = h[(h.basis == basis) & (h["mode"] == mode)].set_index("measure")
    ad = h[(h.basis == "location") & (h["mode"] == "a")].set_index("measure").adopted
    rows = []
    for m in ORDER + EXTRA:
        rows.append({"Budget / spend": m, "Adopted by": ad[m],
                     "Loc (a)": piv[("location", "a")].loc[m].black_share, "Loc (b)": piv[("location", "b")].loc[m].black_share,
                     "Svc (a)": piv[("service", "a")].loc[m].black_share, "Svc (b)": piv[("service", "b")].loc[m].black_share,
                     "R/resident ratio Loc (b)": piv[("location", "b")].loc[m].percap_ratio,
                     "R/resident ratio Svc (b)": piv[("service", "b")].loc[m].percap_ratio,
                     "Ward-attributed % Loc (b)": piv[("location", "b")].loc[m].attributed_pct,
                     "Ward-attributed % Svc (b)": piv[("service", "b")].loc[m].attributed_pct})
    head_tbl = pd.DataFrame(rows).to_markdown(index=False, floatfmt=",.1f")

    # ---- Option B
    bt = b.set_index("measure").reindex(ORDER + EXTRA).reset_index().rename(columns={
        "measure": "Budget / spend", "attributed_pct": "Region-tagged % of budget", "black_share": "Black-ward share (pop. split)",
        "percap_ratio": "R/resident ratio"}).to_markdown(index=False, floatfmt=",.1f")
    cmp_tbl, agree = ab_compare(h, b)
    _a = h[(h.basis == "location") & (h["mode"] == "b")].set_index("measure").black_share.reindex(ORDER)
    _b = b.set_index("measure").black_share.reindex(ORDER)
    b_lo, b_hi, b_max, a_max = _b.min(), _b.max(), _b.diff().abs().max(), _a.diff().abs().max()

    # ---- composition
    ct = comp.pivot_table(index="category", columns="measure", values="Rm", aggfunc="sum").reindex(
        columns=[m for m in ORDER if m in comp.measure.unique()])
    cp = comp.pivot_table(index="category", columns="measure", values="pct", aggfunc="sum").reindex(columns=ct.columns)
    comp_tbl = (ct.round(1).astype(str) + " (" + cp.round(1).astype(str) + "%)").fillna("–").replace("nan (nan%)", "–").to_markdown()

    # ---- carry checks
    spec = cc[cc.check.isin(["agree", "conflict"])]
    rate_n = (spec.check == "agree").mean() * 100
    rate_r = spec[spec.check == "agree"].value.sum() / spec.value.sum() * 100
    chk = cc.groupby("check").agg(Rows=("value", "size"), Rm=("value", lambda s: s.sum() / 1e6)).reset_index().rename(
        columns={"check": "Regions column vs e-GIS region of carried ward"}).to_markdown(index=False, floatfmt=F)
    mism = cc[cc.check != "agree"].sort_values("value", ascending=False)
    mism_tbl = mism.assign(Rm=mism.value / 1e6)[["doc", "page", "project_name", "carried_ward", "egis_region", "region_city_column", "check", "Rm"]].rename(
        columns={"doc": "Document", "page": "Page", "project_name": "Project", "carried_ward": "Carried ward", "egis_region": "e-GIS region of ward",
                 "region_city_column": "City Regions column", "check": "Result", "Rm": "R m"}).to_markdown(index=False, floatfmt=F)
    sens_tbl = sens.rename(columns={"measure": "Budget", "carried_conflicts": "Treatment", "black_share": "Black-ward share Loc (b)",
                                    "percap_ratio": "R/resident ratio", "attributed_pct": "Ward-attributed %"}).to_markdown(index=False, floatfmt=F)

    # ---- step decompositions
    step_rows, step_md = [], []
    for lab, x, y in X.STEPS:
        m, s = X.decompose(x, y)
        a = m[m.adverse > 0].sort_values("adverse", ascending=False)
        f = m[m.favourable > 0].sort_values("favourable", ascending=False)
        gross_a, gross_f = a.adverse.sum(), f.favourable.sum()
        step_rows.append({"Step": lab, "Black share before": s["s1"], "after": s["s2"], "after, budget effects only": s["s2_budget_only"],
                          "Black ward R m Δ": (s["B2"] - s["B1"]) / 1e6, "…budget": m.dB_budget.sum() / 1e6, "…relabelling": m.dB_attr.sum() / 1e6,
                          "Other ward R m Δ": (s["O2"] - s["O1"]) / 1e6, "…budget ": m.dO_budget.sum() / 1e6, "…relabelling ": m.dO_attr.sum() / 1e6,
                          "Top-5 share of moves against Black wards %": a.adverse.head(5).sum() / gross_a * 100 if gross_a else float("nan"),
                          "Top-5 share of moves toward Black wards %": f.favourable.head(5).sum() / gross_f * 100 if gross_f else float("nan")})
        w = lambda v: "–" if not isinstance(v, str) or not v else v
        mk = lambda d, col, lbl: pd.DataFrame([{
            "Project": str(r.name_1 if isinstance(r.name_1, str) else r.name_2)[:70], "Ward": f"{w(r.wards_1)} → {w(r.wards_2)}",
            "Group": f"{r.g_1 if isinstance(r.g_1, str) else '–'} → {r.g_2 if isinstance(r.g_2, str) else '–'}",
            "Before (R m)": r.val_1 / 1e6, "After (R m)": r.val_2 / 1e6, lbl: getattr(r, col) / 1e6,
            "…of which relabelling": ((abs(r.dB_attr) + abs(r.dO_attr)) / 2 if r.dB_attr and r.dO_attr else abs(r.dB_attr) + abs(r.dO_attr)) / 1e6}
            for r in d.head(8).itertuples()]).to_markdown(index=False, floatfmt=F)
        step_md.append(f"**{lab}**\n\nLargest moves *against* Black wards (Black ↓ or other ↑):\n\n{mk(a, 'adverse', 'Impact (R m)')}\n\n"
                       f"Largest moves *toward* Black wards:\n\n{mk(f, 'favourable', 'Impact (R m)')}\n")
    step_tbl = pd.DataFrame(step_rows).to_markdown(index=False, floatfmt=",.1f")
    m1, _ = X.decompose(*X.STEPS[0][1:])
    a1 = m1[m1.adverse > 0].sort_values("adverse", ascending=False).head(6)
    drivers1 = "; ".join(f"{str(r.name_1 if isinstance(r.name_1, str) else r.name_2)[:55]} (ward {r.wards_1 if isinstance(r.wards_1, str) and r.wards_1 else r.wards_2}, "
                         f"{'+' if r.dO > 0 else '−'}R{r.adverse/1e6:,.1f}m)" for r in a1.itertuples())
    svr = [piv[("service", "b")].loc[m].percap_ratio for m in ORDER[5:]]
    lvr = [piv[("location", "b")].loc[m].percap_ratio for m in ORDER[5:]]

    # ---- trace
    tr_tbl = tr.assign(Rm=tr.Rm.round(1))[["project", "measure", "Rm", "listed", "source"]].rename(columns={
        "project": "Project", "measure": "Budget / spend", "Rm": "R m", "listed": "Listed?", "source": "Source"}).to_markdown(index=False)

    hl = piv[("location", "b")]
    sv = piv[("service", "b")]
    return f"""## 9. Extension to the Moya administration (from Oct 2024)

All methods, scripts, the ward classification (Stats SA 2022, ≥80% Black African primary) and the ward→region table are unchanged from §1–§8, so the new columns compare directly with the old ones.

### 9.1 New documents

| File | Pages | Contents used | Ward / region columns | Budget or actual |
|---|---|---|---|---|
| 07. Proposed 2024-25 Adjustment Budget | 151 | Annexure B pp135–139 (project-level original → adjusted 2024/25) | none (no SB19 table) | budget; capital YTD actual only as a citywide total: **R802m to 31 Dec 2024, 34% of the original** (p47) |
| 02. 2025-26 MTREF (Special Council 29-05-2025) | 1,803 | Annexure A pp64–70 (project-level 2025/26 original) | **"Regions" column** (Region 1–7, Tshwane Wide, Administrative); no SA36 table | budget |
| 10. 2025-26 Adjustment Budget | 150 | Annexure B pp144–150 (project-level 2025/26 original → adjusted) | **"Regions" column** | budget; capital YTD actual only citywide: **R1,1 billion, 46% of the original** (p52) |
| 02. 2026-27 MTREF (Final) | 1,508 | Annexure A pp66–72 (project-level 2026/27 original) | **"Regions" column** (adds "Multiple regions") | budget. Cover: "Mayoral Committee to be held on 21 May 2026" (p65). Council adoption date not stated. Corrupt streams and blank pages are in tariff annexures N–P only |
| "-1" copies of the 2022/23 and 2023/24 annual reports | – | byte-identical duplicates (same MD5); ignored | | |

**No ward-level actual spend exists for 2025/26.** There is no 2025/26 annual report or in-year capital report in the folder, and none of the new documents breaks capital actuals down by region either. The only in-year capital actuals are the two citywide figures:

| Period | Capital spent | % of original capital budget | Source |
|---|---|---|---|
| 2024/25, to 31 Dec 2024 | R802 million (incl. entities) | 34% | 2024/25 adjustment budget p47 |
| 2024/25, full year | R2,300,073,481 | 98.3% of adjusted (App N) | AR 2024/25 App N p515 |
| 2025/26, mid-year | R1,1 billion | 46% | 2025/26 adjustment budget p52 |

### 9.2 Extraction and reconciliation

| Budget | Extracted | Stated total | Where stated | Coverage |
|---|---|---|---|---|
| 2024/25 original (adj. budget col.) | R2,347,552,577 | R2,347,552,576 | Annexure B p139 | 100% |
| 2024/25 adjusted (adj. budget) | R2,312,623,793 | R2,312,623,791 | Annexure B p139 | 100% |
| 2025/26 original | R2,459,328,252 | R2,459,328,252 | Annexure A p70 | 100% |
| 2025/26 adjusted | R2,755,935,586 | R2,768,935,587 | Annexure B p150 | **99.5%** |
| 2026/27 original | R2,856,300,535 | R2,856,300,538 | Annexure A p72 | 100% |

- **2025/26 adjusted gap.** The R13,000,000 shortfall (original and adjusted) is in the source document itself. "Upgrading of roads and stormwater systems in Refilwe" (WBS 9.804026.1.R.RO.05.5, R13m in the 2025/26 MTREF) is missing from Annexure B's project list, but its Roads & Transport department total (R602,855,364, p147) still includes it. It is left unattributed rather than reconstructed.
- **2024/25 adjusted, two totals.** The 2024/25 adjustment budget (R2,312.6m, the post-Oct 2024 Council's adjustment) is the new column. The annual report's Appendix N "adjusted" (R2,340.1m) and actual are kept as the final 2024/25 figures, as agreed.
- **2026/27 reconciles.** The Annexure A total of **R2,856,300,538** equals the 2026/27 SDBIP capital total you supplied (R2,856,300,538) exactly, and the MTREF itself says "The capital budget amounts to R2,8 billion for 2026/27" (p109) and "TOTAL CAPITAL BUDGET 2,856,300,538" (p111). Neither the SDBIP nor the budget speech is in the folder, so that match rests on the figure supplied. The column is labelled "2026/27 original (Mayco draft, reconciles to adopted SDBIP)".
- **Name decoding.** Overprinted names were decoded as before; each change is recorded in `name_note` in `work/moya_rows.csv`. The "Critical Worn-Out Water Pipes" rows were given their canonical titles from the 2025/26 MTREF p69 by area letter: Area A covers Regions 1–2, Area B Region 3, and Area C Regions 4, 5, 6 & 7.
- **Linking across years.** Links use the WBS code without the funding segment plus a name check. One extra rule handles sub-codes that were renamed: the same WBS programme plus a name score ≥95, or the old name contained in the new one with no added place name. This covers the Soshanguve JJ line (`SU`→`SO`), Monavoni, Wildebees and the deficient-sewers areas. Weaker candidates were rejected: Baviaanspoort→Rooiwal, Rietvlei→Bronkhorstspruit, Heatherview X79→X42, and area-specific Water Conservation lines→the citywide line.

### 9.3 Option A attribution and the composition of each new budget (check 2)

- **2024/25 adjusted:** each row takes its ward from the same year's Appendix O, via its WBS-linked 2024/25 MTREF row. Otherwise it takes the 2024/25 SA36 region tag.
- **2025/26 onward:** each row takes its ward from the most recent earlier Appendix O (2024/25, else 2023/24), via the WBS link. These rows are flagged "CARRIED FORWARD"; this is an inference across years, not a ward stated in the new documents. Otherwise the row uses the City's Regions column.

Composition (R m, % of each budget):

{comp_tbl}

(i) = ward(s) from Appendix O (carried forward from 2025/26); (i') = Appendix O said city-wide, HQ or "No Intersect"; (ii) = region-only; (iii) = Tshwane Wide or Administrative; (iv) = "Multiple regions" with no region named; (v) = neither a ward nor a region. The asymmetry is visible: **continuing projects carry a ward, new projects can only be placed by region**. The region-only share rises from {comp[(comp.measure == ORDER[6]) & comp.category.str.startswith('(ii)')].pct.sum():.1f}% (2025/26 original) to {comp[(comp.measure == ORDER[8]) & comp.category.str.startswith('(ii)')].pct.sum():.1f}% (2026/27), and carried single-ward money falls from {comp[(comp.measure == ORDER[6]) & comp.category.str.contains('single ward')].pct.sum():.1f}% to {comp[(comp.measure == ORDER[8]) & comp.category.str.contains('single ward')].pct.sum():.1f}%.

### 9.4 Carried-forward wards vs the City's Regions column (check 1)

Every carried-forward single-ward row from 2025/26 on was compared with the official e-GIS region of its carried ward:

{chk}

**Agreement rate** where the column names a specific region: **{rate_n:.1f}% of rows, {rate_r:.1f}% of rand value**. Separately, **R{cc[cc.check.str.startswith('column says')].value.sum()/1e6:,.1f}m** of carried single-ward money is labelled Tshwane Wide, Administrative or "Multiple regions" by the City, which conflicts in scope with Appendix O's single ward. All of these rows are flagged `carry_conflict` in `work/moya_rows.csv`. Mismatches:

{mism_tbl}

The pipe-programme conflicts are internal to the City's documents. The 2025/26 MTREF titles Area A "Region 1-2", but its Regions column says "Region 5" (p69); Areas B and C are titled with regions but tagged "Tshwane Wide". The carried Appendix O wards (96 in Region 2, 53 in Region 3, 100 in Region 5) each lie inside the titled regions, but each places a region-wide programme in a single ward. Under the location basis these rows are already treated as region-only by the title rule (§8.3).

Sensitivity — where the column disagrees (including Tshwane Wide), use the Regions column instead of the carried ward:

{sens_tbl}

### 9.5 Headline: Black-ward share of ward-attributed capex, ≥80% definition

- **Loc** = physical location; **Svc** = stated service area for bulk infrastructure (§8.2 statements, applied to the same projects in later years).
- **(a)** leaves region-only money unattributed; **(b)** splits it across the region's wards by population. The equal-benefit assumption in (b) is an assumption, not something the documents state.
- The per-resident ratio is rand per resident in Black wards ÷ rand per resident in other wards.

{head_tbl}

The two App N rows at the bottom are the final 2024/25 adjusted budget and actual spend (§3), shown for reference.

### 9.6 Robustness: Option B (region level for every year)

Option B uses only region tags, for every year: SA36/SB19 for 2022/23–2024/25, the SA36 tag of the same-named MTREF row for Appendix N, and the Regions column from 2025/26. Each region's money is split across its wards by population. No ward-level information is used.

{bt}

Year-to-year changes, Option A (location, (b)) vs Option B:

{cmp_tbl}

**Agreement.** The two agree on direction in {agree} steps. Option B moves much less: its series stays between {b_lo:.1f}% and {b_hi:.1f}%, with no step larger than ±{b_max:.1f} points, while Option A moves up to ±{a_max:.1f}. Option B is coarse by construction: a region mixes Black and other wards, and splitting by population pulls every year towards the region average. So the large Option A swings depend on ward-level attribution. Where B moves the same way, the direction is confirmed; the size is not.

### 9.7 What drove each step (excluding bulk infrastructure, location basis, (a))

Same method as §7. Projects are linked across steps; each project's change is split into its own budget change and relabelling (attribution moving between groups).

{step_tbl}

How to read the relabelling columns:
- **From 2025/26 on, relabelling is zero by construction.** Carried-forward wards are copied from the same earlier Appendix O, so a continuing project can't change ward between Moya-era budgets. Only real budget changes show up there.
- **The 2024/25 adjusted → 2025/26 original step also changes coverage.** Same-year Appendix O matching (2024/25) gives way to carry-forward, which draws on two years of Appendix O. Ward-attributed coverage (location, (b)) rises from {piv[("location", "b")].loc[ORDER[5]].attributed_pct:.1f}% to {piv[("location", "b")].loc[ORDER[6]].attributed_pct:.1f}%, so part of that step's movement is projects entering the attributable pool.

{chr(10).join(step_md)}

### 9.8 Were the 2024/25 cuts restored?

Traced by WBS programme code, with name as a fallback:

{tr_tbl}

**Findings:**
- **Thorntree View roads & stormwater (ward 36): not restored in the budgets.**
  - 2024/25 under Moya: R18.6m in the adjustment budget (p136); App N records R24.5m adjusted and actual.
  - 2025/26: not listed in the MTREF or the adjustment budget.
  - 2026/27: listed at R0 (p68).
  - **No document says the project was completed.** AR 2022/23 p179 reports progress ("Thorntree view project achieved a total of 15.8km"). AR 2023/24 p432 attributes under-expenditure on it to "underperformance by the contractor". AR 2024/25 p464 lists "Phase 2 – Construction of bulk stormwater channel – Thorntree View (Soshanguve South Extension 7)", ward 36, as not complete.
  - The 2025/26 MTREF procurement plan (p1727) schedules "Appointment of a Contractor for the Completion and remedial works of 2.2 KM stormwater channel at Thorntreeview" at R14,000,000 (MIG), with consultant (R2m) and health-and-safety (R1m) appointments (p1739). That work is not identifiable by name in the 2025/26 or 2026/27 capital annexures.
- **Electricity Distribution Loss (ward 29): held at R20m, partly restored in 2025/26 adjusted.**
  - R20m in the 2024/25 adjusted, 2025/26 original and 2026/27 original budgets.
  - The 2025/26 adjustment added **R27m** "from Urban Development Financing Grant" (adj. budget p62), for **R47m** in total (p149). Still below the R68m of 2023/24.
  - From 2024/25 the programme is re-coded as 9.801645, with "Revenue Enhancement" sub-items.
- **Zithobeni X8 sewer provision (ward 105): not restored.** It hasn't been listed in any budget since 2023/24, which cites contractor underperformance (AR 2023/24 p432). Zithobeni X8&9 bulk water main and roads lines do continue, and the 2025/26 adjustment added R4.4m for "Zithobeni x8 &9" (p61). These are separate projects.
- **Timberlands social housing (ward 81): not restored.** It's listed at a token R1,000 in the 2025/26 original and adjusted budgets (MTREF p65; adj. p146), against an estimated total project cost of R394,550,000 (MTREF p65). Not listed in 2026/27.
- **Correction to §7:** that section said Timberlands was "budgeted R0 in 2024/25". The 2024/25 MTREF has no Timberlands line at all; the R0 came from a code collision with the overprinted Sunnyside/Townlands row. The conclusion (dropped) is unchanged.

### 9.9 Reading

**Location basis, (b):**

| Step | Black-ward share | R/resident ratio |
|---|---|---|
| 2024/25 adjusted (Moya's first adjustment) | {hl.loc[ORDER[5]].black_share:.1f}% | {hl.loc[ORDER[5]].percap_ratio:.2f} |
| 2025/26 original | {hl.loc[ORDER[6]].black_share:.1f}% | {hl.loc[ORDER[6]].percap_ratio:.2f} |
| 2025/26 adjusted | {hl.loc[ORDER[7]].black_share:.1f}% | {hl.loc[ORDER[7]].percap_ratio:.2f} |
| 2026/27 original | {hl.loc[ORDER[8]].black_share:.1f}% | {hl.loc[ORDER[8]].percap_ratio:.2f} |

- **Comparison with earlier budgets.** The 2025/26 and 2026/27 originals are above every Brink-era budget (2023/24 original {hl.loc[ORDER[2]].black_share:.1f}%, 2024/25 original {hl.loc[ORDER[4]].black_share:.1f}%). They are below the 2022/23 adjusted budget ({hl.loc[ORDER[1]].black_share:.1f}%), and the 2026/27 original is {"above" if hl.loc[ORDER[8]].black_share > hl.loc[ORDER[0]].black_share else "below"} the 2022/23 original ({hl.loc[ORDER[0]].black_share:.1f}%).
- **Service-area basis** gives the same up-down pattern at a higher level: {sv.loc[ORDER[5]].black_share:.1f}% → {sv.loc[ORDER[6]].black_share:.1f}% → {sv.loc[ORDER[7]].black_share:.1f}% → {sv.loc[ORDER[8]].black_share:.1f}%.
- **Per resident:** Black wards still receive less than other wards in every Moya-era budget on the location basis (ratio {min(lvr):.1f}–{max(lvr):.1f}). On the service-area basis the ratio is {min(svr):.1f}–{max(svr):.1f}.
- **The 2024/25 dip comes first.** The low point is Moya's first adjustment. Its biggest adverse moves (excluding bulk) are cuts or deferrals in Black wards plus increases in other wards: {drivers1}.
- **Within years, adjustments cut Black-ward shares.** Both Moya-era adjustment budgets lower the Black-ward share relative to that year's original ({hl.loc[ORDER[4]].black_share:.1f}% → {hl.loc[ORDER[5]].black_share:.1f}%; {hl.loc[ORDER[6]].black_share:.1f}% → {hl.loc[ORDER[7]].black_share:.1f}%). So the in-year pattern ActionSA described for Brink also appears under Moya.
- **Caveats that limit these comparisons:**
  1. From 2025/26 the wards are carried forward, not stated in the documents.
  2. New projects can only be placed by region (region-only share up to {comp[(comp.measure == ORDER[8]) & comp.category.str.startswith('(ii)')].pct.sum():.0f}% in 2026/27).
  3. There is no Moya-era actual spend below citywide level.
  4. Option B, which uses no ward information, is nearly flat. The larger ward-level swings rest on the City's own ward attributions.
"""


if __name__ == "__main__":
    print(section()[:3000])
