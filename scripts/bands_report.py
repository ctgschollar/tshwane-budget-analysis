"""Write the v2 summary.md (banded / threshold-free; service-area headline) + v2 CSV outputs.
The full binary_v1 write-up is appended verbatim as Appendix A (only heading levels shifted down one level)."""
import os
import re
import pandas as pd
import bands_engine as E
import bands_metrics as B
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

OUT = ROOT + "/output/"
V1 = OUT + "binary_v1/summary.md"
F = ",.1f"
COMBO_LABEL = {("A", "service", "b"): "Service area, (b) region money population-split — HEADLINE",
               ("A", "service", "a"): "Service area, (a) region money unattributed",
               ("A", "location", "b"): "Physical location, (b) population-split",
               ("A", "location", "a"): "Physical location, (a) unattributed",
               ("B", "region", "b"): "Option B (region tags only, population-split) — robustness"}


def col_label(c: str) -> str:
    m = B.META[c]
    return f"{c} [{m['adopted']}]"


def index_section(it: pd.DataFrame) -> str:
    out = []
    for k in B.COMBOS:
        d = it[(it.option == k[0]) & (it.basis == k[1]) & (it["mode"] == k[2])].set_index("column").reindex(B.ORDER)
        t = pd.DataFrame({"Column [adopted by]": [col_label(c) for c in d.index],
                          "Document / date": [B.META[c]["doc"] for c in d.index],
                          "Spend-weighted mean % Black African": d.spend_weighted.values,
                          "Population-weighted mean, same wards": d.pop_weighted_same_wards.values,
                          "Gap (spend − pop)": d.gap.values,
                          "Gap vs city (82.7%)": d.gap_vs_city.values,
                          "Wards receiving capex": d.wards_with_capex.values,
                          "Ward-attributed % of column": d.attributed_pct.values})
        budgets = t.iloc[:-1]
        actual = t.iloc[[-1]]
        out.append(f"#### {COMBO_LABEL[k]}\n\nBudgets:\n\n{budgets.to_markdown(index=False, floatfmt=F)}\n\n"
                   f"Actual spend (kept separate):\n\n{actual.to_markdown(index=False, floatfmt=F)}\n")
    return "\n".join(out)


def band_tables(bt: pd.DataFrame, k: tuple, scheme: str = "headline") -> str:
    d = bt[(bt.option == k[0]) & (bt.basis == k[1]) & (bt["mode"] == k[2]) & (bt.scheme == scheme)]
    bands = [b[0] for b in E.BANDS[scheme]]
    pv = lambda v: d.pivot_table(index="column", columns="band", values=v, sort=False).reindex(index=B.ORDER, columns=bands)
    popshare = d.drop_duplicates("band").set_index("band").reindex(bands)
    hdr = " | ".join(f"{b}: {int(popshare.loc[b, 'wards'])} wards, {popshare.loc[b, 'share_of_population']:.1f}% of residents" for b in bands)
    def fmt(t: pd.DataFrame, f: str) -> str:
        t = t.copy()
        t.index = [col_label(c) for c in t.index]
        return t.to_markdown(floatfmt=f)
    return (f"Bands: {hdr}\n\n*Rand per resident* (band capex ÷ band population, all wards in the band):\n\n{fmt(pv('R_per_resident'), ',.0f')}\n\n"
            f"*Share of attributed capex (%)*, to compare with the population shares above:\n\n{fmt(pv('share_of_attributed'), ',.1f')}\n\n"
            f"*Rand amount (R m)*:\n\n{fmt(pv('Rm'), ',.1f')}\n")


def dominance(bt: pd.DataFrame) -> str:
    d = bt[(bt.scheme.isin(["headline", "merged_40_80", "split_80_100"])) & bt.dominated & bt.option.eq("A") & bt["mode"].eq("b")]
    d = d.sort_values(["scheme", "basis", "band", "column"])
    t = d[["scheme", "basis", "column", "band", "Rm", "top_project", "top_project_share"]].rename(columns={
        "scheme": "Band scheme", "basis": "Basis", "column": "Column", "band": "Band", "Rm": "Band R m",
        "top_project": "Single project", "top_project_share": "Its share of band money %"})
    t["Single project"] = t["Single project"].str.slice(0, 70)
    counts = bt[bt.dominated].groupby(["scheme", "option", "basis", "mode"]).size().rename("cells").reset_index()
    return (f"Band cells (column × band) where **one project accounts for more than half of the band's money**, for Option A (b). "
            f"These band figures depend on a single project:\n\n{t.to_markdown(index=False, floatfmt=F)}\n\n"
            f"Number of such cells by scheme and basis (all combinations):\n\n{counts.to_markdown(index=False)}\n")


