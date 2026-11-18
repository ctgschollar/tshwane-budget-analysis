"""Build clean Tshwane ward population-group CSVs from downloaded sources (no estimation; raw values kept)."""
import csv
import json
import sys

sys.path.insert(0, sys.argv[1])  # scripts dir (trusted), passed explicitly
from xlsx_dump import read_sheets  # noqa: E402

DL = sys.argv[2]
OUT = sys.argv[3]
XLSX = f"{DL}/x_ward/Ward Product_Locked spreadsheets/PP_Population Group_27-10-2025.xlsx"
SRC22 = ("https://www.statssa.gov.za/wp-content/uploads/2025/11/Ward-Product_Locked-spreadsheets.zip "
         "[PP_Population Group_27-10-2025.xlsx, sheet Wards]")
SRC11 = ("https://services7.arcgis.com/oeoyTUJC8HEeYsRB/arcgis/rest/services/WardProfile2021_gdb/FeatureServer/0 "
         "(MDB ArcGIS item e3e508c18ecc4e788938c4ed3fef899a)")
COLS = ["ward_no", "ward_code", "total_population", "black_african", "coloured", "indian_asian",
        "white", "other", "pct_black_african", "source_url", "census_year", "boundary_vintage"]


def build_2022() -> list[dict]:
    rows = read_sheets(XLSX)["Wards"]
    hdr = rows[0]
    out = []
    for r in rows[1:]:
        if r and r[0].startswith("799"):
            d = dict(zip(hdr, r))
            tot = float(d["Total"])
            out.append({"ward_no": int(d["Ward_Code"][-3:]), "ward_code": d["Ward_Code"],
                        "total_population": d["Total"], "black_african": d["Black African"],
                        "coloured": d["Coloured"], "indian_asian": d["Indian/Asian"], "white": d["White"],
                        "other": d["Other"], "pct_black_african": round(100 * float(d["Black African"]) / tot, 2),
                        "source_url": SRC22,
                        "census_year": "2022 (Stats SA Ward level Small Area Population Estimates 2022; Census 2022 + Census 2011 raking)",
                        "boundary_vintage": "MDB 2020 wards (used for Nov 2021 LGE)"})
    return sorted(out, key=lambda x: x["ward_no"])


def build_2011() -> list[dict]:
    feats = json.load(open(f"{DL}/MDB_WardProfile2021_TSH_attrs.json"))["features"]
    out = []
    for f in feats:
        a = f["attributes"]
        out.append({"ward_no": a["WardNo"], "ward_code": a["WardID"], "total_population": a["Total_Pop"],
                    "black_african": a["Black_African"], "coloured": a["Coloured"],
                    "indian_asian": a["Indian_or_Asian"], "white": a["White"],
                    "other": a["Other_Pop"] + a["Unspecified_Pop"],
                    "pct_black_african": round(100 * a["Black_African"] / a["Total_Pop"], 2),
                    "source_url": SRC11,
                    "census_year": "2011 (inferred: municipal total 2,921,489 matches Census 2011; layer undocumented)",
                    "boundary_vintage": "MDB 2020 wards (used for Nov 2021 LGE)"})
    return sorted(out, key=lambda x: x["ward_no"])


for name, rows in [("tshwane_ward_popgroup.csv", build_2022()),
                   ("tshwane_ward_popgroup_census2011_mdb_wardprofile2021.csv", build_2011())]:
    with open(f"{OUT}/{name}", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    tot = {k: sum(float(r[k]) for r in rows) for k in COLS[2:8]}
    print(name, len(rows), {k: round(v) for k, v in tot.items()})
