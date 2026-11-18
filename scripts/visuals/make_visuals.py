"""General-audience visual summary of the v2 Tshwane capital-budget analysis.

Reads ONLY existing outputs (no recomputation): v2_index.csv, v2_bands.csv, v2_drivers.csv, ward_classification.csv and
v2_alloc_labelled.csv (row-level allocation with a placement label; reconciled exactly to v2_bands / v2_index before use).
Headline basis throughout: service area, region-level money split by population (option A, basis 'service', mode 'b').

Writes output/visuals/: report.html (offline, Plotly embedded), chart PNGs 1600px wide with a footer strip,
headline_figures.md. Colours validated with the dataviz skill's validate_palette.js (party slots: categorical, light;
band ramp: --ordinal)."""
import html
import os
import re
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image, ImageDraw, ImageFont
ROOT = os.environ.get("TSHWANE_ROOT", os.path.expanduser("~/Documents/tshwane"))  # project folder: PDFs + output/

OUT = ROOT + "/output/"
VIS = OUT + "visuals/"
os.makedirs(VIS, exist_ok=True)
FONT_FILE = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_FAMILY = "Noto Sans, Segoe UI, Roboto, Helvetica, Arial, sans-serif"

IX = pd.read_csv(OUT + "v2_index.csv")
BD = pd.read_csv(OUT + "v2_bands.csv")
DR = pd.read_csv(OUT + "v2_drivers.csv")
WC = pd.read_csv(OUT + "ward_classification.csv")
AL = pd.read_csv(OUT + "v2_alloc_labelled.csv")


def hsel(d: pd.DataFrame) -> pd.DataFrame:
    """Headline basis: service area, region money population-split."""
    return d[(d.option == "A") & (d.basis == "service") & (d["mode"] == "b")]


IXH = hsel(IX).set_index("column")
CITY = round(float((IXH.spend_weighted - IXH.gap_vs_city).iloc[0]), 1)   # Tshwane population-weighted mean, 82.7

BUDGETS = [  # (data column, plain label, mayor, kind)
    ("2022/23 original", "2022/23 – Williams (DA)", "Williams", "original"),
    ("2022/23 adjusted", "2022/23 adjusted – Williams (DA)", "Williams", "adjusted"),
    ("2023/24 original", "2023/24 – Brink (DA)", "Brink", "original"),
    ("2023/24 adjusted", "2023/24 adjusted – Brink (DA)", "Brink", "adjusted"),
    ("2024/25 original", "2024/25 – Brink (DA)", "Brink", "original"),
    ("2024/25 adjusted (adj. budget)", "2024/25 adjusted – Moya (ActionSA)", "Moya", "adjusted"),
    ("2025/26 original", "2025/26 – Moya (ActionSA)", "Moya", "original"),
    ("2025/26 adjusted", "2025/26 adjusted – Moya (ActionSA)", "Moya", "adjusted"),
    ("2026/27 original", "2026/27 – Moya (ActionSA)", "Moya", "original"),
]
ACTUAL = "2024/25 actual"
ACTUAL_LABEL = "Actual spending, Jul 2024–Jun 2025 (both mayors)"
PARTY = {"Williams": "#184f95", "Brink": "#5598e7", "Moya": "#eb6834"}
PARTY_TINT = {"Williams": "#8ba7ca", "Brink": "#b0cdf3", "Moya": "#f5b49a"}
PARTY_NAME = {"Williams": "Williams (DA)", "Brink": "Brink (DA)", "Moya": "Moya (ActionSA)"}
BAND_ORDER = ["0–20", "20–40", "40–60", "60–80", "80–100"]
BAND_COL = dict(zip(BAND_ORDER, ["#62bd9a", "#3aa37e", "#228464", "#16664c", "#0c4634"]))
MID = ["In a specific ward", "Spread across an area (by population)", "Listed for several areas, not divided",
       "Citywide or admin", "Not placeable"]
GREY = dict(zip(MID, ["#6b6a66", "#8f8e88", "#b0afa8", "#a29f95", "#3d3c39"]))
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"

COV = hsel(IX)[hsel(IX).column != "2024/25 adjusted (App N, final)"].attributed_pct
COV_LO, COV_HI = int(round(COV.min())), int(round(COV.max()))
FOOTER = (f"Capital budgets only (not day-to-day services). About {COV_LO}–{COV_HI}% of each budget could be linked to specific "
          "areas. Source: City of Tshwane budget documents and annual reports 2022/23–2026/27; Stats SA 2022 ward estimates.")
REPO = "github.com/ctgschollar/tshwane-budget-analysis"
REPO_URL = "https://github.com/ctgschollar/tshwane-budget-analysis"
AI_SHORT = "Made with AI (Anthropic's Claude) under the author's direction."
AI_LONG = ("The data extraction, analysis code, charts and write-up in this project were produced by an AI system (Anthropic's "
           "Claude), working under my direction. I set the questions and method choices and reviewed the results, but I did not "
           "write the code or calculations by hand. AI can make mistakes: every figure is meant to be traceable to a page in the "
           "source documents, and corrections are welcome via GitHub issues.")
