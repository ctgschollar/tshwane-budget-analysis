"""Follow-up 1: decompose the 2023/24 -> 2024/25 change in Black-ward share of ORIGINAL budget, excluding bulk-infrastructure rows.
Projects are linked across years by exact WBS code (both years use the new coding mask); unlinked rows fall back to
normalised-name matching (flagged). Each year's row keeps its own ward (Appendix O of that year)."""
import pandas as pd
import analyze as A
from match import norm, score

T = 80


# Manual cross-year links for projects re-coded between the 2023/24 adjustments budget and the 2024/25 MTREF.
# key = 2024/25 WBS, value = (2023/24 linking key, evidence)
RECODED = {
    "9.801645.1.S.DL.05.W": ("9.801638.1.E.LO.1", "2024/25 MTREF Annexure A line 'Replacement of obsolete of meter test bench ( Electricity Distribution Loss)', IDP 714008 = 2023/24 Electricity Distribution Loss"),
    "9.804713.1.W.EK.05.7": ("9.804721.1.S.SE.7", "identical name 'Ekangala Block A - F sewer reticulation and toilets' under a new WBS"),
    "9.803352.1.W.PH.22.6": ("9.803332.1.W.MA.6", "same erf (Mamelodi X6 erf 34041, Phomolong) water; 2024/25 row is 'Phase 2'"),
    "9.803352.1.S.SR.22.6": ("9.803352.1.S.MA.6", "same erf (Mamelodi X6 erf 34041, Phomolong) sewer; 2024/25 row is 'Phase 2'"),
}


def prep(year: str) -> pd.DataFrame:
    b = A.p[(A.p.year == year) & A.p.record_type.str.startswith("budget")].copy()
    b["g"] = b.apply(lambda r: A.group(r, T, A.pct22, excl_bulk=True), axis=1)
    def k(r: pd.Series) -> str:
        w = r.wbs if isinstance(r.wbs, str) and r.wbs else ""
        if not w:
            return "NAME:" + norm(r.project_name)
        parts = w.split(".")
        # drop the funding-source segment (6th of the new coding mask) so funding switches don't break the link
        return ".".join(parts[:5] + parts[6:]) if len(parts) >= 7 else w
    b["key"] = b.apply(k, axis=1)
    if year == "2024/25":
        for w, (key, _) in RECODED.items():
            b.loc[b.wbs == w, "key"] = key
    return b


def link() -> pd.DataFrame:
    x, y = prep("2023/24"), prep("2024/25")
    # aggregate duplicates per key
    for d in (x, y):
        d["B"] = d.original_budget.where(d.g == "Black", 0.0)
        d["O"] = d.original_budget.where(d.g == "Other", 0.0)
        d["gl"] = d.g
    agg = lambda d: d.groupby("key").agg(name=("project_name", "first"), dept=("department", "first"),
                                         g=("gl", lambda s: "/".join(sorted(set(s)))), wards=("wards", "first"),
                                         val=("original_budget", "sum"), B=("B", "sum"), O=("O", "sum"), page=("page", "first"))
    X, Y = agg(x), agg(y)
    # name fallback: keys present in one year only -> try exact normalised-name match
    xn = {norm(n): k for k, n in X.name.items()}
    remap = {}
    for k, n in Y.name.items():
        if k not in X.index and norm(n) in xn and xn[norm(n)] not in Y.index:
            remap[k] = xn[norm(n)]
    Y = Y.rename(index=remap)
    manual = {v[0] for v in RECODED.values()}
    # a shared code is only a link if the names also agree (codes are occasionally reused for a different project)
    manual = {v[0] for v in RECODED.values()}
    clash = [k for k in Y.index if k in X.index and k not in manual and score(norm(X.at[k, "name"]), norm(Y.at[k, "name"])) < 60]
    Y = Y.rename(index={k: k + "|2425-different-project" for k in clash})
    Y["link"] = ["name" if k in remap.values() else ("manual re-coding link" if k in manual else "") for k in Y.index]
    m = X.join(Y, how="outer", lsuffix="_2324", rsuffix="_2425")
    m["link"] = m.link.fillna("").replace("", "wbs")
    m.loc[m.val_2324.isna() | m.val_2425.isna(), "link"] = "one year only"
    for s in ("_2324", "_2425"):
        m["val" + s] = m["val" + s].fillna(0.0)
        m["g" + s] = m["g" + s].fillna("absent")
    for s_ in ("_2324", "_2425"):
        m["B" + s_] = m["B" + s_].fillna(0.0)
        m["O" + s_] = m["O" + s_].fillna(0.0)
    m["dB"] = m.B_2425 - m.B_2324
    m["dO"] = m.O_2425 - m.O_2324
    B1, O1, B2, O2 = m.B_2324.sum(), m.O_2324.sum(), m.B_2425.sum(), m.O_2425.sum()
    share1, share2 = B1 / (B1 + O1) * 100, B2 / (B2 + O2) * 100
    # counterfactual: share in 2024/25 if only this project had stayed at its 2023/24 contribution
    m["share_pts_effect"] = [share2 - (B2 - b + 0) / ((B2 - b) + (O2 - o)) * 100 for b, o in zip(m.dB, m.dO)]
    m["ward_group_changed"] = (m.g_2324.isin(["Black", "Other"]) & m.g_2425.isin(["Black", "Other"]) & (m.g_2324 != m.g_2425))

    def cat(r: pd.Series) -> str:
        if r.dO > 0:
            return "other wards: new/enlarged"
        if r.dB < 0:
            return "Black wards: reduced/dropped"
        if r.dO < 0:
            return "other wards: reduced/dropped (offsets)"
        if r.dB > 0:
            return "Black wards: new/enlarged (offsets)"
        return "no change"
    m["category"] = m.apply(cat, axis=1)
    return m, (B1, O1, B2, O2, share1, share2)


