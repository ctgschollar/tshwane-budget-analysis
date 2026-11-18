"""Ward classification + share / per-capita / spend-rate analysis. Prints markdown tables."""
import re
import pandas as pd
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

OUT = ROOT + "/output/"
p = pd.read_csv(OUT + "projects.csv")
c22 = pd.read_csv("census_clean/tshwane_ward_popgroup.csv")
c11 = pd.read_csv("census_clean/tshwane_ward_popgroup_census2011_mdb_wardprofile2021.csv")
pct22 = dict(zip(c22.ward_no, c22.pct_black_african))
pct11 = dict(zip(c11.ward_no, c11.pct_black_african))
pop22 = dict(zip(c22.ward_no, c22.total_population))


def ward_class_table() -> pd.DataFrame:
    w = c22[["ward_no", "ward_code", "total_population", "black_african", "pct_black_african"]].copy()
    for t in (50, 80, 90):
        w[f"class_ge{t}"] = w.pct_black_african.map(lambda x: "predominantly Black" if x >= t else "other")
    w["pct_black_african_census2011"] = w.ward_no.map(pct11)
    w["class_ge80_census2011"] = w.pct_black_african_census2011.map(lambda x: "predominantly Black" if x >= 80 else "other")
    w["data_source"] = ("Stats SA Ward-level Small Area Population Estimates 2022 (Nov 2025), PP_Population Group workbook, "
                        "MDB 2020 ward boundaries; 2011 column: MDB WardProfile2021 layer (Census 2011 on 2020 wards)")
    return w


# ---------- grouping
_O = pd.read_csv("work/appO_used.csv", index_col=0)
NI_IMPUTE = {}
for _r in _O[_O.ward_category == "single-ward"].itertuples():
    NI_IMPUTE.setdefault(str(_r.project_name).lower()[:30], {})[_r.year] = int(str(_r.wards).split(";")[0])


def single_ward(r: pd.Series, method: str) -> int | None:
    if method == "appO_impute_ni":
        if r.ward_category == "no-intersect":
            cand = NI_IMPUTE.get(str(r.project_name).lower()[:30], {})
            cand = {y: w for y, w in cand.items() if y != r.year}
            if cand:
                return cand[sorted(cand)[0]]
        method = "appO"
    if method == "appO":
        if r.ward_category == "single-ward":
            return int(str(r.wards).split(";")[0])
        return None
    m = re.fullmatch(r"Ward (\d+)", str(r.dominant_ward_appN))
    return int(m.group(1)) if m else None


def group(r: pd.Series, t: float, pct: dict, method: str = "appO", excl_scope: bool = False, excl_bulk: bool = False,
          excl_name: str | None = None) -> str:
    if excl_bulk and r.bulk_infrastructure_name_flag:
        return "excluded (bulk-infra flag)"
    if excl_name and re.search(excl_name, str(r.project_name), re.I):
        return "excluded (named project)"
    w = single_ward(r, method)
    if w is not None:
        if excl_scope and r.scope_flag_multi_region_name:
            return "non-attributable"
        return "Black" if pct[w] >= t else "Other"
    if method.startswith("appO") and r.ward_category == "multi-ward":
        return "multi-ward"
    return "non-attributable"


MEASURES = [  # (label, year, record_type prefix, value column)
    ("2022/23 original budget", "2022/23", "budget", "original_budget"),
    ("2022/23 adjusted budget", "2022/23", "budget", "adjusted_budget"),
    ("2023/24 original budget", "2023/24", "budget", "original_budget"),
    ("2023/24 adjusted budget", "2023/24", "budget", "adjusted_budget"),
    ("2024/25 original budget", "2024/25", "budget", "original_budget"),
    ("2024/25 adjusted budget", "2024/25", "adjusted+actual", "adjusted_budget"),
    ("2024/25 actual spend", "2024/25", "adjusted+actual", "actual_spend"),
]


def rows_for(year: str, rt: str) -> pd.DataFrame:
    return p[(p.year == year) & p.record_type.str.startswith(rt)]


def share_table(t: float = 80, pct: dict = pct22, method: str = "appO", **kw) -> pd.DataFrame:
    black_pop = sum(v for w, v in pop22.items() if pct[w] >= t)
    other_pop = sum(v for w, v in pop22.items() if pct[w] < t)
    out = []
    for lab, y, rt, col in MEASURES:
        if method == "dominant" and rt != "adjusted+actual":
            continue
        d = rows_for(y, rt).copy()
        d["g"] = d.apply(lambda r: group(r, t, pct, method, **kw), axis=1)
        s = d.groupby("g")[col].sum()
        B, O = s.get("Black", 0.0), s.get("Other", 0.0)
        tot = d[col].sum()
        out.append(dict(measure=lab, total_Rm=tot / 1e6, black_Rm=B / 1e6, other_Rm=O / 1e6,
                        multiward_Rm=s.get("multi-ward", 0.0) / 1e6, nonattrib_Rm=s.get("non-attributable", 0.0) / 1e6,
                        attributable_pct_of_total=(B + O) / tot * 100 if tot else float("nan"),
                        black_share_of_attributable=B / (B + O) * 100 if B + O else float("nan"),
                        black_R_per_capita=B / black_pop, other_R_per_capita=O / other_pop,
                        percap_ratio_black_to_other=(B / black_pop) / (O / other_pop) if O else float("nan")))
    return pd.DataFrame(out)


def coverage() -> pd.DataFrame:
    out = []
    for lab, y, rt, col in MEASURES:
        d = rows_for(y, rt)
        tot = d[col].sum()
        s = d.groupby("ward_category")[col].sum()
        row = dict(measure=lab, total_Rm=tot / 1e6)
        for k in ("single-ward", "multi-ward", "city-wide", "administrative-hq", "no-intersect", "unmatched"):
            row[f"{k}_Rm"] = s.get(k, 0.0) / 1e6
            row[f"{k}_pct"] = s.get(k, 0.0) / tot * 100
        out.append(row)
    return pd.DataFrame(out)


