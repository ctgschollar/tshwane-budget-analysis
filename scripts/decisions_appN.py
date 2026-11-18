"""Match 2024/25 Appendix N rows to 2024/25 Appendix O and apply manual decisions."""
import re
import pandas as pd
from match import best_matches, norm
from run_match import conflict

SAME = "same project, wording differs"
SSP = "same service + place (+ext), wording differs"
ACCEPT = {128: "same 600-unit project, same ward as App N", 122: "same block (App O adds phase label)", 132: SSP, 133: SSP,
          141: "same feeder (word order)", 173: SAME, 86: SSP, 105: "same SEZ programme; same ward as App N",
          165: "same Tsosoloso project (same WBS 9.803900.1.W.WA.03.2 in 2023/24 adj. budget and 2024/25 MTREF)",
          **{i: "developer contribution, same township ext" for i in (36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50)}}
DEPT_REMAP = {0: ("Sports, Recreation", "Capital Mov"), 4: ("Office of the City Manager", "Capital Mov"),
              30: ("Group Financial", "Capital mov"), 155: ("Regional Operations", "Capital Mov"),
              2: ("Health Services", "Capital Funded from Operating")}

if __name__ == "__main__":
    n = pd.read_csv("work/appN_2425.csv")
    o = pd.read_csv("work/appO_used.csv", index_col=0)
    oy = o[o.year == "2024/25"]
    m = best_matches(n, oy.reset_index(drop=True), "project_name", "project_name", conflict_fn=conflict)
    m["appO_row"] = oy.index.values[m.right_pos]
    multi = oy.assign(k=oy.project_name.map(norm)).groupby("k").wards_raw.nunique()
    rows, unreviewed = [], []
    for x in m.itertuples():
        full = n.loc[x.left_index, "project_name"]
        aname = o.loc[x.appO_row, "project_name"]
        nonuniq = multi.get(norm(aname), 1) > 1
        ao, reason = x.appO_row, ""
        a = re.search(r"Area[- ]?([A-E])\b", full)
        if "Worn-Out" in full and a:
            c = oy[oy.project_name.str.contains(rf"Worn-Out Water Network Pipes \(Area[- ]{a.group(1)}\b", regex=True)]
            st, reason, ao = ("accept:manual-remap", f"area letter {a.group(1)} -> App O Area-{a.group(1)} row", c.index[0]) if len(c) == 1 else ("reject:no App O row for area", "", ao)
        elif x.left_index in DEPT_REMAP:
            dp, nm = DEPT_REMAP[x.left_index]
            c = oy[oy.department.str.contains(dp) & oy.project_name.str.contains(nm, case=False)]
            assert len(c) == 1, (x.left_index, len(c))
            st, reason, ao = "accept:manual-remap", f"generic name; remapped to App O row of same department ({dp})", c.index[0]
        elif x.score >= 95 and not nonuniq:
            st = "accept:auto>=95"
        elif x.left_index in ACCEPT:
            st, reason = "accept:manual", ACCEPT[x.left_index]
        elif x.score < 65:
            st = "reject:low score (<65)"
        else:
            st, reason = "reject:manual-review", "different project / generic / ambiguous"
            unreviewed.append((x.left_index, round(x.score), full[:60], aname[:60], o.loc[x.appO_row, "wards_raw"]))
        rows.append(dict(appN_index=x.left_index, appN_name=full, dominant_ward=n.loc[x.left_index, "dominant_ward"],
                         appO_row=ao, score=x.score, status=st, reason=reason))
    d = pd.DataFrame(rows)
    d.to_csv("work/match_decisions_appN.csv", index=False)
    print(d.status.str.split(":").str[0].value_counts().to_dict())
    print("rejected after review (check):")
    for u in unreviewed:
        print("  ", u)