def drivers_section() -> tuple[str, pd.DataFrame]:
    parts, allrows, summ = [], [], []
    for c1, c2 in B.STEPS:
        m, info = B.drivers(c1, c2)
        lm, linfo = B.drivers(c1, c2, "A", "location", "b")
        summ.append({"Step": f"{c1} → {c2}", "Service index before": f"{info['I1']:.1f}", "after": f"{info['I2']:.1f}",
                     "Δ": f"{info['dI']:+.2f}", "Σ project effects": f"{info['sum_effects']:+.2f}",
                     "…of which relabelling": f"{info['sum_relabel']:+.2f}", "Location index Δ": f"{linfo['dI']:+.2f}",
                     "Name-crosswalk links": info["crosswalk_links"]})
        top = m.reindex(m.effect.abs().sort_values(ascending=False).index).head(10)
        rows = []
        for k, r in top.iterrows():
            nm = r.name_1 if isinstance(r.name_1, str) else r.name_2
            wl = r.wards_2 if isinstance(r.wards_2, str) else r.wards_1
            nw = len(str(wl).split(";")) if isinstance(wl, str) else 0
            wtxt = wl if nw <= 3 else f"{nw} wards (region split / township)"
            p1 = r.p_1 if pd.notna(r.p_1) else None
            p2 = r.p_2 if pd.notna(r.p_2) else None
            pp = p2 if p2 is not None else p1
            rows.append({"Project": str(nm)[:65], "Ward(s)": wtxt,
                         "Ward % Black (before → after)": f"{p1:.1f} → {p2:.1f}" if p1 is not None and p2 is not None else (f"{pp:.1f}" if pp is not None else "–"),
                         "Band": B.band_label(pp) if pp is not None else "–",
                         "R m before": f"{r.R_1 / 1e6:,.1f}", "R m after": f"{r.R_2 / 1e6:,.1f}",
                         "Effect on index (pts)": f"{r.effect:+.2f}", "…relabelling": f"{r.relabel_effect:+.2f}",
                         "Link": r.linked_by or ""})
            allrows.append(dict(step=f"{c1} → {c2}", project=nm, wards=wl, pct_before=p1, pct_after=p2,
                                band=B.band_label(pp) if pp is not None else "", R_before=r.R_1, R_after=r.R_2,
                                effect=r.effect, relabel=r.relabel_effect, link=r.linked_by))
        parts.append(f"**{c1} → {c2}**: service index {info['I1']:.1f} → {info['I2']:.1f} ({info['dI']:+.2f} pts).\n\n"
                     f"{pd.DataFrame(rows).to_markdown(index=False, disable_numparse=True)}\n")
    return (pd.DataFrame(summ).to_markdown(index=False, disable_numparse=True) + "\n\n" + "\n".join(parts)), pd.DataFrame(allrows)


def comparison(it: pd.DataFrame) -> str:
    out = []
    for k in (("A", "service", "b"), ("A", "location", "b")):
        rows, prev = [], None
        for c in E.BUDGET_COLS + ["2024/25 adjusted (App N, final)", "2024/25 actual"]:
            ix = it[(it.column == c) & (it.option == k[0]) & (it.basis == k[1]) & (it["mode"] == k[2])].iloc[0]
            bs = B.binary_share(c, *k)
            row = {"Column [adopted by]": col_label(c), "Binary ≥80% share %": bs, "Spend-weighted index": ix.spend_weighted,
                   "Gap (spend − pop)": ix.gap, "Δ binary": None, "Δ index": None, "Direction": ""}
            if prev is not None and c in E.BUDGET_COLS:
                db, di = bs - prev[0], ix.spend_weighted - prev[1]
                row.update({"Δ binary": db, "Δ index": di, "Direction": "agree" if (db > 0) == (di > 0) else "**DISAGREE**"})
            if c in E.BUDGET_COLS:
                prev = (bs, ix.spend_weighted)
            rows.append(row)
        t = pd.DataFrame(rows)
        out.append(f"**{COMBO_LABEL[k]}**\n\n{t.to_markdown(index=False, floatfmt='.1f')}\n")
    return "\n".join(out)