R13 = "Excludes a R13m Refilwe roads item that the City's adjustment budget counts in its total but omits from its project list."
NOTE_WILLIAMS = ("The 2022/23 budget was adopted under Williams; Brink took office in March 2023. The 2022/23 mid-year adjustment "
                 "was prepared before early March 2023; the documents do not give its adoption date.")
NOTE_2425 = "The 2024/25 budget was adopted under Brink; its mid-year adjustment was made under Moya."

FS = 1.0   # font scale: 1.0 for PNG (phone-legible at 1600px), smaller for the HTML page


def fz(n: float) -> int:
    return int(round(n * FS))


def layout(fig: go.Figure, title: str, subtitle: str, height: int, top: int = 200) -> go.Figure:
    fig.update_layout(template="plotly_white", paper_bgcolor=SURF, plot_bgcolor=SURF, height=height,
                      font=dict(family=FONT_FAMILY, size=fz(30), color=INK), hoverlabel=dict(font_size=fz(24)),
                      title=dict(text=f"<b>{title}</b><br><span style='font-size:{fz(28)}px;color:{INK2}'>{subtitle}</span>",
                                 x=0.015, xanchor="left", yref="container", y=1 - fz(80) / height, yanchor="middle",
                                 font=dict(size=fz(44))),
                      margin=dict(t=top, b=60, l=40, r=50))
    return fig


# ---------------- chart 1 ----------------
def chart1() -> tuple[go.Figure, list[str]]:
    cats = [l for _, l, _, _ in BUDGETS] + [ACTUAL_LABEL]
    fig = go.Figure()
    seen = set()
    for c, lab, mayor, kind in BUDGETS:
        g = float(IXH.loc[c, "gap_vs_city"])
        adj = kind == "adjusted"
        fig.add_bar(y=[lab], x=[g], orientation="h", name=PARTY_NAME[mayor], legendgroup=mayor,
                    showlegend=(not adj and mayor not in seen),
                    marker=dict(color=PARTY_TINT[mayor] if adj else PARTY[mayor], line=dict(color=PARTY[mayor], width=3),
                                pattern=dict(shape="/" if adj else "", fgcolor=PARTY[mayor], size=14, solidity=0.3)),
                    text=[f"{g:+.1f}"], textposition="outside", textfont=dict(size=fz(32), color=INK), cliponaxis=False,
                    customdata=[[float(IXH.loc[c, 'spend_weighted'])]],
                    hovertemplate=f"{lab}<br>Budget's number: %{{customdata[0]:.1f}}%<br>Difference from 82.7: %{{x:+.1f}} points<extra></extra>")
        if not adj:
            seen.add(mayor)
    fig.add_bar(y=[None], x=[None], orientation="h", name="Mid-year adjustment (lighter, hatched)",
                marker=dict(color="#e4e3df", line=dict(color=INK2, width=3), pattern=dict(shape="/", fgcolor=INK2, size=14, solidity=0.3)))
    act = float(IXH.loc[ACTUAL, "gap_vs_city"])
    fig.add_scatter(y=[ACTUAL_LABEL], x=[act], mode="markers+text", name="Actual spending (spans both mayors)",
                    marker=dict(symbol="diamond", size=fz(34), color="#ffffff", line=dict(color=INK, width=4)),
                    text=[f"{act:+.1f}"], textposition="middle right", textfont=dict(size=fz(32)), cliponaxis=False,
                    hovertemplate=f"{ACTUAL_LABEL}<br>%{{x:+.1f}} points<extra></extra>")
    xs = [float(IXH.loc[c, "gap_vs_city"]) for c, *_ in BUDGETS] + [act]
    fig.update_yaxes(categoryorder="array", categoryarray=cats[::-1], tickfont=dict(size=fz(28)), showgrid=False, ticksuffix="  ")
    fig.update_xaxes(range=[min(xs + [0]) - 1.5, max(xs) + 1.8], gridcolor=GRID, zeroline=False, tickfont=dict(size=fz(26)),
                     title=dict(text="Points above / below where people live", font=dict(size=fz(28))))
    fig.add_vline(x=0, line=dict(color=INK, width=4))
    fig.add_annotation(x=0, y=1.0, yref="paper", text="matches population (82.7%)", showarrow=False, xanchor="left", xshift=8,
                       yanchor="bottom", font=dict(size=fz(26), color=INK))
    g25 = float(IXH.loc["2025/26 adjusted", "gap_vs_city"])
    fig.add_annotation(x=g25, y="2025/26 adjusted – Moya (ActionSA)", text="† excludes a R13m item (see note)", showarrow=False,
                       xanchor="left", xshift=fz(100), font=dict(size=fz(24), color=INK2))
    layout(fig, "How each budget compares with where people live",
           "Above zero: money leans toward Blacker wards. Below zero: it leans away.", 1500, top=300)
    fig.update_layout(bargap=0.28, legend=dict(orientation="h", xref="container", x=0.015, xanchor="left",
                                                yref="container", y=1 - fz(150) / 1500, yanchor="top",
                                                font=dict(size=fz(26)), traceorder="normal"),
                      margin=dict(l=40, r=60))
    return fig, [NOTE_WILLIAMS, "† " + R13]


