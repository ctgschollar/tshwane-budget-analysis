"""Write output/summary.md from work/summary_data.pkl (figures) + fixed narrative."""
import pandas as pd
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

OUT = ROOT + "/output/summary.md"
D = pd.read_pickle("work/summary_data.pkl")
F = ",.1f"


def t(df: pd.DataFrame, **kw) -> str:
    return df.to_markdown(floatfmt=F, **kw)


prim = D["prim"].set_index("measure")
cov = D["cov"].set_index("measure")
sh = D["sh"]
twn, n_tw, n_ee, tw_pop = D["twn"]
twn = twn.set_index("measure")

p_tbl = pd.DataFrame({
    "Total capex (R m)": prim.total_Rm,
    "Single-ward attributable (R m)": prim.black_Rm + prim.other_Rm,
    "…as % of total": prim.attributable_pct_of_total,
    "Predominantly Black wards (R m)": prim.black_Rm,
    "Other wards (R m)": prim.other_Rm,
    "Black-ward share of attributable (%)": prim.black_share_of_attributable,
    "R per resident – Black wards": prim.black_R_per_capita,
    "R per resident – other wards": prim.other_R_per_capita,
    "Per-capita ratio Black:other": prim.percap_ratio_black_to_other,
})
cov_tbl = pd.DataFrame({
    "Total (R m)": cov.total_Rm,
    "Single ward": cov["single-ward_Rm"], "%": cov["single-ward_pct"],
    "Multi-ward": cov["multi-ward_Rm"], "% ": cov["multi-ward_pct"],
    "City-wide": cov["city-wide_Rm"], "%  ": cov["city-wide_pct"],
    "Admin HQ": cov["administrative-hq_Rm"], "%   ": cov["administrative-hq_pct"],
    "'No Intersect'": cov["no-intersect_Rm"], "%    ": cov["no-intersect_pct"],
    "Unmatched": cov["unmatched_Rm"], "%     ": cov["unmatched_pct"],
})
sens = D["sens_tbl"]
pc = D["pc_tbl"]
dom = D["dom"]
sr = D["sr"].rename(columns={"adjusted_budget": "Adjusted budget (R m)", "actual_spend": "Actual (R m)", "spend_rate_pct": "Spend rate %"})
srd = D["srd"].rename(columns={"adjusted_budget": "Adjusted budget (R m)", "actual_spend": "Actual (R m)", "spend_rate_pct": "Spend rate %"})
sh_tbl = sh.rename(columns={"original_Rm": "Original (R m)", "adjusted_Rm": "Adjusted (R m)", "change_Rm": "Change (R m)",
                            "adjusted_as_pct_of_original": "Adjusted as % of original"})
tw_tbl = pd.DataFrame({"Named-township wards (R m)": twn.township_Rm, "Other wards (R m)": twn.other_Rm,
                       "Eersterust ward 43 (R m)": twn.eersterust_Rm, "Township share of attributable (%)": twn.township_share,
                       "R/resident township wards": twn.township_R_pc, "R/resident other wards": twn.other_R_pc,
                       "Ratio": twn.township_R_pc / twn.other_R_pc})


def top_md() -> str:
    out = []
    for (lab, g), df in D["top"].items():
        d = df.copy()
        for c in ("original_budget", "adjusted_budget", "actual_spend"):
            d[c] = d[c] / 1e6
        d = d.rename(columns={"project_name": "Project", "wards": "Ward(s) (App O)", "original_budget": "Original R m",
                              "adjusted_budget": "Adjusted R m", "actual_spend": "Actual R m", "page": "Source page"})
        if lab.startswith("2024/25"):
            d = d.drop(columns=["Original R m"])
        else:
            d = d.drop(columns=["Actual R m"])
        out.append(f"**{lab} — {'predominantly Black wards' if g == 'Black' else 'other wards'}**\n\n" + d.to_markdown(index=False, floatfmt=F))
    return "\n\n".join(out)


