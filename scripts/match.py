"""Fuzzy name matching between project lists, with optional project-code agreement."""
import re
import pandas as pd
from rapidfuzz import fuzz

SYN = [(r"\bga\s*-?\s*rankuwa\b|\bgarankuwa\b", "garankuwa"), (r"\bwinterveldt?\b", "winterveld"),
       (r"\bextension\b|\bext\b\.?|\bunit\b", "x"), (r"\bx\s+(\d)", r"x\1"), (r"\bext\.?\s*(\d)", r"x\1"), (r"\bsub[- ]?station\b", "substation"),
       (r"\bmoveables\b", "movables"), (r"&", " and "), (r"\bwwtw\b", "wastewater treatment works"),
       (r"\bstorm ?water\b", "stormwater"), (r"\bkv\b", "kv")]


def norm(s: str) -> str:
    s = str(s or "").lower()
    s = re.sub(r"\(\s*\d{6}\w?\s*\)", " ", s)
    for a, b in SYN:
        s = re.sub(a, b, s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def score(a: str, b: str) -> float:
    """Blend of token_set and plain ratio, penalising pure-subset matches of generic names."""
    return 0.6 * fuzz.token_set_ratio(a, b) + 0.4 * fuzz.ratio(a, b)


def best_matches(left: pd.DataFrame, right: pd.DataFrame, lname: str, rname: str,
                 lcode: str | None = None, rcode: str | None = None, conflict_fn=None) -> pd.DataFrame:
    """For each left row return the best right row index, score and whether codes agree.
    If conflict_fn is given, candidates whose discriminating tokens conflict are skipped."""
    rn = right[rname].map(norm).tolist()
    rc = right[rcode].astype(str).tolist() if rcode else [None] * len(right)
    out = []
    for i, r in left.iterrows():
        a = norm(r[lname])
        lc = str(r[lcode]) if lcode else None
        best = (-1, -1.0, False)
        for j, (b, c) in enumerate(zip(rn, rc)):
            if conflict_fn is not None and conflict_fn(r[lname], right.iloc[j][rname]):
                continue
            sc = score(a, b)
            code_ok = bool(lc and c and lc not in ("", "nan") and lc == c)
            eff = sc + (8 if code_ok else 0)
            if eff > best[1] + (8 if best[2] else 0):
                best = (j, sc, code_ok)
        out.append(dict(left_index=i, right_pos=best[0], score=round(best[1], 1), code_agree=best[2]))
    return pd.DataFrame(out)