# ---------------- chart 2 ----------------
PAIRS = [("2022/23", "2022/23 original", "2022/23 adjusted", "Williams", "Williams"),
         ("2023/24", "2023/24 original", "2023/24 adjusted", "Brink", "Brink"),
         ("2024/25", "2024/25 original", "2024/25 adjusted (adj. budget)", "Brink", "Moya"),
         ("2025/26", "2025/26 original", "2025/26 adjusted", "Moya", "Moya")]


def chart2() -> tuple[go.Figure, list[str]]:
    fig = go.Figure()
    xs = []
    n = len(PAIRS)
    for i, (yr, o, a, mo, ma) in enumerate(PAIRS):
        g0, g1 = float(IXH.loc[o, "gap_vs_city"]), float(IXH.loc[a, "gap_vs_city"])
        xs += [g0, g1]
        y = n - i
        fig.add_annotation(x=g1, y=y, ax=g0, ay=y, xref="x", yref="y", axref="x", ayref="y", showarrow=True, text="",
                           arrowhead=2, arrowsize=1.1, arrowwidth=6, arrowcolor=PARTY[ma], standoff=fz(14))
        fig.add_scatter(x=[g0], y=[y], mode="markers", showlegend=False, marker=dict(size=fz(30), color=PARTY[mo], line=dict(color="#fff", width=3)),
                        hovertemplate=f"{yr} as adopted – {PARTY_NAME[mo]}: %{{x:+.1f}}<extra></extra>")
        fig.add_scatter(x=[g1], y=[y], mode="markers", showlegend=False,
                        marker=dict(size=fz(30), color=PARTY_TINT[ma], line=dict(color=PARTY[ma], width=4)),
                        hovertemplate=f"{yr} after mid-year adjustment – {PARTY_NAME[ma]}: %{{x:+.1f}}<extra></extra>")
        fig.add_annotation(x=(g0 + g1) / 2, y=y, text=f"<b>{g1 - g0:+.1f} points</b>{' †' if yr == '2025/26' else ''}",
                           showarrow=False, yshift=fz(42), font=dict(size=fz(30)), bgcolor=SURF)
        who = PARTY_NAME[ma] if mo == ma else f"{PARTY_NAME[mo]} budget,<br>adjusted under {PARTY_NAME[ma]}"
        fig.add_annotation(x=0, xref="paper", y=y, text=f"<b>{yr}</b><br><span style='font-size:{fz(24)}px;color:{INK2}'>{who}</span>",
                           showarrow=False, xanchor="right", xshift=-24, align="right", font=dict(size=fz(30)))
    fig.update_xaxes(range=[min(xs + [0]) - 1.2, max(xs + [0]) + 1.2], gridcolor=GRID, zeroline=True, zerolinecolor=INK, zerolinewidth=4,
                     tickfont=dict(size=fz(26)), title=dict(text="Points above / below where people live (0 = 82.7%)", font=dict(size=fz(28))))
    fig.update_yaxes(visible=False, range=[0.4, n + 0.75])
    layout(fig, "Mid-year changes",
           "Dot = budget as adopted. Arrow head = after the mid-year adjustment.", 1250, top=200)
    fig.update_layout(margin=dict(l=fz(460), r=50))
    return fig, ["Councils revise budgets mid-year, often moving money away from projects that are running late.", NOTE_2425, "† " + R13]


# ---------------- chart 3: Sankey ----------------
UNATT = {"unattributed: city-wide": "Citywide or admin", "unattributed: administrative-hq": "Citywide or admin",
         "unattributed: bulk, no stated beneficiary": "Not placeable", "unattributed: unmatched": "Not placeable",
         "unattributed: no-intersect": "Not placeable", "unattributed: bulk, beneficiary city-wide/unmappable": "Not placeable",
         "multi-ward": "Listed for several areas, not divided"}
PLACE = {"named ward": "In a specific ward", "region split": "Spread across an area (by population)",
         "township split": "Spread across an area (by population)"}
SANKEY_COLS = [("2023/24 original", "2023/24 – Brink (DA)"), ("2024/25 original", "2024/25 – Brink (DA)"),
               ("2025/26 original", "2025/26 – Moya (ActionSA)")]
