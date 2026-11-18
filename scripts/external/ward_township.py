"""Ward x township overlap for City of Tshwane (MDB 2020 wards x Stats SA Census 2011 Main Places)."""
import glob
import os
import re
import sys

import geopandas as gpd
import pandas as pd

S = sys.argv[1]  # scratchpad dir
DL = f"{S}/townships_dl"
OUT = f"{S}/townships"
CRS = "EPSG:32735"
SP_URL = ("https://services3.arcgis.com/GMycIhSIBQnnjV35/arcgis/rest/services/"
          "Census_2011_Sub_Places_of_South_Africa/FeatureServer/0")
POP_URL = "https://census2011.adrianfrith.com/place/<MP_CODE>"
VINTAGE = "Stats SA Census 2011 sub-place boundaries (dissolved to Main Place); MDB 2020 wards"

# township label -> official Census 2011 Main Place name
TOWNSHIPS = {
    "Mabopane": "Mabopane", "Ga-Rankuwa": "Ga-Rankuwa", "Soshanguve": "Soshanguve",
    "Winterveld": "Winterveld", "Hammanskraal": "Hammanskraal", "Temba": "Temba",
    "Mamelodi": "Mamelodi", "Atteridgeville": "Atteridgeville", "Saulsville": "Saulsville",
    "Olievenhoutbosch": "Olievenhoutbos", "Refilwe": "Refilwe", "Ekangala": "Ekangala",
    "Zithobeni": "Zithobeni", "Eersterust": "Eersterust",
}


def load_sp_pop() -> pd.DataFrame:
    rows = []
    pat = re.compile(r'href="/place/(\d{9})">([^<]*)</a></td><td class="text-right">([\d,]+)</td>')
    for f in glob.glob(f"{DL}/af_mp/*.html"):
        txt = open(f, encoding="utf-8").read()
        for code, name, pop in pat.findall(txt):
            rows.append((code, name, int(pop.replace(",", ""))))
    return pd.DataFrame(rows, columns=["SP_CODE_st", "SP_NAME_af", "pop2011"]).drop_duplicates("SP_CODE_st")