if __name__ == "__main__":
    m, (B1, O1, B2, O2, s1, s2) = link()
    print(f"Black {B1/1e6:.1f} -> {B2/1e6:.1f}; Other {O1/1e6:.1f} -> {O2/1e6:.1f}; share {s1:.1f} -> {s2:.1f}")
    m.to_csv("work/part1_decomposition.csv")
    mv = m[m.category != "no change"].copy()
    mv["impact"] = mv.dO.abs() + mv.dB.abs()
    adverse = mv[mv.category.isin(["other wards: new/enlarged", "Black wards: reduced/dropped"])].sort_values("impact", ascending=False)
    gross = adverse.impact.sum()
    print("adverse gross R m", gross / 1e6, "n", len(adverse))
    for k in (1, 3, 5, 10):
        print(f"  top {k}: {adverse.impact.head(k).sum()/gross*100:.1f}% of adverse gross")
    print(mv.groupby("category").agg(n=("impact", "size"), Rm=("impact", "sum")).assign(Rm=lambda d: d.Rm / 1e6))
    cols = ["category", "name_2324", "name_2425", "wards_2324", "wards_2425", "g_2324", "g_2425", "val_2324", "val_2425", "dB", "dO", "share_pts_effect", "link", "ward_group_changed"]
    print(mv.sort_values("impact", ascending=False)[cols].head(30).assign(**{c: lambda d, c=c: d[c] / 1e6 for c in ("val_2324", "val_2425", "dB", "dO")}).to_string())


def cause(r: pd.Series) -> str:
    """Why this project's Black/other contribution changed."""
    att1, att2 = r.B_2324 + r.O_2324, r.B_2425 + r.O_2425
    if r.link == "one year only" and r.val_2425 == 0 and r.name_2425 != r.name_2425:
        return "not in 2024/25 budget"
    if r.link == "one year only" and r.name_2324 != r.name_2324:
        return "new in 2024/25 budget"
    if r.val_2425 == 0:
        return "budgeted R0 in 2024/25"
    if r.val_2324 == 0:
        return "budgeted R0 in 2023/24"
    if att1 > 0 and att2 == 0 and r.val_2425 < 0.5 * r.val_2324:
        return "budget cut; small 2024/25 remainder has no ward match"
    if att1 > 0 and att2 == 0:
        return f"in both budgets; no single-ward attribution in 2024/25 ({r.g_2425})"
    if att1 == 0 and att2 > 0:
        return f"in both budgets; no single-ward attribution in 2023/24 ({r.g_2324})"
    if (r.B_2324 > 0 and r.O_2425 > 0) or (r.O_2324 > 0 and r.B_2425 > 0):
        return "ward group changed between years' Appendix O"
    return "budget value changed"


