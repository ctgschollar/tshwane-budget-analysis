# Tshwane capital-by-ward analysis — scripts

_Made with AI (Anthropic's Claude) under the author's direction._

**Version 2 (banded / threshold-free).** The current summary is produced by `bands_report.py` (step 8 below). The binary
(≥80% Black African) results are preserved in `data/binary_v1/` of this repository. The scripts in this folder produce both:
the binary pipeline is unchanged and v2 only adds `bands_*.py`.

### Paths

The scripts work in two places:
- **Project folder** (`TSHWANE_ROOT`, default `~/Documents/tshwane`): the source PDFs (see the main README for the list),
  and an `output/` folder the scripts write to (`projects.csv`, `summary.md`, `v2_*.csv`, `visuals/` …).
  In this repository those outputs are published as `data/`, `docs/` and `images/` + `index.html`.
- **Working directory** (the current directory when you run a script; `TSHWANE_WORKDIR` for `external/ctx.py`): holds
  `txt/`, `work/`, `census_clean/`, `townships/`, `regions/` as described below.

```bash
export TSHWANE_ROOT=~/tshwane-project          # contains the PDFs; output/ is created here
mkdir -p ~/tshwane-work && cd ~/tshwane-work    # working directory
export PYTHONPATH=/path/to/repo/scripts:/path/to/repo/scripts/visuals
```

## Layout and working directory

All analysis scripts use paths relative to a **working directory** that contains:

| Folder | Contents | How it is made |
|---|---|---|
| `txt/` | `pdftotext -layout` output of every PDF (pages separated by form feeds) | step 0 below |
| `work/` | intermediate CSVs (extractions, match decisions, decompositions) | created by the scripts |
| `census_clean/` | `tshwane_ward_popgroup.csv`, `tshwane_ward_popgroup_census2011_mdb_wardprofile2021.csv` | copy from `data/` (or rebuild with `external/build_csv.py`) |
| `townships/` | `ward_township_overlap.csv`, `ward_township_overlap_all.csv`, `ward_township_flag.csv` | copy from `data/` (or `external/ward_township.py`) |
| `regions/` | `ward_region_overlay.csv` (ward → region from the City e-GIS layer) | copy from `data/` (or `external/ward_region_overlay.py`) |

Run every script **from the working directory** (`cd <workdir>; python <scripts>/<name>.py ...`), with this folder on
`PYTHONPATH` (the scripts import each other). Python deps: `pdfplumber pandas rapidfuzz tabulate`
(geo scripts also need `geopandas shapely pyproj requests`).

PDFs are read from `$TSHWANE_ROOT/` and outputs written to `$TSHWANE_ROOT/output/`. The small inputs in `scripts/data/`
must be copied into the working directory first (`census_clean/`, `townships/`, `regions/`, `work/name_overrides.csv`):

```bash
mkdir -p census_clean townships regions work
cp $REPO/scripts/data/tshwane_ward_popgroup*.csv census_clean/
cp $REPO/scripts/data/ward_township_*.csv townships/
cp $REPO/scripts/data/ward_region_overlay.csv regions/
cp $REPO/scripts/data/name_overrides.csv work/
```

## Run order

0. `mkdir -p txt work && for f in $TSHWANE_ROOT/*.pdf; do pdftotext -layout "$f" "txt/$(basename "${f%.pdf}").txt"; done`
1. Extraction (each prints a reconciliation against the stated totals):
   - `ex_2425_appN.py work/appN_2425.csv` — AR 2024/25 Appendix N (dominant ward, adjusted, actual)
   - `ex_annexB.py work/annexB.csv` — Annexure B of the 2022/23 and 2023/24 adjustments budgets + 2024/25 MTREF Annexure A
   - `ex_regions.py work/regions.csv` — SA36/SB19 region ("Ward Location") tags
   - `ex_appO.py work/appO.csv` — Appendix O ward lists (all three annual reports)
   - `fix_names.py` — applies `data/name_overrides.csv` (copy it to `work/name_overrides.csv` first): hand-decoded
     names for 18 rows whose text is overprinted in the PDFs → `work/annexB_clean.csv`
2. Matching budget rows → Appendix O wards:
   - `run_match.py work/match_all.csv` (candidate matches + automatic rules)
   - `decisions_budget.py` (manual review decisions, with reasons) → `work/match_decisions_budget.csv`
   - `decisions_appN.py` (Appendix N → Appendix O) → `work/match_decisions_appN.csv`
3. `build.py` → `output/projects.csv`
4. `analyze.py > work/analysis.md` (shares, sensitivities, spend rates, top-10s)
5. Follow-ups:
   - `part1_decompose.py` (2023/24 → 2024/25 decomposition, excl. bulk; manual re-coding links are in `RECODED`)
   - `ward_region.py` → `work/ward_region_table.csv`, `work/ward_region_evidence.csv` (ward → region: City documents →
     Rekord cross-check → e-GIS layer; narrative ward/region quotes are listed in the script with file + page)
   - `part2_beneficiaries.py` → `work/bulk_beneficiaries_final.csv` (reviewed, quote-verified beneficiary statements for bulk
     projects; `data/bulk_beneficiaries.csv` is the unreviewed search output from `external/build_beneficiaries.py`)
   - `part2_attribute.py` (location vs service-area basis × region-only money (a) unattributed / (b) population-split)
   - `part2_report.py` (markdown for summary §8; imported by `summary_write.py`)
6. Moya-era extension (§9 of the summary):
   - `ex_annex_new.py work/annex_new.csv` — 2024/25 adjustments budget Annexure B, 2025/26 MTREF Annexure A, 2025/26
     adjustments budget Annexure B, 2026/27 MTREF Annexure A (incl. the City "Regions" column); prints reconciliation
     to each printed "Total Capex Budget" (uses the same `ex_annexB.extract`, which now accepts a document config)
   - `moya_build.py` → `work/moya_rows.csv` (Option A attribution: same-year App O for 2024/25 adj; carried-forward
     App O ward for 2025/26+ via WBS link, else Regions column). Name overrides (`NAME_OVERRIDES`), canonical
     worn-out-pipe titles and manual cross-year links (`MANUAL_LINKS`) are documented in the script
   - `moya_analysis.py` (headline both bases × (a)/(b), Option B region series, carry-forward checks, composition,
     step decompositions, tracing of the four 2024/25 cuts)
   - `moya_report.py` (markdown for summary §9; imported by `summary_write.py`)
7. `summary_build.py` then `summary_write.py` → `output/summary.md`, `output/ward_classification.csv`;
   `output/projects_moya.csv` (Moya-era rows with attribution, links, checks) is written by `summary_write.py` via `moya_analysis.write_projects_moya()`

Helper modules (also `external/ctx.py`, a context grep used for the beneficiary search): `bands.py` (column-band text extraction), `match.py` (name normalisation/fuzzy matching),
`pgrep.py` / `page.py` (page-aware grep / page print for `txt/` files).

## External data (`external/` and `data/`)

`scripts/data/` holds the small **derived** tables the analysis needs (ward population groups, ward × township overlap,
ward → region overlay, name overrides, the unreviewed beneficiary-search output). The **raw third-party downloads are not
in this repository**. To rebuild the derived tables, download them into a new empty folder and run the `external/` scripts
(they read downloads as data only):

| Data | Where to get it | Used by |
|---|---|---|
| Stats SA, *Ward level Small Area Population Estimates, 2022* (Nov 2025): `Ward-Product_Locked-spreadsheets.zip` → `PP_Population Group_*.xlsx` | release page https://www.statssa.gov.za/?p=18967 ; file https://www.statssa.gov.za/wp-content/uploads/2025/11/Ward-Product_Locked-spreadsheets.zip ; technical note https://www.statssa.gov.za/wp-content/uploads/2025/11/Ward-statistical-product-technical-note.pdf | `external/xlsx_dump.py`, `external/build_csv.py` |
| Municipal Demarcation Board, *Wards 2020/2021* ward polygons (Tshwane, WardID 79900001–79900107) | https://services7.arcgis.com/oeoyTUJC8HEeYsRB/arcgis/rest/services/MDB_Wards_2020/FeatureServer/0 | `external/ward_township.py`, `external/ward_region_overlay.py` |
| MDB *WardProfile2021* layer (Census 2011 population group by 2020 ward; sensitivity only) | https://services7.arcgis.com/oeoyTUJC8HEeYsRB/arcgis/rest/services/WardProfile2021_gdb/FeatureServer/0 | `external/build_csv.py` |
| Census 2011 Sub Places (UCT_Geodata mirror of the Stats SA layer) | https://services3.arcgis.com/GMycIhSIBQnnjV35/arcgis/rest/services/Census_2011_Sub_Places_of_South_Africa/FeatureServer/0 | `external/ward_township.py` |
| Census 2011 sub-place populations (Adrian Frith, *Census 2011*, from Stats SA data) | https://census2011.adrianfrith.com/place/&lt;main place code&gt; | `external/ward_township.py` |
| City of Tshwane e-GIS *Tshwane Regions* layer (terms: https://e-gis002.tshwane.gov.za/e_gis_LandingPage/documents/Terms_Conditions_e-GIS.pdf) | https://e-gis001.tshwane.gov.za/server/rest/services/Other_WS/Regions/MapServer/2 | `external/ward_region_overlay.py` |

`external/build_beneficiaries.py` and `external/ctx.py` are the helpers used to search the PDF text for stated
beneficiaries; their reviewed result is hard-coded, with quotes and pages, in `part2_beneficiaries.py`.

## Version 2: banded and threshold-free analysis

8. After steps 1–7 (which also regenerate the binary_v1-equivalent outputs):
   - `bands_engine.py` → `work/v2_alloc.csv`: rand per project × ward for every budget column (2022/23–2026/27 + 2024/25
     App N final adjusted + 2024/25 actual), Option A (service/location × (a)/(b), via `part2_attribute.allocate`) and
     Option B (region tags, population split). Band definitions (`BANDS`: headline 5 bands, 80–100 split, 40–80 merged)
     and column labels (administration + document/date) live here.
   - `bands_metrics.py` → `work/v2_index.csv`, `work/v2_bands.csv`: spend- vs population-weighted mean % Black African
     (same wards; city mean 82.7% shown too), per-band rand / share / rand-per-resident, single-project dominance flags,
     index-based driver decomposition (`drivers`, incl. the 2022/23→2023/24 name crosswalk for the WBS scheme change).
   - `bands_report.py` → `output/summary.md` (v2, with binary_v1 summary appended verbatim as Appendix A),
     `output/v2_index.csv`, `output/v2_bands.csv`, `output/v2_drivers.csv`, and band columns added to
     `output/ward_classification.csv`.
   Check: `bands_engine` reproduces every binary_v1 ≥80% share exactly (see summary §8).

## Visual summary (general audience)

9. `bands_engine.py output/v2_alloc_labelled.csv` (optional re-run): same allocation as `v2_alloc.csv` plus a `placement`
   label per row (named ward / region split / township split). Verified identical to `v2_alloc.csv` row by row
   (all 50,397 rows, every rand) before use. `output/v2_alloc.csv` is a copy of the engine output, kept for traceability.
10. `visuals/make_visuals.py` → `output/visuals/report.html` (self-contained, Plotly JS embedded, works offline),
    `chart1_…png`–`chart4_…png` (1600px wide, footer strip with coverage and sources) and `headline_figures.md`.
    Reads only `v2_index.csv`, `v2_bands.csv`, `v2_drivers.csv`, `ward_classification.csv`, `v2_alloc_labelled.csv`;
    asserts the Sankey band totals equal `v2_bands.csv`. Needs `plotly kaleido pillow` and Chrome for PNG export.
    Colours checked with the dataviz skill's `validate_palette.js` (party: categorical; bands: `--ordinal`).
11. `visuals/check_report.py <outdir> [file:///…/report.html]` (needs `playwright`; uses /usr/bin/google-chrome): opens report.html, checks all
    four charts render without console errors, clicks each Sankey year button, screenshots desktop + phone width and
    reports horizontal overflow.