WARD_BAND = dict(zip(WC.ward, WC.band_headline))
SANKEY_NOTES = ["Spreading money across an area assumes each resident of the area benefits equally.",
                "Infrastructure is counted where its users live, not where it is built: for example, the Rooiwal treatment works "
                "is counted for Temba and Hammanskraal, which it serves.",
                "Green bands: wards grouped by the share of residents who are Black African (Stats SA 2022 ward estimates)."]


def sankey_data(col: str) -> tuple[dict, dict, float]:
    d = hsel(AL[AL.column == col])
    placed = d[d.ward > 0].assign(mid=lambda x: x.placement.map(PLACE), band=lambda x: x.ward.map(WARD_BAND))
    un = d[d.ward < 0].assign(mid=lambda x: x.unattributed.map(UNATT))
    assert placed.mid.notna().all() and un.mid.notna().all(), (col, set(un[un.mid.isna()].unattributed))
    vb = hsel(BD[(BD.column == col) & (BD.scheme == "headline")]).set_index("band").Rm
    assert ((placed.groupby("band").R.sum() / 1e6).reindex(vb.index).fillna(0) - vb).abs().max() < 1e-6, col   # reconciles to v2_bands
    mid = pd.concat([placed.groupby("mid").R.sum(), un.groupby("mid").R.sum()]).groupby(level=0).sum().to_dict()
    return mid, placed.groupby(["mid", "band"]).R.sum().to_dict(), d.R.sum()


MAX_TOTAL = max(hsel(AL[AL.column == c]).R.sum() for c, _ in SANKEY_COLS)


def col_positions(values: list[float], frac: float, gap: float = 0.035, start: float = 0.0) -> list[float]:
    """y centres (0=top) for stacked nodes with values, occupying `frac` of the plot height from `start`, with gaps."""
    tot = sum(values)
    usable = frac - gap * (len(values) - 1)
    ys, cur = [], start
    for v in values:
        h = usable * v / tot
        ys.append(min(max(cur + h / 2, 0.001), 0.999))
        cur += h + gap
    return ys


def sankey_trace(col: str, visible: bool) -> go.Sankey:
    mid, mb, tot = sankey_data(col)
    frac = 0.96 * tot / MAX_TOTAL
    # Display order top->bottom matches Plotly's internal link ordering at the source node (unplaced categories first),
    # which avoids crossing flows out of the total.
    order = ["Listed for several areas, not divided", "Citywide or admin", "Not placeable", "In a specific ward",
             "Spread across an area (by population)"]
    mids = [m for m in order if mid.get(m, 0) > 0]
    bands_v = [sum(v for (m, b), v in mb.items() if b == bb) for bb in BAND_ORDER]
    labels = [f"Total capital budget  R{tot/1e9:.2f} bn"] + [f"{m}<br>R{mid[m]/1e6:,.0f}m" for m in mids] + \
             [f"{b}% Black African  R{v/1e6:,.0f}m" for b, v in zip(BAND_ORDER, bands_v)]
    colors = [INK2] + [GREY[m] for m in mids] + [BAND_COL[b] for b in BAND_ORDER]
    xs = [0.001] + [0.34] * len(mids) + [0.999] * len(BAND_ORDER)
    gap = 0.035
    mid_ys = col_positions([mid[m] for m in mids], frac, gap)
    usable = frac - gap * (len(mids) - 1)
    first_placed = mids.index("In a specific ward") if "In a specific ward" in mids else 0
    start = sum(usable * mid[m] / tot + gap for m in mids[:first_placed])          # top of the first placed node
    bgap = 0.05                                   # room for one label line between small band nodes
    band_frac = usable * sum(bands_v) / tot + bgap * (len(BAND_ORDER) - 1)
    start = max(0.0, min(start, 0.985 - band_frac))
    ys = [frac / 2] + mid_ys + col_positions([max(v, 1) for v in bands_v], band_frac, bgap, start)
    src, tgt, val, lc = [], [], [], []
    for i, m in enumerate(mids):
        src.append(0); tgt.append(1 + i); val.append(mid[m] / 1e6)
        lc.append("rgba(61,60,57,0.55)" if m == "Not placeable" else "rgba(143,142,136,0.35)")
    for i, m in enumerate(mids):
        for j, b in enumerate(BAND_ORDER):
            v = mb.get((m, b), 0)
            if v > 0:
                h = BAND_COL[b].lstrip("#")
                src.append(1 + i); tgt.append(1 + len(mids) + j); val.append(v / 1e6)
                lc.append(f"rgba({int(h[:2],16)},{int(h[2:4],16)},{int(h[4:],16)},0.5)")
    return go.Sankey(visible=visible, arrangement="fixed", valueformat=",.0f", valuesuffix=" R m",
                     node=dict(label=labels, color=colors, x=xs, y=ys, pad=fz(20), thickness=fz(30), line=dict(color=SURF, width=2),
                               hovertemplate="%{label}<extra></extra>"),
                     link=dict(source=src, target=tgt, value=val, color=lc,
                               hovertemplate="%{source.label} → %{target.label}<br>R%{value:,.0f}m<extra></extra>"),
                     textfont=dict(size=fz(26), color=INK, family=FONT_FAMILY))


