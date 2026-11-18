"""Manual review decisions for budget-row -> Appendix O matches (keyed by annexB_clean row index).
Anything in 'review' not listed here is rejected. Scores < 65 were never correct in review and are rejected."""
import re
import pandas as pd

SAME = "same project, wording differs"
SSP = "same service + place (+ext), wording differs"
CONTRIB = "developer contribution, same township ext"
ACCEPT = {
    "2022/23": {318: SAME, 319: SAME, 286: SAME, 121: SSP, 126: SAME, 13: SAME, 39: SAME, 40: SAME, 41: SAME, 292: SAME,
                55: SSP, 104: SSP, 105: SSP, 110: SSP, 54: SSP, 98: SSP},
    "2023/24": {589: SAME, 432: SAME, 433: SSP, 609: SAME, 360: SAME, 497: SAME, 576: SAME, 487: SAME, 378: SSP,
                371: SAME, 602: SAME, 412: SSP, 401: SSP, 368: SAME, 380: SSP, 376: SSP, 389: SSP, 408: SSP,
                514: "same system (SAP 4 Hana)"},
    "2024/25": {758: SAME, 683: SAME, 684: SSP, 759: "decoded overprint; code agrees (Belle Ombre Ph2)", 876: SAME,
                639: SSP, 661: SSP, 631: SAME, 881: SAME, 781: SAME, 637: SSP, 648: SSP, 660: SSP, 671: SSP,
                620: "decoded overprint (Upgrade Refilwe Stadium); code agrees", 666: SSP,
                851: "2024/25 MTREF Annexure A names it '(Electricity Distribution Loss)'; IDP 714008 agrees (revised on follow-up review)",
                **{i: CONTRIB for i in range(700, 716)}},
}
# generic 'Capital Movables' rows: remap to the App O row of the same department (dept pattern, App O name pattern)
DEPT_REMAP = {
    ("2023/24", 353): ("Office of the City Manager", "Capital Mov"),
    ("2023/24", 446): ("Regional Operations", "Capital Mov"),
    ("2023/24", 358): ("Sports, Recreation", "Capital Mov"),
    ("2024/25", 619): ("Sports, Recreation", "Capital Mov"),
}

if __name__ == "__main__":
    m = pd.read_csv("work/match_all.csv")
    o = pd.read_csv("work/appO_used.csv", index_col=0)
    rows = []
    for x in m.itertuples():
        st, reason, ao = x.status, (x.conflict if isinstance(x.conflict, str) else ""), x.appO_row
        wm = re.search(r"\(710026([A-E])\)", str(x.budget_name))
        if wm:
            L = wm.group(1)
            c = o[(o.year == x.year) & o.project_name.str.contains(rf"Worn-Out Water Network Pipes \(Area[- ]{L}\b", regex=True)]
            if len(c) == 1:
                st, reason, ao = "accept:manual-remap", f"area letter {L} in project code -> App O Area-{L} row", c.index[0]
            else:
                st, reason = "reject:no App O row for area", ""
        elif (x.year, x.left_index) in DEPT_REMAP:
            dp, nm = DEPT_REMAP[(x.year, x.left_index)]
            c = o[(o.year == x.year) & o.department.str.contains(dp) & o.project_name.str.contains(nm, case=False)]
            assert len(c) == 1, (x.year, x.left_index, len(c))
            st, reason, ao = "accept:manual-remap", f"generic name; remapped to App O row of same department ({dp})", c.index[0]
        elif st == "review":
            if x.left_index in ACCEPT.get(x.year, {}):
                st, reason = "accept:manual", ACCEPT[x.year][x.left_index]
            elif x.score < 65:
                st, reason = "reject:low score (<65)", ""
            else:
                st, reason = "reject:manual-review", "different sub-project / generic / ambiguous"
        rows.append(dict(year=x.year, left_index=x.left_index, budget_name=x.budget_name, appO_row=ao, score=x.score,
                         code_agree=x.code_agree, status=st, reason=reason))
    d = pd.DataFrame(rows)
    d.to_csv("work/match_decisions_budget.csv", index=False)
    print(d.status.str.split(":").str[0].groupby(d.year).value_counts().unstack())