def main() -> None:
    wards = gpd.read_file(f"{S}/census_dl/MDB_Wards_2020_TSH.geojson").to_crs(CRS)
    wards["geometry"] = wards.geometry.make_valid()
    wards["ward_no"] = wards["WardID"].astype(str)
    wards["ward_area_km2"] = wards.area / 1e6

    sp = pd.concat([gpd.read_file(f) for f in sorted(glob.glob(f"{DL}/sp2011_env_*.geojson"))
                    if os.path.getsize(f) > 200])
    sp = sp[sp.MN_MDB_C == "TSH"].to_crs(CRS)
    sp["geometry"] = sp.geometry.make_valid()
    pop = load_sp_pop()
    sp = sp.merge(pop, on="SP_CODE_st", how="left")
    print("TSH SPs:", len(sp), "missing pop:", sp.pop2011.isna().sum(), "total pop:", sp.pop2011.sum())
    sp["sp_area"] = sp.area

    # SP x ward pieces (areal weighting of population within each sub place)
    pieces = gpd.overlay(sp[["SP_CODE_st", "SP_NAME", "MP_NAME", "pop2011", "sp_area", "geometry"]],
                         wards[["ward_no", "ward_area_km2", "geometry"]], how="intersection",
                         keep_geom_type=True)
    pieces["a"] = pieces.area
    pieces["pop_est"] = pieces.pop2011 * pieces.a / pieces.sp_area
    ward_pop = pieces.groupby("ward_no").pop_est.sum()
    ward_cov = pieces.groupby("ward_no").a.sum() / 1e6

    out = []
    for label, mp in TOWNSHIPS.items():
        t_sp = sp[sp.MP_NAME == mp]
        names = "; ".join(sorted(t_sp.SP_NAME))
        t_area = t_sp.area.sum() / 1e6
        t_pop = t_sp.pop2011.sum()
        p = pieces[pieces.MP_NAME == mp].groupby("ward_no").agg(a=("a", "sum"), pop=("pop_est", "sum"))
        for w, r in p.iterrows():
            wa = wards.loc[wards.ward_no == w, "ward_area_km2"].iloc[0]
            out.append({
                "ward_no": w, "township": label, "place_level": "MP",
                "place_names_included": f"MP '{mp}' (code {t_sp.MP_CODE_st.iloc[0]}); SPs: {names}",
                "ward_area_km2": round(wa, 3), "overlap_km2": round(r.a / 1e6, 3),
                "pct_of_ward_in_township": round(100 * r.a / 1e6 / wa, 2),
                "pct_of_township_in_ward": round(100 * r.a / 1e6 / t_area, 2),
                "pop2011_overlap_est": round(r["pop"]),
                "pct_of_ward_pop2011_in_township": round(100 * r["pop"] / ward_pop[w], 2),
                "pct_of_township_pop2011_in_ward": round(100 * r["pop"] / t_pop, 2),
                "source_url": f"{SP_URL} ; pop: {POP_URL.replace('<MP_CODE>', t_sp.MP_CODE_st.iloc[0])}",
                "vintage": VINTAGE,
            })
    df = pd.DataFrame(out)
    os.makedirs(OUT, exist_ok=True)
    df_all = df[df.overlap_km2 > 0].sort_values(["ward_no", "township"])
    df_all.to_csv(f"{OUT}/ward_township_overlap_all.csv", index=False)
    df = df[df.pct_of_ward_in_township > 1].copy()
    df["ward_sort"] = df.ward_no.astype(int)
    df = df.sort_values(["ward_sort", "pct_of_ward_in_township"], ascending=[True, False]).drop(columns="ward_sort")
    df.to_csv(f"{OUT}/ward_township_overlap.csv", index=False)

    flags = []
    for w in sorted(wards.ward_no, key=int):
        d = df[df.ward_no == w].sort_values("pct_of_ward_in_township", ascending=False)
        mx = d.pct_of_ward_in_township.max() if len(d) else 0.0
        prim = d.township.iloc[0] if len(d) and mx >= 50 else ""
        anyt = ";".join(d[d.pct_of_ward_in_township >= 20].township)
        da = df_all[df_all.ward_no == w]
        mxp = da.pct_of_ward_pop2011_in_township.max() if len(da) else 0.0
        primp = da.sort_values("pct_of_ward_pop2011_in_township", ascending=False).township.iloc[0] if len(da) and mxp >= 50 else ""
        flags.append({"ward_no": w, "township_primary": prim, "township_any": anyt, "max_pct": round(mx, 2),
                      "township_primary_by_pop2011": primp, "max_pct_pop2011": round(mxp, 2),
                      "ward_pop2011_est": round(ward_pop.get(w, 0)),
                      "ward_pct_area_covered_by_2011_TSH_SPs": round(100 * ward_cov.get(w, 0) /
                          wards.loc[wards.ward_no == w, "ward_area_km2"].iloc[0], 2)})
    fl = pd.DataFrame(flags)
    fl.to_csv(f"{OUT}/ward_township_flag.csv", index=False)

    # diagnostics
    print("ward SP coverage min:", fl.ward_pct_area_covered_by_2011_TSH_SPs.min())
    print(fl.township_primary.replace("", "(none)").value_counts().to_string())
    print("any>=20:", pd.Series(";".join(fl.township_any).split(";")).replace("", pd.NA).dropna().value_counts().to_string())
    print("primary_by_pop differs from area:", (fl.township_primary != fl.township_primary_by_pop2011).sum())
    print(fl[fl.township_primary != fl.township_primary_by_pop2011].to_string())
    for label, mp in TOWNSHIPS.items():
        t = sp[sp.MP_NAME == mp]
        print(label, mp, "SPs", len(t), "area km2", round(t.area.sum() / 1e6, 2), "pop", t.pop2011.sum())


if __name__ == "__main__":
    main()
