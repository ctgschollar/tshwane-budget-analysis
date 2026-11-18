"""Follow-up 2: attribute capex to wards by (i) physical location (Appendix O ward, as before) or (ii) stated service area for
bulk infrastructure, and treat region-only money either (a) unattributed or (b) split across the region's wards by population.

Every row is allocated to: a dict {ward: weight} (weights sum to 1), or the label 'multi-ward', or an unattributed reason."""
import re
import pandas as pd
import analyze as A
from match import norm

T = 80
POP = A.pop22
P = A.p.copy()
WR = pd.read_csv("work/ward_region_table.csv")
REGION_WARDS = {}
for r in WR.itertuples():
    REGION_WARDS.setdefault(r.region_final, []).append(int(r.ward))
TWN = pd.read_csv("townships/ward_township_overlap_all.csv")
TWN["ward"] = TWN.ward_no.astype(int) - 79900000
BEN_FILE = "work/bulk_beneficiaries_final.csv"   # reviewed beneficiary statements (built by part2_beneficiaries.py)

# region tag for 2024/25 Appendix N rows: borrow from the same-year budget row with the same normalised name
_b25 = P[(P.year == "2024/25") & P.record_type.str.startswith("budget") & P.region.fillna("").str.match(r"Region \d")]
REGION_BY_NAME_2425 = dict(zip(_b25.project_name.map(norm), _b25.region))


def regions_in_text(s: str) -> list[str]:
    """Regions explicitly named in a project title, e.g. 'Area-C Regions 4, 5, 6 and 7' -> [4,5,6,7]."""
    s = str(s)
    out = []
    for m in re.finditer(r"Regions?\s*((?:\d\s*[AB]?\s*(?:,|and|&|-)?\s*)+)", s):
        out += [f"Region {d}" for d in re.findall(r"\d", m.group(1))]
    return sorted(set(out))


def region_split(regions: list[str]) -> dict[int, float]:
    wards = sorted({w for r in regions for w in REGION_WARDS.get(re.sub(r"[AB]$", "", r), [])})
    tot = sum(POP[w] for w in wards)
    return {w: POP[w] / tot for w in wards} if tot else {}


def township_split(township: str) -> dict[int, float]:
    t = TWN[TWN.township == township]
    tot = t.pct_of_township_pop2011_in_ward.sum()
    return {int(r.ward): r.pct_of_township_pop2011_in_ward / tot for r in t.itertuples() if r.pct_of_township_pop2011_in_ward > 0}


def row_regions(r: pd.Series) -> tuple[list[str], str]:
    """Region(s) a non-ward-attributed row belongs to, and the evidence."""
    appo_name = str(r.ward_source).split("'")[1] if "'" in str(r.ward_source) else ""
    named = regions_in_text(r.project_name) or regions_in_text(appo_name)
    if named:
        return named, "region(s) named in project title"
    if isinstance(r.region, str) and re.match(r"Region \d", r.region):
        return [r.region], f"SA36/SB19 'Ward Location' tag ({r.region_source})"
    if r.record_type.startswith("adjusted+actual"):
        reg = REGION_BY_NAME_2425.get(norm(r.project_name))
        if reg:
            return [reg], "SA36 tag of same-named 2024/25 MTREF row"
    return [], ""


def load_beneficiaries() -> dict[str, dict]:
    """project-name key -> {'alloc': {ward: w} | None, 'regions': [...], 'evidence': str}"""
    import os
    out = {}
    if not os.path.exists(BEN_FILE):
        return out
    b = pd.read_csv(BEN_FILE)
    for r in b.itertuples():
        out[norm(r.project_key)] = dict(kind=r.kind, target=r.target, basis=r.basis,
                                        evidence=f"{r.source_file} p{r.pdf_page}: \"{r.quote}\"" if r.basis == "narrative" else f"project title: \"{r.quote}\"")
    return out


BEN = load_beneficiaries()


INCLUDE_TITLES = False


def bulk_beneficiary(r: pd.Series) -> dict | None:
    n = norm(re.sub(r"^\(\d+\w?\)\s*", "", str(r.project_name)))
    for k, v in BEN.items():
        if n.startswith(k) and (INCLUDE_TITLES or v["basis"] == "narrative"):
            return v
    return None