def report() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    m, tot = link()
    m["cause"] = m.apply(cause, axis=1)
    mv = m[m.category != "no change"].copy()
    mv["impact"] = mv.dO.abs() + mv.dB.abs()
    adverse = mv[mv.category.isin(["other wards: new/enlarged", "Black wards: reduced/dropped"])].sort_values("impact", ascending=False)
    conc = {k: adverse.impact.head(k).sum() / adverse.impact.sum() * 100 for k in (1, 3, 5, 10)}
    conc["n_adverse"] = len(adverse)
    conc["gross_adverse_Rm"] = adverse.impact.sum() / 1e6
    return mv, adverse, dict(tot=tot, conc=conc)


if __name__ == "__main__":
    mv, adverse, info = report()
    mv.to_csv("work/part1_movements.csv")
    print(mv.assign(dBm=mv.dB / 1e6, dOm=mv.dO / 1e6).groupby(["category", "cause"])[["dBm", "dOm"]].sum().round(1).to_string())
    for r in adverse.head(15).itertuples():
        print(f"{r.impact/1e6:6.1f} | {r.category[:12]} | {str(r.name_2324)[:45]} -> {str(r.name_2425)[:30]} | w {r.wards_2324}->{r.wards_2425} | {r.cause}")


def split_effects(m: pd.DataFrame) -> pd.DataFrame:
    """Split each project's change in Black (dB) and other (dO) money into
    budget effect (the project's rand value changed) and attribution effect (money still in the budget but moved
    into/out of a ward group because of ward matching / Appendix O ward changes)."""
    out = m.copy()
    for side, a1, a2, other1, other2 in (("B", "B_2324", "B_2425", "O_2324", "O_2425"), ("O", "O_2324", "O_2425", "B_2324", "B_2425")):
        att = []
        for r in out.itertuples():
            x1, x2 = getattr(r, a1), getattr(r, a2)
            if x1 > 0 and x2 == 0 and r.val_2425 > 0:
                att.append(-min(r.val_2425, x1))          # still budgeted, no longer in this group
            elif x1 == 0 and x2 > 0 and r.val_2324 > 0:
                att.append(min(r.val_2324, x2))           # was budgeted, not in this group before
            else:
                att.append(0.0)
        out[f"d{side}_attribution"] = att
        out[f"d{side}_budget"] = out[f"d{side}"] - out[f"d{side}_attribution"]
    return out


