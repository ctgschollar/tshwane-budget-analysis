"""Extract the Moya-era project-level capital tables (same machinery as ex_annexB.py), incl. the City 'Regions' column.
Writes work/annex_new.csv and prints reconciliation to each document's printed 'Total Capex Budget'."""
import re
import sys
import pandas as pd
from ex_annexB import extract

NEW = {
    "2024/25adj": dict(fy="2024/25", file="07.-Proposed-2024-2025-Adjustment-Budget.pdf", pages=range(135, 140),
                       bands=dict(dept=(40, 190), name=(190, 418), wbs=(418, 488), fund=(488, 520), orig=(520, 570),
                                  ftr=(570, 612), cur=(612, 670), adjm=(670, 722), adjd=(722, 800)),
                       stated=(2347552576, 2312623791), stated_where="Annexure B p139"),
    "2025/26": dict(fy="2025/26", file="02.-2025-2026-MTREF-for-the-City-of-Tshwane-Special-Council-29-05-2025.pdf",
                    pages=range(64, 71),
                    bands=dict(dept=(40, 178), name=(178, 350), wbs=(350, 415), fund=(415, 445), orig=(445, 486),
                               adjm=(9998, 9999), adjd=(9998, 9999), b1=(486, 528), b2=(528, 570), tot=(570, 625),
                               region=(625, 700)),
                    stated=(2459328252, 0), stated_where="Annexure A p70"),
    "2025/26adj": dict(fy="2025/26", file="10.-2025-2026-Adjustment-Budget.pdf", pages=range(144, 151),
                       bands=dict(dept=(40, 162), name=(162, 338), wbs=(338, 410), fund=(410, 470), orig=(470, 505),
                                  ftr=(505, 548), cur=(548, 600), adjm=(600, 660), adjd=(660, 697), region=(697, 745)),
                       skip=r"Capital Budget Annexure", stated=(2459328252, 2768935587), stated_where="Annexure B p150"),
    "2026/27": dict(fy="2026/27", file="02.-2026-2027-MTREF-for-CoT-Final-1.pdf", pages=range(66, 73),
                    bands=dict(dept=(40, 162), name=(162, 335), wbs=(335, 396), fund=(396, 465), orig=(465, 510),
                               adjm=(9998, 9999), adjd=(9998, 9999), b1=(510, 570), b2=(570, 640), tot=(640, 707),
                               region=(707, 770)),
                    stated=(2856300538, 0), stated_where="Annexure A p72"),
}


def norm_region(raw: str) -> str:
    s = re.sub(r"\s+", " ", str(raw or "")).strip()
    m = re.findall(r"Region\s*(\d)", s)
    if m:
        return ";".join(f"Region {x}" for x in sorted(set(m)))
    if re.search(r"Multiple\s*regions", s, re.I):
        return "Multiple regions"
    if re.search(r"Tshwane\s*Wide|City\s*Wide", s, re.I):
        return "Tshwane Wide"
    if re.search(r"Administrative", s, re.I):
        return "Administrative"
    return ""


if __name__ == "__main__":
    out = []
    for k, d in NEW.items():
        df, totals = extract(k, d)
        df["region_city"] = df.region_raw.map(norm_region)
        used = df[df.use_row]
        gt = [t for t in totals if t["label"].startswith("Total Capex")]
        so, sa = d["stated"]
        print(f"{k}: rows {len(df)} used {len(used)} head-fallbacks {(df.note.str.startswith('head row')).sum()}")
        print(f"   extracted orig {used.original_budget.sum():,.0f} adj {used.adjusted_budget.sum():,.0f} | stated orig {so:,.0f} adj {sa:,.0f} ({d['stated_where']}) | printed {gt}")
        dt = [t for t in totals if t["label"] == "Total"]
        print(f"   sum of 'Total' rows: orig {sum(t['orig'] or 0 for t in dt):,.0f} adj {sum(t['adjd'] or 0 for t in dt):,.0f}")
        if "region" in d["bands"]:
            print("   region tags (used rows):", used.region_city.replace("", "(none)").value_counts().to_dict())
        out.append(df)
    pd.concat(out).to_csv(sys.argv[1], index=False)
