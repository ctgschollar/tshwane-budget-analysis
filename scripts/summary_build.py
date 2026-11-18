"""Build output/summary.md and output/ward_classification.csv. All figures computed here from projects.csv."""
import os
import pandas as pd
import analyze as A
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

OUT = ROOT + "/output/"
TWN = "townships/ward_township_flag.csv"
TWN_OV = "townships/ward_township_overlap.csv"


def f1(x: float) -> str:
    return "–" if pd.isna(x) else f"{x:,.1f}"


def md(df: pd.DataFrame, cols: dict) -> str:
    d = df[list(cols)].rename(columns=cols)
    return d.to_markdown(index=False, floatfmt=",.1f")


def township_groups() -> tuple[pd.DataFrame | None, str]:
    if not os.path.exists(TWN):
        return None, "_Township mapping not available._"
    t = pd.read_csv(TWN)
    t["ward_no"] = t.ward_no.astype(int) - 79900000
    t["township_primary"] = t.township_primary_by_pop2011.fillna("")
    t["max_pct"] = t.max_pct_pop2011
    return t, ""


def township_share(t: pd.DataFrame) -> pd.DataFrame:
    prim = dict(zip(t.ward_no, t.township_primary.fillna("")))
    pop = A.pop22
    tw = {w for w, v in prim.items() if v and v.lower() != "eersterust"}
    ee = {w for w, v in prim.items() if v.lower() == "eersterust"}
    tw_pop = sum(pop[w] for w in tw)
    ot_pop = sum(pop[w] for w in pop if w not in tw and w not in ee)
    out = []
    for lab, y, rt, col in A.MEASURES:
        d = A.rows_for(y, rt)
        T = O = E = 0.0
        for r in d.itertuples():
            w = A.single_ward(pd.Series(r._asdict()), "appO")
            v = getattr(r, col)
            if w is None or pd.isna(v):
                continue
            if w in tw:
                T += v
            elif w in ee:
                E += v
            else:
                O += v
        out.append(dict(measure=lab, township_Rm=T / 1e6, other_Rm=O / 1e6, eersterust_Rm=E / 1e6,
                        township_share=T / (T + O) * 100 if T + O else float("nan"),
                        township_R_pc=T / tw_pop, other_R_pc=O / ot_pop))
    return pd.DataFrame(out), len(tw), len(ee), tw_pop


if __name__ == "__main__":
    # ---------------- ward classification CSV
    wc = A.ward_class_table()
    t, _ = township_groups()
    if t is not None:
        wc = wc.merge(t[["ward_no", "township_primary", "township_any", "max_pct"]], on="ward_no", how="left")
        wc = wc.rename(columns={"max_pct": "township_max_pct_of_ward_pop2011", "township_primary": "township_primary_by_pop2011_ge50", "township_any": "township_any_by_area_ge20"})
        wc["township_source"] = "see summary.md (ward × place-boundary overlay)"
    wr = pd.read_csv("work/ward_region_table.csv")
    wc = wc.merge(wr[["ward", "region_final", "assignment_basis", "step1_city_documents", "step1_conflict", "step2_rekord_2021",
                      "step3_official_egis"]].rename(columns={"ward": "ward_no", "region_final": "region",
                                                              "assignment_basis": "region_basis"}), on="ward_no", how="left")
    wc.rename(columns={"ward_no": "ward", "total_population": "population_2022",
                       "pct_black_african": "pct_black_african_2022", "class_ge80": "classification_primary_ge80"}
              ).to_csv(OUT + "ward_classification.csv", index=False)

    prim = A.share_table()
    cov = A.coverage()
    sr = A.spend_rate()
    srd = A.spend_rate(method="dominant")
    sh = A.inyear_shift()
    sens = {}
    for lab, kw in (("≥50%", dict(t=50)), ("≥80% (primary)", {}), ("≥90%", dict(t=90)),
                    ("≥80%, Census 2011 shares", dict(pct=A.pct11)),
                    ("≥80%, excl. single-ward rows whose name states multi-region scope", dict(excl_scope=True)),
                    ("≥80%, excl. Rooiwal WWTW", dict(excl_name=r"Rooiwal")),
                    ("≥80%, excl. all bulk-infrastructure-named rows", dict(excl_bulk=True)),
                    ("≥80%, 'No Intersect' rows given ward from another year's App O", dict(method="appO_impute_ni"))):
        sens[lab] = A.share_table(**kw).set_index("measure")
    sens_tbl = pd.DataFrame({k: v.black_share_of_attributable for k, v in sens.items()}).T
    pc_tbl = pd.DataFrame({k: v.percap_ratio_black_to_other for k, v in sens.items()}).T
    dom = A.share_table(method="dominant").set_index("measure")
    top = A.top10()
    print(prim.to_string())
    pd.to_pickle(dict(prim=prim, cov=cov, sr=sr, srd=srd, sh=sh, sens_tbl=sens_tbl, pc_tbl=pc_tbl, dom=dom, top=top,
                      twn=township_share(t) if t is not None else None), "work/summary_data.pkl")
    print("saved")