def sankey_subtitle() -> str:
    return ("Left: the whole capital budget. Middle: how it could be placed.<br>"
            "Right: wards by share of residents who are Black African. Same scale for every year.")


def chart3_single(col: str, lab: str) -> go.Figure:
    fig = go.Figure(sankey_trace(col, True))
    layout(fig, f"Where the money went: {lab} budget", sankey_subtitle(), 1250, top=230)
    fig.update_layout(margin=dict(l=30, r=30, b=30))
    return fig


def chart3_all() -> go.Figure:
    fig = go.Figure([sankey_trace(c, i == 2) for i, (c, _) in enumerate(SANKEY_COLS)])
    layout(fig, f"Where the money went: {SANKEY_COLS[2][1]} budget", sankey_subtitle(), 1250, top=300)
    buttons = [dict(label=lab, method="update",
                    args=[{"visible": [j == i for j in range(len(SANKEY_COLS))]},
                          {"title.text": f"<b>Where the money went: {lab} budget</b><br><span style='font-size:{fz(28)}px;color:{INK2}'>{sankey_subtitle()}</span>"}])
               for i, (_, lab) in enumerate(SANKEY_COLS)]
    fig.update_layout(updatemenus=[dict(type="buttons", direction="right", buttons=buttons, active=2, x=0.0, xanchor="left",
                                        y=1.03, yanchor="bottom", font=dict(size=fz(24)), pad=dict(r=10, t=6),
                                        bgcolor="#ffffff", bordercolor=INK2)],
                      margin=dict(l=30, r=30, b=30))
    return fig


# ---------------- chart 4 ----------------
def chart4() -> tuple[go.Figure, list[str]]:
    b = hsel(BD[BD.scheme == "headline"])
    thin = [x for x in BAND_ORDER if int(b[b.band == x].wards.iloc[0]) <= 5]
    fig = make_subplots(rows=3, cols=3, shared_yaxes=True, vertical_spacing=0.11, horizontal_spacing=0.025,
                        subplot_titles=[l for _, l, _, _ in BUDGETS])
    ymax = b[b.column.isin([c for c, *_ in BUDGETS])].R_per_resident.max() * 1.22
    for k, (c, lab, mayor, kind) in enumerate(BUDGETS):
        r, cc = divmod(k, 3)
        d = b[b.column == c].set_index("band").reindex(BAND_ORDER)
        fig.add_bar(x=[f"{x}{'*' if x in thin else ''}" for x in BAND_ORDER], y=d.R_per_resident, showlegend=False,
                    marker=dict(color=[BAND_COL[x] for x in BAND_ORDER], line=dict(color=SURF, width=2)),
                    text=[f"R{v:,.0f}" for v in d.R_per_resident], textposition="outside", cliponaxis=False,
                    textfont=dict(size=fz(24)), customdata=d[["Rm", "wards", "share_of_population"]].values,
                    hovertemplate=lab + "<br>%{x}% Black African wards<br>R%{y:,.0f} per resident<br>R%{customdata[0]:,.1f}m in total<br>"
                                        "%{customdata[1]} wards, %{customdata[2]:.1f}% of residents<extra></extra>",
                    row=r + 1, col=cc + 1)
    fig.update_yaxes(range=[0, ymax], gridcolor=GRID, tickprefix="R", tickfont=dict(size=fz(22)), dtick=200)
    fig.update_xaxes(tickfont=dict(size=fz(22)))
    for a in fig.layout.annotations:
        a.font = dict(size=fz(26), color=INK)
    layout(fig, "Spending per resident by area",
           "Rand of capital budget per resident. Wards grouped by % of residents who are Black African (0–20% … 80–100%).", 2050, top=220)
    share8 = float(b[(b.column == "2025/26 original") & (b.band == "80–100")].share_of_population.iloc[0])
    notes = [f"* {', '.join(t + '%' for t in thin)}: small group (5 wards); one project can swing it.",
             f"Wards where 80–100% of residents are Black African are home to {share8:.0f}% of Tshwane's residents, so the big flows to "
             "them in the money-flow chart mostly reflect where people live. This chart divides by residents to compare like with like."]
    return fig, notes


