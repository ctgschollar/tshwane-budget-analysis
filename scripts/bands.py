"""Generic helpers: group pdfplumber words into lines and assign them to x-bands (columns)."""
import re
import pdfplumber

NUM_RE = re.compile(r"[\d,\s]+")


def page_lines(page: pdfplumber.page.Page, ytol: float = 2.5) -> list[list[dict]]:
    """Return words grouped into visual lines, de-duplicating overlaid duplicate words."""
    seen = set()
    words = []
    for w in page.extract_words(keep_blank_chars=False, use_text_flow=False, y_tolerance=1):
        key = (round(w["x0"], 0), round(w["top"], 0), w["text"])
        if key in seen:
            continue
        seen.add(key)
        words.append(w)
    words.sort(key=lambda w: (w["top"], w["x0"]))
    lines: list[list[dict]] = []
    for w in words:
        if lines and abs(lines[-1][0]["top"] - w["top"]) <= ytol:
            lines[-1].append(w)
        else:
            lines.append([w])
    return [sorted(l, key=lambda w: w["x0"]) for l in lines]


def bucket(line: list[dict], bands: dict[str, tuple[float, float]]) -> dict[str, str]:
    """Assign each word to the band containing its x-centre; join texts with spaces."""
    out = {k: [] for k in bands}
    for w in line:
        xc = (w["x0"] + w["x1"]) / 2
        for k, (a, b) in bands.items():
            if a <= xc < b:
                out[k].append(w["text"])
                break
    return {k: " ".join(v).strip() for k, v in out.items()}


def money(s: str) -> float | None:
    """Parse an amount cell; split digits ('2 00,000') are re-joined. '-' alone -> 0. Empty -> None.
    Returns the ABSOLUTE value (signs are not reliable in these layouts)."""
    s = s.strip()
    if not s:
        return None
    digits = re.sub(r"[^\d]", "", s)
    if not digits:
        return 0.0
    return float(digits)


def money_signed(s: str) -> float | None:
    """Like money() but negative if the cell contains a minus sign or parentheses before digits."""
    v = money(s)
    if v is None:
        return None
    if re.search(r"(^|\s)[-–(]", s.strip()) or s.strip().startswith(("-", "–", "(")):
        return -v
    return v
