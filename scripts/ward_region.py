"""Build the ward -> region table (follow-up 2): City documents first, Rekord list cross-check, official e-GIS layer for the rest."""
import re
import pandas as pd
import os
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

AR22 = "City-of-Tshwane-Audited-Annual-Report-for-2022_23-FY.pdf"
AR23 = "13.-The-Consolidated-Annual-Report-for-the-City-of-Tshwane_2023_24.pdf"
AR24 = "22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.pdf"
MT22 = "02.-2022-2023-MTREF-for-the-City-of-Tshwane.pdf"
MT24 = "02.-2024-2025-MTREF-for-the-City-of-Tshwane.pdf"

# (ward, region, source_file, pdf_page, evidence_type, quote)  -- narrative statements read from the text
NARRATIVE = [
    (50, "Region 6", AR22, 27, "City narrative", "Parkmore LL Reservoir associated pipework in Region 6, with work spanning over ward 50 and ward 96"),
    (96, "Region 6", AR22, 27, "City narrative", "Parkmore LL Reservoir associated pipework in Region 6, with work spanning over ward 50 and ward 96"),
    (102, "Region 7", AR22, 27, "City narrative", "Bronkhorstbaai, Summerplace and Kungwini Country Estate in Ward 102, Region 7"),
    (102, "Region 7", AR22, 73, "City narrative", "Bronkhorstbaai, Summerplace and Kungwini Country Estate in Ward 102, Region 7"),
    (50, "Region 6", AR23, 31, "City narrative", "more than 20 000 households in ward 50 and ward 96 across Region 6"),
    (96, "Region 6", AR23, 31, "City narrative", "more than 20 000 households in ward 50 and ward 96 across Region 6"),
    (107, "Region 7", AR23, 32, "City narrative", "Summerplace and Kungwini Country Estate in Ward 107, Region 7"),
    (50, "Region 6", AR23, 83, "City narrative", "households in ward 50 and ward 96 across Region 6"),
    (96, "Region 6", AR23, 83, "City narrative", "households in ward 50 and ward 96 across Region 6"),
    (107, "Region 7", AR23, 83, "City narrative", "Kungwini Country Estate in Ward 107, Region 7"),
    (104, "Region 7", AR23, 89, "City narrative", "Ekangala Block A – F (Ward 104 - Region 7)"),
    (75, "Region 5", AR23, 90, "City narrative", "Kudube Unit 5 - (Ward 75, Region 5)"),
    (10, "Region 6", AR23, 90, "City narrative", "Mamelodi Ext 11 - (Ward 10, Region 6)"),
    (96, "Region 2", AR23, 97, "City narrative", "Construction of Pyramid 132/11kv substation, Ward 96,Region 2"),
    (91, "Region 6", AR23, 97, "City narrative", "Construction of Mooikloof 132/11kV substation, Ward 91, Region 6"),
    (50, "Region 6", AR24, 90, "City narrative", "pipework spanning over ward 50 and ward 96 in region 6"),
    (96, "Region 6", AR24, 90, "City narrative", "pipework spanning over ward 50 and ward 96 in region 6"),
    (101, "Region 6", AR24, 101, "City narrative", "Wapadrand 132/11kV substation, Ward 101, Region 6"),
    (33, "Region 1", AR24, 101, "City narrative", "Upgrading of Soshanguve JJ 132/11kV Substation, Ward 33, Region 1"),
    (48, "Region 4", AR24, 101, "City narrative", "Kentron 132/11kV substation, Ward 48, Region 4"),
    (48, "Region 4", AR24, 102, "City narrative", "Figure 5: Kentron 132/11kV substation, Ward 48, Region 4"),
    # public submissions reproduced in MTREF appendices (authored by residents, not the City) -- flagged
    (79, "Region 4", MT22, 981, "public submission in MTREF", "Region 4 - Ward 79 KLOOFSIG"),
    (3, "Region 3", MT22, 983, "public submission in MTREF", "Region 03, Ward 03"),
    (91, "Region 6", MT24, 1088, "public submission in MTREF", "IDP Comments - Region 6 Ward 91"),
    (5, "Region 2", MT24, 1096, "public submission in MTREF", "Ward Councillor – Ward 5 Region 2 South"),
]
REKORD = {"Region 1": [2, 4, 9, 11, 12, 19, 20, 21, 22, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 88, 89, 90, 94, 98],
          "Region 2": [5, 8, 13, 14, 49, 50, 73, 74, 75, 76, 95, 96],
          "Region 5": [89, 99, 100],
          "Region 7": [102, 103, 104, 105]}


def region_major(r: str) -> str:
    """'Region 3B' -> 'Region 3' (the official layer and Rekord list have no 3A/3B split)."""
    m = re.match(r"Region (\d)", str(r))
    return f"Region {m.group(1)}" if m else ""


