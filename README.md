# Tshwane capital budget: does it go to Blacker or less Black wards?

**Live report:** https://ctgschollar.github.io/tshwane-budget-analysis/

## How this was made

The data extraction, analysis code, charts and write-up in this project were produced by an AI system (Anthropic's Claude), working under my direction. I set the questions and method choices and reviewed the results, but I did not write the code or calculations by hand. AI can make mistakes: every figure is meant to be traceable to a page in the source documents, and corrections are welcome via [GitHub issues](https://github.com/ctgschollar/tshwane-budget-analysis/issues).

## What this looks at

The City of Tshwane's **capital budget** is money for building and fixing infrastructure: roads, pipes, substations, clinics. It is not the money for day-to-day services like refuse collection. The question is whether that money goes to Blacker or less Black parts of the city, compared with the make-up of Tshwane as a whole.

Every rand that can be linked to an area is matched to the wards it serves, and each ward is described by the share of its residents who are Black African (Stats SA 2022 ward estimates). Averaged over all the money, that gives one number per budget. Tshwane's residents, averaged the same way, come to **82.7%**. Infrastructure is counted where its users live, not where it is built (for example, the Rooiwal treatment works is counted for Temba and Hammanskraal, which it serves).

**Headline figures.** The number is the average share of Black African residents in the wards a budget's money goes to. The second column is its difference from Tshwane's 82.7%, in percentage points: +4.5 means 87.3% (money leans toward Blacker wards); −1.2 means 81.5% (leans slightly toward less Black wards); 0 would mean the same mix as Tshwane's residents.

| Budget | Number | Difference from 82.7% |
|---|---|---|
| 2022/23 – Williams (DA) | 87.3% | +4.5 |
| 2023/24 – Brink (DA) | 87.0% | +4.2 |
| 2024/25 – Brink (DA) | 84.1% | +1.3 |
| 2024/25 adjusted – Moya (ActionSA) | 81.5% | −1.2 |
| 2025/26 – Moya (ActionSA) | 85.7% | +2.9 |
| 2026/27 – Moya (ActionSA) | 87.8% | +5.0 |
| Actual spending, Jul 2024–Jun 2025 (spans both mayors) | 83.4% | +0.7 |

The 2022/23 and 2023/24 budgets leaned toward Blacker wards by a similar amount. The 2024/25 budget was lower but still slightly above Tshwane as a whole. Its mid-year adjustment, made under Moya, is the only budget in the series below Tshwane as a whole. The 2025/26 and 2026/27 budgets are above Tshwane as a whole again. Mid-year adjustments moved the number by +1.3 (2022/23), +1.5 (2023/24), −2.6 (2024/25) and −1.9 points (2025/26; excludes a R13m Refilwe roads item missing from the City's project list). The 2022/23 mid-year adjustment is not labelled with a mayor: the City's 2022/23 annual report (p36) gives Williams as mayor from 1 July 2022 to 13 February 2023, Makwarela from 28 February to 10 March 2023 and Brink from 31 March 2023, and the documents do not give the adjustment's adoption date. More: [docs/headline_figures.md](docs/headline_figures.md); full method and results: [docs/summary.md](docs/summary.md).

## What this doesn't show

- Only capital spending. Services such as refuse collection, repairs and response times are not measured.
- Roughly half of each budget can't be linked to specific areas (only 38–53% could be): citywide items, head-office costs, and plants or networks whose users the documents don't name.
- Budgets are plans. Actual spending by area is only available up to June 2025.
- 2026/27 is the budget as tabled in May 2026.
- Population figures are modelled estimates (Stats SA 2022 ward estimates).

## Repository layout

| Path | Contents |
|---|---|
| `index.html` | The visual report (served by GitHub Pages; works offline) |
| `images/` | Chart images (1600px wide) |
| `docs/summary.md` | Full methods, results, page references and every assumption |
| `docs/headline_figures.md` | Plain-language headline figures |
| `data/` | Derived data: project-level extracts (`projects.csv`, `projects_moya.csv`), ward classification, band and index tables, row-level allocation (`v2_alloc*.csv`), driver tables |
| `data/binary_v1/` | The earlier binary (≥80% Black African) version of the analysis, preserved unchanged |
| `scripts/` | Code to reproduce everything, with small derived inputs in `scripts/data/` |

## Sources

**City of Tshwane budget documents and annual reports** (source PDFs are not included in this repository; they were published by the City of Tshwane, www.tshwane.gov.za, and municipal budget documents are also collected by National Treasury, lg.treasury.gov.za; the exact download URLs were not recorded):

- Audited Annual Report 2022/23
- Consolidated Annual Report 2023/24
- Consolidated Audited Annual Report 2024/25
- Medium Term Revenue and Expenditure Framework (budget) 2022/23, 2023/24, 2024/25, 2025/26 (Special Council, 29 May 2025) and 2026/27 (final, for the Mayoral Committee of 21 May 2026)
- Adjustment budgets 2022/23, 2023/24, 2024/25 and 2025/26

**Other data:**

- Statistics South Africa, *Ward level Small Area Population Estimates, 2022* (November 2025), https://www.statssa.gov.za/?p=18967. Source: Statistics South Africa.
- Municipal Demarcation Board, ward boundaries (2020 delimitation, used for the 2021 elections) and the WardProfile2021 layer, via the MDB's ArcGIS services.
- Statistics South Africa, Census 2011 sub-place and main-place boundaries (UCT_Geodata ArcGIS mirror of the Stats SA layer), and Census 2011 sub-place populations as republished by Adrian Frith, https://census2011.adrianfrith.com (data: Statistics South Africa).
- City of Tshwane e-GIS, *Tshwane Regions* layer, https://e-gis001.tshwane.gov.za/server/rest/services/Other_WS/Regions/MapServer/2 (© City of Tshwane; e-GIS terms and conditions apply). Only a derived ward → region list is included here.

Download links and instructions for the third-party data are in [scripts/README.md](scripts/README.md).

## Reproducing the analysis

See [scripts/README.md](scripts/README.md): you need the City's PDFs, Python with `pdfplumber pandas rapidfuzz tabulate` (plus `plotly kaleido pillow` and Chrome for the charts), and the run order listed there.

## Reporting an error

Please [open a GitHub issue](https://github.com/ctgschollar/tshwane-budget-analysis/issues) with the figure, the page of the report or file, and (if you can) the source document and page that disagrees.

## Licence

- **Code** (`scripts/`): MIT, see [LICENSE](LICENSE).
- **Derived data and the report** (`data/`, `docs/`, `images/`, `index.html`): [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- **Source documents and third-party data** remain with their publishers (City of Tshwane, Statistics South Africa, Municipal Demarcation Board, Adrian Frith) under their own terms.
