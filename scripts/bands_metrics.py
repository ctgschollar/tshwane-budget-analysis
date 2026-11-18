"""v2 metrics on top of work/v2_alloc.csv: band tables, spend- vs population-weighted mean %Black African,
single-project dominance, binary comparison, and index-based driver decomposition."""
import pandas as pd
import bands_engine as E
from match import norm, score

AL = pd.read_csv("work/v2_alloc.csv")
ATT = AL[AL.ward > 0].copy()
ATT["pct"] = ATT.ward.map(E.PCT)
ATT["pop"] = ATT.ward.map(E.POP)
ORDER = [c[0] for c in E.COLUMNS]
META = {c[0]: dict(kind=c[1], adopted=c[2], doc=c[3]) for c in E.COLUMNS}
CITY_MEAN = sum(E.PCT[w] * E.POP[w] for w in E.POP) / E.TOTPOP   # population-weighted %Black, whole city
COMBOS = [("A", "service", "b"), ("A", "service", "a"), ("A", "location", "b"), ("A", "location", "a"), ("B", "region", "b")]


def sel(col: str, opt: str, basis: str, mode: str, att_only: bool = True) -> pd.DataFrame:
    d = ATT if att_only else AL
    return d[(d.column == col) & (d.option == opt) & (d.basis == basis) & (d["mode"] == mode)]


def index_row(col: str, opt: str, basis: str, mode: str) -> dict:
    d = sel(col, opt, basis, mode)
    tot = AL[(AL.column == col) & (AL.option == opt) & (AL.basis == basis) & (AL["mode"] == mode)].R.sum()
    wR = d.groupby("ward").R.sum()
    wR = wR[wR > 0]
    spend = (wR * wR.index.map(E.PCT)).sum() / wR.sum()
    pops = pd.Series({w: E.POP[w] for w in wR.index})
    popm = (pops * pops.index.map(E.PCT)).sum() / pops.sum()
    return dict(column=col, option=opt, basis=basis, mode=mode, attributed_Rm=wR.sum() / 1e6,
                attributed_pct=wR.sum() / tot * 100, wards_with_capex=len(wR),
                spend_weighted=spend, pop_weighted_same_wards=popm, gap=spend - popm,
                gap_vs_city=spend - CITY_MEAN)


def index_table() -> pd.DataFrame:
    return pd.DataFrame([index_row(c, *k) for c in ORDER for k in COMBOS])


def band_table(col: str, opt: str, basis: str, mode: str, scheme: str = "headline") -> pd.DataFrame:
    d = sel(col, opt, basis, mode)
    d = d.assign(band=d.ward.map(lambda w: E.band_of(w, scheme)))
    tot = d.R.sum()
    rows = []
    for lab, lo, hi in E.BANDS[scheme]:
        wards = [w for w in E.PCT if lo <= E.PCT[w] < hi]
        pop = sum(E.POP[w] for w in wards)
        g = d[d.band == lab]
        R = g.R.sum()
        byp = g.groupby("key").agg(R=("R", "sum"), name=("project_name", "first")).sort_values("R", ascending=False)
        top_share = byp.R.iloc[0] / R * 100 if R > 0 else 0.0
        rows.append(dict(column=col, option=opt, basis=basis, mode=mode, scheme=scheme, band=lab, wards=len(wards),
                         Rm=R / 1e6, share_of_attributed=R / tot * 100 if tot else float("nan"),
                         share_of_population=pop / E.TOTPOP * 100, R_per_resident=R / pop,
                         top_project=byp.name.iloc[0] if R > 0 else "", top_project_share=top_share,
                         dominated=top_share > 50))
    return pd.DataFrame(rows)


def all_bands() -> pd.DataFrame:
    out = []
    for scheme in ("headline", "split_80_100", "merged_40_80"):
        for c in ORDER:
            for k in COMBOS:
                out.append(band_table(c, *k, scheme=scheme))
    return pd.concat(out, ignore_index=True)


def binary_share(col: str, opt: str, basis: str, mode: str) -> float:
    d = sel(col, opt, basis, mode)
    return d[d.pct >= 80].R.sum() / d.R.sum() * 100