def appendix() -> str:
    v1 = open(V1).read()
    v1 = re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", v1, flags=re.M)
    return ("## Appendix A — binary (≥80% Black African) analysis, carried over unchanged from binary_v1\n\n"
            "The text below is `output/binary_v1/summary.md` reproduced verbatim; only heading levels are shifted down one level "
            "to nest it under this appendix. Section references inside it (§1–§9) refer to its own numbering. "
            "The original file, `projects.csv`, `projects_moya.csv` and `ward_classification.csv` are preserved read-only in "
            "`output/binary_v1/`; the scripts that produced them are in `scripts/binary_v1/`.\n\n" + v1)


def write() -> None:
    it = B.index_table()
    bt = B.all_bands()
    drv_md, drv = drivers_section()
    it.to_csv(OUT + "v2_index.csv", index=False)
    bt.to_csv(OUT + "v2_bands.csv", index=False)
    drv.to_csv(OUT + "v2_drivers.csv", index=False)
    # ward classification with bands (adds columns; binary columns kept)
    wc = pd.read_csv(OUT + "ward_classification.csv")
    wc["band_headline"] = wc.ward.map(lambda w: E.band_of(int(w), "headline"))
    wc["band_split_80_100"] = wc.ward.map(lambda w: E.band_of(int(w), "split_80_100"))
    wc["band_merged_40_80"] = wc.ward.map(lambda w: E.band_of(int(w), "merged_40_80"))
    wc.to_csv(OUT + "ward_classification.csv", index=False)

    S = lambda c, k=("A", "service", "b"): it[(it.column == c) & (it.option == k[0]) & (it.basis == k[1]) & (it["mode"] == k[2])].iloc[0]
    sv = {c: S(c) for c in B.ORDER}
    lo = {c: S(c, ("A", "location", "b")) for c in B.ORDER}
    ob = {c: S(c, ("B", "region", "b")) for c in B.ORDER}
    bands_counts = []
    for scheme in ("headline", "split_80_100", "merged_40_80"):
        for lab, lo_, hi in E.BANDS[scheme]:
            ws = [w for w in E.PCT if lo_ <= E.PCT[w] < hi]
            p = sum(E.POP[w] for w in ws)
            bands_counts.append({"Scheme": {"headline": "Headline (5 bands)", "split_80_100": "Sensitivity: 80–100 split",
                                            "merged_40_80": "Sensitivity: 40–80 merged"}[scheme], "Band": lab, "Wards": len(ws),
                                 "Population (2022)": round(p), "Share of residents %": p / E.TOTPOP * 100,
                                 "Ward range % Black": f"{min(E.PCT[w] for w in ws):.1f}–{max(E.PCT[w] for w in ws):.1f}",
                                 "Flag": "≤5 wards: thin" if len(ws) <= 5 else ""})
    bc = pd.DataFrame(bands_counts).to_markdown(index=False, floatfmt=",.1f")
    sb = bt[(bt.scheme == "headline") & (bt.option == "A") & (bt.basis == "service") & (bt["mode"] == "b")]
    rpr = sb.pivot_table(index="column", columns="band", values="R_per_resident", sort=False)
    top_lt_other = [c for c in E.BUDGET_COLS if rpr.loc[c, "80–100"] < rpr.loc[c].drop("80–100").mean()]
    n6080 = int((rpr.idxmax(axis=1) == "60–80").sum())

    def svs(c: str) -> str:
        return f"{sv[c].spend_weighted:.1f}% (gap {sv[c].gap_vs_city:+.1f})"

    txt = f"""# Tshwane capital spending by ward, 2022/23 – 2026/27: banded and threshold-free analysis (v2)

**What changed from binary_v1.** The headline no longer splits wards into "predominantly Black" (≥80% Black African) and "other". Every ward now carries its own % Black African (Stats SA 2022 ward estimates). Capex is reported in five bands of that percentage, and the headline measure is a **threshold-free index**: the spend-weighted mean % Black African of the wards that receive capital money, compared with the population-weighted mean of the same wards. The **service-area basis** is the headline throughout; physical location is secondary. All extraction, matching, ward and region attribution are unchanged from binary_v1. The engine reproduces every binary_v1 share exactly (checked), and the binary results are kept in full in **Appendix A**. A full list of changes is in §8.

## Plain-language finding

- **Service-area basis (headline): capex leans slightly towards Blacker wards in almost every budget.** The spend-weighted mean % Black African is above Tshwane's population-weighted 82.7% in every budget column except one, Moya's first adjustment budget (2024/25 adjusted: {svs('2024/25 adjusted (adj. budget)')}).
- **The index by budget:**

  | Budget | Adopted by | Spend-weighted index (gap vs city) |
  |---|---|---|
  | 2022/23 original | pre-Brink | {svs('2022/23 original')} |
  | 2022/23 adjusted | pre-Brink | {svs('2022/23 adjusted')} |
  | 2023/24 original | Brink | {svs('2023/24 original')} |
  | 2023/24 adjusted | Brink | {svs('2023/24 adjusted')} |
  | 2024/25 original | Brink | {svs('2024/25 original')} |
  | 2024/25 adjusted | Moya | {svs('2024/25 adjusted (adj. budget)')} |
  | 2025/26 original | Moya | {svs('2025/26 original')} |
  | 2025/26 adjusted | Moya | {svs('2025/26 adjusted')} |
  | 2026/27 original | Moya | {svs('2026/27 original')} |

  Final 2024/25 adjusted (App N): {svs('2024/25 adjusted (App N, final)')}. **2024/25 actual spend: {svs('2024/25 actual')}.**
- **The claim about Brink's first budgets.** On this measure, the first Brink budgets (2023/24) are essentially unchanged from the pre-Brink 2022/23 budgets: {sv['2023/24 original'].spend_weighted - sv['2022/23 original'].spend_weighted:+.1f} points original vs original, {sv['2023/24 adjusted'].spend_weighted - sv['2022/23 adjusted'].spend_weighted:+.1f} adjusted vs adjusted. The large 2023/24 fall in binary_v1 came mainly from the location basis (where the index also falls, by {lo['2023/24 original'].spend_weighted - lo['2022/23 adjusted'].spend_weighted:+.1f} points from the 2022/23 adjusted budget).
- **The fall comes later.** It appears in the Brink-era 2024/25 original budget ({sv['2023/24 adjusted'].spend_weighted:.1f} → {sv['2024/25 original'].spend_weighted:.1f}) and continues into Moya's first adjustment ({sv['2024/25 adjusted (adj. budget)'].spend_weighted:.1f}). Moya's 2025/26 and 2026/27 originals recover to {sv['2025/26 original'].spend_weighted:.1f} and {sv['2026/27 original'].spend_weighted:.1f}, but the 2025/26 adjustment again pulls the index down ({sv['2025/26 adjusted'].spend_weighted:.1f}).
- **Physical-location basis (secondary): the picture differs, mainly because of where bulk plants sit.** The index drops from {lo['2022/23 adjusted'].spend_weighted:.1f} (2022/23 adjusted) to {lo['2023/24 original'].spend_weighted:.1f} (2023/24 original). Capex leans *away* from Blacker wards relative to population (gap {lo['2023/24 original'].gap_vs_city:+.1f} to {lo['2024/25 adjusted (adj. budget)'].gap_vs_city:+.1f}) until the 2026/27 original ({lo['2026/27 original'].gap_vs_city:+.1f}).
- **Region-level robustness check (Option B):** essentially flat ({min(ob[c].spend_weighted for c in B.ORDER):.1f}–{max(ob[c].spend_weighted for c in B.ORDER):.1f}), so region tags alone can't detect these shifts.
- **Overall reading.** The banded and index results do **not** support a specific "Brink neglected Black areas" story on the service-area basis. They show a dip spanning the 2024/25 Brink budget and Moya's first adjustment, and a recovery in Moya's later original budgets. In-year adjustments go both ways: the pre-Brink 2022/23 and Brink 2023/24 adjustments raised the index ({sv['2022/23 adjusted'].spend_weighted - sv['2022/23 original'].spend_weighted:+.1f}, {sv['2023/24 adjusted'].spend_weighted - sv['2023/24 original'].spend_weighted:+.1f}). Both Moya-era adjustments lowered it ({sv['2024/25 adjusted (adj. budget)'].spend_weighted - sv['2024/25 original'].spend_weighted:+.1f}, {sv['2025/26 adjusted'].spend_weighted - sv['2025/26 original'].spend_weighted:+.1f}).
- **Coverage limits all of this.** Only {min(sv[c].attributed_pct for c in E.BUDGET_COLS):.0f}–{max(sv[c].attributed_pct for c in E.BUDGET_COLS):.0f}% of each budget can be attributed to wards on the service-area basis. From 2025/26 wards are carried forward, not stated in the documents, and there is no ward-level actual spend after 2024/25.

## 1. Method

- **Ward % Black African:** Stats SA Ward-level Small Area Population Estimates 2022 (MDB 2020 wards; see Appendix A §3). Unchanged.
- **Attribution:** unchanged from binary_v1 (Appendix A §2, §8, §9).
  - **Service area:** bulk infrastructure goes to the area a document states it serves (Appendix A §8.2), and is unattributed if none is stated. All other projects use their Appendix O ward. From 2025/26 that ward is carried forward, flagged, or the City's Regions column is used.
  - **Physical location:** every project uses its Appendix O ward.
  - **(a):** region-only money is unattributed.
  - **(b):** region-only money is split across the region's wards by population. **This assumes each resident benefits equally.**
  - **Multi-ward projects** remain unattributed, as in binary_v1.
- **Index:**
  - spend-weighted mean = Σ(capex in ward × ward %Black) ÷ Σ(capex), over ward-attributed capex;
  - population-weighted mean = Σ(pop × %Black) ÷ Σ(pop), over the **same wards** (those receiving any attributed capex).

  A positive gap means capex leans towards Blacker wards. Under (b), region splits reach every ward of a region, so from 2023/24 the "same wards" set is usually all 107 wards and the comparison mean is the city's 82.7%. The "gap vs city" column is shown throughout for that reason.
- **Rand per resident by band** = band capex ÷ the band's 2022 population (all wards in the band, whether or not they receive capex).
- **Columns** are labelled with the administration that adopted the budget and the document or date (§3 tables). The 2024/25 actual spend is reported separately and spans both administrations: about 3 months Brink and 9 months Moya, on the tenure dates in the brief. "2024/25 adjusted (App N, final)" is the annual report's final adjusted budget; "2024/25 adjusted (adj. budget)" is the mid-year adjustments budget (Moya-era Council).

## 2. Bands

{bc}

Band edges are half-open [lo, hi). Wards 91 (39.95%) and 41 (39.77%) sit just below the 40% cut, which is kept as specified. The 60–80 and 80–90 bands each have exactly 5 wards: treat their figures as thin, and see the single-project flags in §4.4.

## 3. Threshold-free index (headline)

{index_section(it)}

## 4. Results by band

### 4.1 Service area, (b) — headline

{band_tables(bt, ('A', 'service', 'b'))}

Rand per resident in the 80–100 band is below the average of the other four bands in {len(top_lt_other)} of {len(E.BUDGET_COLS)} budget columns: {', '.join(top_lt_other) if top_lt_other else 'none'}. The 60–80 band (5 wards) has the highest rand per resident in {n6080} of {len(B.ORDER)} columns. That reflects a small number of large projects (see §4.4), not a broad pattern.

### 4.2 Service area, (a)

{band_tables(bt, ('A', 'service', 'a'))}

### 4.3 Physical location (secondary), (b) and (a)

**(b)**

{band_tables(bt, ('A', 'location', 'b'))}

**(a)**

{band_tables(bt, ('A', 'location', 'a'))}

**Option B (region tags only) — robustness**

{band_tables(bt, ('B', 'region', 'b'))}

### 4.4 Sensitivity bands and single-project dependence

**80–100 split into 80–90 (5 wards, thin) and 90–100 (64 wards), service area (b):**

{band_tables(bt, ('A', 'service', 'b'), 'split_80_100')}

**Merged 40–80 "mixed" band (11 wards), service area (b):**

{band_tables(bt, ('A', 'service', 'b'), 'merged_40_80')}

**80–100 split and 40–80 merged, physical location (b):**

{band_tables(bt, ('A', 'location', 'b'), 'split_80_100')}

{band_tables(bt, ('A', 'location', 'b'), 'merged_40_80')}

{dominance(bt)}

## 5. What drove each step (service area, (b), in index terms)

For each step, each project's **effect on the index** is the change in the after-step index if that project alone had stayed at its before-step amount and wards. The **relabelling** part is the effect of a change in the project's ward %Black (ward attribution changed between years) at its after-step amount. Effects don't add exactly to the index change: when total attributed capex changes a lot, the counterfactuals interact.
- **Projects are linked** by WBS code without the funding segment (binary_v1 §7, §9.2), plus the documented manual links.
- **2022/23 → 2023/24:** the WBS coding scheme changed, so projects are linked by unique exact normalised-name matches ("name crosswalk").
- **From 2025/26** relabelling is zero by construction, because carried-forward wards don't change.
- **Location-basis** index changes are shown for comparison.

{drv_md}

## 6. Binary ≥80% share vs threshold-free index

{comparison(it)}

Disagreements in direction (one per basis):
- **Service area, 2022/23 original → adjusted.** The binary share barely moves (84.4 → 84.2) while the index rises by 1.3. Attributed capex moved out of the 0–20 band (4.2% → 1.4% of attributed capex) into the 60–80 band (4.1% → 6.4%). Both bands are below the 80% cut, so the binary measure can't see the shift; the index can.
- **Physical location, 2023/24 original → adjusted.** The binary share falls (61.5 → 59.2) while the index rises by 0.6. The 0–20 band fell (8.3% → 6.0%) and the 60–80 band rose (7.0% → 10.7%), while the ≥80% bands fell slightly (61.6% → 59.2%).

Every other step agrees in direction. On the location basis the binary measure moves further than the index in 6 of 7 agreeing steps (by 1.3–2.4×); the exception is 2023/24 adjusted → 2024/25 original (binary −2.1, index −3.2). On the service basis the sizes are similar (the index moves further in 3 of 7 agreeing steps). The difference arises because the binary measure counts a ward at 81% the same as one at 99%, and ignores shifts between bands below 80%.

## 7. Data, sources and limitations

- **Sources, unchanged from binary_v1:** extraction, reconciliation (100% coverage except the 2025/26 adjustment budget at 99.5%), matching decisions, name overrides, ward→region table, beneficiary statements, Moya-era carry-forward and its checks. See Appendix A §2, §6, §8, §9. Every rand figure traces to a page through `projects.csv` and `projects_moya.csv`.
- **Coverage of the index:** it covers only ward-attributed capex — {min(sv[c].attributed_pct for c in E.BUDGET_COLS):.0f}–{max(sv[c].attributed_pct for c in E.BUDGET_COLS):.0f}% of each budget on the service-area basis (b), and {min(lo[c].attributed_pct for c in E.BUDGET_COLS):.0f}–{max(lo[c].attributed_pct for c in E.BUDGET_COLS):.0f}% on the location basis (b).
- **Labelled assumptions:**
  1. Ward %Black is from 2022 estimates, applied to all years.
  2. Region-only money under (b) benefits every resident of the region equally.
  3. Wards are carried forward from 2025/26 (inferred, not stated).
  4. Bulk infrastructure counts only where a document names its beneficiary.
  5. Multi-ward projects are left out of the index and bands.
- **Not in the folder:** no ward-level actual spend after 2024/25, and no region-level in-year actuals.

## 8. What changed versus binary_v1

1. **Headline measure:** from the binary ≥80% share to the spend- vs population-weighted mean % Black African, plus five bands. The binary results are unchanged and in Appendix A.
2. **Basis order:** the service-area basis is now the headline; physical location is secondary. In binary_v1 location was the primary basis.
3. **Columns:** the series now includes the final 2024/25 adjusted budget (App N) as a labelled column, and keeps the 2024/25 actual separate. Every column is labelled with the adopting administration and document date.
4. **Drivers:** the driver analysis now covers every step from 2022/23 to 2026/27, in index terms, with each mover's ward % Black and band. binary_v1 covered 2023/24 → 2024/25 and the Moya steps, with Black/other labels. The 2022/23 → 2023/24 step needed a new name crosswalk because the WBS coding scheme changed.
5. **New sensitivities:** 80–100 split into 80–90 and 90–100; 40–80 merged; single-project dominance flags.
6. **New outputs:** `v2_index.csv`, `v2_bands.csv`, `v2_drivers.csv`, and band columns added to `ward_classification.csv` (binary columns kept). `projects.csv` and `projects_moya.csv` are unchanged.
7. **New scripts:** `bands_engine.py`, `bands_metrics.py`, `bands_report.py`. All binary_v1 scripts are unchanged; binary_v1 is preserved read-only in `output/binary_v1/` and `scripts/binary_v1/`.

{appendix()}
"""
    txt = re.sub(r"(?<=\|)(\s*)nan(\s*)(?=\|)", r"\1–\2", txt)
    open(OUT + "summary.md", "w").write(txt)
    print("written", len(txt))


if __name__ == "__main__":
    write()
