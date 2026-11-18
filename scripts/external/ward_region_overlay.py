"""Ward x City of Tshwane administrative region overlay (MDB 2020 wards x CoT 'Tshwane Regions' layer).

Usage: python3 -I ward_region_overlay.py <scratchpad_dir>
Region polygons downloaded (2026-11-18) with:
  <SRC_URL>/query?where=1=1&outFields=*&returnGeometry=true&outSR=4326&f=geojson
"""
import glob
import os
import re
import sys

import geopandas as gpd
import pandas as pd

S = sys.argv[1]
CRS = "EPSG:32735"
SRC_URL = "https://e-gis001.tshwane.gov.za/server/rest/services/Other_WS/Regions/MapServer/2"
LAYER = "Tshwane Regions (MapServer layer 2, service Other_WS/Regions; publisher City of Tshwane e-GIS)"
VINTAGE = ("No date in service metadata; ArcGIS Online item 373aab0ab11b4acf93064338ceea828e "
           "(owner Tshwane_Web_GIS) created 2018-02-06, modified 2018-02-13; retrieved 2026-11-18")


def load_sp_pop() -> pd.DataFrame:
    # Same loader as scripts/ward_township.py
    rows = []
    pat = re.compile(r'href="/place/(\d{9})">([^<]*)</a></td><td class="text-right">([\d,]+)</td>')
    for f in glob.glob(f"{S}/townships_dl/af_mp/*.html"):
        txt = open(f, encoding="utf-8").read()
        for code, name, pop in pat.findall(txt):
            rows.append((code, name, int(pop.replace(",", ""))))
    return pd.DataFrame(rows, columns=["SP_CODE_st", "SP_NAME_af", "pop2011"]).drop_duplicates("SP_CODE_st")


def top2(s: pd.Series) -> tuple[str, float, str, float]:
    s = s.sort_values(ascending=False)
    pct = 100 * s / s.sum()
    second = (s.index[1], round(pct.iloc[1], 2)) if len(s) > 1 else ("", 0.0)
    return s.index[0], round(pct.iloc[0], 2), second[0], second[1]


def main() -> None:
    wards = gpd.read_file(f"{S}/census_dl/MDB_Wards_2020_TSH.geojson").to_crs(CRS)
    wards["geometry"] = wards.geometry.make_valid()
    wards["ward_no"] = wards["WardNo"].astype(int)
    wards["ward_area"] = wards.area

    reg = gpd.read_file(f"{S}/regions_dl/regions_layer2.geojson").to_crs(CRS)
    reg["geometry"] = reg.geometry.make_valid()
    reg["region"] = reg["name"]

    # Area overlay
    wr = gpd.overlay(wards[["ward_no", "ward_area", "geometry"]], reg[["region", "geometry"]],
                     how="intersection", keep_geom_type=True)
    wr["a"] = wr.area
    cov = wr.groupby("ward_no").a.sum() / wards.set_index("ward_no").ward_area
    print("ward coverage by region polygons: min %.4f max %.4f" % (cov.min(), cov.max()))

    # Population overlay: SP pop split by area within SP, then SP-piece x ward x region
    sp = pd.concat([gpd.read_file(f) for f in sorted(glob.glob(f"{S}/townships_dl/sp2011_env_*.geojson"))
                    if os.path.getsize(f) > 200])
    sp = sp[sp.MN_MDB_C == "TSH"].to_crs(CRS)
    sp["geometry"] = sp.geometry.make_valid()
    sp = sp.merge(load_sp_pop(), on="SP_CODE_st", how="left")
    sp["sp_area"] = sp.area
    print("TSH SPs:", len(sp), "missing pop:", sp.pop2011.isna().sum())
    pieces = gpd.overlay(sp[["SP_CODE_st", "pop2011", "sp_area", "geometry"]],
                         wr[["ward_no", "region", "geometry"]], how="intersection", keep_geom_type=True)
    pieces["pop_est"] = pieces.pop2011 * pieces.area / pieces.sp_area

    out = []
    for w in sorted(wards.ward_no):
        ra, pa, r2, p2 = top2(wr[wr.ward_no == w].groupby("region").a.sum())
        pp = pieces[pieces.ward_no == w].groupby("region").pop_est.sum()
        rp, ppct, _, _ = top2(pp) if pp.sum() > 0 else ("", 0.0, "", 0.0)
        out.append({"ward_no": w, "region_by_area": ra, "pct_area": pa, "second_region": r2,
                    "second_pct_area": p2, "region_by_pop2011": rp, "pct_pop2011": ppct,
                    "source_url": SRC_URL, "layer_name": LAYER, "vintage": VINTAGE})
    df = pd.DataFrame(out)
    os.makedirs(f"{S}/regions", exist_ok=True)
    df.to_csv(f"{S}/regions/ward_region_overlay.csv", index=False)

    print(df.region_by_area.value_counts().sort_index().to_string())
    print("split (<80%):")
    print(df[df.pct_area < 80][["ward_no", "region_by_area", "pct_area", "second_region",
                                "second_pct_area", "region_by_pop2011", "pct_pop2011"]].to_string(index=False))
    print("area vs pop disagree:", df[df.region_by_area != df.region_by_pop2011].ward_no.tolist())


if __name__ == "__main__":
    main()