# ---------------- footer strip (PNG) ----------------
def with_footer(png: str, notes: list[str]) -> None:
    img = Image.open(png).convert("RGB")
    W = img.width
    f_note = ImageFont.truetype(FONT_FILE, 27)
    f_foot = ImageFont.truetype(FONT_FILE, 24)

    def wrap(text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
        out, cur = [], ""
        for w in text.split():
            t = (cur + " " + w).strip()
            if font.getlength(t) > width:
                out.append(cur)
                cur = w
            else:
                cur = t
        return out + [cur]
    margin = 40
    f_ai = ImageFont.truetype(FONT_FILE.replace("Regular", "Bold"), 26)
    lines = [(l, f_note, INK2) for n in notes for l in wrap(n, f_note, W - 2 * margin)]
    lines += [("", f_foot, INK2)] + [(l, f_ai, INK) for l in wrap(f"{AI_SHORT}  {REPO}", f_ai, W - 2 * margin)]
    lines += [(l, f_foot, "#6b6a66") for l in wrap(FOOTER, f_foot, W - 2 * margin)]
    lh = {f_note: 38, f_foot: 33, f_ai: 38}
    H = 28 + sum(lh[f] for _, f, _ in lines) + 24
    strip = Image.new("RGB", (W, H), SURF)
    dr = ImageDraw.Draw(strip)
    dr.line([(margin, 10), (W - margin, 10)], fill=GRID, width=2)
    y = 26
    for t, f, col in lines:
        dr.text((margin, y), t, font=f, fill=col)
        y += lh[f]
    out = Image.new("RGB", (W, img.height + H), SURF)
    out.paste(img, (0, 0))
    out.paste(strip, (0, img.height))
    out.save(png)


def save_png(fig: go.Figure, name: str, notes: list[str]) -> str:
    path = VIS + name
    fig.write_image(path, width=1600, height=int(fig.layout.height), scale=1)
    with_footer(path, notes)
    return path


# ---------------- table ----------------
TWN = dict(zip(WC.ward, WC.township_primary_by_pop2011_ge50.fillna("")))


def plain_name(s: str) -> str:
    s = re.sub(r"^\(\s*\d{6}\w?\s*\)\s*", "", str(s))
    s = re.sub(r"\s+", " ", s).strip()
    return s[0].upper() + s[1:] if s else s


def area(wards: str) -> str:
    ws = [int(w) for w in str(wards).split(";") if w.strip().isdigit()]
    if len(ws) == 1:
        t = TWN.get(ws[0], "")
        return f"Ward {ws[0]}" + (f" ({t})" if t else "")
    return f"Spread across {len(ws)} wards"


ALH = hsel(AL)
WPCT = dict(zip(WC.ward, WC.pct_black_african_2022))


def wards_in(col: str, name: str) -> str:
    """Wards a project's money was placed in, in one budget column (from v2_alloc_labelled.csv; headline basis)."""
    d = ALH[(ALH.column == col) & (ALH.project_name == name) & (ALH.ward > 0)]
    return ";".join(str(int(w)) for w in sorted(set(d.ward)))


def side(wards: str, pct: float) -> tuple[str, str]:
    nw = len([w for w in wards.split(";") if w]) if wards else 0
    if nw == 0 or pd.isna(pct):
        return "not placed", "–"
    return area(wards), f"{pct:.0f}%{' (average)' if nw > 1 else ''}"


def changes_table(step: str, title: str) -> tuple[str, list[dict]]:
    c1, c2 = step.split(" → ")
    d = DR[DR.step == step].head(5)
    rows, recs = [], []
    for r in d.itertuples():
        a1, p1 = side(wards_in(c1, r.project) if r.R_before > 0 else "", r.pct_before)
        a2, p2 = side(wards_in(c2, r.project) if r.R_after > 0 else "", r.pct_after)
        ar = a2 if a1 in (a2, "not placed") else (a1 if a2 == "not placed" else f"{a1} → {a2}")
        pc = p2 if p1 in (p2, "–") else (p1 if p2 == "–" else f"{p1} → {p2}")
        ch = (r.R_after - r.R_before) / 1e6
        rec = dict(project=plain_name(r.project), area=ar, pct=pc, change=f"{'+' if ch >= 0 else '−'}R{abs(ch):,.1f}m")
        recs.append(rec)
        rows.append("<tr>" + "".join(f"<td{' class=num' if k in ('pct', 'change') else ''}>{html.escape(v)}</td>" for k, v in rec.items()) + "</tr>")
    return (f"<h3>{title}</h3><div class='tablewrap'><table><thead><tr><th>Project</th><th>Area / ward</th><th>% Black African in the ward</th>"
            f"<th>Change in budget</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>"), recs


# ---------------- page ----------------
def build_html() -> str:
    global FS
    FS = 0.62
    c1, n1 = chart1()
    c2, n2 = chart2()
    c3 = chart3_all()
    c4, n4 = chart4()
    cfg = dict(displaylogo=False, responsive=True, modeBarButtonsToRemove=["lasso2d", "select2d"])
    for f in (c1, c2, c3, c4):
        mb = (f.layout.margin.b or 40) + 46
        f.update_layout(margin=dict(b=mb), height=int(f.layout.height) + 46)
        f.add_annotation(text=f"{AI_SHORT}  {REPO}", xref="paper", yref="paper", x=0, y=0, xanchor="left", yanchor="top",
                         yshift=-(mb - 30), showarrow=False, font=dict(size=13, color=INK2))
    div = lambda f, first=False, h=None: f.to_html(full_html=False, include_plotlyjs=("inline" if first else False), config=cfg,
                                                   default_height=f"{int(f.layout.height)}px", default_width="100%")
    note = lambda ns: "".join(f"<p class='note'>{html.escape(n)}</p>" for n in ns)
    t1, _ = changes_table("2023/24 adjusted → 2024/25 original", "From 2023/24 to the 2024/25 budget – Brink (DA)")
    t2, _ = changes_table("2024/25 original → 2024/25 adjusted (adj. budget)", "2024/25 mid-year adjustment – Moya (ActionSA)")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tshwane capital budget by area</title>
<style>
*, *::before, *::after {{ box-sizing:border-box; }}
body {{ background:{SURF}; color:{INK}; font-family:{FONT_FAMILY}; font-size:19px; line-height:1.55; margin:0; }}
main {{ max-width:1180px; margin:0 auto; padding:24px 16px 64px; }}
h1 {{ font-size:34px; line-height:1.2; margin:8px 0 14px; }} h2 {{ font-size:26px; margin:52px 0 6px; }} h3 {{ font-size:21px; margin:28px 0 8px; }}
.panel {{ background:#fff; border:1px solid {GRID}; border-radius:10px; padding:16px 22px; }}
.note {{ color:{INK2}; font-size:16px; margin:6px 0; }}
.chart {{ background:#fff; border:1px solid {GRID}; border-radius:10px; padding:6px; margin-top:10px; overflow-x:auto; }}
.chart > div {{ min-width:760px; }}
table {{ border-collapse:collapse; width:100%; font-size:17px; background:#fff; }}
th, td {{ border-bottom:1px solid {GRID}; padding:8px 10px; text-align:left; vertical-align:top; }}
th {{ font-size:15px; color:{INK2}; font-weight:600; }} td.num {{ text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; }}
.ai {{ background:#f4f3ef; border:1px solid {GRID}; border-radius:8px; padding:10px 14px; font-size:16px; color:{INK}; }}
.basis {{ border-left:4px solid {PARTY['Brink']}; padding-left:12px; }}
code {{ overflow-wrap:anywhere; word-break:break-all; font-size:15px; }}
footer {{ color:{INK2}; font-size:15px; margin-top:40px; border-top:1px solid {GRID}; padding-top:12px; }}
.tablewrap {{ overflow-x:auto; max-width:100%; }}
@media (max-width:640px) {{ body {{ font-size:17px; }} h1 {{ font-size:26px; }} table {{ font-size:15px; }} th,td {{ padding:6px; }} td.num {{ white-space:normal; }} }}
</style></head><body><main>
<h1>Tshwane's capital budget: does it follow where people live?</h1>
<div class="panel">
<p>The <b>capital budget</b> is money for building and fixing infrastructure: roads, pipes, substations, clinics. It is not the money for day-to-day services like refuse collection.</p>
<p>The question: does this money go to Blacker or less Black parts of the city, compared with where people live?</p>
<p>We take every rand of capital spending, look at the ward it serves, and ask what share of that ward's residents are Black African. Averaged over all the money, that gives one number per budget. Tshwane's residents, averaged the same way, come to {CITY:.1f}%. If the budget's number is higher, money leans toward Blacker wards; if lower, it leans away.</p>
<p class="basis">Infrastructure is counted where its users live, not where it is built. For example, the Rooiwal treatment works is counted for Temba and Hammanskraal, which it serves.</p>
<p class="note">Population figures are Stats SA 2022 ward estimates. A ward is one of Tshwane's 107 electoral wards.</p>
<p class="ai"><b>How this was made.</b> {html.escape(AI_LONG)} Code, data and full method: <a href="{REPO_URL}">{REPO}</a>.</p>
</div>

<h2>1. How each budget compares with where people live</h2>
<div class="chart">{div(c1, True)}</div>{note(n1)}

<h2>2. Mid-year changes</h2>
<div class="chart">{div(c2)}</div>{note(n2)}

<h2>3. Where the money went</h2>
<p class="note">Use the buttons above the chart to switch year. All three years are drawn on the same scale.</p>
<div class="chart" id="sankey">{div(c3)}</div>{note(SANKEY_NOTES)}

<h2>4. Spending per resident by area</h2>
<div class="chart">{div(c4)}</div>{note(n4)}

<h2>The biggest changes</h2>
<p class="note">The five projects that moved each budget's number the most, with the change in their budget. Where money is spread over several wards, the % Black African is the average across them.</p>
{t1}{t2}
<p class="note">"→" shows where a project's money was placed before and after the change. For example, Thorntree View's remaining R1.0m in the 2024/25 budget could only be placed by region, so it is spread across that region's wards.</p>

<h2>What this doesn't show</h2>
<div class="panel">
<ul>
<li>Only capital spending. Services such as refuse collection, repairs and response times are not measured.</li>
<li>Roughly half of each budget can't be linked to specific areas (only {COV_LO}–{COV_HI}% could be): citywide items, head-office costs, and plants or networks whose users the documents don't name.</li>
<li>Budgets are plans. Actual spending by area is only available up to June 2025.</li>
<li>2026/27 is the budget as tabled in May 2026.</li>
<li>Population figures are modelled estimates (Stats SA 2022 ward estimates).</li>
</ul>
<h3>How this was done</h3>
<p>Every capital project in the City's budget documents and annual reports for 2022/23 to 2026/27 was extracted and matched to the ward lists the City publishes in its annual reports. Large plants are counted for the areas the City's own reports say they serve. Money listed only by region is spread across that region's wards in proportion to population. From 2025/26, wards for continuing projects are carried over from earlier ward lists, because the newer documents list regions only. Full detail, page references and every assumption: <a href="docs/summary.md">docs/summary.md</a>. Data and code: <a href="{REPO_URL}">{REPO}</a>.</p>
</div>
<footer>{html.escape(FOOTER)}<br>{html.escape(AI_SHORT)} <a href="{REPO_URL}">{REPO}</a></footer>
</main></body></html>"""


def headline_md() -> str:
    s = lambda c: float(IXH.loc[c, "spend_weighted"])
    g = lambda c: float(IXH.loc[c, "gap_vs_city"])
    b = hsel(BD[BD.scheme == "headline"])
    share8 = float(b[(b.column == "2025/26 original") & (b.band == "80–100")].share_of_population.iloc[0])
    lines = [
        f"- **Tshwane's residents average {CITY:.1f}% Black African** (Stats SA 2022 ward estimates). A budget whose money averages higher leans toward Blacker wards; lower, it leans away.",
        f"- **2022/23 – Williams (DA): {s('2022/23 original'):.1f}% ({g('2022/23 original'):+.1f} points); 2023/24 – Brink (DA): {s('2023/24 original'):.1f}% ({g('2023/24 original'):+.1f}).** Both budgets leaned toward Blacker wards by a similar amount.",
        f"- **2024/25 – Brink (DA): {s('2024/25 original'):.1f}% ({g('2024/25 original'):+.1f}).** Lower than the two years before, still slightly above where people live.",
        f"- **2024/25 adjusted – Moya (ActionSA): {s('2024/25 adjusted (adj. budget)'):.1f}% ({g('2024/25 adjusted (adj. budget)'):+.1f}).** The mid-year adjustment to the 2024/25 budget, made under Moya; the only budget in the series below where people live. Actual spending that year (July 2024–June 2025, spanning both mayors): {s(ACTUAL):.1f}% ({g(ACTUAL):+.1f}).",
        f"- **2025/26 – Moya (ActionSA): {s('2025/26 original'):.1f}% ({g('2025/26 original'):+.1f}); 2026/27 – Moya (ActionSA): {s('2026/27 original'):.1f}% ({g('2026/27 original'):+.1f}).** Above where people live again; 2026/27 is the budget as tabled in May 2026.",
        f"- **Mid-year adjustments moved the number by {s('2022/23 adjusted') - s('2022/23 original'):+.1f} (2022/23), {s('2023/24 adjusted') - s('2023/24 original'):+.1f} (2023/24), {s('2024/25 adjusted (adj. budget)') - s('2024/25 original'):+.1f} (2024/25) and {s('2025/26 adjusted') - s('2025/26 original'):+.1f} points (2025/26; excludes a R13m Refilwe roads item missing from the City's project list).** Wards that are 80–100% Black African are home to {share8:.0f}% of residents; only {COV_LO}–{COV_HI}% of each budget could be linked to specific areas.",
    ]
    return ("# Tshwane capital budget: headline figures\n\n"
            "Infrastructure is counted where its users live, not where it is built; money listed only by region is spread across "
            "the region's wards by population. Figures from `output/v2_index.csv` and `output/v2_bands.csv` (service-area basis).\n\n"
            + "\n".join(lines) + f"\n\n_{FOOTER}_\n")


def main() -> None:
    global FS
    FS = 1.0
    c1, n1 = chart1()
    c2, n2 = chart2()
    c4, n4 = chart4()
    pngs = [save_png(c1, "chart1_budget_vs_population.png", n1), save_png(c2, "chart2_mid_year_changes.png", n2)]
    for c, lab in SANKEY_COLS:
        pngs.append(save_png(chart3_single(c, lab), f"chart3_money_flow_{c[:7].replace('/', '-')}.png", SANKEY_NOTES))
    pngs.append(save_png(c4, "chart4_spending_per_resident.png", n4))
    open(VIS + "report.html", "w").write(build_html())
    open(VIS + "headline_figures.md", "w").write(headline_md())
    print("\n".join(pngs))


if __name__ == "__main__":
    main()