def evidence() -> pd.DataFrame:
    rows = [dict(ward=w, region=r, region_as_stated=r, source_file=f, pdf_page=pg, evidence_type=t, detail=q)
            for w, r, f, pg, t, q in NARRATIVE]
    p = pd.read_csv(ROOT + "/output/projects.csv")
    # (b) single Appendix O row whose project name states a region and which gives a single ward
    o = pd.read_csv("work/appO_used.csv", index_col=0)
    for r in o[o.ward_category == "single-ward"].itertuples():
        m = re.search(r"Region\s*(\d)\b", str(r.project_name))
        if m and not re.search(r"Regions|Region \d\s*(and|,|&|-)\s*\d", str(r.project_name)):
            rows.append(dict(ward=int(str(r.wards).split(";")[0]), region=f"Region {m.group(1)}", region_as_stated=f"Region {m.group(1)}",
                             source_file=r.source_file, pdf_page=r.page, evidence_type="App O row: project name states region + ward",
                             detail=f"{r.project_name} -> ward {r.wards_raw}"))
    # (a) project rows with a single App O ward AND an SA36/SB19 region tag (joined across documents by WBS)
    q = p[(p.ward_category == "single-ward") & p.region.fillna("").str.match(r"Region \d")]
    for r in q.itertuples():
        rows.append(dict(ward=int(str(r.wards).split(";")[0]), region=region_major(r.region), region_as_stated=r.region,
                         source_file=f"{r.ward_source.split(' (')[0]} + {r.region_source.split(' (')[0]}", pdf_page="",
                         evidence_type="joined: App O ward + SA36/SB19 region tag (same WBS)", detail=r.project_name))
    e = pd.DataFrame(rows)
    e["region"] = e.region.map(region_major)
    return e


def build() -> tuple[pd.DataFrame, pd.DataFrame]:
    e = evidence()
    city = e[e.evidence_type != "public submission in MTREF"]
    off = pd.read_csv("regions/ward_region_overlay.csv")
    off["ward_no"] = off.ward_no.astype(int)
    offd = dict(zip(off.ward_no, off.region_by_area))
    rek = {}
    for reg, ws in REKORD.items():
        for w in ws:
            rek.setdefault(w, []).append(reg)
    out = []
    for w in range(1, 108):
        c = city[city.ward == w]
        counts = c.region.value_counts()
        s1 = ";".join(f"{k} (x{v})" for k, v in counts.items())
        regs = list(counts.index)
        conflict = len(regs) > 1
        rk = rek.get(w, [])
        o_ = offd.get(w, "")
        if len(regs) == 1:
            final, how = regs[0], "step 1: City documents (unanimous)"
        elif conflict:
            final, how = o_, "step 1 conflict -> official e-GIS layer used as tie-break"
        else:
            final, how = o_, "step 3: official e-GIS region layer (no step-1 evidence)"
        out.append(dict(ward=w, step1_city_documents=s1, step1_conflict=conflict,
                        step2_rekord_2021=";".join(rk) + (" (ambiguous: listed twice)" if len(rk) > 1 else ""),
                        step3_official_egis=o_, region_final=final, assignment_basis=how,
                        disagree_step1_vs_rekord=bool(regs) and bool(rk) and any(r_ not in rk for r_ in regs),
                        disagree_final_vs_egis=final != o_))
    return pd.DataFrame(out), e


if __name__ == "__main__":
    t, e = build()
    e.to_csv("work/ward_region_evidence.csv", index=False)
    t.to_csv("work/ward_region_table.csv", index=False)
    print(e.evidence_type.value_counts().to_string())
    print(t.assignment_basis.value_counts().to_string())
    print("step-1 conflicts:"); print(t[t.step1_conflict][["ward", "step1_city_documents", "step2_rekord_2021", "step3_official_egis"]].to_string(index=False))
    print("step1 vs Rekord disagreements:"); print(t[t.disagree_step1_vs_rekord][["ward", "step1_city_documents", "step2_rekord_2021", "step3_official_egis"]].to_string(index=False))
    print("final vs eGIS disagreements:", t.disagree_final_vs_egis.sum())
    print(t[t.disagree_final_vs_egis][["ward", "step1_city_documents", "step3_official_egis", "region_final"]].to_string(index=False))
    rk = {w: r for r, ws in REKORD.items() for w in ws}
    print("Rekord vs eGIS disagreements:", [(w, r, dict(zip(t.ward, t.step3_official_egis))[w]) for r, ws in REKORD.items() for w in ws if dict(zip(t.ward, t.step3_official_egis))[w] != r])
    pub = e[e.evidence_type == "public submission in MTREF"]
    print("public submissions vs final:", [(r.ward, r.region, dict(zip(t.ward, t.region_final))[r.ward]) for r in pub.itertuples()])