def markdown_section() -> str:
    """Markdown for summary.md (follow-up 1)."""
    m, (B1, O1, B2, O2, s1, s2) = link()
    s = split_effects(m)
    s["cause"] = s.apply(cause, axis=1)
    s["adv"] = (-s.dB.clip(upper=0)) + s.dO.clip(lower=0)
    s["off"] = s.dB.clip(lower=0) + (-s.dO.clip(upper=0))
    s["adv_budget"] = (-s.dB_budget.clip(upper=0)) + s.dO_budget.clip(lower=0)
    s["adv_attr"] = (-s.dB_attribution.clip(upper=0)) + s.dO_attribution.clip(lower=0)
    a = s[s.adv > 0].sort_values("adv", ascending=False)
    g = a.adv.sum()
    conc = {k: a.adv.head(k).sum() / g * 100 for k in (1, 3, 5, 10)}
    Bb, Ob = B1 + s.dB_budget.sum(), O1 + s.dO_budget.sum()
    nm = lambda r: (r.name_2324 if isinstance(r.name_2324, str) else r.name_2425)
    w = lambda x: "–" if not isinstance(x, str) else x
    rows = []
    for r in a.head(15).itertuples():
        rows.append(dict(**{"Project": str(nm(r))[:80], "Direction": "other wards ↑" if r.dO > 0 else "Black wards ↓",
                            "Ward 23/24→24/25": f"{w(r.wards_2324)} → {w(r.wards_2425)}",
                            "Budget 23/24 (R m)": r.val_2324 / 1e6, "Budget 24/25 (R m)": r.val_2425 / 1e6,
                            "Impact (R m)": r.adv / 1e6, "…real budget change": r.adv_budget / 1e6,
                            "…ward attribution": r.adv_attr / 1e6, "Cause": r.cause, "Link": r.link}))
    top = pd.DataFrame(rows).to_markdown(index=False, floatfmt=",.1f")
    o = s[s.off > 0].sort_values("off", ascending=False)
    orows = [dict(Project=str(nm(r))[:80], Direction="Black wards ↑" if r.dB > 0 else "other wards ↓",
                  **{"Ward 23/24→24/25": f"{w(r.wards_2324)} → {w(r.wards_2425)}", "Offset (R m)": r.off / 1e6, "Cause": r.cause})
             for r in o.head(8).itertuples()]
    offs = pd.DataFrame(orows).to_markdown(index=False, floatfmt=",.1f")
    bycause = (s.assign(Black=s.dB / 1e6, Other=s.dO / 1e6).groupby("cause")[["Black", "Other"]].sum()
               .loc[lambda d: (d.Black.abs() + d.Other.abs()) > 0.05].sort_values("Black"))
    links = "\n".join(f"- `{k}` → `{v[0]}`: {v[1]}" for k, v in RECODED.items())
    return f"""## 7. Follow-up 1 — what drove the 2024/25 original-budget drop (excluding bulk infrastructure)

Comparison: 2023/24 original budget (2023/24 adjustments budget, Annexure B) vs 2024/25 original budget (2024/25 MTREF, Annexure A). Bulk-infrastructure-named rows are excluded; each year's ward comes from that year's Appendix O (≥80% definition). Projects are linked by WBS code without the funding-source segment, so funding switches don't break the link. A shared code counts as a link only if the names also agree; one code was reused for a different project (Ekangala). Four re-coded projects were linked by hand:

{links}

The share fell from **{s1:.1f}% to {s2:.1f}%**. Single-ward money in predominantly Black wards went from R{B1/1e6:,.1f}m to R{B2/1e6:,.1f}m (**{(B2-B1)/1e6:+,.1f}m**); in other wards from R{O1/1e6:,.1f}m to R{O2/1e6:,.1f}m (**{(O2-O1)/1e6:+,.1f}m**). (This corrects the 67.2% in the first version of this summary: one 2024/25 ward match, Electricity Distribution Loss, was wrongly rejected and has been restored; see §6.)

**Real budget changes vs. ward-labelling effects.** Each project's change is split into the change in its own budget and the part caused only by a change in ward attribution. The second covers projects whose Appendix O ward moved between groups, or that were single-ward in one year and not the other.

| | Black wards (R m) | Other wards (R m) |
|---|---|---|
| Total change | {s.dB.sum()/1e6:+,.1f} | {s.dO.sum()/1e6:+,.1f} |
| …from projects' own budget changes | {s.dB_budget.sum()/1e6:+,.1f} | {s.dO_budget.sum()/1e6:+,.1f} |
| …from ward-attribution changes | {s.dB_attribution.sum()/1e6:+,.1f} | {s.dO_attribution.sum()/1e6:+,.1f} |

With attribution held fixed, the 2024/25 share would be **{Bb/(Bb+Ob)*100:.1f}%**. So roughly {(s1-Bb/(Bb+Ob)*100):.0f} of the {s1-s2:.0f} points are real budget re-allocation and the rest is ward labelling. Most of the labelling effect is the "Critical Worn-Out Water Pipes" Areas A and B. Appendix O moved them from ward 100 (Black) in 2023/24 to wards 96 and 53 (other) in 2024/25, although the titles say they cover Regions 1–2 and Region 3.

**Concentrated or broad?** Moderately concentrated. {len(a)} projects moved money in the adverse direction (Black ↓ or other ↑), R{g/1e6:,.1f}m gross. The largest single project is {conc[1]:.0f}% of that, the top 3 are {conc[3]:.0f}%, the top 5 {conc[5]:.0f}% and the top 10 {conc[10]:.0f}%. Black-ward gains elsewhere offset R{s.off.sum()/1e6:,.1f}m.

Largest adverse movements, ranked by rand impact:

{top}

Largest offsetting movements:

{offs}

By cause (sum of changes, R m):

{bycause.to_markdown(floatfmt=",.1f")}

Reading: the biggest real cut is Thorntree View roads and stormwater (ward 36): R90.2m in the 2023/24 original budget, R1.0m in the 2024/25 MTREF. Appendix N shows R24.5m adjusted and actual for it in 2024/25. Next come Electricity Distribution Loss (ward 29, R68.0m → R20.0m), the Zithobeni X8 sewer (ward 105, R30.6m, not in the 2024/25 MTREF) and Timberlands social housing (ward 81, R26.0m → R0). On the other side are two Andeon X37 projects (ward 55, 75.7% Black African, so "other" at the 80% threshold) totalling +R39m.
"""