def region_table() -> pd.DataFrame:
    d = p[p.record_type.str.startswith("budget")].copy()
    d["region"] = d.region.fillna("").replace("", "(no region tag found)")
    t = d.pivot_table(index="region", columns="year", values="original_budget", aggfunc="sum") / 1e6
    return t.assign(**{c: t[c] for c in t.columns}).round(1)


def spend_rate(t: float = 80, method: str = "appO") -> pd.DataFrame:
    d = rows_for("2024/25", "adjusted+actual").copy()
    d["g"] = d.apply(lambda r: group(r, t, pct22, method), axis=1)
    s = d.groupby("g")[["adjusted_budget", "actual_spend"]].sum()
    s["spend_rate_pct"] = s.actual_spend / s.adjusted_budget * 100
    s.loc["TOTAL"] = [d.adjusted_budget.sum(), d.actual_spend.sum(), d.actual_spend.sum() / d.adjusted_budget.sum() * 100]
    return (s.assign(adjusted_budget=s.adjusted_budget / 1e6, actual_spend=s.actual_spend / 1e6))


def inyear_shift(t: float = 80) -> pd.DataFrame:
    out = []
    for y, orig_rt, adj_rt in (("2022/23", "budget", "budget"), ("2023/24", "budget", "budget"),
                               ("2024/25", "budget", "adjusted+actual")):
        for g in ("Black", "Other", "multi-ward", "non-attributable"):
            o_ = rows_for(y, orig_rt)
            a_ = rows_for(y, adj_rt)
            ov = o_[o_.apply(lambda r: group(r, t, pct22) == g, axis=1)].original_budget.sum()
            av = a_[a_.apply(lambda r: group(r, t, pct22) == g, axis=1)].adjusted_budget.sum()
            out.append(dict(year=y, group=g, original_Rm=ov / 1e6, adjusted_Rm=av / 1e6,
                            change_Rm=(av - ov) / 1e6, adjusted_as_pct_of_original=av / ov * 100 if ov else float("nan")))
    return pd.DataFrame(out)


def top10(t: float = 80) -> dict:
    res = {}
    for lab, y, rt, col in (("2022/23 (adjusted budget)", "2022/23", "budget", "adjusted_budget"),
                            ("2023/24 (adjusted budget)", "2023/24", "budget", "adjusted_budget"),
                            ("2024/25 (actual spend, Appendix N)", "2024/25", "adjusted+actual", "actual_spend")):
        d = rows_for(y, rt).copy()
        d["g"] = d.apply(lambda r: group(r, t, pct22), axis=1)
        for g in ("Black", "Other"):
            x = d[d.g == g].nlargest(10, col)
            cols = ["project_name", "wards", "original_budget", "adjusted_budget", "actual_spend", "page"]
            res[(lab, g)] = x[cols]
    return res


if __name__ == "__main__":
    wc = ward_class_table()
    wc.to_csv("work/ward_class_base.csv", index=False)
    pd.set_option("display.float_format", lambda v: f"{v:,.1f}")
    pd.set_option("display.width", 250)
    print("## PRIMARY (>=80%, 2022 SAPE, App O method)")
    print(share_table().to_markdown(index=False, floatfmt=",.1f"))
    for lab, kw in ((">=50%", dict(t=50)), (">=90%", dict(t=90)), (">=80% Census 2011 class", dict(pct=pct11)),
                    (">=80% excl. multi-region-named single-ward rows", dict(excl_scope=True)),
                    (">=80% excl. bulk-infrastructure-named rows", dict(excl_bulk=True)),
                    (">=80% excl. Rooiwal WWTW rows only", dict(excl_name=r"Rooiwal")),
                    (">=80% 'No Intersect' rows given the ward from another year's App O", dict(method="appO_impute_ni")),
                    (">=80% App N dominant-ward method (2024/25 only)", dict(method="dominant"))):
        print(f"\n## SENS {lab}")
        print(share_table(**kw)[["measure", "attributable_pct_of_total", "black_share_of_attributable",
                                 "black_R_per_capita", "other_R_per_capita", "percap_ratio_black_to_other"]].to_markdown(index=False, floatfmt=",.1f"))
    print("\n## COVERAGE by ward category (R m and % of each measure's total)")
    print(coverage().to_markdown(index=False, floatfmt=",.1f"))
    print("\n## REGION (original budget R m, region tag via WBS join to SA36/SB19)")
    print(region_table().to_markdown(floatfmt=",.1f"))
    print("\n## SPEND RATE 2024/25 (App O method)")
    print(spend_rate().to_markdown(floatfmt=",.1f"))
    print("\n## SPEND RATE 2024/25 (App N dominant ward)")
    print(spend_rate(method="dominant").to_markdown(floatfmt=",.1f"))
    for t in (50, 90):
        print(f"\n## SPEND RATE 2024/25 t={t}")
        print(spend_rate(t=t).to_markdown(floatfmt=",.1f"))
    print("\n## IN-YEAR SHIFT original -> adjusted")
    print(inyear_shift().to_markdown(index=False, floatfmt=",.1f"))
    for k, v in top10().items():
        print(f"\n## TOP10 {k[0]} — {k[1]}")
        print(v.assign(**{c: v[c] / 1e6 for c in ("original_budget", "adjusted_budget", "actual_spend")}).to_markdown(index=False, floatfmt=",.1f"))
    print("\npop: black wards", sum(v for w, v in pop22.items() if pct22[w] >= 80), "other", sum(v for w, v in pop22.items() if pct22[w] < 80))