def allocate(r: pd.Series, basis: str, region_mode: str) -> tuple[object, str]:
    """basis: 'location' | 'service'; region_mode: 'a' (unattributed) | 'b' (population split)."""
    named = set(regions_in_text(r.project_name)) | set(regions_in_text(str(r.ward_source)))
    named_multi = len(named) > 1
    if r.ward_category == "single-ward" and len(named) == 1:
        w0 = int(str(r.wards).split(";")[0])
        reg_wards = {w for g in named for w in REGION_WARDS.get(g, [])}
        named_multi = w0 not in reg_wards     # title names a region that does not contain the App O ward
    if basis == "service" and r.bulk_infrastructure_name_flag:
        bnf = bulk_beneficiary(r)
        if bnf is None:
            return "unattributed: bulk, no stated beneficiary", ""
        if bnf["kind"] == "wards":
            ws = [int(x) for x in str(bnf["target"]).split(";")]
            tot = sum(POP[w] for w in ws)
            return {w: POP[w] / tot for w in ws}, bnf["evidence"]
        if bnf["kind"] == "township":
            alloc = {}
            towns = str(bnf["target"]).split(";")
            tp = {t: TWN[TWN.township == t].pop2011_overlap_est.sum() for t in towns}
            for t in towns:
                for w, x in township_split(t).items():
                    alloc[w] = alloc.get(w, 0) + x * tp[t] / sum(tp.values())
            return alloc, bnf["evidence"]
        if bnf["kind"] == "regions":
            if region_mode == "a":
                return "unattributed: region-only", bnf["evidence"]
            return region_split(str(bnf["target"]).split(";")), "population split; " + bnf["evidence"]
        return "unattributed: bulk, beneficiary city-wide/unmappable", bnf["evidence"]
    # location basis (and non-bulk rows under service basis)
    if r.ward_category == "single-ward" and not named_multi:
        return {int(str(r.wards).split(";")[0]): 1.0}, "Appendix O ward"
    if r.ward_category == "multi-ward":
        return "multi-ward", "Appendix O"
    if r.ward_category in ("city-wide", "administrative-hq"):
        return f"unattributed: {r.ward_category}", "Appendix O"
    regs, ev = row_regions(r)
    if regs:
        if region_mode == "a":
            return "unattributed: region-only", ev
        return region_split(regs), "population split; " + ev
    return f"unattributed: {r.ward_category}", ""


def run(basis: str, region_mode: str, t: float = T) -> pd.DataFrame:
    black = {w for w, v in A.pct22.items() if v >= t}
    bpop = sum(POP[w] for w in black)
    opop = sum(v for w, v in POP.items() if w not in black)
    out = []
    for lab, y, rt, col in A.MEASURES:
        d = A.rows_for(y, rt)
        B = O = M = 0.0
        un = {}
        for _, r in d.iterrows():
            v = r[col]
            if pd.isna(v) or v == 0:
                continue
            a, _ = allocate(r, basis, region_mode)
            if isinstance(a, dict):
                for w, x in a.items():
                    if w in black:
                        B += v * x
                    else:
                        O += v * x
            elif a == "multi-ward":
                M += v
            else:
                un[a] = un.get(a, 0) + v
        tot = d[col].sum()
        row = dict(measure=lab, total_Rm=tot / 1e6, black_Rm=B / 1e6, other_Rm=O / 1e6, multiward_Rm=M / 1e6,
                   attributed_pct=(B + O) / tot * 100, black_share=B / (B + O) * 100,
                   percap_ratio=(B / bpop) / (O / opop), unattributed_pct=sum(un.values()) / tot * 100)
        for k, v in un.items():
            row[k.replace("unattributed: ", "un_") + "_Rm"] = v / 1e6
        out.append(row)
    return pd.DataFrame(out)


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    for basis in ("location", "service"):
        for mode in ("a", "b"):
            print(f"## basis={basis} region_mode={mode}")
            print(run(basis, mode).round(1).to_string(index=False))
