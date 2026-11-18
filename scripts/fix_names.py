"""Apply hand-decoded names for project rows whose text is overprinted in the source PDFs.
Input: work/annexB.csv, work/name_overrides.csv (year, wbs, clean_name, reason). Output: work/annexB_clean.csv."""
import pandas as pd

d = pd.read_csv("work/annexB.csv")
ov = pd.read_csv("work/name_overrides.csv")
d["raw_project_name"] = d.project_name
d["name_note"] = ""
for r in ov.itertuples():
    if r.wbs == "UPGRADING_MARKET":  # row has no WBS in the source; identified by its garbled text
        m = (d.year == r.year) & d.project_name.str.contains("aUl pPglarn", na=False)
    else:
        m = (d.year == r.year) & (d.wbs == r.wbs) & d.use_row
    if m.sum() != 1:
        print(f"WARNING: override {r.year} {r.wbs} matched {m.sum()} rows")
        continue
    d.loc[m, "project_name"] = r.clean_name
    d.loc[m, "name_note"] = r.reason
d.to_csv("work/annexB_clean.csv", index=False)
print("applied", len(ov))