S = f"""# Tshwane capital spending by ward, 2022/23 – 2024/25

**Question tested:** did the share of capital budget and actual capital spend going to predominantly Black wards fall, hold or rise from 2022/23 to 2023/24 to 2024/25, i.e. is there evidence that the DA-led administration under Mayor Cilliers Brink (Mar 2023 – Sep 2024, dates as given in the brief) neglected predominantly Black areas?

## Plain-language finding

On the primary measure, the predominantly Black wards' share of ward-attributable capital budget **fell** between the last pre-Brink budget (2022/23: {prim.black_share_of_attributable.iloc[0]:.1f}% of original, {prim.black_share_of_attributable.iloc[1]:.1f}% of adjusted) and the first Brink budget (2023/24: {prim.black_share_of_attributable.iloc[2]:.1f}% / {prim.black_share_of_attributable.iloc[3]:.1f}%), and fell again in the 2024/25 original budget ({prim.black_share_of_attributable.iloc[4]:.1f}%), before partly recovering in the 2024/25 adjusted budget and actual spend ({prim.black_share_of_attributable.iloc[5]:.1f}% / {prim.black_share_of_attributable.iloc[6]:.1f}%), which were mostly executed after the end of the tenure dates given. In rand terms, single-ward budget in predominantly Black wards fell from R{prim.black_Rm.iloc[0]:,.0f}m to R{prim.black_Rm.iloc[2]:,.0f}m (original), while other wards held at about R{prim.other_Rm.iloc[2]:,.0f}m; per resident, Black wards went from {prim.percap_ratio_black_to_other.iloc[0]:.1f}× to {prim.percap_ratio_black_to_other.iloc[2]:.1f}× what other wards received. The direction of that fall survives every threshold (50/80/90%), the Census 2011 classification and the named-township definition. **But the numbers cannot resolve the "neglect" claim**, for three reasons: (1) only about half of each year's capital budget can be tied to a single ward (well under the 80% you asked me to flag); (2) the 2022/23 → 2023/24 fall disappears when bulk infrastructure is excluded (Black-ward share of original budget {sens.iloc[6, 0]:.1f}% → {sens.iloc[6, 2]:.1f}%). That step is driven by where large plants sit, chiefly the Rooiwal wastewater works in ward 96 (47.5% Black African), whose upgrade the City's own 2024/25 annual report (p94) describes as addressing Hammanskraal's water crisis. A fall does survive the bulk exclusion one year later, in the Brink-era 2024/25 original budget ({sens.iloc[6, 4]:.1f}%; {sens.iloc[6, 6]:.1f}% of actual spend), so that budget is the strongest evidence for the claim; and (3) there is no ward-level actual spend for 2022/23 or 2023/24, so the only spend-rate test is 2024/25, which shows no meaningful gap (Black wards {D['sr'].loc['Black', 'spend_rate_pct']:.1f}% vs other {D['sr'].loc['Other', 'spend_rate_pct']:.1f}%). The in-year reprioritisation data for 2023/24 points the way ActionSA claims but is small (Black-ward projects cut R{-sh.iloc[4]['change_Rm']:.1f}m or {100 - sh.iloc[4]['adjusted_as_pct_of_original']:.1f}%, other wards R{-sh.iloc[5]['change_Rm']:.1f}m or {100 - sh.iloc[5]['adjusted_as_pct_of_original']:.1f}%). Net: the data are *consistent with* a reduced allocation to Black wards in Brink-era budgets on location-of-project measures, but not robust evidence of neglect.

**Update after the two follow-ups (§7–§8).**
- **The 2024/25 drop** in the Black-ward share excluding bulk infrastructure (84.6% → 68.2%, corrected) is moderately concentrated: the top 5 projects account for about half of the adverse movement. About 11 of the 16 points come from real budget changes, mainly Thorntree View roads cut from R90.2m to R1.0m, Electricity Distribution Loss from R68m to R20m, and the Zithobeni X8 sewer and Timberlands housing dropped. The remaining 5 points come from Appendix O moving the water-pipe programmes from a Black ward to other wards.
- **Bulk infrastructure by documented service area:** where the City's reports name a beneficiary, Rooiwal goes to Temba and Hammanskraal, and Klipgat, Bronkhorstbaai, Parkmore and Wildebees go to their stated regions. On that basis the 2022/23 → 2023/24 fall disappears (84.4% → 83.0% of original budget, region-only money population-split). The 2024/25 fall remains (76.2% original, 74.9% actual), and Black wards still receive about as much per resident as other wards in 2024/25 (ratio ≈1.0, against 1.6–1.8 in the earlier years). The caveat is that this basis attributes less than half of the budget.

**Moya administration (§9).** On the same methods, the Black-ward share (location basis, region money population-split) runs:
- 53.7% in Moya's first adjustment budget (2024/25);
- 69.4% in the 2025/26 original and 63.5% in the 2025/26 adjusted;
- 72.1% in the 2026/27 original.

The 2025/26 and 2026/27 originals are above every Brink-era budget but not above 2022/23. Rand per resident in Black wards is still below other wards (ratio 0.4–0.8). Both Moya adjustment budgets cut the Black-ward share within the year. There is no ward-level actual spend after 2024/25, and from 2025/26 wards are carried forward from earlier years. The region-level robustness series (Option B) is nearly flat (73–78%). None of the four 2024/25 cuts was restored in full: Electricity Distribution Loss got R47m in the 2025/26 adjusted budget, partly restored against R68m in 2023/24. No document says Thorntree View was completed; a 2025/26 procurement plan schedules "completion and remedial works" of 2.2km of its stormwater channel.

## 1. Sources, and what each year can support

| Year | Original budget (project level) | Adjusted budget (project level) | Actual spend (project level) | Ward link |
|---|---|---|---|---|
| 2022/23 | 2022/23 Adjustment Budget, Annexure B pp141–148 ("Current Budget") | same, "Adjusted Budget" | **not available** (AR 2022/23 App N pp379–384 is asset-class only) | AR 2022/23 App O pp385–393 (ward lists, no rands) — joined by project name/code |
| 2023/24 | 2023/24 Adjustments Budget, Annexure B pp132–138 | same | **not available** (AR 2023/24 App N pp401–404 is asset-class only, and its "actual" column mostly repeats the adjusted budget) | AR 2023/24 App O pp405–411 — joined by name |
| 2024/25 | 2024/25 MTREF, Annexure A pp58–65 | AR 2024/25 App N pp503–515 | AR 2024/25 App N pp503–515 | AR 2024/25 App O pp516–525 — joined by name; App N's own "dominant ward" used as a check |

Region tags (Census-free cross-check) come from MBRR SA36/SB19 tables: 2022/23 MTREF pp199–234, 2022/23 adjustments budget pp100–104, 2023/24 MTREF pp181–188, 2023/24 adjustments budget pp90–93, 2024/25 MTREF pp205–216. Despite the column name "Ward Location", these only carry regions.

Budget timing, from the documents: 2022/23 MTREF approved 26 May 2022 (2022/23 adj. budget p51); 2022/23 adjustments budget prepared before the 2–3 March 2023 Treasury engagement it refers to (p52); 2023/24 MTREF approved 31 May 2023 (2023/24 adj. budget p48); 2024/25 MTREF "will be tabled for approval by Council in May 2024" (2024/25 MTREF p76). The date of the 2024/25 adjustments budget is not in these documents. On the tenure dates in the brief, 2022/23 is the pre-Brink baseline, 2023/24 and the 2024/25 original budget are Brink-era, and roughly 3 of the 12 months of 2024/25 spending fall within the tenure.

## 2. Reconciliation and coverage

**Extraction is complete** — every project table reconciles to the rand with the stated total in the same document:

| Measure | Extracted total | Stated total | Where stated | Coverage |
|---|---|---|---|---|
| 2022/23 original | R2,793,105,151 | R2,793,105,151 | 2022/23 adj. budget Annexure B p148; AR 2022/23 App N p384 | 100% |
| 2022/23 adjusted | R2,816,190,045 | R2,816,190,047 | same | 100% (R2 rounding) |
| 2023/24 original | R2,347,686,908 | R2,347,686,908 | 2023/24 adj. budget Annexure B p138; AR 2023/24 App N p404 | 100% |
| 2023/24 adjusted | R2,112,614,368 | R2,112,614,368 | same | 100% |
| 2024/25 original | R2,347,552,577 | R2,347,552,576 | 2024/25 MTREF Annexure A p65 | 100% |
| 2024/25 adjusted | R2,340,123,792 | R2,340,123,791 | AR 2024/25 App N p515 | 100% |
| 2024/25 actual | R2,300,073,485 | R2,300,073,481 | AR 2024/25 App N p515 | 100% |

Not extractable at ward level (asset-class totals only): 2022/23 actual R2,227,704,869 (AR 2022/23 p384); 2023/24 actual R2,127,678,733.67 (AR 2023/24 p404).

**⚠️ WARD-ATTRIBUTABLE COVERAGE IS LOW: ONLY 49–60% OF EACH YEAR'S CAPITAL BUDGET CAN BE TIED TO A SINGLE WARD.** The rest is multi-ward, city-wide, administrative HQ, "No Intersect" in the source, or could not be matched to Appendix O. Every share below is a share of that single-ward slice.

Rand value and share of total by ward category (R m, % of measure total):

{t(cov_tbl)}

Multi-ward, city-wide and Administrative HQ projects are kept as their own categories and not split across wards.

## 3. Year-by-year shares — primary definition (Black African ≥ 80% of ward population)

Ward populations: Stats SA Ward-level Small Area Population Estimates 2022 (Nov 2025), on MDB 2020 wards. 69 of 107 wards are ≥ 80% Black African and hold 75.4% of residents (3.05m of 4.04m).

{t(p_tbl)}

### Sensitivity — Black-ward share of single-ward-attributable capex (%)

{t(sens)}

Per-capita ratio (R per resident in Black wards ÷ R per resident in other wards):

{t(pc)}

2024/25 using Appendix N's own "dominant ward" instead of Appendix O: Black-ward share {dom.black_share_of_attributable.iloc[0]:.1f}% of adjusted and {dom.black_share_of_attributable.iloc[1]:.1f}% of actual; per-capita ratio {dom.percap_ratio_black_to_other.iloc[0]:.1f} / {dom.percap_ratio_black_to_other.iloc[1]:.1f}. This method attributes {dom.attributable_pct_of_total.iloc[0]:.1f}% of the budget to single wards, because it assigns every project one ward.

### Secondary definition — wards covering named townships

A ward counts as a township ward if at least 50% of its 2011 population lived in one of the named townships' official Stats SA Census 2011 Main Places. Eersterust is reported separately. Boundaries come from Census 2011 Sub Places (UCT_Geodata mirror of the Stats SA layer), intersected with MDB 2020 wards; populations are Census 2011 sub-place counts split by area. This gives {n_tw} township wards with {tw_pop/1e6:.2f}m residents (2022 estimates), and Eersterust is ward 43.

{t(tw_tbl)}

Caveats on this mapping. "Hammanskraal" is the narrow official Main Place (Rens Town and Kanana); Majaneng, Suurman, Stinkwater and New Eersterus are separate Main Places and are not grouped in. Main Places include some non-residential sub-places (Medunsa, Ekandustria, Tswaing). Boundaries are from 2011. On this definition the township share falls from 2022/23 to 2023/24 by less than on the primary definition, and recovers in 2024/25.

## 4. Spend rate and in-year reprioritisation (ActionSA's claim)

**Spend rate (actual ÷ adjusted budget) is available for 2024/25 only.**

Ward from Appendix O:

{t(sr)}

Ward from Appendix N's "dominant ward":

{t(srd)}

At ≥50% the rates are Black 96.8% vs other 97.4%; at ≥90% they are 95.8% vs 98.2%. There is no meaningful under-spend in Black wards relative to other wards in 2024/25.

**Original → adjusted budget, by ward group (≥80%)** — tests whether money was moved away during the year.

{t(sh_tbl, index=False)}

The 2022/23 and 2023/24 rows compare the same project rows (Annexure B). The 2024/25 row compares two different sources: the MTREF Annexure A original budget against Appendix N's adjusted budget, each matched to wards separately. The unmatched share also differs (14.1% vs 2.0%), so treat the 2024/25 shift as indicative only.

## 5. Top 10 projects by value, by group (≥80% definition, ward from Appendix O)

The Rooiwal rows show the location issue: the plant is in ward 96 ("other"), but AR 2024/25 p94 says its refurbishment addresses Hammanskraal's water problems.

{top_md()}

## 6. Data gaps, assumptions and judgement calls

1. **No ward-level actual spend before 2024/25.** The 2022/23 and 2023/24 annual reports give actuals by asset class only. The 2023/24 "actual" column repeats the adjusted budget in most rows (AR 2023/24 pp401–404), so it looks copied rather than measured.
2. **Ward attribution comes from Appendix O, which has no rand values.** Budget rows were joined to Appendix O by fuzzy project-name matching, plus project-code agreement where both sides carry codes (2022/23 and 2024/25). Rules:
   - Auto-accept at a score of 95 or more.
   - Auto-reject where service, place, extension, area or section conflict, or the score is below 65.
   - Hand-review everything else. Every decision and its reason is recorded (`match_status`, `match_reason` in projects.csv).
   - Unmatched rows are reported, not guessed. They are 8.6%, 11.5% and 14.1% of the original budget in the three years. The largest each year is Housing Company Tshwane's "Chantelle detail design and bulk infrastructure upgrade", which has no Appendix O row.
3. **Appendix O ward assignments are the City's, taken as published.** They are sometimes inconsistent across years:
   - Thorntree View roads are in ward 90 in 2022/23 and ward 36 in 2023/24.
   - The "Critical Worn-Out Water Pipes" areas, which by name span several regions, are all put in ward 100 in 2023/24, and in wards 96, 53 and 100 in 2024/25.
   - From 2023/24 some projects are labelled "No Intersect" that had a ward in 2022/23. Sensitivity rows test both issues.
4. **Overprinted text in the PDFs.** 18 project names were printed on top of each other in the source. They were decoded from WBS codes and recorded in `name_note`. One (Sunnyside/Townlands, 2023/24, R20m adjusted) is genuinely ambiguous and left unmatched.
5. **Rows used.** Where a programme row has sub-project rows, the sub-projects are used when they sum exactly to the parent. In one case (SAP4 Hana, 2023/24) the source leaves the sub-project's adjusted figure blank, so the parent row is used.
6. **Population data.**
   - The 2022 ward populations are Stats SA small-area estimates (Census 2011 ward structure benchmarked to Census 2022 municipal totals), not raw counts; for about 3% of wards nationally they are modelled values.
   - Values are fractional as published, and "Other" includes "Unspecified".
   - Census 2011 shares on the same 2020 wards (MDB WardProfile2021 layer) are used as a sensitivity check. That layer has no metadata; its total matches Census 2011.
   - Both use the 2020/2021 ward boundaries the reports use, so no boundary crosswalk was needed.
7. **"Bulk infrastructure" flag.** This is a name-based sensitivity flag (substation, infeed, WWTW, power line, reservoir, bulk, canal, feeder, outfall, purification), not an official classification.
8. **Per-capita figures** divide a group's single-ward rands by that group's total 2022 population. Multi-ward, city-wide and HQ spending is excluded from both groups.
9. **Region tags** come from SA36/SB19 by exact WBS code. They cover about 78–90% of rands and are descriptive only; regions were not classified by population group.
10. **Draft 2024/25 MTREF** (12.1 Item 12 annexures) was not used; the final 2024/25 MTREF supersedes it.
11. **Revision after follow-up review.** The 2024/25 MTREF row "Replacement of obsolete of meter test bench ( Electricity Distribution Loss)" (IDP 714008, R20.0m) was originally rejected as a ward match. It is now matched to Appendix O "Electricity Distribution Loss" (ward 29): the name is in brackets and the project code agrees. This raises the 2024/25 original-budget Black-ward share from 55.1% to 55.9%. All tables above use the corrected figure.

## Files

- `projects.csv`: one row per project per source table. Columns: year, source file and page, names, department, WBS code, wards (as published and parsed), ward category, ward source and page, region and its source, original, adjusted and actual amounts, match status, score and reason, name notes, and the scope and bulk flags.
- `ward_classification.csv`: all 107 wards. Population and Black African share (2022), classification at 50, 80 and 90%, the 2011 share and class, township flags (population-based) and data sources.
"""
import part1_decompose as P1
import part2_report as P2
import moya_report as P3
S += "\n" + P1.markdown_section() + "\n" + P2.markdown_section() + "\n" + P3.section()
import re as _re
S = _re.sub(r"(?<=\|)(\s*)nan(\s*)(?=\|)", r"\1–\2", S)   # empty table cells
open(OUT, "w").write(S)
import moya_analysis as _MA
_MA.write_projects_moya()
print("written", len(S))
