"""Match budget rows (Annexure A/B) to same-year Appendix O ward lists. Writes candidate matches with rule-based status."""
import re
import sys
import pandas as pd
from match import best_matches, norm

SERVICE = {"water", "sewer", "sanitation", "sewerage", "roads", "road", "stormwater", "electricity", "reservoir",
           "substation", "clinic", "stadium", "hostels", "lighting", "toilets", "bulk", "reticulation", "provision"}
PLACES = {"winterveld", "garankuwa", "mabopane", "soshanguve", "mamelodi", "atteridgeville", "saulsville", "refilwe",
          "ekangala", "zithobeni", "olievenhoutbosch", "hammanskraal", "temba", "babelegi", "kudube", "fort", "fortwest",
          "pretorius", "nellmapius", "nelmapius", "pienaarspoort", "kopanong", "booysens", "andeon", "rama", "gatsebe",
          "ga", "tsebe", "rooiwal", "klipgat", "baviaanspoort", "sunderland", "rietspruit", "silver", "zwavelpoort",
          "kentron", "wildebees", "ifafi", "wapadrand", "mooikloof", "pyramid", "rosslyn", "saulsville", "monavoni",
          "kwagga", "denneboom", "belle", "mahube", "thorntree", "laudium", "garsfontein", "klapperkop", "babelegi",
          "stinkwater", "matenteng", "ramotse", "cullinan", "rayton", "sinoville", "lusaka", "eersterust", "marabastad",
          "caledonian", "kameelfontein", "midtown", "lotusgardens", "montana", "heatherview", "annlin", "wolmer",
          "amandasig", "heuweloord", "menlo", "willow", "bronkhorstspruit", "roodeplaat", "rietvlei", "bronkhorstbaai"}


def discriminators(name: str) -> tuple[set, set, set]:
    t = set(norm(name).split())
    nums = set(re.findall(r"\bx\d+\b|\bunit \d+|\barea [a-e]\b|\barea \d+|\bsection \d|\bzone \d+|\bregion \d\b|\bphase ?\d\b|\bblock [a-z]+\b",
                          norm(name)))
    # drop 'water' as a service word when it appears only inside 'water network pipes' etc. -- keep simple
    return t & SERVICE & {"water", "sewer", "sanitation", "roads", "stormwater", "electricity", "reservoir",
                          "substation"}, t & PLACES, nums


def conflict(a: str, b: str) -> str:
    sa, pa, na = discriminators(a)
    sb, pb, nb = discriminators(b)
    if sa and sb and not (sa & sb):
        return f"service differs {sorted(sa)} vs {sorted(sb)}"
    if pa and pb and not (pa & pb):
        return f"place differs {sorted(pa)} vs {sorted(pb)}"
    if na and nb and na != nb:
        return f"number/area differs {sorted(na)} vs {sorted(nb)}"
    return ""


if __name__ == "__main__":
    a = pd.read_csv("work/annexB_clean.csv")
    a = a[a.use_row].copy()
    a["idp"] = a.wbs.astype(str).str.extract(r"^9\.(\d{6})")[0]
    o = pd.read_csv("work/appO.csv", dtype={"idp_number": str}).fillna({"idp_number": "", "wards_raw": ""})
    o["idp_number"] = o.idp_number.str.replace(r"\.0$", "", regex=True)
    o = o[o.ward_category != "unspecified"].reset_index(drop=True)
    o.to_csv("work/appO_used.csv")
    res = []
    for y in ("2022/23", "2023/24", "2024/25"):
        ay = a[a.year == y]
        oy = o[o.year == y]
        m = best_matches(ay, oy.reset_index(drop=True), "project_name", "project_name", "idp", "idp_number", conflict_fn=conflict)
        m["appO_row"] = oy.index.values[m.right_pos]
        m["year"] = y
        m["budget_name"] = ay.project_name.values
        m["budget_dept"] = ay.department.values
        m["appO_name"] = o.loc[m.appO_row, "project_name"].values
        m["appO_dept"] = o.loc[m.appO_row, "department"].values
        m["appO_wards"] = o.loc[m.appO_row, "wards_raw"].values
        m["orig"] = ay.original_budget.values
        m["adj"] = ay.adjusted_budget.values
        m["ambiguous_note"] = ay.name_note.fillna("").str.startswith("ambiguous").values
        # generic names: same normalised App O name appears with >1 distinct ward value this year
        oy_n = oy.assign(n=oy.project_name.map(norm))
        multi = oy_n.groupby("n").wards_raw.nunique()
        m["appO_name_nonunique"] = m.appO_name.map(lambda s: multi.get(norm(s), 1) > 1)
        m["conflict"] = [conflict(x, z) for x, z in zip(m.budget_name, m.appO_name)]
        st = []
        for r in m.itertuples():
            if r.ambiguous_note:
                st.append("reject:ambiguous-name")
            elif r.conflict:
                st.append("reject:" + r.conflict)
            elif r.score >= 95 and not r.appO_name_nonunique:
                st.append("accept:auto>=95")
            else:
                st.append("review")
        m["status"] = st
        res.append(m)
    out = pd.concat(res)
    out.to_csv(sys.argv[1], index=False)
    for y, g in out.groupby("year"):
        print(y, g.status.str.split(":").str[0].value_counts().to_dict(),
              "| orig R m:", g.groupby(g.status.str.split(":").str[0]).orig.sum().div(1e6).round(0).to_dict())