# ---------------- drivers (index terms) ----------------
STEPS = list(zip(E.BUDGET_COLS[:-1], E.BUDGET_COLS[1:]))


def project_view(col: str, opt: str = "A", basis: str = "service", mode: str = "b") -> pd.DataFrame:
    d = sel(col, opt, basis, mode)
    g = d.assign(Rp=d.R * d.pct).groupby("key").agg(name=("project_name", "first"), R=("R", "sum"), Rp=("Rp", "sum"),
                                                    wards=("ward", lambda s: ";".join(str(int(x)) for x in sorted(set(s)))))
    g["p"] = g.Rp / g.R
    return g


def crosswalk(before: pd.DataFrame, after: pd.DataFrame) -> dict:
    """Link keys that differ only because the WBS coding scheme changed (2022/23 old mask -> 2023/24 new mask): unique exact
    normalised-name matches (score >= 95)."""
    unmatched_b = [k for k in before.index if k not in after.index]
    unmatched_a = [k for k in after.index if k not in before.index]
    na = {k: norm(after.at[k, "name"]) for k in unmatched_a}
    out = {}
    for k in unmatched_b:
        nb = norm(before.at[k, "name"])
        cands = [ka for ka, n in na.items() if score(nb, n) >= 95]
        if len(cands) == 1 and cands[0] not in out.values():
            out[k] = cands[0]
    return out


def band_label(p: float) -> str:
    for lab, lo, hi in E.BANDS["headline"]:
        if lo <= p < hi:
            return lab
    return "?"


def drivers(c1: str, c2: str, opt: str = "A", basis: str = "service", mode: str = "b") -> tuple[pd.DataFrame, dict]:
    b, a = project_view(c1, opt, basis, mode), project_view(c2, opt, basis, mode)
    cw = crosswalk(b, a)
    b = b.rename(index=cw)
    m = b.join(a, how="outer", lsuffix="_1", rsuffix="_2")
    for c in ("R", "Rp"):
        for s in ("_1", "_2"):
            m[c + s] = m[c + s].fillna(0.0)
    S1, W1, S2, W2 = m.R_1.sum(), m.Rp_1.sum(), m.R_2.sum(), m.Rp_2.sum()
    I1, I2 = W1 / S1, W2 / S2
    # counterfactual effect of each project's change on the after-index
    m["effect"] = I2 - (W2 - m.Rp_2 + m.Rp_1) / (S2 - m.R_2 + m.R_1)
    both = (m.R_1 > 0) & (m.R_2 > 0)
    relabel = I2 - (W2 - m.Rp_2 + m.R_2 * m.p_1.fillna(0)) / S2
    m["relabel_effect"] = relabel.where(both & ((m.p_1 - m.p_2).abs() > 0.05), 0.0)
    m["budget_effect"] = m.effect - m.relabel_effect
    m["linked_by"] = ["name crosswalk (WBS scheme change)" if k in cw.values() else "" for k in m.index]
    info = dict(I1=I1, I2=I2, dI=I2 - I1, sum_effects=m.effect.sum(), sum_relabel=m.relabel_effect.sum(),
                S1=S1 / 1e6, S2=S2 / 1e6, crosswalk_links=len(cw))
    return m, info


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    it = index_table()
    it.to_csv("work/v2_index.csv", index=False)
    print(it[it.option.eq("A") & it.basis.eq("service") & it["mode"].eq("b")].round(1).to_string(index=False))
    bt = all_bands()
    bt.to_csv("work/v2_bands.csv", index=False)
    print(bt[(bt.scheme == "headline") & (bt.basis == "service") & (bt["mode"] == "b")].pivot_table(
        index="column", columns="band", values="R_per_resident", sort=False).round(0).to_string())
    print("dominated band-cells:", int(bt.dominated.sum()))
    for c1, c2 in STEPS:
        m, i = drivers(c1, c2)
        print(c1, "->", c2, {k: round(v, 2) for k, v in i.items()})
