_Made with AI (Anthropic's Claude) under the author's direction._

> In this repository, files the text refers to under `output/` are in `data/` (CSVs), `data/binary_v1/` (binary version), `images/` and `index.html` (visual summary); scripts are in `scripts/`.

# Tshwane capital spending by ward, 2022/23 – 2026/27: banded and threshold-free analysis (v2)

**What changed from binary_v1.** The headline no longer splits wards into "predominantly Black" (≥80% Black African) and "other". Every ward now carries its own % Black African (Stats SA 2022 ward estimates). Capex is reported in five bands of that percentage, and the headline measure is a **threshold-free index**: the spend-weighted mean % Black African of the wards that receive capital money, compared with the population-weighted mean of the same wards. The **service-area basis** is the headline throughout; physical location is secondary. All extraction, matching, ward and region attribution are unchanged from binary_v1. The engine reproduces every binary_v1 share exactly (checked), and the binary results are kept in full in **Appendix A**. A full list of changes is in §8.

## Plain-language finding

- **Service-area basis (headline): capex leans slightly towards Blacker wards in almost every budget.** The spend-weighted mean % Black African is above Tshwane's population-weighted 82.7% in every budget column except one, Moya's first adjustment budget (2024/25 adjusted: 81.5% (gap -1.2)).
- **The index by budget:**

  | Budget | Adopted by | Spend-weighted index (gap vs city) |
  |---|---|---|
  | 2022/23 original | pre-Brink | 87.3% (gap +4.5) |
  | 2022/23 adjusted | pre-Brink | 88.6% (gap +5.8) |
  | 2023/24 original | Brink | 87.0% (gap +4.2) |
  | 2023/24 adjusted | Brink | 88.5% (gap +5.7) |
  | 2024/25 original | Brink | 84.1% (gap +1.3) |
  | 2024/25 adjusted | Moya | 81.5% (gap -1.2) |
  | 2025/26 original | Moya | 85.7% (gap +2.9) |
  | 2025/26 adjusted | Moya | 83.8% (gap +1.1) |
  | 2026/27 original | Moya | 87.8% (gap +5.0) |

  Final 2024/25 adjusted (App N): 83.4% (gap +0.6). **2024/25 actual spend: 83.4% (gap +0.7).**
- **The claim about Brink's first budgets.** On this measure, the first Brink budgets (2023/24) are essentially unchanged from the pre-Brink 2022/23 budgets: -0.3 points original vs original, -0.1 adjusted vs adjusted. The large 2023/24 fall in binary_v1 came mainly from the location basis (where the index also falls, by -8.7 points from the 2022/23 adjusted budget).
- **The fall comes later.** It appears in the Brink-era 2024/25 original budget (88.5 → 84.1) and continues into Moya's first adjustment (81.5). Moya's 2025/26 and 2026/27 originals recover to 85.7 and 87.8, but the 2025/26 adjustment again pulls the index down (83.8).
- **Physical-location basis (secondary): the picture differs, mainly because of where bulk plants sit.** The index drops from 84.4 (2022/23 adjusted) to 75.7 (2023/24 original). Capex leans *away* from Blacker wards relative to population (gap -7.0 to -11.3) until the 2026/27 original (+0.7).
- **Region-level robustness check (Option B):** essentially flat (81.3–84.2), so region tags alone can't detect these shifts.
- **Overall reading.** The banded and index results do **not** support a specific "Brink neglected Black areas" story on the service-area basis. They show a dip spanning the 2024/25 Brink budget and Moya's first adjustment, and a recovery in Moya's later original budgets. In-year adjustments go both ways: the pre-Brink 2022/23 and Brink 2023/24 adjustments raised the index (+1.3, +1.5). Both Moya-era adjustments lowered it (-2.6, -1.9).
- **Coverage limits all of this.** Only 38–53% of each budget can be attributed to wards on the service-area basis. From 2025/26 wards are carried forward, not stated in the documents, and there is no ward-level actual spend after 2024/25.

## 1. Method

- **Ward % Black African:** Stats SA Ward-level Small Area Population Estimates 2022 (MDB 2020 wards; see Appendix A §3). Unchanged.
- **Attribution:** unchanged from binary_v1 (Appendix A §2, §8, §9).
  - **Service area:** bulk infrastructure goes to the area a document states it serves (Appendix A §8.2), and is unattributed if none is stated. All other projects use their Appendix O ward. From 2025/26 that ward is carried forward, flagged, or the City's Regions column is used.
  - **Physical location:** every project uses its Appendix O ward.
  - **(a):** region-only money is unattributed.
  - **(b):** region-only money is split across the region's wards by population. **This assumes each resident benefits equally.**
  - **Multi-ward projects** remain unattributed, as in binary_v1.
- **Index:**
  - spend-weighted mean = Σ(capex in ward × ward %Black) ÷ Σ(capex), over ward-attributed capex;
  - population-weighted mean = Σ(pop × %Black) ÷ Σ(pop), over the **same wards** (those receiving any attributed capex).

  A positive gap means capex leans towards Blacker wards. Under (b), region splits reach every ward of a region, so from 2023/24 the "same wards" set is usually all 107 wards and the comparison mean is the city's 82.7%. The "gap vs city" column is shown throughout for that reason.
- **Rand per resident by band** = band capex ÷ the band's 2022 population (all wards in the band, whether or not they receive capex).
- **Columns** are labelled with the administration that adopted the budget and the document or date (§3 tables). The 2024/25 actual spend is reported separately and spans both administrations: about 3 months Brink and 9 months Moya, on the tenure dates in the brief. "2024/25 adjusted (App N, final)" is the annual report's final adjusted budget; "2024/25 adjusted (adj. budget)" is the mid-year adjustments budget (Moya-era Council).

## 2. Bands

| Scheme                    | Band          |   Wards |   Population (2022) |   Share of residents % | Ward range % Black   | Flag           |
|:--------------------------|:--------------|--------:|--------------------:|-----------------------:|:---------------------|:---------------|
| Headline (5 bands)        | 0–20          |      12 |              252761 |                    6.3 | 8.6–18.2             |                |
| Headline (5 bands)        | 20–40         |      15 |              378961 |                    9.4 | 21.2–40.0            |                |
| Headline (5 bands)        | 40–60         |       6 |              199661 |                    4.9 | 41.2–57.3            |                |
| Headline (5 bands)        | 60–80         |       5 |              162340 |                    4.0 | 65.4–77.1            | ≤5 wards: thin |
| Headline (5 bands)        | 80–100        |      69 |             3046591 |                   75.4 | 81.2–99.6            |                |
| Sensitivity: 80–100 split | 0–20          |      12 |              252761 |                    6.3 | 8.6–18.2             |                |
| Sensitivity: 80–100 split | 20–40         |      15 |              378961 |                    9.4 | 21.2–40.0            |                |
| Sensitivity: 80–100 split | 40–60         |       6 |              199661 |                    4.9 | 41.2–57.3            |                |
| Sensitivity: 80–100 split | 60–80         |       5 |              162340 |                    4.0 | 65.4–77.1            | ≤5 wards: thin |
| Sensitivity: 80–100 split | 80–90         |       5 |              175584 |                    4.3 | 81.2–88.0            | ≤5 wards: thin |
| Sensitivity: 80–100 split | 90–100        |      64 |             2871007 |                   71.1 | 93.0–99.6            |                |
| Sensitivity: 40–80 merged | 0–20          |      12 |              252761 |                    6.3 | 8.6–18.2             |                |
| Sensitivity: 40–80 merged | 20–40         |      15 |              378961 |                    9.4 | 21.2–40.0            |                |
| Sensitivity: 40–80 merged | 40–80 (mixed) |      11 |              362002 |                    9.0 | 41.2–77.1            |                |
| Sensitivity: 40–80 merged | 80–100        |      69 |             3046591 |                   75.4 | 81.2–99.6            |                |

Band edges are half-open [lo, hi). Wards 91 (39.95%) and 41 (39.77%) sit just below the 40% cut, which is kept as specified. The 60–80 and 80–90 bands each have exactly 5 wards: treat their figures as thin, and see the single-project flags in §4.4.

## 3. Threshold-free index (headline)

#### Service area, (b) region money population-split — HEADLINE

Budgets:

| Column [adopted by]                    | Document / date                                                                                          |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2022/23 original [pre-Brink]           | 2022/23 MTREF approved 26 May 2022 (2022/23 adj. budget p51)                                             |                                  87.3 |                                   85.0 |                 2.2 |                   4.5 |                      93 |                          47.4 |
| 2022/23 adjusted [pre-Brink]           | 2022/23 adjustments budget, prepared before the 2–3 Mar 2023 NT engagement (p52)                         |                                  88.6 |                                   85.2 |                 3.4 |                   5.8 |                      94 |                          48.2 |
| 2023/24 original [Brink]               | 2023/24 MTREF approved 31 May 2023 (2023/24 adj. budget p48)                                             |                                  87.0 |                                   82.7 |                 4.2 |                   4.2 |                     107 |                          48.5 |
| 2023/24 adjusted [Brink]               | 2023/24 adjustments budget, based on results to 31 Dec 2023 (p48)                                        |                                  88.5 |                                   82.7 |                 5.7 |                   5.7 |                     107 |                          48.3 |
| 2024/25 original [Brink]               | 2024/25 MTREF, 'tabled for approval by Council in May 2024' (p76)                                        |                                  84.1 |                                   82.7 |                 1.3 |                   1.3 |                     107 |                          41.0 |
| 2024/25 adjusted (adj. budget) [Moya]  | 2024/25 adjustments budget, based on results to 31 Dec 2024 (p47)                                        |                                  81.5 |                                   82.7 |                -1.2 |                  -1.2 |                     107 |                          37.6 |
| 2024/25 adjusted (App N, final) [Moya] | AR 2024/25 Appendix N pp503–515 (final adjusted incl. later amendments)                                  |                                  83.4 |                                   82.7 |                 0.6 |                   0.6 |                     107 |                          39.4 |
| 2025/26 original [Moya]                | 2025/26 MTREF, Special Council 29 May 2025 (file title; p152 'approval in May 2025')                     |                                  85.7 |                                   82.7 |                 2.9 |                   2.9 |                     107 |                          53.0 |
| 2025/26 adjusted [Moya]                | 2025/26 adjustments budget, based on results to 31 Dec 2025 (p52)                                        |                                  83.8 |                                   82.7 |                 1.1 |                   1.1 |                     107 |                          43.1 |
| 2026/27 original [Moya]                | 2026/27 MTREF, version for Mayoral Committee 21 May 2026 (p65); total reconciles to SDBIP R2,856,300,538 |                                  87.8 |                                   82.7 |                 5.0 |                   5.0 |                     107 |                          42.3 |

Actual spend (kept separate):

| Column [adopted by]                                         | Document / date                                         |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:------------------------------------------------------------|:--------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] | AR 2024/25 Appendix N pp503–515 (audited annual report) |                                  83.4 |                                   82.7 |                 0.7 |                   0.7 |                     107 |                          38.4 |

#### Service area, (a) region money unattributed

Budgets:

| Column [adopted by]                    | Document / date                                                                                          |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2022/23 original [pre-Brink]           | 2022/23 MTREF approved 26 May 2022 (2022/23 adj. budget p51)                                             |                                  87.0 |                                   87.2 |                -0.2 |                   4.2 |                      42 |                          40.3 |
| 2022/23 adjusted [pre-Brink]           | 2022/23 adjustments budget, prepared before the 2–3 Mar 2023 NT engagement (p52)                         |                                  88.0 |                                   87.5 |                 0.6 |                   5.3 |                      43 |                          42.8 |
| 2023/24 original [Brink]               | 2023/24 MTREF approved 31 May 2023 (2023/24 adj. budget p48)                                             |                                  89.4 |                                   93.6 |                -4.2 |                   6.6 |                      35 |                          35.2 |
| 2023/24 adjusted [Brink]               | 2023/24 adjustments budget, based on results to 31 Dec 2023 (p48)                                        |                                  91.0 |                                   93.6 |                -2.6 |                   8.3 |                      35 |                          37.0 |
| 2024/25 original [Brink]               | 2024/25 MTREF, 'tabled for approval by Council in May 2024' (p76)                                        |                                  85.0 |                                   89.1 |                -4.1 |                   2.3 |                      43 |                          32.8 |
| 2024/25 adjusted (adj. budget) [Moya]  | 2024/25 adjustments budget, based on results to 31 Dec 2024 (p47)                                        |                                  81.9 |                                   88.9 |                -7.0 |                  -0.9 |                      42 |                          31.7 |
| 2024/25 adjusted (App N, final) [Moya] | AR 2024/25 Appendix N pp503–515 (final adjusted incl. later amendments)                                  |                                  83.8 |                                   90.0 |                -6.2 |                   1.1 |                      47 |                          35.4 |
| 2025/26 original [Moya]                | 2025/26 MTREF, Special Council 29 May 2025 (file title; p152 'approval in May 2025')                     |                                  87.6 |                                   90.7 |                -3.1 |                   4.9 |                      37 |                          40.2 |
| 2025/26 adjusted [Moya]                | 2025/26 adjustments budget, based on results to 31 Dec 2025 (p52)                                        |                                  86.4 |                                   90.8 |                -4.4 |                   3.7 |                      37 |                          31.7 |
| 2026/27 original [Moya]                | 2026/27 MTREF, version for Mayoral Committee 21 May 2026 (p65); total reconciles to SDBIP R2,856,300,538 |                                  90.8 |                                   91.0 |                -0.2 |                   8.0 |                      32 |                          28.7 |

Actual spend (kept separate):

| Column [adopted by]                                         | Document / date                                         |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:------------------------------------------------------------|:--------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] | AR 2024/25 Appendix N pp503–515 (audited annual report) |                                  83.9 |                                   89.1 |                -5.1 |                   1.2 |                      43 |                          34.3 |

#### Physical location, (b) population-split

Budgets:

| Column [adopted by]                    | Document / date                                                                                          |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2022/23 original [pre-Brink]           | 2022/23 MTREF approved 26 May 2022 (2022/23 adj. budget p51)                                             |                                  82.5 |                                   85.3 |                -2.8 |                  -0.2 |                      98 |                          63.3 |
| 2022/23 adjusted [pre-Brink]           | 2022/23 adjustments budget, prepared before the 2–3 Mar 2023 NT engagement (p52)                         |                                  84.4 |                                   82.2 |                 2.1 |                   1.6 |                      75 |                          58.9 |
| 2023/24 original [Brink]               | 2023/24 MTREF approved 31 May 2023 (2023/24 adj. budget p48)                                             |                                  75.7 |                                   82.7 |                -7.0 |                  -7.0 |                     107 |                          61.2 |
| 2023/24 adjusted [Brink]               | 2023/24 adjustments budget, based on results to 31 Dec 2023 (p48)                                        |                                  76.3 |                                   82.7 |                -6.4 |                  -6.4 |                     107 |                          58.5 |
| 2024/25 original [Brink]               | 2024/25 MTREF, 'tabled for approval by Council in May 2024' (p76)                                        |                                  73.1 |                                   82.7 |                -9.7 |                  -9.7 |                     107 |                          58.7 |
| 2024/25 adjusted (adj. budget) [Moya]  | 2024/25 adjustments budget, based on results to 31 Dec 2024 (p47)                                        |                                  71.4 |                                   82.7 |               -11.3 |                 -11.3 |                     107 |                          54.1 |
| 2024/25 adjusted (App N, final) [Moya] | AR 2024/25 Appendix N pp503–515 (final adjusted incl. later amendments)                                  |                                  75.4 |                                   82.7 |                -7.3 |                  -7.3 |                     107 |                          58.2 |
| 2025/26 original [Moya]                | 2025/26 MTREF, Special Council 29 May 2025 (file title; p152 'approval in May 2025')                     |                                  81.1 |                                   82.7 |                -1.6 |                  -1.6 |                     107 |                          72.1 |
| 2025/26 adjusted [Moya]                | 2025/26 adjustments budget, based on results to 31 Dec 2025 (p52)                                        |                                  76.8 |                                   82.7 |                -5.9 |                  -5.9 |                     107 |                          55.5 |
| 2026/27 original [Moya]                | 2026/27 MTREF, version for Mayoral Committee 21 May 2026 (p65); total reconciles to SDBIP R2,856,300,538 |                                  83.5 |                                   82.7 |                 0.7 |                   0.7 |                     107 |                          59.8 |

Actual spend (kept separate):

| Column [adopted by]                                         | Document / date                                         |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:------------------------------------------------------------|:--------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] | AR 2024/25 Appendix N pp503–515 (audited annual report) |                                  75.4 |                                   82.7 |                -7.3 |                  -7.3 |                     107 |                          57.6 |

#### Physical location, (a) unattributed

Budgets:

| Column [adopted by]                    | Document / date                                                                                          |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2022/23 original [pre-Brink]           | 2022/23 MTREF approved 26 May 2022 (2022/23 adj. budget p51)                                             |                                  82.3 |                                   85.5 |                -3.2 |                  -0.4 |                      45 |                          59.6 |
| 2022/23 adjusted [pre-Brink]           | 2022/23 adjustments budget, prepared before the 2–3 Mar 2023 NT engagement (p52)                         |                                  84.4 |                                   85.8 |                -1.4 |                   1.7 |                      46 |                          58.7 |
| 2023/24 original [Brink]               | 2023/24 MTREF approved 31 May 2023 (2023/24 adj. budget p48)                                             |                                  75.0 |                                   88.0 |               -13.1 |                  -7.8 |                      36 |                          47.3 |
| 2023/24 adjusted [Brink]               | 2023/24 adjustments budget, based on results to 31 Dec 2023 (p48)                                        |                                  76.5 |                                   88.0 |               -11.5 |                  -6.2 |                      36 |                          50.1 |
| 2024/25 original [Brink]               | 2024/25 MTREF, 'tabled for approval by Council in May 2024' (p76)                                        |                                  73.0 |                                   87.0 |               -13.9 |                  -9.7 |                      47 |                          47.9 |
| 2024/25 adjusted (adj. budget) [Moya]  | 2024/25 adjustments budget, based on results to 31 Dec 2024 (p47)                                        |                                  70.9 |                                   87.7 |               -16.8 |                 -11.8 |                      45 |                          47.2 |
| 2024/25 adjusted (App N, final) [Moya] | AR 2024/25 Appendix N pp503–515 (final adjusted incl. later amendments)                                  |                                  75.7 |                                   87.7 |               -12.0 |                  -7.1 |                      51 |                          52.7 |
| 2025/26 original [Moya]                | 2025/26 MTREF, Special Council 29 May 2025 (file title; p152 'approval in May 2025')                     |                                  82.2 |                                   88.5 |                -6.3 |                  -0.5 |                      38 |                          55.4 |
| 2025/26 adjusted [Moya]                | 2025/26 adjustments budget, based on results to 31 Dec 2025 (p52)                                        |                                  77.4 |                                   88.6 |               -11.2 |                  -5.4 |                      39 |                          39.5 |
| 2026/27 original [Moya]                | 2026/27 MTREF, version for Mayoral Committee 21 May 2026 (p65); total reconciles to SDBIP R2,856,300,538 |                                  86.0 |                                   90.1 |                -4.1 |                   3.2 |                      32 |                          37.0 |

Actual spend (kept separate):

| Column [adopted by]                                         | Document / date                                         |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:------------------------------------------------------------|:--------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] | AR 2024/25 Appendix N pp503–515 (audited annual report) |                                  75.6 |                                   86.5 |               -10.8 |                  -7.1 |                      47 |                          51.9 |

#### Option B (region tags only, population-split) — robustness

Budgets:

| Column [adopted by]                    | Document / date                                                                                          |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2022/23 original [pre-Brink]           | 2022/23 MTREF approved 26 May 2022 (2022/23 adj. budget p51)                                             |                                  81.9 |                                   82.7 |                -0.8 |                  -0.8 |                     107 |                          66.1 |
| 2022/23 adjusted [pre-Brink]           | 2022/23 adjustments budget, prepared before the 2–3 Mar 2023 NT engagement (p52)                         |                                  83.9 |                                   82.7 |                 1.2 |                   1.2 |                     107 |                          53.1 |
| 2023/24 original [Brink]               | 2023/24 MTREF approved 31 May 2023 (2023/24 adj. budget p48)                                             |                                  82.6 |                                   82.7 |                -0.1 |                  -0.1 |                     107 |                          67.4 |
| 2023/24 adjusted [Brink]               | 2023/24 adjustments budget, based on results to 31 Dec 2023 (p48)                                        |                                  82.3 |                                   82.7 |                -0.5 |                  -0.5 |                     107 |                          61.5 |
| 2024/25 original [Brink]               | 2024/25 MTREF, 'tabled for approval by Council in May 2024' (p76)                                        |                                  81.3 |                                   82.7 |                -1.5 |                  -1.5 |                     107 |                          64.1 |
| 2024/25 adjusted (adj. budget) [Moya]  | 2024/25 adjustments budget, based on results to 31 Dec 2024 (p47)                                        |                                  82.6 |                                   82.7 |                -0.1 |                  -0.1 |                     107 |                          60.1 |
| 2024/25 adjusted (App N, final) [Moya] | AR 2024/25 Appendix N pp503–515 (final adjusted incl. later amendments)                                  |                                  83.9 |                                   82.7 |                 1.2 |                   1.2 |                     107 |                          47.5 |
| 2025/26 original [Moya]                | 2025/26 MTREF, Special Council 29 May 2025 (file title; p152 'approval in May 2025')                     |                                  83.5 |                                   82.7 |                 0.8 |                   0.8 |                     107 |                          71.0 |
| 2025/26 adjusted [Moya]                | 2025/26 adjustments budget, based on results to 31 Dec 2025 (p52)                                        |                                  83.1 |                                   82.7 |                 0.4 |                   0.4 |                     107 |                          53.0 |
| 2026/27 original [Moya]                | 2026/27 MTREF, version for Mayoral Committee 21 May 2026 (p65); total reconciles to SDBIP R2,856,300,538 |                                  82.9 |                                   82.7 |                 0.1 |                   0.1 |                     107 |                          61.6 |

Actual spend (kept separate):

| Column [adopted by]                                         | Document / date                                         |   Spend-weighted mean % Black African |   Population-weighted mean, same wards |   Gap (spend − pop) |   Gap vs city (82.7%) |   Wards receiving capex |   Ward-attributed % of column |
|:------------------------------------------------------------|:--------------------------------------------------------|--------------------------------------:|---------------------------------------:|--------------------:|----------------------:|------------------------:|------------------------------:|
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] | AR 2024/25 Appendix N pp503–515 (audited annual report) |                                  84.2 |                                   82.7 |                 1.5 |                   1.5 |                     107 |                          48.1 |


## 4. Results by band

### 4.1 Service area, (b) — headline

Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–60: 6 wards, 4.9% of residents | 60–80: 5 wards, 4.0% of residents | 80–100: 69 wards, 75.4% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    218 |     153 |     197 |     337 |      367 |
| 2022/23 adjusted [pre-Brink]                                |     78 |     166 |     226 |     535 |      375 |
| 2023/24 original [Brink]                                    |    316 |      79 |      82 |     417 |      310 |
| 2023/24 adjusted [Brink]                                    |    204 |      63 |      67 |     482 |      280 |
| 2024/25 original [Brink]                                    |    252 |     176 |      65 |     528 |      241 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    286 |     190 |      54 |     524 |      207 |
| 2024/25 adjusted (App N, final) [Moya]                      |    229 |     210 |      55 |     502 |      227 |
| 2025/26 original [Moya]                                     |    370 |     158 |      92 |     623 |      339 |
| 2025/26 adjusted [Moya]                                     |    418 |     167 |      92 |     609 |      296 |
| 2026/27 original [Moya]                                     |    202 |     163 |      69 |     740 |      315 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    205 |     205 |      58 |     496 |      217 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    4.2 |     4.4 |     3.0 |     4.1 |     84.4 |
| 2022/23 adjusted [pre-Brink]                                |    1.4 |     4.6 |     3.3 |     6.4 |     84.2 |
| 2023/24 original [Brink]                                    |    7.0 |     2.6 |     1.4 |     6.0 |     83.0 |
| 2023/24 adjusted [Brink]                                    |    5.0 |     2.4 |     1.3 |     7.7 |     83.6 |
| 2024/25 original [Brink]                                    |    6.6 |     6.9 |     1.4 |     8.9 |     76.2 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    8.3 |     8.3 |     1.2 |     9.8 |     72.4 |
| 2024/25 adjusted (App N, final) [Moya]                      |    6.3 |     8.6 |     1.2 |     8.8 |     75.1 |
| 2025/26 original [Moya]                                     |    7.2 |     4.6 |     1.4 |     7.8 |     79.1 |
| 2025/26 adjusted [Moya]                                     |    8.9 |     5.3 |     1.6 |     8.3 |     75.9 |
| 2026/27 original [Moya]                                     |    4.2 |     5.1 |     1.1 |    10.0 |     79.6 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.9 |     8.8 |     1.3 |     9.1 |     74.9 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |   55.2 |    58.0 |    39.3 |    54.7 |  1,117.2 |
| 2022/23 adjusted [pre-Brink]                                |   19.7 |    63.0 |    45.1 |    86.9 |  1,142.4 |
| 2023/24 original [Brink]                                    |   79.8 |    29.8 |    16.3 |    67.7 |    944.4 |
| 2023/24 adjusted [Brink]                                    |   51.5 |    24.0 |    13.4 |    78.3 |    853.3 |
| 2024/25 original [Brink]                                    |   63.8 |    66.6 |    13.1 |    85.6 |    733.1 |
| 2024/25 adjusted (adj. budget) [Moya]                       |   72.3 |    72.1 |    10.8 |    85.1 |    629.4 |
| 2024/25 adjusted (App N, final) [Moya]                      |   57.8 |    79.5 |    11.0 |    81.5 |    692.3 |
| 2025/26 original [Moya]                                     |   93.5 |    59.8 |    18.3 |   101.1 |  1,031.3 |
| 2025/26 adjusted [Moya]                                     |  105.6 |    63.4 |    18.4 |    98.8 |    900.7 |
| 2026/27 original [Moya]                                     |   51.0 |    61.8 |    13.7 |   120.2 |    960.9 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   51.8 |    77.8 |    11.6 |    80.5 |    662.2 |


Rand per resident in the 80–100 band is below the average of the other four bands in 3 of 9 budget columns: 2024/25 original, 2024/25 adjusted (adj. budget), 2025/26 adjusted. The 60–80 band (5 wards) has the highest rand per resident in 10 of 11 columns. That reflects a small number of large projects (see §4.4), not a broad pattern.

### 4.2 Service area, (a)

Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–60: 6 wards, 4.9% of residents | 60–80: 5 wards, 4.0% of residents | 80–100: 69 wards, 75.4% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    176 |     125 |     195 |     294 |      311 |
| 2022/23 adjusted [pre-Brink]                                |     67 |     154 |     226 |     514 |      328 |
| 2023/24 original [Brink]                                    |    203 |       0 |      15 |     359 |      234 |
| 2023/24 adjusted [Brink]                                    |    120 |       0 |      10 |     434 |      222 |
| 2024/25 original [Brink]                                    |    190 |     122 |      15 |     486 |      195 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    233 |     153 |      29 |     486 |      175 |
| 2024/25 adjusted (App N, final) [Moya]                      |    196 |     182 |      29 |     486 |      205 |
| 2025/26 original [Moya]                                     |    247 |      70 |      20 |     569 |      264 |
| 2025/26 adjusted [Moya]                                     |    280 |      70 |      20 |     498 |      227 |
| 2026/27 original [Moya]                                     |     62 |      72 |      15 |     645 |      219 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    172 |     178 |      31 |     480 |      195 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    4.0 |     4.2 |     3.5 |     4.2 |     84.1 |
| 2022/23 adjusted [pre-Brink]                                |    1.4 |     4.9 |     3.7 |     6.9 |     83.1 |
| 2023/24 original [Brink]                                    |    6.2 |     0.0 |     0.4 |     7.0 |     86.4 |
| 2023/24 adjusted [Brink]                                    |    3.9 |     0.0 |     0.3 |     9.0 |     86.8 |
| 2024/25 original [Brink]                                    |    6.2 |     6.0 |     0.4 |    10.3 |     77.1 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    8.0 |     7.9 |     0.8 |    10.8 |     72.5 |
| 2024/25 adjusted (App N, final) [Moya]                      |    6.0 |     8.3 |     0.7 |     9.5 |     75.5 |
| 2025/26 original [Moya]                                     |    6.3 |     2.7 |     0.4 |     9.3 |     81.2 |
| 2025/26 adjusted [Moya]                                     |    8.1 |     3.1 |     0.5 |     9.3 |     79.1 |
| 2026/27 original [Moya]                                     |    1.9 |     3.4 |     0.4 |    12.8 |     81.6 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.5 |     8.5 |     0.8 |     9.9 |     75.3 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |   44.6 |    47.3 |    38.9 |    47.7 |    946.4 |
| 2022/23 adjusted [pre-Brink]                                |   16.9 |    58.5 |    45.1 |    83.5 |  1,000.7 |
| 2023/24 original [Brink]                                    |   51.3 |     0.0 |     3.0 |    58.2 |    713.8 |
| 2023/24 adjusted [Brink]                                    |   30.3 |     0.0 |     2.0 |    70.5 |    677.8 |
| 2024/25 original [Brink]                                    |   48.0 |    46.2 |     3.0 |    79.0 |    593.5 |
| 2024/25 adjusted (adj. budget) [Moya]                       |   58.9 |    58.0 |     5.8 |    79.0 |    532.4 |
| 2024/25 adjusted (App N, final) [Moya]                      |   49.5 |    69.0 |     5.8 |    79.0 |    625.1 |
| 2025/26 original [Moya]                                     |   62.5 |    26.6 |     4.0 |    92.4 |    803.1 |
| 2025/26 adjusted [Moya]                                     |   70.7 |    26.6 |     4.0 |    80.8 |    690.3 |
| 2026/27 original [Moya]                                     |   15.7 |    27.4 |     3.0 |   104.7 |    667.6 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   43.6 |    67.4 |     6.2 |    78.0 |    594.4 |


### 4.3 Physical location (secondary), (b) and (a)

**(b)**

Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–60: 6 wards, 4.9% of residents | 60–80: 5 wards, 4.0% of residents | 80–100: 69 wards, 75.4% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    244 |     377 |     666 |     849 |      424 |
| 2022/23 adjusted [pre-Brink]                                |    110 |     354 |     599 |     573 |      422 |
| 2023/24 original [Brink]                                    |    470 |     216 |   1,261 |     615 |      290 |
| 2023/24 adjusted [Brink]                                    |    293 |     187 |   1,135 |     817 |      240 |
| 2024/25 original [Brink]                                    |    395 |     387 |   1,272 |     565 |      258 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    401 |     355 |   1,257 |     569 |      220 |
| 2024/25 adjusted (App N, final) [Moya]                      |    303 |     389 |   1,139 |     546 |      270 |
| 2025/26 original [Moya]                                     |    416 |     226 |   1,090 |     829 |      404 |
| 2025/26 adjusted [Moya]                                     |    536 |     266 |   1,114 |     616 |      319 |
| 2026/27 original [Moya]                                     |    357 |     239 |     598 |   1,079 |      404 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    278 |     380 |   1,139 |     539 |      261 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    3.5 |     8.1 |     7.5 |     7.8 |     73.1 |
| 2022/23 adjusted [pre-Brink]                                |    1.7 |     8.1 |     7.2 |     5.6 |     77.4 |
| 2023/24 original [Brink]                                    |    8.3 |     5.7 |    17.5 |     7.0 |     61.5 |
| 2023/24 adjusted [Brink]                                    |    6.0 |     5.7 |    18.4 |    10.7 |     59.2 |
| 2024/25 original [Brink]                                    |    7.2 |    10.6 |    18.4 |     6.7 |     57.1 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    8.1 |    10.8 |    20.1 |     7.4 |     53.7 |
| 2024/25 adjusted (App N, final) [Moya]                      |    5.6 |    10.8 |    16.7 |     6.5 |     60.3 |
| 2025/26 original [Moya]                                     |    5.9 |     4.8 |    12.3 |     7.6 |     69.4 |
| 2025/26 adjusted [Moya]                                     |    8.9 |     6.6 |    14.5 |     6.5 |     63.5 |
| 2026/27 original [Moya]                                     |    5.3 |     5.3 |     7.0 |    10.3 |     72.1 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.3 |    10.9 |    17.2 |     6.6 |     60.0 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |   61.7 |   143.0 |   132.9 |   137.8 |  1,291.3 |
| 2022/23 adjusted [pre-Brink]                                |   27.7 |   134.2 |   119.6 |    93.0 |  1,285.4 |
| 2023/24 original [Brink]                                    |  118.9 |    81.7 |   251.8 |    99.8 |    884.0 |
| 2023/24 adjusted [Brink]                                    |   74.1 |    70.8 |   226.7 |   132.6 |    730.8 |
| 2024/25 original [Brink]                                    |   99.8 |   146.6 |   253.9 |    91.7 |    787.1 |
| 2024/25 adjusted (adj. budget) [Moya]                       |  101.4 |   134.6 |   251.1 |    92.3 |    671.5 |
| 2024/25 adjusted (App N, final) [Moya]                      |   76.7 |   147.6 |   227.5 |    88.7 |    822.0 |
| 2025/26 original [Moya]                                     |  105.3 |    85.6 |   217.6 |   134.6 |  1,230.3 |
| 2025/26 adjusted [Moya]                                     |  135.6 |   100.9 |   222.5 |   100.0 |    971.3 |
| 2026/27 original [Moya]                                     |   90.3 |    90.5 |   119.4 |   175.2 |  1,231.5 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   70.3 |   143.9 |   227.4 |    87.6 |    795.1 |


**(a)**

Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–60: 6 wards, 4.9% of residents | 60–80: 5 wards, 4.0% of residents | 80–100: 69 wards, 75.4% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    216 |     357 |     661 |     817 |      397 |
| 2022/23 adjusted [pre-Brink]                                |    106 |     353 |     599 |     568 |      421 |
| 2023/24 original [Brink]                                    |    361 |     127 |   1,153 |     510 |      216 |
| 2023/24 adjusted [Brink]                                    |    231 |     127 |   1,059 |     752 |      203 |
| 2024/25 original [Brink]                                    |    331 |     283 |   1,099 |     505 |      208 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    350 |     298 |   1,183 |     505 |      188 |
| 2024/25 adjusted (App N, final) [Moya]                      |    262 |     338 |   1,065 |     505 |      244 |
| 2025/26 original [Moya]                                     |    275 |      94 |     943 |     738 |      312 |
| 2025/26 adjusted [Moya]                                     |    356 |     112 |     960 |     498 |      225 |
| 2026/27 original [Moya]                                     |     62 |      72 |     541 |     881 |      250 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    238 |     328 |   1,064 |     499 |      235 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    3.3 |     8.1 |     7.9 |     8.0 |     72.7 |
| 2022/23 adjusted [pre-Brink]                                |    1.6 |     8.1 |     7.2 |     5.6 |     77.5 |
| 2023/24 original [Brink]                                    |    8.2 |     4.3 |    20.7 |     7.5 |     59.3 |
| 2023/24 adjusted [Brink]                                    |    5.5 |     4.5 |    20.0 |    11.5 |     58.4 |
| 2024/25 original [Brink]                                    |    7.4 |     9.5 |    19.5 |     7.3 |     56.2 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    8.1 |    10.4 |    21.6 |     7.5 |     52.4 |
| 2024/25 adjusted (App N, final) [Moya]                      |    5.4 |    10.4 |    17.2 |     6.6 |     60.4 |
| 2025/26 original [Moya]                                     |    5.1 |     2.6 |    13.8 |     8.8 |     69.7 |
| 2025/26 adjusted [Moya]                                     |    8.3 |     3.9 |    17.6 |     7.4 |     62.8 |
| 2026/27 original [Moya]                                     |    1.5 |     2.6 |    10.2 |    13.5 |     72.2 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.0 |    10.4 |    17.8 |     6.8 |     60.0 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |   54.6 |   135.4 |   131.9 |   132.7 |  1,209.4 |
| 2022/23 adjusted [pre-Brink]                                |   26.9 |   133.6 |   119.6 |    92.2 |  1,282.1 |
| 2023/24 original [Brink]                                    |   91.3 |    48.0 |   230.3 |    82.8 |    658.1 |
| 2023/24 adjusted [Brink]                                    |   58.3 |    48.0 |   211.4 |   122.1 |    618.0 |
| 2024/25 original [Brink]                                    |   83.7 |   107.2 |   219.4 |    82.0 |    632.5 |
| 2024/25 adjusted (adj. budget) [Moya]                       |   88.5 |   113.0 |   236.2 |    82.0 |    572.3 |
| 2024/25 adjusted (App N, final) [Moya]                      |   66.3 |   128.0 |   212.7 |    82.0 |    744.2 |
| 2025/26 original [Moya]                                     |   69.5 |    35.5 |   188.2 |   119.9 |    949.8 |
| 2025/26 adjusted [Moya]                                     |   89.9 |    42.3 |   191.6 |    80.8 |    684.1 |
| 2026/27 original [Moya]                                     |   15.7 |    27.4 |   108.0 |   143.0 |    762.2 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   60.1 |   124.4 |   212.4 |    81.0 |    716.7 |


**Option B (region tags only) — robustness**

Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–60: 6 wards, 4.9% of residents | 60–80: 5 wards, 4.0% of residents | 80–100: 69 wards, 75.4% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    566 |     392 |     355 |     601 |      455 |
| 2022/23 adjusted [pre-Brink]                                |    329 |     283 |     353 |     422 |      383 |
| 2023/24 original [Brink]                                    |    377 |     369 |     433 |     404 |      392 |
| 2023/24 adjusted [Brink]                                    |    315 |     308 |     348 |     378 |      319 |
| 2024/25 original [Brink]                                    |    384 |     394 |     451 |     426 |      361 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    332 |     332 |     344 |     452 |      341 |
| 2024/25 adjusted (App N, final) [Moya]                      |    251 |     245 |     220 |     366 |      279 |
| 2025/26 original [Moya]                                     |    421 |     399 |     393 |     417 |      441 |
| 2025/26 adjusted [Moya]                                     |    359 |     339 |     363 |     330 |      366 |
| 2026/27 original [Moya]                                     |    531 |     388 |     266 |     505 |      441 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    243 |     240 |     217 |     355 |      280 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    7.8 |     8.0 |     3.8 |     5.3 |     75.1 |
| 2022/23 adjusted [pre-Brink]                                |    5.6 |     7.2 |     4.7 |     4.6 |     78.0 |
| 2023/24 original [Brink]                                    |    6.0 |     8.8 |     5.5 |     4.1 |     75.5 |
| 2023/24 adjusted [Brink]                                    |    6.1 |     9.0 |     5.3 |     4.7 |     74.8 |
| 2024/25 original [Brink]                                    |    6.5 |     9.9 |     6.0 |     4.6 |     73.0 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    6.0 |     9.1 |     4.9 |     5.3 |     74.7 |
| 2024/25 adjusted (App N, final) [Moya]                      |    5.7 |     8.4 |     4.0 |     5.4 |     76.6 |
| 2025/26 original [Moya]                                     |    6.1 |     8.7 |     4.5 |     3.9 |     76.9 |
| 2025/26 adjusted [Moya]                                     |    6.2 |     8.8 |     5.0 |     3.7 |     76.4 |
| 2026/27 original [Moya]                                     |    7.6 |     8.4 |     3.0 |     4.7 |     76.3 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.6 |     8.2 |     3.9 |     5.2 |     77.1 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |  143.1 |   148.5 |    70.9 |    97.6 |  1,385.9 |
| 2022/23 adjusted [pre-Brink]                                |   83.1 |   107.1 |    70.4 |    68.6 |  1,166.8 |
| 2023/24 original [Brink]                                    |   95.3 |   139.8 |    86.5 |    65.7 |  1,195.7 |
| 2023/24 adjusted [Brink]                                    |   79.6 |   116.7 |    69.4 |    61.3 |    971.4 |
| 2024/25 original [Brink]                                    |   97.1 |   149.4 |    90.1 |    69.1 |  1,098.5 |
| 2024/25 adjusted (adj. budget) [Moya]                       |   83.9 |   125.8 |    68.8 |    73.3 |  1,037.9 |
| 2024/25 adjusted (App N, final) [Moya]                      |   63.5 |    92.8 |    43.9 |    59.5 |    851.4 |
| 2025/26 original [Moya]                                     |  106.4 |   151.4 |    78.5 |    67.6 |  1,342.4 |
| 2025/26 adjusted [Moya]                                     |   90.9 |   128.4 |    72.5 |    53.6 |  1,115.1 |
| 2026/27 original [Moya]                                     |  134.3 |   147.2 |    53.2 |    82.0 |  1,343.5 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   61.4 |    91.0 |    43.4 |    57.6 |    852.0 |


### 4.4 Sensitivity bands and single-project dependence

**80–100 split into 80–90 (5 wards, thin) and 90–100 (64 wards), service area (b):**

Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–60: 6 wards, 4.9% of residents | 60–80: 5 wards, 4.0% of residents | 80–90: 5 wards, 4.3% of residents | 90–100: 64 wards, 71.1% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–90 |   90–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    218 |     153 |     197 |     337 |   1,285 |      311 |
| 2022/23 adjusted [pre-Brink]                                |     78 |     166 |     226 |     535 |   1,302 |      318 |
| 2023/24 original [Brink]                                    |    316 |      79 |      82 |     417 |     598 |      292 |
| 2023/24 adjusted [Brink]                                    |    204 |      63 |      67 |     482 |     468 |      269 |
| 2024/25 original [Brink]                                    |    252 |     176 |      65 |     528 |     451 |      228 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    286 |     190 |      54 |     524 |     370 |      197 |
| 2024/25 adjusted (App N, final) [Moya]                      |    229 |     210 |      55 |     502 |     308 |      222 |
| 2025/26 original [Moya]                                     |    370 |     158 |      92 |     623 |     404 |      335 |
| 2025/26 adjusted [Moya]                                     |    418 |     167 |      92 |     609 |     162 |      304 |
| 2026/27 original [Moya]                                     |    202 |     163 |      69 |     740 |     256 |      319 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    205 |     205 |      58 |     496 |     319 |      211 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–90 |   90–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    4.2 |     4.4 |     3.0 |     4.1 |    17.0 |     67.3 |
| 2022/23 adjusted [pre-Brink]                                |    1.4 |     4.6 |     3.3 |     6.4 |    16.9 |     67.3 |
| 2023/24 original [Brink]                                    |    7.0 |     2.6 |     1.4 |     6.0 |     9.2 |     73.8 |
| 2023/24 adjusted [Brink]                                    |    5.0 |     2.4 |     1.3 |     7.7 |     8.0 |     75.6 |
| 2024/25 original [Brink]                                    |    6.6 |     6.9 |     1.4 |     8.9 |     8.2 |     68.0 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    8.3 |     8.3 |     1.2 |     9.8 |     7.5 |     64.9 |
| 2024/25 adjusted (App N, final) [Moya]                      |    6.3 |     8.6 |     1.2 |     8.8 |     5.9 |     69.2 |
| 2025/26 original [Moya]                                     |    7.2 |     4.6 |     1.4 |     7.8 |     5.4 |     73.7 |
| 2025/26 adjusted [Moya]                                     |    8.9 |     5.3 |     1.6 |     8.3 |     2.4 |     73.5 |
| 2026/27 original [Moya]                                     |    4.2 |     5.1 |     1.1 |    10.0 |     3.7 |     75.8 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.9 |     8.8 |     1.3 |     9.1 |     6.3 |     68.6 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–90 |   90–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |   55.2 |    58.0 |    39.3 |    54.7 |   225.7 |    891.5 |
| 2022/23 adjusted [pre-Brink]                                |   19.7 |    63.0 |    45.1 |    86.9 |   228.7 |    913.7 |
| 2023/24 original [Brink]                                    |   79.8 |    29.8 |    16.3 |    67.7 |   104.9 |    839.4 |
| 2023/24 adjusted [Brink]                                    |   51.5 |    24.0 |    13.4 |    78.3 |    82.1 |    771.1 |
| 2024/25 original [Brink]                                    |   63.8 |    66.6 |    13.1 |    85.6 |    79.2 |    654.0 |
| 2024/25 adjusted (adj. budget) [Moya]                       |   72.3 |    72.1 |    10.8 |    85.1 |    65.0 |    564.4 |
| 2024/25 adjusted (App N, final) [Moya]                      |   57.8 |    79.5 |    11.0 |    81.5 |    54.1 |    638.3 |
| 2025/26 original [Moya]                                     |   93.5 |    59.8 |    18.3 |   101.1 |    70.9 |    960.5 |
| 2025/26 adjusted [Moya]                                     |  105.6 |    63.4 |    18.4 |    98.8 |    28.4 |    872.3 |
| 2026/27 original [Moya]                                     |   51.0 |    61.8 |    13.7 |   120.2 |    45.0 |    915.9 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   51.8 |    77.8 |    11.6 |    80.5 |    55.9 |    606.3 |


**Merged 40–80 "mixed" band (11 wards), service area (b):**

Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–80 (mixed): 11 wards, 9.0% of residents | 80–100: 69 wards, 75.4% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–80 (mixed) |   80–100 |
|:------------------------------------------------------------|-------:|--------:|----------------:|---------:|
| 2022/23 original [pre-Brink]                                |    218 |     153 |             260 |      367 |
| 2022/23 adjusted [pre-Brink]                                |     78 |     166 |             365 |      375 |
| 2023/24 original [Brink]                                    |    316 |      79 |             232 |      310 |
| 2023/24 adjusted [Brink]                                    |    204 |      63 |             253 |      280 |
| 2024/25 original [Brink]                                    |    252 |     176 |             273 |      241 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    286 |     190 |             265 |      207 |
| 2024/25 adjusted (App N, final) [Moya]                      |    229 |     210 |             256 |      227 |
| 2025/26 original [Moya]                                     |    370 |     158 |             330 |      339 |
| 2025/26 adjusted [Moya]                                     |    418 |     167 |             324 |      296 |
| 2026/27 original [Moya]                                     |    202 |     163 |             370 |      315 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    205 |     205 |             255 |      217 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–80 (mixed) |   80–100 |
|:------------------------------------------------------------|-------:|--------:|----------------:|---------:|
| 2022/23 original [pre-Brink]                                |    4.2 |     4.4 |             7.1 |     84.4 |
| 2022/23 adjusted [pre-Brink]                                |    1.4 |     4.6 |             9.7 |     84.2 |
| 2023/24 original [Brink]                                    |    7.0 |     2.6 |             7.4 |     83.0 |
| 2023/24 adjusted [Brink]                                    |    5.0 |     2.4 |             9.0 |     83.6 |
| 2024/25 original [Brink]                                    |    6.6 |     6.9 |            10.3 |     76.2 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    8.3 |     8.3 |            11.0 |     72.4 |
| 2024/25 adjusted (App N, final) [Moya]                      |    6.3 |     8.6 |            10.0 |     75.1 |
| 2025/26 original [Moya]                                     |    7.2 |     4.6 |             9.2 |     79.1 |
| 2025/26 adjusted [Moya]                                     |    8.9 |     5.3 |             9.9 |     75.9 |
| 2026/27 original [Moya]                                     |    4.2 |     5.1 |            11.1 |     79.6 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.9 |     8.8 |            10.4 |     74.9 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–80 (mixed) |   80–100 |
|:------------------------------------------------------------|-------:|--------:|----------------:|---------:|
| 2022/23 original [pre-Brink]                                |   55.2 |    58.0 |            94.0 |  1,117.2 |
| 2022/23 adjusted [pre-Brink]                                |   19.7 |    63.0 |           132.0 |  1,142.4 |
| 2023/24 original [Brink]                                    |   79.8 |    29.8 |            84.1 |    944.4 |
| 2023/24 adjusted [Brink]                                    |   51.5 |    24.0 |            91.6 |    853.3 |
| 2024/25 original [Brink]                                    |   63.8 |    66.6 |            98.7 |    733.1 |
| 2024/25 adjusted (adj. budget) [Moya]                       |   72.3 |    72.1 |            95.9 |    629.4 |
| 2024/25 adjusted (App N, final) [Moya]                      |   57.8 |    79.5 |            92.5 |    692.3 |
| 2025/26 original [Moya]                                     |   93.5 |    59.8 |           119.4 |  1,031.3 |
| 2025/26 adjusted [Moya]                                     |  105.6 |    63.4 |           117.2 |    900.7 |
| 2026/27 original [Moya]                                     |   51.0 |    61.8 |           133.9 |    960.9 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   51.8 |    77.8 |            92.1 |    662.2 |


**80–100 split and 40–80 merged, physical location (b):**

Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–60: 6 wards, 4.9% of residents | 60–80: 5 wards, 4.0% of residents | 80–90: 5 wards, 4.3% of residents | 90–100: 64 wards, 71.1% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–90 |   90–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    244 |     377 |     666 |     849 |   1,423 |      363 |
| 2022/23 adjusted [pre-Brink]                                |    110 |     354 |     599 |     573 |   1,557 |      352 |
| 2023/24 original [Brink]                                    |    470 |     216 |   1,261 |     615 |     659 |      268 |
| 2023/24 adjusted [Brink]                                    |    293 |     187 |   1,135 |     817 |     468 |      226 |
| 2024/25 original [Brink]                                    |    395 |     387 |   1,272 |     565 |     514 |      243 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    401 |     355 |   1,257 |     569 |     420 |      208 |
| 2024/25 adjusted (App N, final) [Moya]                      |    303 |     389 |   1,139 |     546 |     350 |      265 |
| 2025/26 original [Moya]                                     |    416 |     226 |   1,090 |     829 |     554 |      395 |
| 2025/26 adjusted [Moya]                                     |    536 |     266 |   1,114 |     616 |     277 |      321 |
| 2026/27 original [Moya]                                     |    357 |     239 |     598 |   1,079 |     594 |      393 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    278 |     380 |   1,139 |     539 |     360 |      255 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–90 |   90–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |    3.5 |     8.1 |     7.5 |     7.8 |    14.1 |     58.9 |
| 2022/23 adjusted [pre-Brink]                                |    1.7 |     8.1 |     7.2 |     5.6 |    16.5 |     61.0 |
| 2023/24 original [Brink]                                    |    8.3 |     5.7 |    17.5 |     7.0 |     8.1 |     53.5 |
| 2023/24 adjusted [Brink]                                    |    6.0 |     5.7 |    18.4 |    10.7 |     6.7 |     52.5 |
| 2024/25 original [Brink]                                    |    7.2 |    10.6 |    18.4 |     6.7 |     6.6 |     50.5 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    8.1 |    10.8 |    20.1 |     7.4 |     5.9 |     47.8 |
| 2024/25 adjusted (App N, final) [Moya]                      |    5.6 |    10.8 |    16.7 |     6.5 |     4.5 |     55.8 |
| 2025/26 original [Moya]                                     |    5.9 |     4.8 |    12.3 |     7.6 |     5.5 |     63.9 |
| 2025/26 adjusted [Moya]                                     |    8.9 |     6.6 |    14.5 |     6.5 |     3.2 |     60.3 |
| 2026/27 original [Moya]                                     |    5.3 |     5.3 |     7.0 |    10.3 |     6.1 |     66.0 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.3 |    10.9 |    17.2 |     6.6 |     4.8 |     55.3 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–60 |   60–80 |   80–90 |   90–100 |
|:------------------------------------------------------------|-------:|--------:|--------:|--------:|--------:|---------:|
| 2022/23 original [pre-Brink]                                |   61.7 |   143.0 |   132.9 |   137.8 |   249.8 |  1,041.5 |
| 2022/23 adjusted [pre-Brink]                                |   27.7 |   134.2 |   119.6 |    93.0 |   273.4 |  1,012.0 |
| 2023/24 original [Brink]                                    |  118.9 |    81.7 |   251.8 |    99.8 |   115.8 |    768.2 |
| 2023/24 adjusted [Brink]                                    |   74.1 |    70.8 |   226.7 |   132.6 |    82.1 |    648.6 |
| 2024/25 original [Brink]                                    |   99.8 |   146.6 |   253.9 |    91.7 |    90.3 |    696.7 |
| 2024/25 adjusted (adj. budget) [Moya]                       |  101.4 |   134.6 |   251.1 |    92.3 |    73.7 |    597.8 |
| 2024/25 adjusted (App N, final) [Moya]                      |   76.7 |   147.6 |   227.5 |    88.7 |    61.5 |    760.5 |
| 2025/26 original [Moya]                                     |  105.3 |    85.6 |   217.6 |   134.6 |    97.3 |  1,133.0 |
| 2025/26 adjusted [Moya]                                     |  135.6 |   100.9 |   222.5 |   100.0 |    48.6 |    922.7 |
| 2026/27 original [Moya]                                     |   90.3 |    90.5 |   119.4 |   175.2 |   104.4 |  1,127.2 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   70.3 |   143.9 |   227.4 |    87.6 |    63.2 |    731.9 |


Bands: 0–20: 12 wards, 6.3% of residents | 20–40: 15 wards, 9.4% of residents | 40–80 (mixed): 11 wards, 9.0% of residents | 80–100: 69 wards, 75.4% of residents

*Rand per resident* (band capex ÷ band population, all wards in the band):

|                                                             |   0–20 |   20–40 |   40–80 (mixed) |   80–100 |
|:------------------------------------------------------------|-------:|--------:|----------------:|---------:|
| 2022/23 original [pre-Brink]                                |    244 |     377 |             748 |      424 |
| 2022/23 adjusted [pre-Brink]                                |    110 |     354 |             587 |      422 |
| 2023/24 original [Brink]                                    |    470 |     216 |             971 |      290 |
| 2023/24 adjusted [Brink]                                    |    293 |     187 |             993 |      240 |
| 2024/25 original [Brink]                                    |    395 |     387 |             955 |      258 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    401 |     355 |             949 |      220 |
| 2024/25 adjusted (App N, final) [Moya]                      |    303 |     389 |             873 |      270 |
| 2025/26 original [Moya]                                     |    416 |     226 |             973 |      404 |
| 2025/26 adjusted [Moya]                                     |    536 |     266 |             891 |      319 |
| 2026/27 original [Moya]                                     |    357 |     239 |             814 |      404 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    278 |     380 |             870 |      261 |

*Share of attributed capex (%)*, to compare with the population shares above:

|                                                             |   0–20 |   20–40 |   40–80 (mixed) |   80–100 |
|:------------------------------------------------------------|-------:|--------:|----------------:|---------:|
| 2022/23 original [pre-Brink]                                |    3.5 |     8.1 |            15.3 |     73.1 |
| 2022/23 adjusted [pre-Brink]                                |    1.7 |     8.1 |            12.8 |     77.4 |
| 2023/24 original [Brink]                                    |    8.3 |     5.7 |            24.5 |     61.5 |
| 2023/24 adjusted [Brink]                                    |    6.0 |     5.7 |            29.1 |     59.2 |
| 2024/25 original [Brink]                                    |    7.2 |    10.6 |            25.1 |     57.1 |
| 2024/25 adjusted (adj. budget) [Moya]                       |    8.1 |    10.8 |            27.5 |     53.7 |
| 2024/25 adjusted (App N, final) [Moya]                      |    5.6 |    10.8 |            23.2 |     60.3 |
| 2025/26 original [Moya]                                     |    5.9 |     4.8 |            19.9 |     69.4 |
| 2025/26 adjusted [Moya]                                     |    8.9 |     6.6 |            21.1 |     63.5 |
| 2026/27 original [Moya]                                     |    5.3 |     5.3 |            17.3 |     72.1 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |    5.3 |    10.9 |            23.8 |     60.0 |

*Rand amount (R m)*:

|                                                             |   0–20 |   20–40 |   40–80 (mixed) |   80–100 |
|:------------------------------------------------------------|-------:|--------:|----------------:|---------:|
| 2022/23 original [pre-Brink]                                |   61.7 |   143.0 |           270.7 |  1,291.3 |
| 2022/23 adjusted [pre-Brink]                                |   27.7 |   134.2 |           212.6 |  1,285.4 |
| 2023/24 original [Brink]                                    |  118.9 |    81.7 |           351.6 |    884.0 |
| 2023/24 adjusted [Brink]                                    |   74.1 |    70.8 |           359.3 |    730.8 |
| 2024/25 original [Brink]                                    |   99.8 |   146.6 |           345.7 |    787.1 |
| 2024/25 adjusted (adj. budget) [Moya]                       |  101.4 |   134.6 |           343.4 |    671.5 |
| 2024/25 adjusted (App N, final) [Moya]                      |   76.7 |   147.6 |           316.2 |    822.0 |
| 2025/26 original [Moya]                                     |  105.3 |    85.6 |           352.3 |  1,230.3 |
| 2025/26 adjusted [Moya]                                     |  135.6 |   100.9 |           322.5 |    971.3 |
| 2026/27 original [Moya]                                     |   90.3 |    90.5 |           294.6 |  1,231.5 |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |   70.3 |   143.9 |           314.9 |    795.1 |


Band cells (column × band) where **one project accounts for more than half of the band's money**, for Option A (b). These band figures depend on a single project:

| Band scheme   | Basis    | Column                          | Band   |   Band R m | Single project                                             |   Its share of band money % |
|:--------------|:---------|:--------------------------------|:-------|-----------:|:-----------------------------------------------------------|----------------------------:|
| headline      | location | 2023/24 adjusted                | 40–60  |      226.7 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        66.0 |
| headline      | location | 2023/24 original                | 40–60  |      251.8 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        59.6 |
| headline      | location | 2024/25 actual                  | 40–60  |      227.4 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure |                        66.0 |
| headline      | location | 2024/25 adjusted (App N, final) | 40–60  |      227.5 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure |                        65.9 |
| headline      | location | 2024/25 adjusted (adj. budget)  | 40–60  |      251.1 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        59.7 |
| headline      | location | 2024/25 original                | 40–60  |      253.9 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        59.1 |
| headline      | location | 2025/26 adjusted                | 40–60  |      222.5 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        68.7 |
| headline      | location | 2025/26 original                | 40–60  |      217.6 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        68.9 |
| headline      | location | 2026/27 original                | 40–60  |      119.4 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure |                        75.4 |
| headline      | service  | 2022/23 adjusted                | 0–20   |       19.7 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.5 |
| headline      | service  | 2022/23 original                | 0–20   |       55.2 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.8 |
| headline      | service  | 2023/24 adjusted                | 0–20   |       51.5 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        56.3 |
| headline      | service  | 2023/24 original                | 0–20   |       79.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        57.6 |
| headline      | service  | 2024/25 actual                  | 0–20   |       51.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        61.2 |
| headline      | service  | 2024/25 adjusted (App N, final) | 0–20   |       57.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        64.8 |
| headline      | service  | 2024/25 adjusted (adj. budget)  | 0–20   |       72.3 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.8 |
| headline      | service  | 2024/25 original                | 0–20   |       63.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        60.4 |
| headline      | service  | 2022/23 adjusted                | 20–40  |       63.0 | Electricity for All - Region 6                             |                        81.5 |
| headline      | service  | 2022/23 original                | 20–40  |       58.0 | Electricity for All - Region 6                             |                        61.8 |
| headline      | service  | 2023/24 adjusted                | 40–60  |       13.4 | Electricity for All - Region 4                             |                        54.1 |
| headline      | service  | 2024/25 actual                  | 40–60  |       11.6 | Region 4 (Public Lighting)                                 |                        53.2 |
| headline      | service  | 2024/25 adjusted (App N, final) | 40–60  |       11.0 | Region 4 (Public Lighting)                                 |                        52.3 |
| headline      | service  | 2024/25 adjusted (adj. budget)  | 40–60  |       10.8 | Region 4 (Public Lighting)                                 |                        53.5 |
| merged_40_80  | service  | 2022/23 adjusted                | 0–20   |       19.7 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.5 |
| merged_40_80  | service  | 2022/23 original                | 0–20   |       55.2 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.8 |
| merged_40_80  | service  | 2023/24 adjusted                | 0–20   |       51.5 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        56.3 |
| merged_40_80  | service  | 2023/24 original                | 0–20   |       79.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        57.6 |
| merged_40_80  | service  | 2024/25 actual                  | 0–20   |       51.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        61.2 |
| merged_40_80  | service  | 2024/25 adjusted (App N, final) | 0–20   |       57.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        64.8 |
| merged_40_80  | service  | 2024/25 adjusted (adj. budget)  | 0–20   |       72.3 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.8 |
| merged_40_80  | service  | 2024/25 original                | 0–20   |       63.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        60.4 |
| merged_40_80  | service  | 2022/23 adjusted                | 20–40  |       63.0 | Electricity for All - Region 6                             |                        81.5 |
| merged_40_80  | service  | 2022/23 original                | 20–40  |       58.0 | Electricity for All - Region 6                             |                        61.8 |
| split_80_100  | location | 2023/24 adjusted                | 40–60  |      226.7 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        66.0 |
| split_80_100  | location | 2023/24 original                | 40–60  |      251.8 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        59.6 |
| split_80_100  | location | 2024/25 actual                  | 40–60  |      227.4 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure |                        66.0 |
| split_80_100  | location | 2024/25 adjusted (App N, final) | 40–60  |      227.5 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure |                        65.9 |
| split_80_100  | location | 2024/25 adjusted (adj. budget)  | 40–60  |      251.1 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        59.7 |
| split_80_100  | location | 2024/25 original                | 40–60  |      253.9 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        59.1 |
| split_80_100  | location | 2025/26 adjusted                | 40–60  |      222.5 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        68.7 |
| split_80_100  | location | 2025/26 original                | 40–60  |      217.6 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture  |                        68.9 |
| split_80_100  | location | 2026/27 original                | 40–60  |      119.4 | Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure |                        75.4 |
| split_80_100  | location | 2026/27 original                | 80–90  |      104.4 | Bronkhorstspruit Water Purification Plant Refurbishment    |                        54.6 |
| split_80_100  | service  | 2022/23 adjusted                | 0–20   |       19.7 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.5 |
| split_80_100  | service  | 2022/23 original                | 0–20   |       55.2 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.8 |
| split_80_100  | service  | 2023/24 adjusted                | 0–20   |       51.5 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        56.3 |
| split_80_100  | service  | 2023/24 original                | 0–20   |       79.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        57.6 |
| split_80_100  | service  | 2024/25 actual                  | 0–20   |       51.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        61.2 |
| split_80_100  | service  | 2024/25 adjusted (App N, final) | 0–20   |       57.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        64.8 |
| split_80_100  | service  | 2024/25 adjusted (adj. budget)  | 0–20   |       72.3 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        51.8 |
| split_80_100  | service  | 2024/25 original                | 0–20   |       63.8 | Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)     |                        60.4 |
| split_80_100  | service  | 2022/23 adjusted                | 20–40  |       63.0 | Electricity for All - Region 6                             |                        81.5 |
| split_80_100  | service  | 2022/23 original                | 20–40  |       58.0 | Electricity for All - Region 6                             |                        61.8 |
| split_80_100  | service  | 2023/24 adjusted                | 40–60  |       13.4 | Electricity for All - Region 4                             |                        54.1 |
| split_80_100  | service  | 2024/25 actual                  | 40–60  |       11.6 | Region 4 (Public Lighting)                                 |                        53.2 |
| split_80_100  | service  | 2024/25 adjusted (App N, final) | 40–60  |       11.0 | Region 4 (Public Lighting)                                 |                        52.3 |
| split_80_100  | service  | 2024/25 adjusted (adj. budget)  | 40–60  |       10.8 | Region 4 (Public Lighting)                                 |                        53.5 |
| split_80_100  | service  | 2025/26 adjusted                | 80–90  |       28.4 | Electricity for All - Region 7                             |                        53.8 |

Number of such cells by scheme and basis (all combinations):

| scheme       | option   | basis    | mode   |   cells |
|:-------------|:---------|:---------|:-------|--------:|
| headline     | A        | location | a      |      17 |
| headline     | A        | location | b      |       9 |
| headline     | A        | service  | a      |      25 |
| headline     | A        | service  | b      |      14 |
| merged_40_80 | A        | location | a      |      11 |
| merged_40_80 | A        | service  | a      |      15 |
| merged_40_80 | A        | service  | b      |      10 |
| split_80_100 | A        | location | a      |      19 |
| split_80_100 | A        | location | b      |      10 |
| split_80_100 | A        | service  | a      |      27 |
| split_80_100 | A        | service  | b      |      15 |


## 5. What drove each step (service area, (b), in index terms)

For each step, each project's **effect on the index** is the change in the after-step index if that project alone had stayed at its before-step amount and wards. The **relabelling** part is the effect of a change in the project's ward %Black (ward attribution changed between years) at its after-step amount. Effects don't add exactly to the index change: when total attributed capex changes a lot, the counterfactuals interact.
- **Projects are linked** by WBS code without the funding segment (binary_v1 §7, §9.2), plus the documented manual links.
- **2022/23 → 2023/24:** the WBS coding scheme changed, so projects are linked by unique exact normalised-name matches ("name crosswalk").
- **From 2025/26** relabelling is zero by construction, because carried-forward wards don't change.
- **Location-basis** index changes are shown for comparison.

| Step                                              | Service index before   | after   | Δ     | Σ project effects   | …of which relabelling   | Location index Δ   | Name-crosswalk links   |
|:--------------------------------------------------|:-----------------------|:--------|:------|:--------------------|:------------------------|:-------------------|:-----------------------|
| 2022/23 original → 2022/23 adjusted               | 87.3                   | 88.6    | +1.33 | +1.35               | +0.00                   | +1.85              | 3                      |
| 2022/23 adjusted → 2023/24 original               | 88.6                   | 87.0    | -1.62 | -1.49               | +1.01                   | -8.65              | 47                     |
| 2023/24 original → 2023/24 adjusted               | 87.0                   | 88.5    | +1.52 | +1.71               | +0.00                   | +0.60              | 0                      |
| 2023/24 adjusted → 2024/25 original               | 88.5                   | 84.1    | -4.42 | -4.46               | -1.41                   | -3.22              | 3                      |
| 2024/25 original → 2024/25 adjusted (adj. budget) | 84.1                   | 81.5    | -2.55 | -2.80               | -0.12                   | -1.69              | 1                      |
| 2024/25 adjusted (adj. budget) → 2025/26 original | 81.5                   | 85.7    | +4.15 | +2.78               | +0.82                   | +9.75              | 1                      |
| 2025/26 original → 2025/26 adjusted               | 85.7                   | 83.8    | -1.86 | -2.02               | -0.01                   | -4.32              | 1                      |
| 2025/26 adjusted → 2026/27 original               | 83.8                   | 87.8    | +3.95 | +3.84               | -0.05                   | +6.66              | 4                      |

**2022/23 original → 2022/23 adjusted**: service index 87.3 → 88.6 (+1.33 pts).

| Project                                                           | Ward(s)                           | Ward % Black (before → after)   | Band   | R m before   | R m after   | Effect on index (pts)   | …relabelling   | Link   |
|:------------------------------------------------------------------|:----------------------------------|:--------------------------------|:-------|:-------------|:------------|:------------------------|:---------------|:-------|
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)            | 82                                | 11.3 → 11.3                     | 0–20   | 28.6         | 10.1        | +1.04                   | +0.00          |        |
| Construction of roads & stormwater - Thorntree View               | 90                                | 98.9 → 98.9                     | 80–100 | 31.5         | 126.8       | +0.78                   | +0.00          |        |
| Electricity for All - Region 6                                    | 101                               | 30.4 → 30.4                     | 20–40  | 35.8         | 51.3        | -0.67                   | +0.00          |        |
| Electricity for All - Region 4                                    | 70                                | 55.0                            | 40–60  | 0.0          | 16.9        | -0.42                   | +0.00          |        |
| Menlyn Taxi Interchange (Gobie)                                   | 46                                | 16.8 → 16.8                     | 0–20   | 10.0         | 2.9         | +0.38                   | +0.00          |        |
| Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure        | 5 wards (region split / township) | 98.7                            | 80–100 | 40.0         | 0.0         | -0.29                   | +0.00          |        |
| Townlands Project - Construction of 1,200 social housing units    | 58                                | 93.7 → 93.7                     | 80–100 | 85.2         | 148.8       | +0.25                   | +0.00          |        |
| Mamelodi Ext 11 water (Bulk and reticulation) and sanitation serv | 10                                | 98.8 → 98.8                     | 80–100 | 36.0         | 3.0         | -0.24                   | +0.00          |        |
| Soshanguve MM Sewer Reticulation                                  | 96                                | 47.5 → 47.5                     | 40–60  | 8.4          | 1.2         | +0.22                   | +0.00          |        |
| Electricity for All - Region 3                                    | 55                                | 75.7 → 75.7                     | 60–80  | 23.2         | 42.2        | -0.18                   | +0.00          |        |

**2022/23 adjusted → 2023/24 original**: service index 88.6 → 87.0 (-1.62 pts).

| Project                                                        | Ward(s)                            | Ward % Black (before → after)   | Band   | R m before   | R m after   | Effect on index (pts)   | …relabelling   | Link                               |
|:---------------------------------------------------------------|:-----------------------------------|:--------------------------------|:-------|:-------------|:------------|:------------------------|:---------------|:-----------------------------------|
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)         | 82                                 | 11.3 → 11.3                     | 0–20   | 10.1         | 46.0        | -2.46                   | +0.00          | name crosswalk (WBS scheme change) |
| Electricity for All - Region 6                                 | 101                                | 30.4                            | 20–40  | 51.3         | 0.0         | +2.44                   | +0.00          |                                    |
| Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture      | 5 wards (region split / township)  | 98.7 → 98.7                     | 80–100 | 11.4         | 150.0       | +1.62                   | +0.00          | name crosswalk (WBS scheme change) |
| Construction of roads & stormwater - Thorntree View            | 90                                 | 98.9                            | 80–100 | 126.8        | 0.0         | -1.19                   | +0.00          |                                    |
| Construction of roads & stormwater - Thorntree View            | 36                                 | 98.9 → 99.2                     | 80–100 | 9.5          | 90.2        | +0.94                   | +0.03          | name crosswalk (WBS scheme change) |
| Townlands Project - Construction of 1,200 social housing units | 58                                 | 93.7                            | 80–100 | 148.8        | 0.0         | -0.77                   | +0.00          |                                    |
| Electricity Distribution Loss                                  | 29                                 | 99.3 → 99.0                     | 80–100 | 7.2          | 68.0        | +0.68                   | -0.02          | name crosswalk (WBS scheme change) |
| Electricity for All - Region 4                                 | 12 wards (region split / township) | 56.1                            | 40–60  | 0.0          | 23.5        | -0.65                   | +0.00          |                                    |
| Ekangala Block A - F sewer reticulation and toilets            | 104                                | 99.4 → 99.4                     | 80–100 | 65.0         | 8.3         | -0.59                   | +0.00          |                                    |
| Electricity for All - Region 4                                 | 70                                 | 55.0                            | 40–60  | 16.9         | 0.0         | +0.47                   | +0.00          |                                    |

**2023/24 original → 2023/24 adjusted**: service index 87.0 → 88.5 (+1.52 pts).

| Project                                                        | Ward(s)                            | Ward % Black (before → after)   | Band   | R m before   | R m after   | Effect on index (pts)   | …relabelling   | Link   |
|:---------------------------------------------------------------|:-----------------------------------|:--------------------------------|:-------|:-------------|:------------|:------------------------|:---------------|:-------|
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)         | 82                                 | 11.3 → 11.3                     | 0–20   | 46.0         | 29.0        | +1.27                   | +0.00          |        |
| Electricity Distribution Loss                                  | 29                                 | 99.0 → 99.0                     | 80–100 | 68.0         | 30.0        | -0.38                   | +0.00          |        |
| Electricity for All - Region 1                                 | 32                                 | 99.2 → 99.2                     | 80–100 | 25.0         | 52.0        | +0.29                   | +0.00          |        |
| Menlyn Taxi Interchange (Gobie)                                | 83                                 | 15.7 → 15.7                     | 0–20   | 4.8          | 0.8         | +0.28                   | +0.00          |        |
| Townlands Project - Construction of 1,200 social housing units | 58                                 | 93.7                            | 80–100 | 0.0          | 48.8        | +0.26                   | +0.00          |        |
| Denneboom Depot                                                | 38                                 | 96.3 → 96.3                     | 80–100 | 33.5         | 10.6        | -0.17                   | +0.00          |        |
| Upgrading of Road from gravel to tar in Ekangala (Ward 103     | 103                                | 99.1 → 99.1                     | 80–100 | 13.0         | 26.6        | +0.14                   | +0.00          |        |
| New Parkmore LL Reservoir and HL Reservoir                     | 23 wards (region split / township) | 76.9 → 76.9                     | 60–80  | 40.0         | 28.0        | +0.14                   | +0.00          |        |
| Wildebees 400/132kV, 315MVA Infeed station                     | 26 wards (region split / township) | 77.9 → 77.9                     | 60–80  | 50.0         | 38.0        | +0.12                   | +0.00          |        |
| Wonderboom Intermodal Facility (Building Works)                | 3                                  | 77.1 → 77.1                     | 60–80  | 1.0          | 11.0        | -0.11                   | +0.00          |        |

**2023/24 adjusted → 2024/25 original**: service index 88.5 → 84.1 (-4.42 pts).

| Project                                                           | Ward(s)                            | Ward % Black (before → after)   | Band   | R m before   | R m after   | Effect on index (pts)   | …relabelling   | Link   |
|:------------------------------------------------------------------|:-----------------------------------|:--------------------------------|:-------|:-------------|:------------|:------------------------|:---------------|:-------|
| Construction of roads & stormwater - Thorntree View               | 29 wards (region split / township) | 99.2 → 95.6                     | 80–100 | 84.2         | 1.0         | -1.21                   | -0.00          |        |
| Electricity for All - Region 6                                    | 101                                | 76.9 → 30.4                     | 20–40  | 16.0         | 20.0        | -1.00                   | -0.96          |        |
| Contributions Roads - Garsfontein Road                            | 45                                 | 10.6                            | 0–20   | 0.0          | 9.5         | -0.73                   | +0.00          |        |
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)            | 82                                 | 11.3 → 11.3                     | 0–20   | 29.0         | 38.6        | -0.73                   | +0.00          |        |
| Sewer provision - Rama City                                       | 32                                 | 99.2 → 99.2                     | 80–100 | 2.0          | 37.9        | +0.59                   | +0.00          |        |
| (710026B) Replacement Of Critical Worn-Out Water Network Pipes (A | 53                                 | 73.4 → 33.6                     | 20–40  | 24.0         | 15.6        | -0.55                   | -0.65          |        |
| Electricity for All - Region 1                                    | 32                                 | 99.2 → 99.2                     | 80–100 | 52.0         | 20.0        | -0.49                   | +0.00          |        |
| Klipgat WWTW: Upgrading of existing infrastructure to 40Ml/d      | 29 wards (region split / township) | 95.6                            | 80–100 | 40.6         | 0.0         | -0.47                   | +0.00          |        |
| Townlands Project - Construction of 1,200 social housing units    | 58                                 | 93.7                            | 80–100 | 48.8         | 0.0         | -0.46                   | +0.00          |        |
| Electricity Distribution Loss                                     | 29                                 | 99.0                            | 80–100 | 30.0         | 0.0         | -0.45                   | +0.00          |        |

**2024/25 original → 2024/25 adjusted (adj. budget)**: service index 84.1 → 81.5 (-2.55 pts).

| Project                                                           | Ward(s)                            | Ward % Black (before → after)   | Band   | R m before   | R m after   | Effect on index (pts)   | …relabelling   | Link   |
|:------------------------------------------------------------------|:-----------------------------------|:--------------------------------|:-------|:-------------|:------------|:------------------------|:---------------|:-------|
| Contributions Roads - Garsfontein Road                            | 45                                 | 10.6 → 10.6                     | 0–20   | 9.5          | 21.4        | -0.99                   | +0.00          |        |
| Electricity for All - Region 6                                    | 101                                | 30.4 → 30.4                     | 20–40  | 20.0         | 4.0         | +0.92                   | +0.00          |        |
| Pretorious Park: sewer provision                                  | 91                                 | 40.0 → 40.0                     | 20–40  | 0.7          | 15.0        | -0.70                   | +0.00          |        |
| Sewer provision - Rama City                                       | 32                                 | 99.2 → 99.2                     | 80–100 | 37.9         | 12.4        | -0.50                   | +0.00          |        |
| Electricity for All - Region 4                                    | 12 wards (region split / township) | 56.1 → 56.1                     | 40–60  | 21.0         | 5.0         | +0.46                   | +0.00          |        |
| Turnaround of Municipal Water Service - Reduction of Water losses | 58                                 | 93.7 → 93.7                     | 80–100 | 20.0         | 50.0        | +0.43                   | +0.00          |        |
| Region (710026B) 1-2) Replacement Of Critical Worn-Out Water Netw | 53                                 | 33.6 → 33.6                     | 20–40  | 15.6         | 22.1        | -0.36                   | +0.00          |        |
| (710026A) Replacement Of Critical Worn-Out Water Network Pipes (A | 41 wards (region split / township) | 93.8 → 93.8                     | 80–100 | 26.5         | 2.0         | -0.34                   | +0.00          |        |
| Electricity for All - Region 1                                    | 32                                 | 99.2 → 99.2                     | 80–100 | 20.0         | 36.0        | +0.33                   | +0.00          |        |
| New Clinic Lusaka                                                 | 10                                 | 98.8 → 98.8                     | 80–100 | 17.5         | 0.5         | -0.33                   | +0.00          |        |

**2024/25 adjusted (adj. budget) → 2025/26 original**: service index 81.5 → 85.7 (+4.15 pts).

| Project                                                           | Ward(s)                            | Ward % Black (before → after)   | Band   | R m before   | R m after   | Effect on index (pts)   | …relabelling   | Link   |
|:------------------------------------------------------------------|:-----------------------------------|:--------------------------------|:-------|:-------------|:------------|:------------------------|:---------------|:-------|
| Contributions Roads - Garsfontein Road                            | 45                                 | 10.6 → 10.6                     | 0–20   | 21.4         | 35.0        | -0.79                   | +0.00          |        |
| (710026B) Replacement Of Critical Worn-Out Water Network Pipes (A | 23 wards (region split / township) | 33.6 → 73.4                     | 60–80  | 22.1         | 21.9        | +0.68                   | +0.67          |        |
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)            | 82                                 | 11.3 → 11.3                     | 0–20   | 37.5         | 27.5        | +0.57                   | +0.00          |        |
| Water Conservation and Demand Management (Olievenhoutbosch        | 12 wards (region split / township) | 56.1                            | 40–60  | 0.0          | 18.0        | -0.41                   | +0.00          |        |
| Electricity for All - Region 6                                    | 101                                | 30.4 → 30.4                     | 20–40  | 4.0          | 13.5        | -0.41                   | +0.00          |        |
| Contributions Water - Kameelfontein X1                            | 65                                 | 24.1                            | 20–40  | 8.0          | 0.0         | +0.38                   | +0.00          |        |
| Pretorious Park: sewer provision                                  | 91                                 | 40.0 → 40.0                     | 20–40  | 15.0         | 5.8         | +0.32                   | +0.00          |        |
| Ekangala Block A - F sewer reticulation and toilets               | 104                                | 99.4 → 99.4                     | 80–100 | 32.4         | 3.0         | -0.30                   | +0.00          |        |
| Wildebees 400/132kV, 315MVA Infeed station                        | 26 wards (region split / township) | 77.9 → 77.9                     | 60–80  | 6.2          | 55.0        | -0.30                   | +0.00          |        |
| Denneboom Intermodal facility                                     | 28                                 | 98.9 → 98.9                     | 80–100 | 10.0         | 38.5        | +0.30                   | +0.00          |        |

**2025/26 original → 2025/26 adjusted**: service index 85.7 → 83.8 (-1.86 pts).

| Project                                                           | Ward(s)                            | Ward % Black (before → after)   | Band   | R m before   | R m after   | Effect on index (pts)   | …relabelling   | Link   |
|:------------------------------------------------------------------|:-----------------------------------|:--------------------------------|:-------|:-------------|:------------|:------------------------|:---------------|:-------|
| Mamelodi Ext 11 water (Bulk and reticulation) and sanitation serv | 10                                 | 98.8                            | 80–100 | 0.0          | 45.0        | +0.59                   | +0.00          |        |
| Contributions Roads - Garsfontein Road                            | 45                                 | 10.6 → 10.6                     | 0–20   | 35.0         | 43.2        | -0.51                   | +0.00          |        |
| (710026B) Replacement Of Critical Worn-Out Water Network Pipes (A | 23 wards (region split / township) | 73.4 → 73.4                     | 60–80  | 21.9         | 57.6        | -0.32                   | +0.00          |        |
| Construction of roads & stormwater - Olievenhoutbosch X60         | 77                                 | 93.4 → 93.4                     | 80–100 | 39.5         | 4.0         | -0.28                   | +0.00          |        |
| Wildebees 400/132kV, 315MVA Infeed station                        | 26 wards (region split / township) | 77.9 → 77.9                     | 60–80  | 55.0         | 10.0        | +0.22                   | +0.00          |        |
| Construction of roads & stormwater - Soshanguve South X12         | 37                                 | 99.0 → 99.0                     | 80–100 | 23.2         | 6.2         | -0.21                   | +0.00          |        |
| Townlands Project - Construction of 1,200 social housing units    | 23 wards (region split / township) | 73.4                            | 60–80  | 0.0          | 23.6        | -0.21                   | +0.00          |        |
| Internal Roads Mabopane Block R (Phase 2)                         | 22                                 | 99.3                            | 80–100 | 15.0         | 0.0         | -0.19                   | +0.00          |        |
| and Flooding 5 backlog: Ramotse (Network 1A, 1C & 1F)             | 73                                 | 98.2 → 98.2                     | 80–100 | 22.5         | 7.5         | -0.18                   | +0.00          |        |
| Denneboom Intermodal facility                                     | 28                                 | 98.9 → 98.9                     | 80–100 | 38.5         | 25.5        | -0.16                   | +0.00          |        |

**2025/26 adjusted → 2026/27 original**: service index 83.8 → 87.8 (+3.95 pts).

| Project                                                           | Ward(s)                            | Ward % Black (before → after)   | Band   | R m before   | R m after   | Effect on index (pts)   | …relabelling   | Link   |
|:------------------------------------------------------------------|:-----------------------------------|:--------------------------------|:-------|:-------------|:------------|:------------------------|:---------------|:-------|
| (804000) - 16 Contributions Roads - Garsfontein Road              | 45                                 | 10.6 → 10.6                     | 0–20   | 43.2         | 15.7        | +1.71                   | +0.00          |        |
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)            | 82                                 | 11.3                            | 0–20   | 27.5         | 0.0         | +1.70                   | +0.00          |        |
| Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture         | 5 wards (region split / township)  | 98.7 → 98.7                     | 80–100 | 152.9        | 90.0        | -0.54                   | +0.00          |        |
| Water Conservation and Demand Management (Olievenhoutbosch replac | 12 wards (region split / township) | 56.1                            | 40–60  | 18.0         | 0.0         | +0.47                   | +0.00          |        |
| Water reticulation - Andeon X37                                   | 55                                 | 75.7                            | 60–80  | 0.0          | 36.5        | -0.38                   | +0.00          |        |
| Line 3: CBD to Atteridgeville - Section 1 (Pretoria West - Atteri | 23 wards (region split / township) | 76.9 → 76.9                     | 60–80  | 38.0         | 0.1         | +0.33                   | +0.00          |        |
| Upgrade of Bronkhorstspruit Landfill Site                         | 5 wards (region split / township)  | 94.7                            | 80–100 | 0.0          | 52.4        | +0.32                   | +0.00          |        |
| Temba and Hammanskraal - Upgrading of Existing Gravel Road        | 74                                 | 98.8 → 99.1                     | 80–100 | 20.6         | 49.3        | +0.28                   | +0.01          |        |
| (710026B) Replacement Of Critical Worn-Out Water Network Pipes (A | 23 wards (region split / township) | 73.4 → 73.4                     | 60–80  | 57.6         | 35.3        | +0.26                   | +0.00          |        |
| Wildebees 400/132kV, 315MVA Infeed station                        | 26 wards (region split / township) | 77.9 → 77.9                     | 60–80  | 10.0         | 40.0        | -0.25                   | +0.00          |        |


## 6. Binary ≥80% share vs threshold-free index

**Service area, (b) region money population-split — HEADLINE**

| Column [adopted by]                                         |   Binary ≥80% share % |   Spend-weighted index |   Gap (spend − pop) |   Δ binary |   Δ index | Direction    |
|:------------------------------------------------------------|----------------------:|-----------------------:|--------------------:|-----------:|----------:|:-------------|
| 2022/23 original [pre-Brink]                                |                  84.4 |                   87.3 |                 2.2 |      –   |     –   |              |
| 2022/23 adjusted [pre-Brink]                                |                  84.2 |                   88.6 |                 3.4 |       -0.2 |       1.3 | **DISAGREE** |
| 2023/24 original [Brink]                                    |                  83.0 |                   87.0 |                 4.2 |       -1.2 |      -1.6 | agree        |
| 2023/24 adjusted [Brink]                                    |                  83.6 |                   88.5 |                 5.7 |        0.6 |       1.5 | agree        |
| 2024/25 original [Brink]                                    |                  76.2 |                   84.1 |                 1.3 |       -7.4 |      -4.4 | agree        |
| 2024/25 adjusted (adj. budget) [Moya]                       |                  72.4 |                   81.5 |                -1.2 |       -3.8 |      -2.6 | agree        |
| 2025/26 original [Moya]                                     |                  79.1 |                   85.7 |                 2.9 |        6.7 |       4.2 | agree        |
| 2025/26 adjusted [Moya]                                     |                  75.9 |                   83.8 |                 1.1 |       -3.2 |      -1.9 | agree        |
| 2026/27 original [Moya]                                     |                  79.6 |                   87.8 |                 5.0 |        3.7 |       4.0 | agree        |
| 2024/25 adjusted (App N, final) [Moya]                      |                  75.1 |                   83.4 |                 0.6 |      –   |     –   |              |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |                  74.9 |                   83.4 |                 0.7 |      –   |     –   |              |

**Physical location, (b) population-split**

| Column [adopted by]                                         |   Binary ≥80% share % |   Spend-weighted index |   Gap (spend − pop) |   Δ binary |   Δ index | Direction    |
|:------------------------------------------------------------|----------------------:|-----------------------:|--------------------:|-----------:|----------:|:-------------|
| 2022/23 original [pre-Brink]                                |                  73.1 |                   82.5 |                -2.8 |      –   |     –   |              |
| 2022/23 adjusted [pre-Brink]                                |                  77.4 |                   84.4 |                 2.1 |        4.4 |       1.8 | agree        |
| 2023/24 original [Brink]                                    |                  61.5 |                   75.7 |                -7.0 |      -15.9 |      -8.7 | agree        |
| 2023/24 adjusted [Brink]                                    |                  59.2 |                   76.3 |                -6.4 |       -2.4 |       0.6 | **DISAGREE** |
| 2024/25 original [Brink]                                    |                  57.1 |                   73.1 |                -9.7 |       -2.1 |      -3.2 | agree        |
| 2024/25 adjusted (adj. budget) [Moya]                       |                  53.7 |                   71.4 |               -11.3 |       -3.4 |      -1.7 | agree        |
| 2025/26 original [Moya]                                     |                  69.4 |                   81.1 |                -1.6 |       15.7 |       9.7 | agree        |
| 2025/26 adjusted [Moya]                                     |                  63.5 |                   76.8 |                -5.9 |       -5.9 |      -4.3 | agree        |
| 2026/27 original [Moya]                                     |                  72.1 |                   83.5 |                 0.7 |        8.7 |       6.7 | agree        |
| 2024/25 adjusted (App N, final) [Moya]                      |                  60.3 |                   75.4 |                -7.3 |      –   |     –   |              |
| 2024/25 actual [Brink Jul–Sep 2024, Moya Oct 2024–Jun 2025] |                  60.0 |                   75.4 |                -7.3 |      –   |     –   |              |


Disagreements in direction (one per basis):
- **Service area, 2022/23 original → adjusted.** The binary share barely moves (84.4 → 84.2) while the index rises by 1.3. Attributed capex moved out of the 0–20 band (4.2% → 1.4% of attributed capex) into the 60–80 band (4.1% → 6.4%). Both bands are below the 80% cut, so the binary measure can't see the shift; the index can.
- **Physical location, 2023/24 original → adjusted.** The binary share falls (61.5 → 59.2) while the index rises by 0.6. The 0–20 band fell (8.3% → 6.0%) and the 60–80 band rose (7.0% → 10.7%), while the ≥80% bands fell slightly (61.6% → 59.2%).

Every other step agrees in direction. On the location basis the binary measure moves further than the index in 6 of 7 agreeing steps (by 1.3–2.4×); the exception is 2023/24 adjusted → 2024/25 original (binary −2.1, index −3.2). On the service basis the sizes are similar (the index moves further in 3 of 7 agreeing steps). The difference arises because the binary measure counts a ward at 81% the same as one at 99%, and ignores shifts between bands below 80%.

## 7. Data, sources and limitations

- **Sources, unchanged from binary_v1:** extraction, reconciliation (100% coverage except the 2025/26 adjustment budget at 99.5%), matching decisions, name overrides, ward→region table, beneficiary statements, Moya-era carry-forward and its checks. See Appendix A §2, §6, §8, §9. Every rand figure traces to a page through `projects.csv` and `projects_moya.csv`.
- **Coverage of the index:** it covers only ward-attributed capex — 38–53% of each budget on the service-area basis (b), and 54–72% on the location basis (b).
- **Labelled assumptions:**
  1. Ward %Black is from 2022 estimates, applied to all years.
  2. Region-only money under (b) benefits every resident of the region equally.
  3. Wards are carried forward from 2025/26 (inferred, not stated).
  4. Bulk infrastructure counts only where a document names its beneficiary.
  5. Multi-ward projects are left out of the index and bands.
- **Not in the folder:** no ward-level actual spend after 2024/25, and no region-level in-year actuals.

## 8. What changed versus binary_v1

1. **Headline measure:** from the binary ≥80% share to the spend- vs population-weighted mean % Black African, plus five bands. The binary results are unchanged and in Appendix A.
2. **Basis order:** the service-area basis is now the headline; physical location is secondary. In binary_v1 location was the primary basis.
3. **Columns:** the series now includes the final 2024/25 adjusted budget (App N) as a labelled column, and keeps the 2024/25 actual separate. Every column is labelled with the adopting administration and document date.
4. **Drivers:** the driver analysis now covers every step from 2022/23 to 2026/27, in index terms, with each mover's ward % Black and band. binary_v1 covered 2023/24 → 2024/25 and the Moya steps, with Black/other labels. The 2022/23 → 2023/24 step needed a new name crosswalk because the WBS coding scheme changed.
5. **New sensitivities:** 80–100 split into 80–90 and 90–100; 40–80 merged; single-project dominance flags.
6. **New outputs:** `v2_index.csv`, `v2_bands.csv`, `v2_drivers.csv`, and band columns added to `ward_classification.csv` (binary columns kept). `projects.csv` and `projects_moya.csv` are unchanged.
7. **New scripts:** `bands_engine.py`, `bands_metrics.py`, `bands_report.py`. All binary_v1 scripts are unchanged; binary_v1 is preserved read-only in `output/binary_v1/` and `scripts/binary_v1/`.

## Appendix A — binary (≥80% Black African) analysis, carried over unchanged from binary_v1

The text below is `output/binary_v1/summary.md` reproduced verbatim; only heading levels are shifted down one level to nest it under this appendix. Section references inside it (§1–§9) refer to its own numbering. The original file, `projects.csv`, `projects_moya.csv` and `ward_classification.csv` are preserved read-only in `output/binary_v1/`; the scripts that produced them are in `scripts/binary_v1/`.

## Tshwane capital spending by ward, 2022/23 – 2024/25

**Question tested:** did the share of capital budget and actual capital spend going to predominantly Black wards fall, hold or rise from 2022/23 to 2023/24 to 2024/25, i.e. is there evidence that the DA-led administration under Mayor Cilliers Brink (Mar 2023 – Sep 2024, dates as given in the brief) neglected predominantly Black areas?

### Plain-language finding

On the primary measure, the predominantly Black wards' share of ward-attributable capital budget **fell** between the last pre-Brink budget (2022/23: 72.7% of original, 77.5% of adjusted) and the first Brink budget (2023/24: 61.7% / 60.9%), and fell again in the 2024/25 original budget (55.9%), before partly recovering in the 2024/25 adjusted budget and actual spend (61.5% / 61.2%), which were mostly executed after the end of the tenure dates given. In rand terms, single-ward budget in predominantly Black wards fell from R1,209m to R728m (original), while other wards held at about R452m; per resident, Black wards went from 0.9× to 0.5× what other wards received. The direction of that fall survives every threshold (50/80/90%), the Census 2011 classification and the named-township definition. **But the numbers cannot resolve the "neglect" claim**, for three reasons: (1) only about half of each year's capital budget can be tied to a single ward (well under the 80% you asked me to flag); (2) the 2022/23 → 2023/24 fall disappears when bulk infrastructure is excluded (Black-ward share of original budget 82.9% → 84.6%). That step is driven by where large plants sit, chiefly the Rooiwal wastewater works in ward 96 (47.5% Black African), whose upgrade the City's own 2024/25 annual report (p94) describes as addressing Hammanskraal's water crisis. A fall does survive the bulk exclusion one year later, in the Brink-era 2024/25 original budget (68.2%; 69.9% of actual spend), so that budget is the strongest evidence for the claim; and (3) there is no ward-level actual spend for 2022/23 or 2023/24, so the only spend-rate test is 2024/25, which shows no meaningful gap (Black wards 96.4% vs other 97.7%). The in-year reprioritisation data for 2023/24 points the way ActionSA claims but is small (Black-ward projects cut R43.2m or 5.9%, other wards R12.6m or 2.8%). Net: the data are *consistent with* a reduced allocation to Black wards in Brink-era budgets on location-of-project measures, but not robust evidence of neglect.

**Update after the two follow-ups (§7–§8).**
- **The 2024/25 drop** in the Black-ward share excluding bulk infrastructure (84.6% → 68.2%, corrected) is moderately concentrated: the top 5 projects account for about half of the adverse movement. About 11 of the 16 points come from real budget changes, mainly Thorntree View roads cut from R90.2m to R1.0m, Electricity Distribution Loss from R68m to R20m, and the Zithobeni X8 sewer and Timberlands housing dropped. The remaining 5 points come from Appendix O moving the water-pipe programmes from a Black ward to other wards.
- **Bulk infrastructure by documented service area:** where the City's reports name a beneficiary, Rooiwal goes to Temba and Hammanskraal, and Klipgat, Bronkhorstbaai, Parkmore and Wildebees go to their stated regions. On that basis the 2022/23 → 2023/24 fall disappears (84.4% → 83.0% of original budget, region-only money population-split). The 2024/25 fall remains (76.2% original, 74.9% actual), and Black wards still receive about as much per resident as other wards in 2024/25 (ratio ≈1.0, against 1.6–1.8 in the earlier years). The caveat is that this basis attributes less than half of the budget.

**Moya administration (§9).** On the same methods, the Black-ward share (location basis, region money population-split) runs:
- 53.7% in Moya's first adjustment budget (2024/25);
- 69.4% in the 2025/26 original and 63.5% in the 2025/26 adjusted;
- 72.1% in the 2026/27 original.

The 2025/26 and 2026/27 originals are above every Brink-era budget but not above 2022/23. Rand per resident in Black wards is still below other wards (ratio 0.4–0.8). Both Moya adjustment budgets cut the Black-ward share within the year. There is no ward-level actual spend after 2024/25, and from 2025/26 wards are carried forward from earlier years. The region-level robustness series (Option B) is nearly flat (73–78%). None of the four 2024/25 cuts was restored in full: Electricity Distribution Loss got R47m in the 2025/26 adjusted budget, partly restored against R68m in 2023/24. No document says Thorntree View was completed; a 2025/26 procurement plan schedules "completion and remedial works" of 2.2km of its stormwater channel.

### 1. Sources, and what each year can support

| Year | Original budget (project level) | Adjusted budget (project level) | Actual spend (project level) | Ward link |
|---|---|---|---|---|
| 2022/23 | 2022/23 Adjustment Budget, Annexure B pp141–148 ("Current Budget") | same, "Adjusted Budget" | **not available** (AR 2022/23 App N pp379–384 is asset-class only) | AR 2022/23 App O pp385–393 (ward lists, no rands) — joined by project name/code |
| 2023/24 | 2023/24 Adjustments Budget, Annexure B pp132–138 | same | **not available** (AR 2023/24 App N pp401–404 is asset-class only, and its "actual" column mostly repeats the adjusted budget) | AR 2023/24 App O pp405–411 — joined by name |
| 2024/25 | 2024/25 MTREF, Annexure A pp58–65 | AR 2024/25 App N pp503–515 | AR 2024/25 App N pp503–515 | AR 2024/25 App O pp516–525 — joined by name; App N's own "dominant ward" used as a check |

Region tags (Census-free cross-check) come from MBRR SA36/SB19 tables: 2022/23 MTREF pp199–234, 2022/23 adjustments budget pp100–104, 2023/24 MTREF pp181–188, 2023/24 adjustments budget pp90–93, 2024/25 MTREF pp205–216. Despite the column name "Ward Location", these only carry regions.

Budget timing, from the documents: 2022/23 MTREF approved 26 May 2022 (2022/23 adj. budget p51); 2022/23 adjustments budget prepared before the 2–3 March 2023 Treasury engagement it refers to (p52); 2023/24 MTREF approved 31 May 2023 (2023/24 adj. budget p48); 2024/25 MTREF "will be tabled for approval by Council in May 2024" (2024/25 MTREF p76). The date of the 2024/25 adjustments budget is not in these documents. On the tenure dates in the brief, 2022/23 is the pre-Brink baseline, 2023/24 and the 2024/25 original budget are Brink-era, and roughly 3 of the 12 months of 2024/25 spending fall within the tenure.

### 2. Reconciliation and coverage

**Extraction is complete** — every project table reconciles to the rand with the stated total in the same document:

| Measure | Extracted total | Stated total | Where stated | Coverage |
|---|---|---|---|---|
| 2022/23 original | R2,793,105,151 | R2,793,105,151 | 2022/23 adj. budget Annexure B p148; AR 2022/23 App N p384 | 100% |
| 2022/23 adjusted | R2,816,190,045 | R2,816,190,047 | same | 100% (R2 rounding) |
| 2023/24 original | R2,347,686,908 | R2,347,686,908 | 2023/24 adj. budget Annexure B p138; AR 2023/24 App N p404 | 100% |
| 2023/24 adjusted | R2,112,614,368 | R2,112,614,368 | same | 100% |
| 2024/25 original | R2,347,552,577 | R2,347,552,576 | 2024/25 MTREF Annexure A p65 | 100% |
| 2024/25 adjusted | R2,340,123,792 | R2,340,123,791 | AR 2024/25 App N p515 | 100% |
| 2024/25 actual | R2,300,073,485 | R2,300,073,481 | AR 2024/25 App N p515 | 100% |

Not extractable at ward level (asset-class totals only): 2022/23 actual R2,227,704,869 (AR 2022/23 p384); 2023/24 actual R2,127,678,733.67 (AR 2023/24 p404).

**⚠️ WARD-ATTRIBUTABLE COVERAGE IS LOW: ONLY 49–60% OF EACH YEAR'S CAPITAL BUDGET CAN BE TIED TO A SINGLE WARD.** The rest is multi-ward, city-wide, administrative HQ, "No Intersect" in the source, or could not be matched to Appendix O. Every share below is a share of that single-ward slice.

Rand value and share of total by ward category (R m, % of measure total):

| measure                 |   Total (R m) |   Single ward |    % |   Multi-ward |   %  |   City-wide |   %   |   Admin HQ |   %    |   'No Intersect' |   %     |   Unmatched |   %      |
|:------------------------|--------------:|--------------:|-----:|-------------:|-----:|------------:|------:|-----------:|-------:|-----------------:|--------:|------------:|---------:|
| 2022/23 original budget |       2,793.1 |       1,664.0 | 59.6 |        256.2 |  9.2 |       473.8 |  17.0 |      159.5 |    5.7 |              0.0 |     0.0 |       239.7 |      8.6 |
| 2022/23 adjusted budget |       2,816.2 |       1,654.5 | 58.7 |        226.5 |  8.0 |       586.7 |  20.8 |      165.8 |    5.9 |              0.0 |     0.0 |       182.7 |      6.5 |
| 2023/24 original budget |       2,347.7 |       1,180.5 | 50.3 |        220.2 |  9.4 |       451.8 |  19.2 |      134.7 |    5.7 |             90.5 |     3.9 |       270.1 |     11.5 |
| 2023/24 adjusted budget |       2,112.6 |       1,124.6 | 53.2 |        202.7 |  9.6 |       453.3 |  21.5 |      125.8 |    6.0 |             87.5 |     4.1 |       118.7 |      5.6 |
| 2024/25 original budget |       2,347.6 |       1,175.3 | 50.1 |        208.5 |  8.9 |       461.5 |  19.7 |      137.1 |    5.8 |             54.8 |     2.3 |       310.4 |     13.2 |
| 2024/25 adjusted budget |       2,340.1 |       1,271.8 | 54.3 |        276.9 | 11.8 |       568.1 |  24.3 |      117.5 |    5.0 |             59.8 |     2.6 |        46.1 |      2.0 |
| 2024/25 actual spend    |       2,300.1 |       1,232.9 | 53.6 |        281.3 | 12.2 |       560.1 |  24.4 |      119.4 |    5.2 |             58.7 |     2.6 |        47.7 |      2.1 |

Multi-ward, city-wide and Administrative HQ projects are kept as their own categories and not split across wards.

### 3. Year-by-year shares — primary definition (Black African ≥ 80% of ward population)

Ward populations: Stats SA Ward-level Small Area Population Estimates 2022 (Nov 2025), on MDB 2020 wards. 69 of 107 wards are ≥ 80% Black African and hold 75.4% of residents (3.05m of 4.04m).

| measure                 |   Total capex (R m) |   Single-ward attributable (R m) |   …as % of total |   Predominantly Black wards (R m) |   Other wards (R m) |   Black-ward share of attributable (%) |   R per resident – Black wards |   R per resident – other wards |   Per-capita ratio Black:other |
|:------------------------|--------------------:|---------------------------------:|-----------------:|----------------------------------:|--------------------:|---------------------------------------:|-------------------------------:|-------------------------------:|-------------------------------:|
| 2022/23 original budget |             2,793.1 |                          1,664.0 |             59.6 |                           1,209.4 |               454.6 |                                   72.7 |                          397.0 |                          457.5 |                            0.9 |
| 2022/23 adjusted budget |             2,816.2 |                          1,654.5 |             58.7 |                           1,282.1 |               372.3 |                                   77.5 |                          420.8 |                          374.7 |                            1.1 |
| 2023/24 original budget |             2,347.7 |                          1,180.5 |             50.3 |                             728.1 |               452.4 |                                   61.7 |                          239.0 |                          455.2 |                            0.5 |
| 2023/24 adjusted budget |             2,112.6 |                          1,124.6 |             53.2 |                             684.9 |               439.8 |                                   60.9 |                          224.8 |                          442.5 |                            0.5 |
| 2024/25 original budget |             2,347.6 |                          1,175.3 |             50.1 |                             656.5 |               518.7 |                                   55.9 |                          215.5 |                          522.0 |                            0.4 |
| 2024/25 adjusted budget |             2,340.1 |                          1,271.8 |             54.3 |                             782.2 |               489.5 |                                   61.5 |                          256.8 |                          492.6 |                            0.5 |
| 2024/25 actual spend    |             2,300.1 |                          1,232.9 |             53.6 |                             754.4 |               478.4 |                                   61.2 |                          247.6 |                          481.5 |                            0.5 |

#### Sensitivity — Black-ward share of single-ward-attributable capex (%)

|                                                                   |   2022/23 original budget |   2022/23 adjusted budget |   2023/24 original budget |   2023/24 adjusted budget |   2024/25 original budget |   2024/25 adjusted budget |   2024/25 actual spend |
|:------------------------------------------------------------------|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|-----------------------:|
| ≥50%                                                              |                      83.2 |                      86.7 |                      73.8 |                      75.5 |                      66.3 |                      70.4 |                   70.3 |
| ≥80% (primary)                                                    |                      72.7 |                      77.5 |                      61.7 |                      60.9 |                      55.9 |                      61.5 |                   61.2 |
| ≥90%                                                              |                      57.8 |                      61.0 |                      48.5 |                      48.7 |                      47.3 |                      54.1 |                   53.5 |
| ≥80%, Census 2011 shares                                          |                      61.8 |                      65.7 |                      48.5 |                      48.7 |                      47.3 |                      54.1 |                   53.5 |
| ≥80%, excl. single-ward rows whose name states multi-region scope |                      72.7 |                      77.5 |                      60.0 |                      59.2 |                      57.2 |                      62.0 |                   61.6 |
| ≥80%, excl. Rooiwal WWTW                                          |                      74.5 |                      78.2 |                      70.7 |                      70.2 |                      64.0 |                      69.7 |                   69.7 |
| ≥80%, excl. all bulk-infrastructure-named rows                    |                      82.9 |                      82.8 |                      84.6 |                      85.3 |                      68.2 |                      70.6 |                   69.9 |
| ≥80%, 'No Intersect' rows given ward from another year's App O    |                      72.7 |                      77.5 |                      60.6 |                      59.6 |                      56.1 |                      62.8 |                   62.5 |

Per-capita ratio (R per resident in Black wards ÷ R per resident in other wards):

|                                                                   |   2022/23 original budget |   2022/23 adjusted budget |   2023/24 original budget |   2023/24 adjusted budget |   2024/25 original budget |   2024/25 adjusted budget |   2024/25 actual spend |
|:------------------------------------------------------------------|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|-----------------------:|
| ≥50%                                                              |                       1.2 |                       1.5 |                       0.7 |                       0.7 |                       0.5 |                       0.6 |                    0.6 |
| ≥80% (primary)                                                    |                       0.9 |                       1.1 |                       0.5 |                       0.5 |                       0.4 |                       0.5 |                    0.5 |
| ≥90%                                                              |                       0.6 |                       0.6 |                       0.4 |                       0.4 |                       0.4 |                       0.5 |                    0.5 |
| ≥80%, Census 2011 shares                                          |                       0.6 |                       0.7 |                       0.4 |                       0.4 |                       0.3 |                       0.5 |                    0.4 |
| ≥80%, excl. single-ward rows whose name states multi-region scope |                       0.9 |                       1.1 |                       0.5 |                       0.5 |                       0.4 |                       0.5 |                    0.5 |
| ≥80%, excl. Rooiwal WWTW                                          |                       1.0 |                       1.2 |                       0.8 |                       0.8 |                       0.6 |                       0.8 |                    0.7 |
| ≥80%, excl. all bulk-infrastructure-named rows                    |                       1.6 |                       1.6 |                       1.8 |                       1.9 |                       0.7 |                       0.8 |                    0.8 |
| ≥80%, 'No Intersect' rows given ward from another year's App O    |                       0.9 |                       1.1 |                       0.5 |                       0.5 |                       0.4 |                       0.6 |                    0.5 |

2024/25 using Appendix N's own "dominant ward" instead of Appendix O: Black-ward share 59.9% of adjusted and 60.0% of actual; per-capita ratio 0.5 / 0.5. This method attributes 69.7% of the budget to single wards, because it assigns every project one ward.

#### Secondary definition — wards covering named townships

A ward counts as a township ward if at least 50% of its 2011 population lived in one of the named townships' official Stats SA Census 2011 Main Places. Eersterust is reported separately. Boundaries come from Census 2011 Sub Places (UCT_Geodata mirror of the Stats SA layer), intersected with MDB 2020 wards; populations are Census 2011 sub-place counts split by area. This gives 52 township wards with 2.29m residents (2022 estimates), and Eersterust is ward 43.

| measure                 |   Named-township wards (R m) |   Other wards (R m) |   Eersterust ward 43 (R m) |   Township share of attributable (%) |   R/resident township wards |   R/resident other wards |   Ratio |
|:------------------------|-----------------------------:|--------------------:|---------------------------:|-------------------------------------:|----------------------------:|-------------------------:|--------:|
| 2022/23 original budget |                        658.7 |             1,005.4 |                        0.0 |                                 39.6 |                       287.2 |                    588.2 |     0.5 |
| 2022/23 adjusted budget |                        696.2 |               958.3 |                        0.0 |                                 42.1 |                       303.6 |                    560.7 |     0.5 |
| 2023/24 original budget |                        413.3 |               767.2 |                        0.0 |                                 35.0 |                       180.2 |                    448.9 |     0.4 |
| 2023/24 adjusted budget |                        400.9 |               723.8 |                        0.0 |                                 35.6 |                       174.8 |                    423.5 |     0.4 |
| 2024/25 original budget |                        437.3 |               738.0 |                        0.0 |                                 37.2 |                       190.7 |                    431.8 |     0.4 |
| 2024/25 adjusted budget |                        528.0 |               743.8 |                        0.0 |                                 41.5 |                       230.2 |                    435.2 |     0.5 |
| 2024/25 actual spend    |                        515.7 |               717.1 |                        0.0 |                                 41.8 |                       224.9 |                    419.6 |     0.5 |

Caveats on this mapping. "Hammanskraal" is the narrow official Main Place (Rens Town and Kanana); Majaneng, Suurman, Stinkwater and New Eersterus are separate Main Places and are not grouped in. Main Places include some non-residential sub-places (Medunsa, Ekandustria, Tswaing). Boundaries are from 2011. On this definition the township share falls from 2022/23 to 2023/24 by less than on the primary definition, and recovers in 2024/25.

### 4. Spend rate and in-year reprioritisation (ActionSA's claim)

**Spend rate (actual ÷ adjusted budget) is available for 2024/25 only.**

Ward from Appendix O:

| g                |   Adjusted budget (R m) |   Actual (R m) |   Spend rate % |
|:-----------------|------------------------:|---------------:|---------------:|
| Black            |                   782.2 |          754.4 |           96.4 |
| Other            |                   489.5 |          478.4 |           97.7 |
| multi-ward       |                   276.9 |          281.3 |          101.6 |
| non-attributable |                   791.5 |          785.9 |           99.3 |
| TOTAL            |                 2,340.1 |        2,300.1 |           98.3 |

Ward from Appendix N's "dominant ward":

| g                |   Adjusted budget (R m) |   Actual (R m) |   Spend rate % |
|:-----------------|------------------------:|---------------:|---------------:|
| Black            |                   977.7 |          958.9 |           98.1 |
| Other            |                   653.4 |          638.4 |           97.7 |
| non-attributable |                   709.0 |          702.7 |           99.1 |
| TOTAL            |                 2,340.1 |        2,300.1 |           98.3 |

At ≥50% the rates are Black 96.8% vs other 97.4%; at ≥90% they are 95.8% vs 98.2%. There is no meaningful under-spend in Black wards relative to other wards in 2024/25.

**Original → adjusted budget, by ward group (≥80%)** — tests whether money was moved away during the year.

| year    | group            |   Original (R m) |   Adjusted (R m) |   Change (R m) |   Adjusted as % of original |
|:--------|:-----------------|-----------------:|-----------------:|---------------:|----------------------------:|
| 2022/23 | Black            |          1,209.4 |          1,282.1 |           72.7 |                       106.0 |
| 2022/23 | Other            |            454.6 |            372.3 |          -82.2 |                        81.9 |
| 2022/23 | multi-ward       |            256.2 |            226.5 |          -29.7 |                        88.4 |
| 2022/23 | non-attributable |            872.9 |            935.2 |           62.3 |                       107.1 |
| 2023/24 | Black            |            728.1 |            684.9 |          -43.2 |                        94.1 |
| 2023/24 | Other            |            452.4 |            439.8 |          -12.6 |                        97.2 |
| 2023/24 | multi-ward       |            220.2 |            202.7 |          -17.5 |                        92.1 |
| 2023/24 | non-attributable |            947.1 |            785.3 |         -161.8 |                        82.9 |
| 2024/25 | Black            |            656.5 |            782.2 |          125.7 |                       119.1 |
| 2024/25 | Other            |            518.7 |            489.5 |          -29.2 |                        94.4 |
| 2024/25 | multi-ward       |            208.5 |            276.9 |           68.4 |                       132.8 |
| 2024/25 | non-attributable |            963.8 |            791.5 |         -172.4 |                        82.1 |

The 2022/23 and 2023/24 rows compare the same project rows (Annexure B). The 2024/25 row compares two different sources: the MTREF Annexure A original budget against Appendix N's adjusted budget, each matched to wards separately. The unmatched share also differs (14.1% vs 2.0%), so treat the 2024/25 shift as indicative only.

### 5. Top 10 projects by value, by group (≥80% definition, ward from Appendix O)

The Rooiwal rows show the location issue: the plant is in ward 96 ("other"), but AR 2024/25 p94 says its refurbishment addresses Hammanskraal's water problems.

**2022/23 (adjusted budget) — predominantly Black wards**

| Project                                                               |   Ward(s) (App O) |   Original R m |   Adjusted R m |   Source page |
|:----------------------------------------------------------------------|------------------:|---------------:|---------------:|--------------:|
| Townlands Project - Construction of 1,200 social housing units        |                58 |           85.2 |          148.8 |           144 |
| Construction of roads & stormwater - Thorntree View                   |                90 |           31.5 |          126.8 |           143 |
| Tshwane Automotive SEZ Phase 1 Bulk Infrastructure Roll out           |                86 |            0.0 |          113.5 |           141 |
| Replacement Of Worn-Out Water Network Pipes                           |               100 |           75.0 |           75.0 |           147 |
| Klipgat WWTW: Upgrading of existing infrastructure to 40Ml/d          |                22 |           74.8 |           70.0 |           147 |
| Ekangala Block A - F sewer reticulation and toilets                   |               104 |           59.0 |           65.0 |           147 |
| Bronkhorstbaai: Refurbishment and upgrade of Water Purification Plant |               102 |           35.0 |           65.0 |           147 |
| Wonderboom Intermodal Facility (Building Works)                       |                58 |           52.5 |           47.2 |           144 |
| Electricity Distribution Loss                                         |                34 |           42.8 |           42.8 |           147 |
| Upgrade Refilwe Stadium                                               |               100 |           32.0 |           32.0 |           141 |

**2022/23 (adjusted budget) — other wards**

| Project                                                          |   Ward(s) (App O) |   Original R m |   Adjusted R m |   Source page |
|:-----------------------------------------------------------------|------------------:|---------------:|---------------:|--------------:|
| Electricity for All - Region 6                                   |               101 |           35.8 |           51.3 |           146 |
| Electricity for All - Region 3                                   |                55 |           23.2 |           42.2 |           145 |
| Kentron 132/11kV Substation                                      |                78 |           30.0 |           40.0 |           146 |
| Refurbishment of Mooikloof Substation                            |                91 |           30.0 |           30.0 |           145 |
| Refurbishment of Pyramid Sub Station                             |                96 |           25.0 |           25.0 |           145 |
| Acquisition of Land                                              |                55 |            5.0 |           20.1 |           143 |
| Sunderland Ridge WWTW Phase1: Upgrade of existing infrastructure |                70 |           19.0 |           19.0 |           147 |
| Electricity for All - Region 4                                   |                70 |            0.0 |           16.9 |           146 |
| Refurbishment Of Laudium Bulk Pipeline                           |                61 |            9.0 |           15.7 |           147 |
| Electricity for All - Region 4                                   |                70 |           14.0 |           14.0 |           145 |

**2023/24 (adjusted budget) — predominantly Black wards**

| Project                                                                                  |   Ward(s) (App O) |   Original R m |   Adjusted R m |   Source page |
|:-----------------------------------------------------------------------------------------|------------------:|---------------:|---------------:|--------------:|
| Construction of roads & stormwater - Thorntree View                                      |                36 |           48.3 |           52.3 |           133 |
| Townlands Project - Construction of 1,200 social housing units                           |                58 |            0.0 |           48.8 |           134 |
| Klipgat WWTW: Upgrading of existing infrastructure to 40Ml/d                             |                22 |           35.0 |           40.6 |           137 |
| Electricity for All - Region 1                                                           |                32 |           24.0 |           39.0 |           135 |
| Construction of roads & stormwater - Thorntree View                                      |                36 |           41.9 |           31.9 |           133 |
| (710864) Sewer provision - Zithobeni X8                                                  |               105 |           30.6 |           30.6 |           133 |
| Electricity Distribution Loss                                                            |                29 |           68.0 |           30.0 |           137 |
| Electricity for All - Region 7                                                           |               105 |           26.4 |           29.4 |           136 |
| Electricity for All - Region 5                                                           |                99 |           26.0 |           26.0 |           136 |
| Acquisition and Refurbishment of Midtown Building Acquisition Old-Mercedes Benz Building |                81 |           25.1 |           25.1 |           132 |

**2023/24 (adjusted budget) — other wards**

| Project                                                          |   Ward(s) (App O) |   Original R m |   Adjusted R m |   Source page |
|:-----------------------------------------------------------------|------------------:|---------------:|---------------:|--------------:|
| Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture        |                96 |           46.7 |           84.7 |           137 |
| Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure       |                96 |          103.3 |           65.0 |           137 |
| Booysens X4 (30ML Reservoir)                                     |                55 |           14.6 |           41.5 |           132 |
| Sunderland Ridge WWTW Phase1: Upgrade of existing infrastructure |                70 |           36.1 |           36.1 |           137 |
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)           |                82 |           46.0 |           29.0 |           135 |
| Kentron 132/11kV Substation                                      |                65 |           28.0 |           28.0 |           136 |
| New Parkmore LL Reservoir and HL Reservoir                       |                45 |           40.0 |           28.0 |           137 |
| Acquisition of Land                                              |                55 |           26.2 |           24.2 |           134 |
| Refurbishment of Mooikloof Substation                            |                91 |           20.0 |           20.0 |           135 |
| Refurbishment of Pyramid Sub Station                             |                96 |           20.0 |           20.0 |           135 |

**2024/25 (actual spend, Appendix N) — predominantly Black wards**

| Project                                                                                     |   Ward(s) (App O) |   Adjusted R m |   Actual R m |   Source page |
|:--------------------------------------------------------------------------------------------|------------------:|---------------:|-------------:|--------------:|
| Water provision – Winterveldt 20ML Reservoir                                                |                19 |           62.7 |         69.1 |           508 |
| Soshanguve - JJ 132KV Power Line                                                            |                26 |           60.0 |         59.9 |           509 |
| Water Provision - Winterveldt Bulk water line                                               |                19 |           53.2 |         53.2 |           508 |
| Turnaround of Municipal Water Services - Reduction of Water Losses and Revenue Enhancement. |                58 |           50.0 |         49.4 |           512 |
| Tshwane SEZ                                                                                 |                28 |           56.0 |         48.7 |           509 |
| Bulk Sewer Line - Winterveldt                                                               |                25 |           46.4 |         45.4 |           509 |
| Electricity for All - Region 1                                                              |                32 |           36.0 |         38.3 |           510 |
| Replacement Of Critical Worn-Out Water Network Pipes (Area C)                               |               100 |           38.0 |         37.8 |           507 |
| Electricity for All - Region 5                                                              |                99 |           36.0 |         36.0 |           514 |
| Ekangala Block A - F sewer reticulation and toilets                                         |               104 |           32.4 |         29.1 |           507 |

**2024/25 (actual spend, Appendix N) — other wards**

| Project                                                          |   Ward(s) (App O) |   Adjusted R m |   Actual R m |   Source page |
|:-----------------------------------------------------------------|------------------:|---------------:|-------------:|--------------:|
| Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure       |                96 |          150.0 |        150.0 |           514 |
| Kentron 132/11kV Substation                                      |                65 |           38.0 |         38.0 |           513 |
| Replacement Of Critical Worn-Out Water Network Pipes (Area B)    |                53 |           32.1 |         32.0 |           507 |
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)           |                82 |           37.5 |         31.7 |           514 |
| Refurbishment of Pyramid Sub Station                             |                96 |           27.0 |         27.0 |           514 |
| Sunderland Ridge WWTW Phase1: Upgrade of existing infrastructure |                70 |           25.9 |         25.2 |           513 |
| Sewer reticulation - Andeon X37                                  |                55 |           23.6 |         23.4 |           512 |
| Electricity for All - Region 3                                   |                55 |           20.0 |         20.0 |           511 |
| Water reticulation - Andeon X37                                  |                55 |           18.4 |         18.4 |           512 |
| New Parkmore LL Reservoir and HL Reservoir                       |                45 |           16.9 |         16.6 |           511 |

### 6. Data gaps, assumptions and judgement calls

1. **No ward-level actual spend before 2024/25.** The 2022/23 and 2023/24 annual reports give actuals by asset class only. The 2023/24 "actual" column repeats the adjusted budget in most rows (AR 2023/24 pp401–404), so it looks copied rather than measured.
2. **Ward attribution comes from Appendix O, which has no rand values.** Budget rows were joined to Appendix O by fuzzy project-name matching, plus project-code agreement where both sides carry codes (2022/23 and 2024/25). Rules:
   - Auto-accept at a score of 95 or more.
   - Auto-reject where service, place, extension, area or section conflict, or the score is below 65.
   - Hand-review everything else. Every decision and its reason is recorded (`match_status`, `match_reason` in projects.csv).
   - Unmatched rows are reported, not guessed. They are 8.6%, 11.5% and 14.1% of the original budget in the three years. The largest each year is Housing Company Tshwane's "Chantelle detail design and bulk infrastructure upgrade", which has no Appendix O row.
3. **Appendix O ward assignments are the City's, taken as published.** They are sometimes inconsistent across years:
   - Thorntree View roads are in ward 90 in 2022/23 and ward 36 in 2023/24.
   - The "Critical Worn-Out Water Pipes" areas, which by name span several regions, are all put in ward 100 in 2023/24, and in wards 96, 53 and 100 in 2024/25.
   - From 2023/24 some projects are labelled "No Intersect" that had a ward in 2022/23. Sensitivity rows test both issues.
4. **Overprinted text in the PDFs.** 18 project names were printed on top of each other in the source. They were decoded from WBS codes and recorded in `name_note`. One (Sunnyside/Townlands, 2023/24, R20m adjusted) is genuinely ambiguous and left unmatched.
5. **Rows used.** Where a programme row has sub-project rows, the sub-projects are used when they sum exactly to the parent. In one case (SAP4 Hana, 2023/24) the source leaves the sub-project's adjusted figure blank, so the parent row is used.
6. **Population data.**
   - The 2022 ward populations are Stats SA small-area estimates (Census 2011 ward structure benchmarked to Census 2022 municipal totals), not raw counts; for about 3% of wards nationally they are modelled values.
   - Values are fractional as published, and "Other" includes "Unspecified".
   - Census 2011 shares on the same 2020 wards (MDB WardProfile2021 layer) are used as a sensitivity check. That layer has no metadata; its total matches Census 2011.
   - Both use the 2020/2021 ward boundaries the reports use, so no boundary crosswalk was needed.
7. **"Bulk infrastructure" flag.** This is a name-based sensitivity flag (substation, infeed, WWTW, power line, reservoir, bulk, canal, feeder, outfall, purification), not an official classification.
8. **Per-capita figures** divide a group's single-ward rands by that group's total 2022 population. Multi-ward, city-wide and HQ spending is excluded from both groups.
9. **Region tags** come from SA36/SB19 by exact WBS code. They cover about 78–90% of rands and are descriptive only; regions were not classified by population group.
10. **Draft 2024/25 MTREF** (12.1 Item 12 annexures) was not used; the final 2024/25 MTREF supersedes it.
11. **Revision after follow-up review.** The 2024/25 MTREF row "Replacement of obsolete of meter test bench ( Electricity Distribution Loss)" (IDP 714008, R20.0m) was originally rejected as a ward match. It is now matched to Appendix O "Electricity Distribution Loss" (ward 29): the name is in brackets and the project code agrees. This raises the 2024/25 original-budget Black-ward share from 55.1% to 55.9%. All tables above use the corrected figure.

### Files

- `projects.csv`: one row per project per source table. Columns: year, source file and page, names, department, WBS code, wards (as published and parsed), ward category, ward source and page, region and its source, original, adjusted and actual amounts, match status, score and reason, name notes, and the scope and bulk flags.
- `ward_classification.csv`: all 107 wards. Population and Black African share (2022), classification at 50, 80 and 90%, the 2011 share and class, township flags (population-based) and data sources.

### 7. Follow-up 1 — what drove the 2024/25 original-budget drop (excluding bulk infrastructure)

Comparison: 2023/24 original budget (2023/24 adjustments budget, Annexure B) vs 2024/25 original budget (2024/25 MTREF, Annexure A). Bulk-infrastructure-named rows are excluded; each year's ward comes from that year's Appendix O (≥80% definition). Projects are linked by WBS code without the funding-source segment, so funding switches don't break the link. A shared code counts as a link only if the names also agree; one code was reused for a different project (Ekangala). Four re-coded projects were linked by hand:

- `9.801645.1.S.DL.05.W` → `9.801638.1.E.LO.1`: 2024/25 MTREF Annexure A line 'Replacement of obsolete of meter test bench ( Electricity Distribution Loss)', IDP 714008 = 2023/24 Electricity Distribution Loss
- `9.804713.1.W.EK.05.7` → `9.804721.1.S.SE.7`: identical name 'Ekangala Block A - F sewer reticulation and toilets' under a new WBS
- `9.803352.1.W.PH.22.6` → `9.803332.1.W.MA.6`: same erf (Mamelodi X6 erf 34041, Phomolong) water; 2024/25 row is 'Phase 2'
- `9.803352.1.S.SR.22.6` → `9.803352.1.S.MA.6`: same erf (Mamelodi X6 erf 34041, Phomolong) sewer; 2024/25 row is 'Phase 2'

The share fell from **84.6% to 68.2%**. Single-ward money in predominantly Black wards went from R619.8m to R435.2m (**-184.6m**); in other wards from R112.5m to R202.7m (**+90.2m**). (This corrects the 67.2% in the first version of this summary: one 2024/25 ward match, Electricity Distribution Loss, was wrongly rejected and has been restored; see §6.)

**Real budget changes vs. ward-labelling effects.** Each project's change is split into the change in its own budget and the part caused only by a change in ward attribution. The second covers projects whose Appendix O ward moved between groups, or that were single-ward in one year and not the other.

| | Black wards (R m) | Other wards (R m) |
|---|---|---|
| Total change | -184.6 | +90.2 |
| …from projects' own budget changes | -172.1 | +50.4 |
| …from ward-attribution changes | -12.5 | +39.8 |

With attribution held fixed, the 2024/25 share would be **73.3%**. So roughly 11 of the 16 points are real budget re-allocation and the rest is ward labelling. Most of the labelling effect is the "Critical Worn-Out Water Pipes" Areas A and B. Appendix O moved them from ward 100 (Black) in 2023/24 to wards 96 and 53 (other) in 2024/25, although the titles say they cover Regions 1–2 and Region 3.

**Concentrated or broad?** Moderately concentrated. 50 projects moved money in the adverse direction (Black ↓ or other ↑), R532.7m gross. The largest single project is 17% of that, the top 3 are 35%, the top 5 48% and the top 10 67%. Black-ward gains elsewhere offset R257.9m.

Largest adverse movements, ranked by rand impact:

| Project                                                                         | Direction     | Ward 23/24→24/25   |   Budget 23/24 (R m) |   Budget 24/25 (R m) |   Impact (R m) |   …real budget change |   …ward attribution | Cause                                                                     | Link                  |
|:--------------------------------------------------------------------------------|:--------------|:-------------------|---------------------:|---------------------:|---------------:|----------------------:|--------------------:|:--------------------------------------------------------------------------|:----------------------|
| Construction of roads & stormwater - Thorntree View                             | Black wards ↓ | 36 → –             |                 90.2 |                  1.0 |           90.2 |                  89.2 |                 1.0 | budget cut; small 2024/25 remainder has no ward match                     | wbs                   |
| Electricity Distribution Loss                                                   | Black wards ↓ | 29 → 29            |                 68.0 |                 20.0 |           48.0 |                  48.0 |                 0.0 | budget value changed                                                      | manual re-coding link |
| (710026A) Replacement Of Critical Worn-Out Water Network                        | other wards ↑ | 100 → 96           |                 20.8 |                 26.5 |           47.3 |                   5.7 |                41.6 | ward group changed between years' Appendix O                              | wbs                   |
| (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B)         | other wards ↑ | 100 → 53           |                 24.0 |                 15.6 |           39.6 |                   8.4 |                31.3 | ward group changed between years' Appendix O                              | wbs                   |
| (710864) Sewer provision - Zithobeni X8                                         | Black wards ↓ | 105 → –            |                 30.6 |                  0.0 |           30.6 |                  30.6 |                 0.0 | not in 2024/25 budget                                                     | one year only         |
| Timberlands Construction Of 607 Social Housing Units                            | Black wards ↓ | 81 → –             |                 26.0 |                  0.0 |           26.0 |                  26.0 |                 0.0 | budgeted R0 in 2024/25                                                    | wbs                   |
| Sewer reticulation - Andeon X37                                                 | other wards ↑ | 55 → 55            |                  1.0 |                 23.6 |           22.6 |                  22.6 |                 0.0 | budget value changed                                                      | wbs                   |
| Electricity for All - Region 6                                                  | other wards ↑ | – → 101            |                 12.0 |                 20.0 |           20.0 |                   8.0 |                12.0 | in both budgets; no single-ward attribution in 2023/24 (non-attributable) | wbs                   |
| Denneboom Depot                                                                 | Black wards ↓ | 38 → 38            |                 33.5 |                 16.5 |           17.0 |                  17.0 |                 0.0 | budget value changed                                                      | wbs                   |
| Water reticulation - Andeon X37                                                 | other wards ↑ | 55 → 55            |                  2.0 |                 18.4 |           16.4 |                  16.4 |                 0.0 | budget value changed                                                      | wbs                   |
| (710026D) Replacement Of Critical Worn-Out Water Network Pipes (Area D)         | Black wards ↓ | 100 → –            |                 12.2 |                  0.0 |           12.2 |                  12.2 |                 0.0 | not in 2024/25 budget                                                     | one year only         |
| Acquisition and Refurbishment of Midtown Building Acquisition Old-Mercedes Benz | Black wards ↓ | 81 → 81            |                 25.1 |                 13.1 |           12.0 |                  12.0 |                 0.0 | budget value changed                                                      | wbs                   |
| Soshanguve MM Sewer Reticulation                                                | Black wards ↓ | 33 → –             |                 10.6 |                  0.0 |           10.6 |                  10.6 |                 0.0 | not in 2024/25 budget                                                     | one year only         |
| Upgrading of roads and stormwater systems in Cullinan - Phase                   | Black wards ↓ | 100 → –            |                 10.0 |                  0.0 |           10.0 |                  10.0 |                 0.0 | budgeted R0 in 2024/25                                                    | wbs                   |
| Contributions Roads - Garsfontein Road                                          | other wards ↑ | – → 45             |                  0.0 |                  9.5 |            9.5 |                   9.5 |                 0.0 | new in 2024/25 budget                                                     | one year only         |

Largest offsetting movements:

| Project                                                                 | Direction     | Ward 23/24→24/25   |   Offset (R m) | Cause                                                                     |
|:------------------------------------------------------------------------|:--------------|:-------------------|---------------:|:--------------------------------------------------------------------------|
| Sewer provision - Rama City                                             | Black wards ↑ | 32 → 32            |           32.9 | budget value changed                                                      |
| Acquisition of Land                                                     | other wards ↓ | 55 → –             |           26.2 | in both budgets; no single-ward attribution in 2024/25 (non-attributable) |
| Ekangala Block A - F sewer reticulation and toilets                     | Black wards ↑ | 104 → 104          |           24.1 | budget value changed                                                      |
| (710026C) Replacement Of Critical Worn-Out Water Network Pipes (Area C) | Black wards ↑ | 100 → 100          |           16.0 | budget value changed                                                      |
| Flooding Backlogs: Stinkwater & New Eersterust Area                     | Black wards ↑ | – → 14             |           15.0 | in both budgets; no single-ward attribution in 2023/24 (non-attributable) |
| Soshanguve Block L Area 3                                               | Black wards ↑ | – → 35             |           15.0 | budgeted R0 in 2023/24                                                    |
| Upgrading of roads and stormwater systems in Rayton                     | Black wards ↑ | – → 100            |           13.0 | new in 2024/25 budget                                                     |
| Upgrade Refilwe Stadium                                                 | Black wards ↑ | – → 99             |           10.0 | budgeted R0 in 2023/24                                                    |

By cause (sum of changes, R m):

| cause                                                                     |   Black |   Other |
|:--------------------------------------------------------------------------|--------:|--------:|
| budget cut; small 2024/25 remainder has no ward match                     |   -94.3 |     0.0 |
| not in 2024/25 budget                                                     |   -72.0 |     0.0 |
| ward group changed between years' Appendix O                              |   -44.8 |    42.1 |
| budget value changed                                                      |   -40.2 |    39.5 |
| budgeted R0 in 2024/25                                                    |   -36.0 |    -5.3 |
| in both budgets; no single-ward attribution in 2024/25 (non-attributable) |    -6.0 |   -26.2 |
| in both budgets; no single-ward attribution in 2023/24 (multi-ward)       |     7.7 |     0.0 |
| new in 2024/25 budget                                                     |    18.0 |    14.5 |
| budgeted R0 in 2023/24                                                    |    25.0 |     0.0 |
| in both budgets; no single-ward attribution in 2023/24 (non-attributable) |    57.9 |    25.5 |

Reading: the biggest real cut is Thorntree View roads and stormwater (ward 36): R90.2m in the 2023/24 original budget, R1.0m in the 2024/25 MTREF. Appendix N shows R24.5m adjusted and actual for it in 2024/25. Next come Electricity Distribution Loss (ward 29, R68.0m → R20.0m), the Zithobeni X8 sewer (ward 105, R30.6m, not in the 2024/25 MTREF) and Timberlands social housing (ward 81, R26.0m → R0). On the other side are two Andeon X37 projects (ward 55, 75.7% Black African, so "other" at the 80% threshold) totalling +R39m.

### 8. Follow-up 2 — bulk infrastructure by service area, and region-only money

#### 8.1 Ward → region table

Built in the order you specified; the result is in `ward_classification.csv` (`region`, `region_basis`, and the evidence columns).

1. **City documents.** These are every row in the City's documents that gives both a ward and a region:
   - narrative statements in the annual reports (each quoted, with its page, in `work/ward_region_evidence.csv`);
   - Appendix O rows whose project name states a region, e.g. "Region 5 (Public Lighting)" → ward 99;
   - project rows whose Appendix O ward and SA36/SB19 region tag share a WBS code. These are joined across two documents, so they are weaker evidence.

   Four public submissions reproduced in the MTREF appendices also state a ward and region. They are written by residents, not the City, so they are reported but not used.

| Evidence type                                        |   Rows |
|:-----------------------------------------------------|-------:|
| joined: App O ward + SA36/SB19 region tag (same WBS) |    294 |
| App O row: project name states region + ward         |     36 |
| City narrative                                       |     21 |
| public submission in MTREF                           |      4 |

2. **Rekord cross-check.** The City-supplied list published by Rekord (18 Oct 2021) was compared ward by ward. Ward 89 is listed under both Region 1 and Region 5, so it is treated as ambiguous.
3. **Official boundary file.** City of Tshwane e-GIS "Tshwane Regions" layer: https://e-gis001.tshwane.gov.za/server/rest/services/Other_WS/Regions/MapServer/2 (ArcGIS Online item 373aab0ab11b4acf93064338ceea828e, owner `Tshwane_Web_GIS`, retrieved 18 Nov 2026). Overlaid on the MDB 2020 wards, **every ward falls 100% inside one region by both area and 2011 population**; the region polygons are built from whole 2020 wards. The layer has Regions 1–7 only, with no 3A/3B split.

Assignment rule:
- One region across all step-1 rows: use it.
- Step-1 rows disagree: use the e-GIS layer as tie-break.
- No step-1 evidence: use the e-GIS layer.

| Basis                                                     |   Wards |
|:----------------------------------------------------------|--------:|
| step 1: City documents (unanimous)                        |      46 |
| step 3: official e-GIS region layer (no step-1 evidence)  |      40 |
| step 1 conflict -> official e-GIS layer used as tie-break |      21 |

**Wards the City assigns to different regions in different rows** (21). Most are one stray joined row against a clear majority:

|   ward | step1_city_documents                                     | step2_rekord_2021                           | step3_official_egis   | region_final   |
|-------:|:---------------------------------------------------------|:--------------------------------------------|:----------------------|:---------------|
|      7 | Region 3 (x3);Region 7 (x1);Region 1 (x1)                |                                             | Region 3              | Region 3       |
|     22 | Region 1 (x11);Region 5 (x1)                             | Region 1                                    | Region 1              | Region 1       |
|     26 | Region 1 (x2);Region 2 (x1)                              | Region 1                                    | Region 1              | Region 1       |
|     32 | Region 1 (x8);Region 6 (x1)                              | Region 1                                    | Region 1              | Region 1       |
|     33 | Region 2 (x2);Region 1 (x1)                              | Region 1                                    | Region 1              | Region 1       |
|     34 | Region 1 (x2);Region 6 (x1)                              | Region 1                                    | Region 1              | Region 1       |
|     50 | Region 6 (x4);Region 2 (x1)                              | Region 2                                    | Region 2              | Region 2       |
|     55 | Region 3 (x31);Region 6 (x1);Region 1 (x1)               |                                             | Region 3              | Region 3       |
|     58 | Region 3 (x9);Region 6 (x1)                              |                                             | Region 3              | Region 3       |
|     61 | Region 4 (x3);Region 2 (x1)                              |                                             | Region 4              | Region 4       |
|     65 | Region 4 (x3);Region 5 (x1)                              |                                             | Region 4              | Region 4       |
|     70 | Region 4 (x9);Region 3 (x1)                              |                                             | Region 4              | Region 4       |
|     75 | Region 2 (x3);Region 5 (x1)                              | Region 2                                    | Region 2              | Region 2       |
|     81 | Region 3 (x5);Region 5 (x2)                              |                                             | Region 3              | Region 3       |
|     89 | Region 1 (x1);Region 3 (x1)                              | Region 1;Region 5 (ambiguous: listed twice) | Region 1              | Region 1       |
|     96 | Region 2 (x13);Region 6 (x4);Region 3 (x1);Region 5 (x1) | Region 2                                    | Region 2              | Region 2       |
|     99 | Region 5 (x18);Region 1 (x1);Region 4 (x1);Region 3 (x1) | Region 5                                    | Region 5              | Region 5       |
|    100 | Region 5 (x19);Region 6 (x1);Region 3 (x1)               | Region 5                                    | Region 5              | Region 5       |
|    101 | Region 6 (x9);Region 4 (x1);Region 5 (x1);Region 3 (x1)  |                                             | Region 6              | Region 6       |
|    104 | Region 7 (x5);Region 3 (x2)                              | Region 7                                    | Region 7              | Region 7       |
|    105 | Region 7 (x18);Region 5 (x1);Region 6 (x1)               | Region 7                                    | Region 7              | Region 7       |

**Step 1 vs Rekord disagreements** (13):

|   ward | step1_city_documents                                     | step2_rekord_2021                           | step3_official_egis   |
|-------:|:---------------------------------------------------------|:--------------------------------------------|:----------------------|
|     22 | Region 1 (x11);Region 5 (x1)                             | Region 1                                    | Region 1              |
|     26 | Region 1 (x2);Region 2 (x1)                              | Region 1                                    | Region 1              |
|     32 | Region 1 (x8);Region 6 (x1)                              | Region 1                                    | Region 1              |
|     33 | Region 2 (x2);Region 1 (x1)                              | Region 1                                    | Region 1              |
|     34 | Region 1 (x2);Region 6 (x1)                              | Region 1                                    | Region 1              |
|     50 | Region 6 (x4);Region 2 (x1)                              | Region 2                                    | Region 2              |
|     75 | Region 2 (x3);Region 5 (x1)                              | Region 2                                    | Region 2              |
|     89 | Region 1 (x1);Region 3 (x1)                              | Region 1;Region 5 (ambiguous: listed twice) | Region 1              |
|     96 | Region 2 (x13);Region 6 (x4);Region 3 (x1);Region 5 (x1) | Region 2                                    | Region 2              |
|     99 | Region 5 (x18);Region 1 (x1);Region 4 (x1);Region 3 (x1) | Region 5                                    | Region 5              |
|    100 | Region 5 (x19);Region 6 (x1);Region 3 (x1)               | Region 5                                    | Region 5              |
|    104 | Region 7 (x5);Region 3 (x2)                              | Region 7                                    | Region 7              |
|    105 | Region 7 (x18);Region 5 (x1);Region 6 (x1)               | Region 7                                    | Region 7              |

The Rekord list and the e-GIS layer agree on every ward except ward 89, which Rekord lists under both Regions 1 and 5 (e-GIS: Region 1). All four public submissions agree with the final table.

**Where City documents override the e-GIS layer** (unanimous step-1 evidence, per your order of evidence). Ward 107 rests only on the 2023/24 Bronkhorstbaai narrative, which the 2022/23 report places in ward 102, so treat it with caution.

|   ward | step1_city_documents   | step3_official_egis   | region_final   |
|-------:|:-----------------------|:----------------------|:---------------|
|     78 | Region 1 (x1)          | Region 4              | Region 1       |
|     85 | Region 4 (x1)          | Region 6              | Region 4       |
|    107 | Region 7 (x2)          | Region 3              | Region 7       |

Final assignment:

| Region   | Wards                                                                                                           |
|:---------|:----------------------------------------------------------------------------------------------------------------|
| Region 1 | 2, 4, 9, 11, 12, 19, 20, 21, 22, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 78, 88, 89, 90, 94, 98 |
| Region 2 | 5, 8, 13, 14, 49, 50, 73, 74, 75, 76, 95, 96                                                                    |
| Region 3 | 1, 3, 7, 42, 51, 52, 53, 54, 55, 56, 58, 59, 60, 62, 63, 68, 71, 72, 80, 81, 82, 84, 92                         |
| Region 4 | 48, 57, 61, 64, 65, 66, 69, 70, 77, 79, 85, 106                                                                 |
| Region 5 | 87, 99, 100                                                                                                     |
| Region 6 | 6, 10, 15, 16, 17, 18, 23, 28, 38, 40, 41, 43, 44, 45, 46, 47, 67, 83, 86, 91, 93, 97, 101                      |
| Region 7 | 102, 103, 104, 105, 107                                                                                         |

**Region 3A/3B.** The budget tables tag some projects "Region 3A" or "Region 3B"; no source lists which wards belong to each half. That money is split across all of Region 3.

#### 8.2 Bulk infrastructure: stated beneficiaries

The 84 bulk-infrastructure project names (name-based flag; see §6) were searched across all nine documents for an explicit statement of the area served. Every quote below was checked against the PDF text. Rules for turning a statement into ward weights:
- A stated **ward** goes to that ward.
- A stated **township** goes to its wards, weighted by each ward's share of the township's 2011 population (Census 2011 Main Place mapping).
- A stated **region**, or a statement whose ward conflicts with its own stated region, counts as **region-only money**.
- Anything without a stated beneficiary is **unattributed**, even when Appendix O gives the plant's ward.

The primary run uses narrative and table statements only. Project titles with a service verb ("Water provision – Winterveldt …") are added as a separate variant.

| Project                                       | Basis     | Attributed to   | Target             | Source                                                                 |   Page | Quote                                                                                                                                       | Decision note                                                                                                                                                                                                                                                         |
|:----------------------------------------------|:----------|:----------------|:-------------------|:-----------------------------------------------------------------------|-------:|:--------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Rooiwal WWTW Phase 1                          | narrative | township        | Temba;Hammanskraal | City-of-Tshwane-Audited-Annual-Report-for-2022_23-FY.pdf               |     77 | it will benefit the communities of Temba, Hammanskraal and Marokolong in Region 2                                                           | also AR 2023/24 p90 (same words) and AR 2024/25 p94 ('to address the Hammanskraal's water challenges'). Marokolong is a separate Census Main Place not in the township mapping, so it is not allocated; 'Hammanskraal' = the official Main Place (Rens Town, Kanana). |
| Klipgat WWTW                                  | narrative | regions         | Region 1           | 13.-The-Consolidated-Annual-Report-for-the-City-of-Tshwane_2023_24.pdf |     91 | now servicing the communities of several wards to the south of Ga-Rankuwa, Mabopane and parts of Winterveldt and Soshanguve in Region 1     | wards not named ('several wards to the south of'); attributed at the stated region level. Similar wording AR 2024/25 p93.                                                                                                                                             |
| Bronkhorstbaai                                | narrative | regions         | Region 7           | City-of-Tshwane-Audited-Annual-Report-for-2022_23-FY.pdf               |     27 | will benefit the community of Bronkhorstbaai, Summerplace and Kungwini Country Estate in Ward 102, Region 7                                 | AR 2023/24 p83 says 'Ward 107, Region 7' for the same communities; ward conflicts, region agrees -> region level.                                                                                                                                                     |
| New Parkmore LL Reservoir                     | narrative | regions         | Region 6           | 13.-The-Consolidated-Annual-Report-for-the-City-of-Tshwane_2023_24.pdf |     83 | will service more than 20 000 households in ward 50 and ward 96 across Region 6                                                             | the City's e-GIS region layer places wards 50 and 96 in Region 2; ward/region conflict -> stated region used. Region 6 also in AR 2022/23 p72.                                                                                                                        |
| Mamelodi Ext 11 water (Bulk and reticulation) | narrative | wards           | 10                 | 13.-The-Consolidated-Annual-Report-for-the-City-of-Tshwane_2023_24.pdf |     90 | Mamelodi Ext 11 - (Ward 10, Region 6): ... a bulk supply pipeline and house connections to service a total of 1 859 households              | ward 10 is in Region 6 on the e-GIS layer (consistent).                                                                                                                                                                                                               |
| Wildebees                                     | narrative | regions         | Region 5;Region 6  | City-of-Tshwane-Audited-Annual-Report-for-2022_23-FY.pdf               |     83 | Infeed Station to lessen the bulk capacity constraints in Region 5 and 6 including surrounding areas that are being serviced by the station | –                                                                                                                                                                                                                                                                   |
| Zithobeni X8&9 - Bulk                         | narrative | township        | Zithobeni          | City-of-Tshwane-Audited-Annual-Report-for-2022_23-FY.pdf               |    330 | (710863) Zithobeni X8&9 - Bulk ... Connection to bulk water supply for Zithobeni X8&9                                                       | project performance table (target text).                                                                                                                                                                                                                              |
| Water provision - Winterveldt 20ML Reservoir  | title     | township        | Winterveld         | budget tables / Appendix N                                             |        | Water provision - Winterveldt 20ML Reservoir                                                                                                | title states service ('Water provision') + area                                                                                                                                                                                                                       |
| Water provision – Winterveldt 20ML Reservoir  | title     | township        | Winterveld         | budget tables / Appendix N                                             |        | Water provision – Winterveldt 20ML Reservoir                                                                                                | title states service ('Water provision') + area                                                                                                                                                                                                                       |
| Water Provision - Winterveldt Bulk water line | title     | township        | Winterveld         | budget tables / Appendix N                                             |        | Water Provision - Winterveldt Bulk water line                                                                                               | title states service ('Water provision') + area                                                                                                                                                                                                                       |

Statements found but not used:

| Project                                                                                                               | Statement                                                                                 | Why not used                                                                                                                                 |
|:----------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| Sunderland Ridge WWTW                                                                                                 | AR 2024/25 p93: 'now servicing communities of Ward 24 and sorrounding areas in, Region 6' | internally inconsistent: ward 24 is Region 1 in every City source; budget tables place the plant in Region 4 / ward 70                       |
| Water provision - Hammanskraal West X10 (Bulk water line)                                                             | title                                                                                     | Hammanskraal West X10 is not part of the official Hammanskraal Main Place; no mapping                                                        |
| Water provision - Rama City (20 ML Reservoir)                                                                         | title                                                                                     | Rama City not in the township mapping                                                                                                        |
| Wapadrand / Mooikloof / Pyramid / Monavoni / Rosslyn / Kwagga / Soshanguve JJ line / Laudium / Tshwane Automotive SEZ | AR text                                                                                   | beneficiary not named ('surrounding areas', 'these fast-growing areas', 'neighbouring communities') or link to the budget project not stated |

Most bulk projects have **no stated beneficiary**. None was found for Waltloo–Nyala lines, Temba/Babelegi, Ekangala and Baviaanspoort WWTWs, Bronkhorstspruit WPP, the Booysens, Fort West, Refilwe Manor, Babelegi, Magalies, Garsfontein and Klapperkop reservoirs, Salvokop, the Network Control Centre, Ifafi, Kentron, Pyramid, the Olievenhoutbosch X60 bulk line, Bulk Sewer Line – Winterveldt, or the canals. All of those are unattributed on the service-area basis.

#### 8.3 Results: Black-ward share (≥80%) of ward-attributed capex

- **Location:** the earlier method (Appendix O ward). Two exceptions: titles naming more than one region (the "Critical Worn-Out Water Pipes" areas), and titles naming a region that doesn't contain the Appendix O ward (Areas B and D in 2023/24), are treated as region-only.
- **Service area:** bulk rows attributed only through a stated beneficiary (§8.2); all other rows as under location.
- **(a):** region-only money left unattributed.
- **(b):** region-only money split across that region's wards in proportion to 2022 population. **This assumes every resident of the region benefits equally; it is an assumption, not a fact from the documents.**
- **(c):** (b) minus (a), in percentage points.

| Measure                 |   Location (a) |   Location (b) |   Location (c) = b − a |   Service area (a) |   Service area (b) |   Service (c) = b − a |   Service + titles (b) |
|:------------------------|---------------:|---------------:|-----------------------:|-------------------:|-------------------:|----------------------:|-----------------------:|
| 2022/23 original budget |           72.7 |           73.1 |                    0.4 |               84.1 |               84.4 |                   0.2 |                   84.5 |
| 2022/23 adjusted budget |           77.5 |           77.4 |                   -0.1 |               83.1 |               84.2 |                   1.1 |                   84.2 |
| 2023/24 original budget |           59.3 |           61.5 |                    2.3 |               86.4 |               83.0 |                  -3.4 |                   83.2 |
| 2023/24 adjusted budget |           58.4 |           59.2 |                    0.7 |               86.8 |               83.6 |                  -3.2 |                   83.7 |
| 2024/25 original budget |           56.2 |           57.1 |                    0.8 |               77.1 |               76.2 |                  -0.9 |                   77.0 |
| 2024/25 adjusted budget |           60.4 |           60.3 |                   -0.0 |               75.5 |               75.1 |                  -0.4 |                   77.9 |
| 2024/25 actual spend    |           60.0 |           60.0 |                    0.1 |               75.3 |               74.9 |                  -0.4 |                   78.0 |

Per-capita ratio (R per resident in Black wards ÷ R per resident in other wards):

| Measure                 |   Location (a) |   Location (b) |   Service area (a) |   Service area (b) |
|:------------------------|---------------:|---------------:|-------------------:|-------------------:|
| 2022/23 original budget |           0.87 |           0.89 |               1.73 |               1.76 |
| 2022/23 adjusted budget |           1.12 |           1.12 |               1.60 |               1.74 |
| 2023/24 original budget |           0.47 |           0.52 |               2.07 |               1.59 |
| 2023/24 adjusted budget |           0.46 |           0.47 |               2.15 |               1.67 |
| 2024/25 original budget |           0.42 |           0.43 |               1.10 |               1.04 |
| 2024/25 adjusted budget |           0.50 |           0.50 |               1.00 |               0.98 |
| 2024/25 actual spend    |           0.49 |           0.49 |               0.99 |               0.97 |

#### 8.4 What remains unattributed

After (b), the unattributed share of each measure's capex is **28–33%** on the location basis and **43–52%** on the service-area basis. On top of that, multi-ward projects (shown separately) are not split across wards.

Location basis, (b):

| measure                 |   Total (R m) |   Ward-attributed % |   Multi-ward (R m) |   unmatched (R m) |   city-wide (R m) |   administrative-hq (R m) |   no-intersect (R m) |   Unattributed % |
|:------------------------|--------------:|--------------------:|-------------------:|------------------:|------------------:|--------------------------:|---------------------:|-----------------:|
| 2022/23 original budget |       2,793.1 |                63.3 |              256.2 |             137.0 |             473.8 |                     159.5 |                –   |             27.6 |
| 2022/23 adjusted budget |       2,816.2 |                58.9 |              226.5 |             177.3 |             586.7 |                     165.8 |                –   |             33.0 |
| 2023/24 original budget |       2,347.7 |                61.2 |              220.2 |             104.9 |             451.8 |                     134.7 |                –   |             29.4 |
| 2023/24 adjusted budget |       2,112.6 |                58.5 |              202.7 |              95.9 |             453.3 |                     125.8 |                –   |             31.9 |
| 2024/25 original budget |       2,347.6 |                58.7 |              208.5 |             159.6 |             461.5 |                     137.1 |                  1.8 |             32.4 |
| 2024/25 adjusted budget |       2,340.1 |                58.2 |              276.9 |              13.4 |             568.1 |                     117.5 |                  1.8 |             29.9 |
| 2024/25 actual spend    |       2,300.1 |                57.6 |              281.3 |              13.3 |             560.1 |                     119.4 |                  1.8 |             30.2 |

Service-area basis, (b):

| measure                 |   Total (R m) |   Ward-attributed % |   Multi-ward (R m) |   unmatched (R m) |   city-wide (R m) |   bulk, no stated beneficiary (R m) |   administrative-hq (R m) |   Unattributed % |
|:------------------------|--------------:|--------------------:|-------------------:|------------------:|------------------:|------------------------------------:|--------------------------:|-----------------:|
| 2022/23 original budget |       2,793.1 |                47.4 |              221.2 |              35.8 |             458.8 |                               593.6 |                     159.5 |             44.7 |
| 2022/23 adjusted budget |       2,816.2 |                48.2 |              191.5 |               1.5 |             566.7 |                               533.7 |                     165.8 |             45.0 |
| 2023/24 original budget |       2,347.7 |                48.5 |              190.2 |              14.0 |             424.8 |                               446.0 |                     134.7 |             43.4 |
| 2023/24 adjusted budget |       2,112.6 |                48.3 |              148.6 |              37.9 |             432.8 |                               347.2 |                     125.8 |             44.7 |
| 2024/25 original budget |       2,347.6 |                41.0 |              168.5 |              38.8 |             433.5 |                               607.5 |                     137.1 |             51.8 |
| 2024/25 adjusted budget |       2,340.1 |                39.4 |              245.0 |              11.4 |             520.4 |                               523.6 |                     117.5 |             50.1 |
| 2024/25 actual spend    |       2,300.1 |                38.4 |              249.5 |              11.3 |             513.3 |                               522.6 |                     119.4 |             50.7 |

Where the region-only money comes from (R m, split in (b)):

|                                                               |   2022/23 original budget |   2022/23 adjusted budget |   2023/24 original budget |   2023/24 adjusted budget |   2024/25 original budget |   2024/25 adjusted budget |   2024/25 actual spend |
|:--------------------------------------------------------------|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|-----------------------:|
| ('location', 'App N row -> SA36 tag of same-named MTREF row') |                     –   |                     –   |                     –   |                     –   |                     –   |                      85.7 |                   85.0 |
| ('location', 'SA36/SB19 region tag')                          |                     102.7 |                       5.4 |                     216.2 |                      68.8 |                     176.1 |                     –   |                  –   |
| ('location', 'region(s) named in project title')              |                     –   |                     –   |                     109.5 |                     108.4 |                      78.3 |                      43.6 |                   44.7 |
| ('service', 'App N row -> SA36 tag of same-named MTREF row')  |                     –   |                     –   |                     –   |                     –   |                     –   |                      32.7 |                   33.1 |
| ('service', 'SA36/SB19 region tag')                           |                      59.7 |                       5.4 |                      77.2 |                      24.8 |                      72.4 |                     –   |                  –   |
| ('service', 'bulk: stated beneficiary region (AR narrative)') |                     139.8 |                     147.0 |                     125.0 |                     106.6 |                      41.9 |                      17.6 |                   16.6 |
| ('service', 'region(s) named in project title')               |                     –   |                     –   |                     109.5 |                     108.4 |                      78.3 |                      43.6 |                   44.7 |

Of which tagged "Region 3A/3B" and therefore spread over all of Region 3 (R m):

| basis    |   2022/23 original budget |   2022/23 adjusted budget |   2023/24 original budget |   2023/24 adjusted budget |   2024/25 original budget |   2024/25 adjusted budget |   2024/25 actual spend |
|:---------|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|-----------------------:|
| location |                      18.1 |                       4.1 |                      53.2 |                      26.3 |                      39.5 |                      30.2 |                   29.0 |
| service  |                      18.1 |                       4.1 |                      11.7 |                       4.0 |                      23.5 |                       8.2 |                    8.2 |

#### 8.5 Reading

- **Service area.** Re-attributing bulk infrastructure by stated service area mainly removes it from the ward analysis, because only a handful of plants have a documented beneficiary. On that basis the Black-ward share is roughly flat between 2022/23 and 2023/24 (84.4% → 83.0% original; 84.2% → 83.6% adjusted, under (b)). It is lower in all three 2024/25 measures (76.2% original, 75.1% adjusted, 74.9% actual).
- **Rooiwal.** Under the location basis, Rooiwal counts against Black wards because the plant sits in ward 96. Under the service-area basis it counts for Temba and Hammanskraal, as the City's annual reports state. Because so much other bulk spending drops out, the service-area shares rest on 33–49% of the budget.
- **Region-only split.** Population-splitting region-only money moves the Black-ward share by at most 3.4 points in any year. It raises ward-attributed coverage by 0–14 points on the location basis and 4–13 points on the service-area basis, depending on the year, but leaves the year-to-year pattern unchanged.
- **Overall.** The 2022/23 → 2023/24 fall in §3 depends on counting bulk plants by location; it doesn't survive service-area attribution. The 2024/25 fall (Brink-era original budget, and the adjusted budget and actual spend executed mostly afterwards) survives every variant here, though a third of that step is ward labelling (§7).

### 9. Extension to the Moya administration (from Oct 2024)

All methods, scripts, the ward classification (Stats SA 2022, ≥80% Black African primary) and the ward→region table are unchanged from §1–§8, so the new columns compare directly with the old ones.

#### 9.1 New documents

| File | Pages | Contents used | Ward / region columns | Budget or actual |
|---|---|---|---|---|
| 07. Proposed 2024-25 Adjustment Budget | 151 | Annexure B pp135–139 (project-level original → adjusted 2024/25) | none (no SB19 table) | budget; capital YTD actual only as a citywide total: **R802m to 31 Dec 2024, 34% of the original** (p47) |
| 02. 2025-26 MTREF (Special Council 29-05-2025) | 1,803 | Annexure A pp64–70 (project-level 2025/26 original) | **"Regions" column** (Region 1–7, Tshwane Wide, Administrative); no SA36 table | budget |
| 10. 2025-26 Adjustment Budget | 150 | Annexure B pp144–150 (project-level 2025/26 original → adjusted) | **"Regions" column** | budget; capital YTD actual only citywide: **R1,1 billion, 46% of the original** (p52) |
| 02. 2026-27 MTREF (Final) | 1,508 | Annexure A pp66–72 (project-level 2026/27 original) | **"Regions" column** (adds "Multiple regions") | budget. Cover: "Mayoral Committee to be held on 21 May 2026" (p65). Council adoption date not stated. Corrupt streams and blank pages are in tariff annexures N–P only |
| "-1" copies of the 2022/23 and 2023/24 annual reports | – | byte-identical duplicates (same MD5); ignored | | |

**No ward-level actual spend exists for 2025/26.** There is no 2025/26 annual report or in-year capital report in the folder, and none of the new documents breaks capital actuals down by region either. The only in-year capital actuals are the two citywide figures:

| Period | Capital spent | % of original capital budget | Source |
|---|---|---|---|
| 2024/25, to 31 Dec 2024 | R802 million (incl. entities) | 34% | 2024/25 adjustment budget p47 |
| 2024/25, full year | R2,300,073,481 | 98.3% of adjusted (App N) | AR 2024/25 App N p515 |
| 2025/26, mid-year | R1,1 billion | 46% | 2025/26 adjustment budget p52 |

#### 9.2 Extraction and reconciliation

| Budget | Extracted | Stated total | Where stated | Coverage |
|---|---|---|---|---|
| 2024/25 original (adj. budget col.) | R2,347,552,577 | R2,347,552,576 | Annexure B p139 | 100% |
| 2024/25 adjusted (adj. budget) | R2,312,623,793 | R2,312,623,791 | Annexure B p139 | 100% |
| 2025/26 original | R2,459,328,252 | R2,459,328,252 | Annexure A p70 | 100% |
| 2025/26 adjusted | R2,755,935,586 | R2,768,935,587 | Annexure B p150 | **99.5%** |
| 2026/27 original | R2,856,300,535 | R2,856,300,538 | Annexure A p72 | 100% |

- **2025/26 adjusted gap.** The R13,000,000 shortfall (original and adjusted) is in the source document itself. "Upgrading of roads and stormwater systems in Refilwe" (WBS 9.804026.1.R.RO.05.5, R13m in the 2025/26 MTREF) is missing from Annexure B's project list, but its Roads & Transport department total (R602,855,364, p147) still includes it. It is left unattributed rather than reconstructed.
- **2024/25 adjusted, two totals.** The 2024/25 adjustment budget (R2,312.6m, the post-Oct 2024 Council's adjustment) is the new column. The annual report's Appendix N "adjusted" (R2,340.1m) and actual are kept as the final 2024/25 figures, as agreed.
- **2026/27 reconciles.** The Annexure A total of **R2,856,300,538** equals the 2026/27 SDBIP capital total you supplied (R2,856,300,538) exactly, and the MTREF itself says "The capital budget amounts to R2,8 billion for 2026/27" (p109) and "TOTAL CAPITAL BUDGET 2,856,300,538" (p111). Neither the SDBIP nor the budget speech is in the folder, so that match rests on the figure supplied. The column is labelled "2026/27 original (Mayco draft, reconciles to adopted SDBIP)".
- **Name decoding.** Overprinted names were decoded as before; each change is recorded in `name_note` in `work/moya_rows.csv`. The "Critical Worn-Out Water Pipes" rows were given their canonical titles from the 2025/26 MTREF p69 by area letter: Area A covers Regions 1–2, Area B Region 3, and Area C Regions 4, 5, 6 & 7.
- **Linking across years.** Links use the WBS code without the funding segment plus a name check. One extra rule handles sub-codes that were renamed: the same WBS programme plus a name score ≥95, or the old name contained in the new one with no added place name. This covers the Soshanguve JJ line (`SU`→`SO`), Monavoni, Wildebees and the deficient-sewers areas. Weaker candidates were rejected: Baviaanspoort→Rooiwal, Rietvlei→Bronkhorstspruit, Heatherview X79→X42, and area-specific Water Conservation lines→the citywide line.

#### 9.3 Option A attribution and the composition of each new budget (check 2)

- **2024/25 adjusted:** each row takes its ward from the same year's Appendix O, via its WBS-linked 2024/25 MTREF row. Otherwise it takes the 2024/25 SA36 region tag.
- **2025/26 onward:** each row takes its ward from the most recent earlier Appendix O (2024/25, else 2023/24), via the WBS link. These rows are flagged "CARRIED FORWARD"; this is an inference across years, not a ward stated in the new documents. Otherwise the row uses the City's Regions column.

Composition (R m, % of each budget):

| category                                                  | 2024/25 adjusted (adj. budget)   | 2025/26 original   | 2025/26 adjusted   | 2026/27 original (Mayco draft, reconciles to adopted SDBIP)   |
|:----------------------------------------------------------|:---------------------------------|:-------------------|:-------------------|:--------------------------------------------------------------|
| (i') carried-forward: App O city-wide / HQ / no-intersect | –                                | 491.2 (20.0%)      | 726.2 (26.4%)      | 554.2 (19.4%)                                                 |
| (i') same-year App O: App O city-wide / HQ / no-intersect | 707.1 (30.6%)                    | –                  | –                  | –                                                             |
| (i) carried-forward: multi-ward                           | –                                | 136.3 (5.5%)       | 111.7 (4.1%)       | 117.3 (4.1%)                                                  |
| (i) carried-forward: single ward                          | –                                | 1423.7 (57.9%)     | 1201.5 (43.6%)     | 1091.7 (38.2%)                                                |
| (i) same-year App O: multi-ward                           | 263.9 (11.4%)                    | –                  | –                  | –                                                             |
| (i) same-year App O: single ward                          | 1128.0 (48.8%)                   | –                  | –                  | –                                                             |
| (ii) region-only (Regions column)                         | –                                | 293.7 (11.9%)      | 278.9 (10.1%)      | 525.9 (18.4%)                                                 |
| (ii) region-only (SA36 tag)                               | 76.5 (3.3%)                      | –                  | –                  | –                                                             |
| (iii) Tshwane Wide / Administrative                       | –                                | 76.9 (3.1%)        | 360.4 (13.1%)      | 425.4 (14.9%)                                                 |
| (iv) 'Multiple regions' (unspecified)                     | –                                | –                  | –                  | 116.4 (4.1%)                                                  |
| (v) no ward or region                                     | 137.2 (5.9%)                     | 37.5 (1.5%)        | 77.2 (2.8%)        | 25.5 (0.9%)                                                   |

(i) = ward(s) from Appendix O (carried forward from 2025/26); (i') = Appendix O said city-wide, HQ or "No Intersect"; (ii) = region-only; (iii) = Tshwane Wide or Administrative; (iv) = "Multiple regions" with no region named; (v) = neither a ward nor a region. The asymmetry is visible: **continuing projects carry a ward, new projects can only be placed by region**. The region-only share rises from 11.9% (2025/26 original) to 18.4% (2026/27), and carried single-ward money falls from 57.9% to 38.2%.

#### 9.4 Carried-forward wards vs the City's Regions column (check 1)

Every carried-forward single-ward row from 2025/26 on was compared with the official e-GIS region of its carried ward:

| Regions column vs e-GIS region of carried ward   |   Rows |      Rm |
|:-------------------------------------------------|-------:|--------:|
| agree                                            |    242 | 3,172.6 |
| column says Administrative                       |      3 |    20.5 |
| column says Multiple regions                     |      3 |    16.0 |
| column says Tshwane Wide                         |     17 |   396.0 |
| conflict                                         |     10 |    60.0 |
| no Regions value                                 |      7 |    51.8 |

**Agreement rate** where the column names a specific region: **96.0% of rows, 98.1% of rand value**. Separately, **R432.5m** of carried single-ward money is labelled Tshwane Wide, Administrative or "Multiple regions" by the City, which conflicts in scope with Appendix O's single ward. All of these rows are flagged `carry_conflict` in `work/moya_rows.csv`. Mismatches:

| Document   |   Page | Project                                                                                          |   Carried ward | e-GIS region of ward   | City Regions column   | Result                       |   R m |
|:-----------|-------:|:-------------------------------------------------------------------------------------------------|---------------:|:-----------------------|:----------------------|:-----------------------------|------:|
| 2025/26    |     64 | Turnaround of Municipal Water Service - Reduction of Water losses                                |             58 | Region 3               | Tshwane Wide          | column says Tshwane Wide     |  50.0 |
| 2025/26adj |    144 | Turnaround of Municipal Water Service - Reduction of Water losses                                |             58 | Region 3               | Tshwane Wide          | column says Tshwane Wide     |  45.3 |
| 2025/26adj |    146 | (804000) - 16 Contributions Roads - Garsfontein Road                                             |             45 | Region 6               | Tshwane Wide          | column says Tshwane Wide     |  43.2 |
| 2025/26    |     66 | Contributions Roads - Garsfontein Road                                                           |             45 | Region 6               | Tshwane Wide          | column says Tshwane Wide     |  35.0 |
| 2025/26adj |    149 | (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B - Region 3)               |            100 | Region 5               | Tshwane Wide          | column says Tshwane Wide     |  33.6 |
| 2025/26adj |    149 | (710026C) Replacement Of Critical Worn-Out Water Network Pipes (Area C - Region 4,5,6&7)         |            100 | Region 5               | Tshwane Wide          | column says Tshwane Wide     |  32.1 |
| 2025/26adj |    149 | (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B - Region 3)               |            100 | Region 5               | Tshwane Wide          | column says Tshwane Wide     |  24.0 |
| 2025/26    |     69 | (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B - Region 3)               |            100 | Region 5               | Tshwane Wide          | column says Tshwane Wide     |  21.9 |
| 2025/26    |     69 | (710026C) Replacement Of Critical Worn-Out Water Network Pipes (Area C - Region 4,5,6&7)         |            100 | Region 5               | Tshwane Wide          | column says Tshwane Wide     |  21.9 |
| 2026/27    |     72 | Turnaround Reduction of Water Losses                                                             |             58 | Region 3               | Tshwane Wide          | column says Tshwane Wide     |  20.0 |
| 2025/26adj |    149 | Replacement of obsolete of meter test bench ( Electricity Distribution                           |             29 | Region 1               | Tshwane Wide          | column says Tshwane Wide     |  20.0 |
| 2025/26adj |    144 | Turnaround of Municipal Water Service - Reduction of Water losses                                |             58 | Region 3               | Tshwane Wide          | column says Tshwane Wide     |  20.0 |
| 2025/26    |     68 | Replacement of obsolete of meter test bench ( Electricity Distribution                           |             29 | Region 1               | Tshwane Wide          | column says Tshwane Wide     |  20.0 |
| 2025/26    |     66 | Flooding backlog: Soshanguve Block WW                                                            |             36 | Region 1               |                       | no Regions value             |  20.0 |
| 2026/27    |     71 | (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B - Region 3)               |            100 | Region 5               | Region 3              | conflict                     |  19.3 |
| 2025/26    |     69 | (710026A) Replacement Of Critical Worn-Out Water Network Pipes (Area A - Region 1-2)             |             96 | Region 2               | Region 5              | conflict                     |  17.0 |
| 2026/27    |     71 | (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B - Region 3)               |            100 | Region 5               | Multiple regions      | column says Multiple regions |  16.0 |
| 2025/26    |     64 | Upgrade Refilwe Stadium                                                                          |             99 | Region 5               |                       | no Regions value             |  16.0 |
| 2025/26adj |    149 | (710026A) Replacement Of Critical Worn-Out Water Network Pipes (Area A - Region 1-2)             |             96 | Region 2               | Region 5              | conflict                     |  10.0 |
| 2025/26adj |    149 | (710026C) Replacement Of Critical Worn-Out Water Network Pipes (Area C - Region 4,5,6&7)         |            100 | Region 5               | Tshwane Wide          | column says Tshwane Wide     |   9.0 |
| 2025/26    |     65 | Capital Movables                                                                                 |             58 | Region 3               | Administrative        | column says Administrative   |   7.7 |
| 2025/26adj |    146 | Capital Moveables                                                                                |             58 | Region 3               | Administrative        | column says Administrative   |   7.7 |
| 2025/26adj |    148 | Refurbishment of Mooikloof Substation                                                            |             91 | Region 6               |                       | no Regions value             |   5.9 |
| 2026/27    |     68 | Capital Moveables                                                                                |             58 | Region 3               | Administrative        | column says Administrative   |   5.2 |
| 2025/26adj |    149 | (710026A) Replacement Of Critical Worn-Out Water Network Pipes (Area A - Region 1-2)             |             96 | Region 2               | Region 5              | conflict                     |   4.0 |
| 2025/26    |     68 | Tshwane Public Lighting Program                                                                  |             49 | Region 2               |                       | no Regions value             |   4.0 |
| 2025/26    |     68 | Contributions Water- Louwlardia Ext 57 ( Pretoriusrand Reservoir)                                |             65 | Region 4               | Region 5              | conflict                     |   3.8 |
| 2025/26adj |    149 | Contributions Contributions (City Water- Wide) Louwlardia Ext 57 ( Pretoriusrand Reservoir)      |             65 | Region 4               | Region 5              | conflict                     |   3.8 |
| 2025/26    |     69 | Refurbishing of Water Networks and Backlog - Ekangala Block A - F sewer reticulation and toilets |            104 | Region 7               |                       | no Regions value             |   3.0 |
| 2025/26adj |    145 | Acquisition and Refurbishment of Midtown Building                                                |             81 | Region 3               |                       | no Regions value             |   2.3 |
| 2025/26    |     65 | Water reticulation -Gatsebe                                                                      |             22 | Region 1               | Region 5              | conflict                     |   1.0 |
| 2026/27    |     67 | Water reticulation -Gatsebe                                                                      |             22 | Region 1               | Region 5              | conflict                     |   1.0 |
| 2025/26adj |    146 | Townlands Project - Construction of 1,200 social housing units                                   |             81 | Region 3               |                       | no Regions value             |   0.6 |
| 2025/26    |     69 | (710026A) Replacement Of Critical Worn-Out Water Network Pipes (Area A - Region 1-2)             |             96 | Region 2               | Region 5              | conflict                     |   0.0 |
| 2025/26    |     69 | (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B - Region 3)               |            100 | Region 5               | Tshwane Wide          | column says Tshwane Wide     |   0.0 |
| 2025/26    |     69 | (710026C) Replacement Of Critical Worn-Out Water Network Pipes (Area C - Region 4,5,6&7)         |            100 | Region 5               | Tshwane Wide          | column says Tshwane Wide     |   0.0 |
| 2025/26    |     68 | Loss) Electricity Distribution Loss                                                              |             29 | Region 1               | Tshwane Wide          | column says Tshwane Wide     |   0.0 |
| 2026/27    |     71 | (710026A) Replacement Of Critical Worn-Out Water Network Pipes (Area A - Region 1-2)             |             96 | Region 2               | Multiple regions      | column says Multiple regions |   0.0 |
| 2026/27    |     71 | (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B - Region 3)               |            100 | Region 5               | Region 3              | conflict                     |   0.0 |
| 2026/27    |     71 | (710026C) Replacement Of Critical Worn-Out Water Network Pipes (Area C - Region 4,5,6&7)         |            100 | Region 5               | Multiple regions      | column says Multiple regions |   0.0 |

The pipe-programme conflicts are internal to the City's documents. The 2025/26 MTREF titles Area A "Region 1-2", but its Regions column says "Region 5" (p69); Areas B and C are titled with regions but tagged "Tshwane Wide". The carried Appendix O wards (96 in Region 2, 53 in Region 3, 100 in Region 5) each lie inside the titled regions, but each places a region-wide programme in a single ward. Under the location basis these rows are already treated as region-only by the title rule (§8.3).

Sensitivity — where the column disagrees (including Tshwane Wide), use the Regions column instead of the carried ward:

| Budget                                                      | Treatment                                                   |   Black-ward share Loc (b) |   R/resident ratio |   Ward-attributed % |
|:------------------------------------------------------------|:------------------------------------------------------------|---------------------------:|-------------------:|--------------------:|
| 2025/26 original                                            | carried ward kept (primary)                                 |                       69.4 |                0.7 |                72.1 |
| 2025/26 original                                            | Regions column used where it disagrees (incl. Tshwane Wide) |                       69.8 |                0.8 |                65.7 |
| 2025/26 adjusted                                            | carried ward kept (primary)                                 |                       63.5 |                0.6 |                55.5 |
| 2025/26 adjusted                                            | Regions column used where it disagrees (incl. Tshwane Wide) |                       63.4 |                0.6 |                47.0 |
| 2026/27 original (Mayco draft, reconciles to adopted SDBIP) | carried ward kept (primary)                                 |                       72.1 |                0.8 |                59.8 |
| 2026/27 original (Mayco draft, reconciles to adopted SDBIP) | Regions column used where it disagrees (incl. Tshwane Wide) |                       71.7 |                0.8 |                58.9 |

#### 9.5 Headline: Black-ward share of ward-attributed capex, ≥80% definition

- **Loc** = physical location; **Svc** = stated service area for bulk infrastructure (§8.2 statements, applied to the same projects in later years).
- **(a)** leaves region-only money unattributed; **(b)** splits it across the region's wards by population. The equal-benefit assumption in (b) is an assumption, not something the documents state.
- The per-resident ratio is rand per resident in Black wards ÷ rand per resident in other wards.

| Budget / spend                                              | Adopted by                                                                                     |   Loc (a) |   Loc (b) |   Svc (a) |   Svc (b) |   R/resident ratio Loc (b) |   R/resident ratio Svc (b) |   Ward-attributed % Loc (b) |   Ward-attributed % Svc (b) |
|:------------------------------------------------------------|:-----------------------------------------------------------------------------------------------|----------:|----------:|----------:|----------:|---------------------------:|---------------------------:|----------------------------:|----------------------------:|
| 2022/23 original budget                                     | pre-Brink (MTREF approved 26 May 2022)                                                         |      72.7 |      73.1 |      84.1 |      84.4 |                        0.9 |                        1.8 |                        63.3 |                        47.4 |
| 2022/23 adjusted budget                                     | pre-Brink (adjustments budget prepared before 2–3 Mar 2023)                                    |      77.5 |      77.4 |      83.1 |      84.2 |                        1.1 |                        1.7 |                        58.9 |                        48.2 |
| 2023/24 original budget                                     | Brink (MTREF approved 31 May 2023)                                                             |      59.3 |      61.5 |      86.4 |      83.0 |                        0.5 |                        1.6 |                        61.2 |                        48.5 |
| 2023/24 adjusted budget                                     | Brink (adjustments budget, early 2024)                                                         |      58.4 |      59.2 |      86.8 |      83.6 |                        0.5 |                        1.7 |                        58.5 |                        48.3 |
| 2024/25 original budget                                     | Brink (MTREF tabled May 2024)                                                                  |      56.2 |      57.1 |      77.1 |      76.2 |                        0.4 |                        1.0 |                        58.7 |                        41.0 |
| 2024/25 adjusted (adj. budget)                              | Moya-era Council (adjustments budget after Oct 2024; adoption date not stated in the document) |      52.4 |      53.7 |      72.5 |      72.4 |                        0.4 |                        0.9 |                        54.1 |                        37.6 |
| 2025/26 original                                            | Moya-era Council (MTREF, Special Council 29 May 2025 per file title)                           |      69.7 |      69.4 |      81.2 |      79.1 |                        0.7 |                        1.2 |                        72.1 |                        53.0 |
| 2025/26 adjusted                                            | Moya-era Council (2025/26 adjustments budget; adoption date not stated)                        |      62.8 |      63.5 |      79.1 |      75.9 |                        0.6 |                        1.0 |                        55.5 |                        43.1 |
| 2026/27 original (Mayco draft, reconciles to adopted SDBIP) | Moya-era; document is the version for the Mayoral Committee of 21 May 2026 (p65)               |      72.2 |      72.1 |      81.6 |      79.6 |                        0.8 |                        1.3 |                        59.8 |                        42.3 |
| 2024/25 adjusted budget                                     | App N adjusted (final, incl. later amendments) — Moya-era                                      |      60.4 |      60.3 |      75.5 |      75.1 |                        0.5 |                        1.0 |                        58.2 |                        39.4 |
| 2024/25 actual spend                                        | spent Jul 2024–Jun 2025 (≈3 months Brink, 9 months Moya)                                       |      60.0 |      60.0 |      75.3 |      74.9 |                        0.5 |                        1.0 |                        57.6 |                        38.4 |

The two App N rows at the bottom are the final 2024/25 adjusted budget and actual spend (§3), shown for reference.

#### 9.6 Robustness: Option B (region level for every year)

Option B uses only region tags, for every year: SA36/SB19 for 2022/23–2024/25, the SA36 tag of the same-named MTREF row for Appendix N, and the Regions column from 2025/26. Each region's money is split across its wards by population. No ward-level information is used.

| Budget / spend                                              |   Region-tagged % of budget |   Black-ward share (pop. split) |   R/resident ratio |
|:------------------------------------------------------------|----------------------------:|--------------------------------:|-------------------:|
| 2022/23 original budget                                     |                        66.1 |                            75.1 |                1.0 |
| 2022/23 adjusted budget                                     |                        53.1 |                            78.0 |                1.2 |
| 2023/24 original budget                                     |                        67.4 |                            75.5 |                1.0 |
| 2023/24 adjusted budget                                     |                        61.5 |                            74.8 |                1.0 |
| 2024/25 original budget                                     |                        64.1 |                            73.0 |                0.9 |
| 2024/25 adjusted (adj. budget)                              |                        60.1 |                            74.7 |                1.0 |
| 2025/26 original                                            |                        71.0 |                            76.9 |                1.1 |
| 2025/26 adjusted                                            |                        53.0 |                            76.4 |                1.1 |
| 2026/27 original (Mayco draft, reconciles to adopted SDBIP) |                        61.6 |                            76.3 |                1.1 |
| 2024/25 adjusted budget                                     |                        47.5 |                            76.6 |                1.1 |
| 2024/25 actual spend                                        |                        48.1 |                            77.1 |                1.1 |

Year-to-year changes, Option A (location, (b)) vs Option B:

| Step                                                                           |   Option A Δ (pts) |   Option B Δ (pts) | Same direction?   | Size     |
|:-------------------------------------------------------------------------------|-------------------:|-------------------:|:------------------|:---------|
| 2022/23 original budget → 2022/23 adjusted budget                              |               +4.4 |               +2.9 | yes               | similar  |
| 2022/23 adjusted budget → 2023/24 original budget                              |              -15.9 |               -2.5 | yes               | A larger |
| 2023/24 original budget → 2023/24 adjusted budget                              |               -2.4 |               -0.7 | yes               | similar  |
| 2023/24 adjusted budget → 2024/25 original budget                              |               -2.1 |               -1.8 | yes               | similar  |
| 2024/25 original budget → 2024/25 adjusted (adj. budget)                       |               -3.4 |               +1.7 | NO                | similar  |
| 2024/25 adjusted (adj. budget) → 2025/26 original                              |              +15.7 |               +2.2 | yes               | A larger |
| 2025/26 original → 2025/26 adjusted                                            |               -5.9 |               -0.5 | yes               | A larger |
| 2025/26 adjusted → 2026/27 original (Mayco draft, reconciles to adopted SDBIP) |               +8.7 |               -0.0 | NO                | A larger |

**Agreement.** The two agree on direction in 6 of 8 steps. Option B moves much less: its series stays between 73.0% and 78.0%, with no step larger than ±2.9 points, while Option A moves up to ±15.9. Option B is coarse by construction: a region mixes Black and other wards, and splitting by population pulls every year towards the region average. So the large Option A swings depend on ward-level attribution. Where B moves the same way, the direction is confirmed; the size is not.

#### 9.7 What drove each step (excluding bulk infrastructure, location basis, (a))

Same method as §7. Projects are linked across steps; each project's change is split into its own budget change and relabelling (attribution moving between groups).

| Step                                |   Black share before |   after |   after, budget effects only |   Black ward R m Δ |   …budget |   …relabelling |   Other ward R m Δ |   …budget  |   …relabelling  |   Top-5 share of moves against Black wards % |   Top-5 share of moves toward Black wards % |
|:------------------------------------|---------------------:|--------:|-----------------------------:|-------------------:|----------:|---------------:|-------------------:|-----------:|----------------:|---------------------------------------------:|--------------------------------------------:|
| 2024/25 original → 2024/25 adjusted |                 70.0 |    63.4 |                         63.5 |              -61.7 |     -60.4 |           -1.3 |               25.5 |       25.5 |             0.0 |                                         47.6 |                                        95.8 |
| 2024/25 adjusted → 2025/26 original |                 63.4 |    77.2 |                         74.8 |              279.7 |     267.0 |           12.7 |              -16.2 |        5.7 |           -21.9 |                                         68.9 |                                        29.6 |
| 2025/26 original → 2025/26 adjusted |                 77.2 |    73.0 |                         73.0 |             -136.8 |    -136.8 |            0.0 |               -3.4 |       -3.4 |             0.0 |                                         50.7 |                                        95.6 |
| 2025/26 adjusted → 2026/27 original |                 73.0 |    77.5 |                         77.5 |               28.3 |      28.3 |            0.0 |              -31.2 |      -31.2 |             0.0 |                                         56.1 |                                        49.3 |

How to read the relabelling columns:
- **From 2025/26 on, relabelling is zero by construction.** Carried-forward wards are copied from the same earlier Appendix O, so a continuing project can't change ward between Moya-era budgets. Only real budget changes show up there.
- **The 2024/25 adjusted → 2025/26 original step also changes coverage.** Same-year Appendix O matching (2024/25) gives way to carry-forward, which draws on two years of Appendix O. Ward-attributed coverage (location, (b)) rises from 54.1% to 72.1%, so part of that step's movement is projects entering the attributable pool.

**2024/25 original → 2024/25 adjusted**

Largest moves *against* Black wards (Black ↓ or other ↑):

| Project                                             | Ward      | Group         |   Before (R m) |   After (R m) |   Impact (R m) |   …of which relabelling |
|:----------------------------------------------------|:----------|:--------------|---------------:|--------------:|---------------:|------------------------:|
| Sewer provision - Rama City                         | 32 → 32   | Black → Black |           37.9 |          12.4 |           25.5 |                     0.0 |
| New Clinic Lusaka                                   | 10 → 10   | Black → Black |           17.5 |           0.5 |           17.0 |                     0.0 |
| Pretorious Park: sewer provision                    | 91 → 91   | Other → Other |            0.7 |          15.0 |           14.4 |                     0.0 |
| Denneboom Depot                                     | 38 → 38   | Black → Black |           16.5 |           2.5 |           14.0 |                     0.0 |
| Upgrading of roads and stormwater systems in Rayton | 100 → 100 | Black → Black |           13.0 |           1.0 |           12.0 |                     0.0 |
| Flooding Backlogs: Stinkwater & New Eersterust Area | 14 → 14   | Black → Black |           15.0 |           3.0 |           12.0 |                     0.0 |
| Contributions Roads - Garsfontein Road              | 45 → 45   | Other → Other |            9.5 |          21.4 |           12.0 |                     0.0 |
| Denneboom Intermodal facility                       | 28 → 28   | Black → Black |           20.0 |          10.0 |           10.0 |                     0.0 |

Largest moves *toward* Black wards:

| Project                                                           | Ward      | Group         |   Before (R m) |   After (R m) |   Impact (R m) |   …of which relabelling |
|:------------------------------------------------------------------|:----------|:--------------|---------------:|--------------:|---------------:|------------------------:|
| Turnaround of Municipal Water Service - Reduction of Water losses | 58 → 58   | Black → Black |           20.0 |          50.0 |           30.0 |                     0.0 |
| Electricity for All - Region 1                                    | 32 → 32   | Black → Black |           20.0 |          36.0 |           16.0 |                     0.0 |
| Electricity for All - Region 5                                    | 99 → 99   | Black → Black |           20.0 |          36.0 |           16.0 |                     0.0 |
| Electricity for All - Region 6                                    | 101 → 101 | Other → Other |           20.0 |           4.0 |           16.0 |                     0.0 |
| Acquisition and Refurbishment of Midtown Building                 | 81 → 81   | Black → Black |           13.1 |          18.1 |            5.0 |                     0.0 |
| Mabopane Ext 12 Sewer reticulation                                | 22 → 22   | Black → Black |            1.0 |           3.0 |            2.0 |                     0.0 |
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)            | 82 → 82   | Other → Other |           38.6 |          37.5 |            1.1 |                     0.0 |
| Sewer reticulation -Gatsebe                                       | 22 → 22   | Black → Black |            0.7 |           1.0 |            0.3 |                     0.0 |

**2024/25 adjusted → 2025/26 original**

Largest moves *against* Black wards (Black ↓ or other ↑):

| Project                                             | Ward      | Group         |   Before (R m) |   After (R m) |   Impact (R m) |   …of which relabelling |
|:----------------------------------------------------|:----------|:--------------|---------------:|--------------:|---------------:|------------------------:|
| Ekangala Block A - F sewer reticulation and toilets | 104 → 104 | Black → Black |           32.4 |           3.0 |           29.4 |                     0.0 |
| Electricity for All - Region 5                      | 99 → 99   | Black → Black |           36.0 |          14.6 |           21.4 |                     0.0 |
| Electricity for All - Region 1                      | 32 → 32   | Black → Black |           36.0 |          15.6 |           20.4 |                     0.0 |
| Acquisition and Refurbishment of Midtown Building   | 81 → –    | Black → –     |           18.1 |           0.0 |           18.1 |                     0.0 |
| Contributions Roads - Garsfontein Road              | 45 → 45   | Other → Other |           21.4 |          35.0 |           13.6 |                     0.0 |
| Sewer reticulation - Booysens X4                    | 55 → 55   | Other → Other |            2.0 |          12.0 |           10.0 |                     0.0 |
| Electricity for All - Region 6                      | 101 → 101 | Other → Other |            4.0 |          13.5 |            9.5 |                     0.0 |
| Electricity for All - Region 7                      | 105 → 105 | Black → Black |           20.0 |          15.3 |            4.7 |                     0.0 |

Largest moves *toward* Black wards:

| Project                                                                | Ward     | Group                   |   Before (R m) |   After (R m) |   Impact (R m) |   …of which relabelling |
|:-----------------------------------------------------------------------|:---------|:------------------------|---------------:|--------------:|---------------:|------------------------:|
| Construction of roads & stormwater - Olievenhoutbosch X60              | – → 77   | – → Black               |            0.0 |          39.5 |           39.5 |                     0.0 |
| Denneboom Intermodal facility                                          | 28 → 28  | Black → Black           |           10.0 |          38.5 |           28.5 |                     0.0 |
| (710026B) Replacement Of Critical Worn-Out Water Network Pipes (Area B | 53 → 100 | Other → not single-ward |           22.1 |          21.9 |           22.1 |                    21.9 |
| Construction of roads & stormwater - Soshanguve South X12              | 37 → 37  | Black → Black           |            1.7 |          23.2 |           21.5 |                     0.0 |
| Soshanguve Block WW                                                    | – → 36   | not single-ward → Black |            5.0 |          20.0 |           20.0 |                     5.0 |
| Temba and Hammanskraal - Upgrading of Existing Gravel Road             | 74 → 74  | Black → Black           |            1.7 |          20.0 |           18.3 |                     0.0 |
| Sewer provision - Rama City                                            | 32 → 32  | Black → Black           |           12.4 |          30.6 |           18.2 |                     0.0 |
| New Clinic Lusaka                                                      | 10 → 10  | Black → Black           |            0.5 |          18.0 |           17.5 |                     0.0 |

**2025/26 original → 2025/26 adjusted**

Largest moves *against* Black wards (Black ↓ or other ↑):

| Project                                                   | Ward      | Group         |   Before (R m) |   After (R m) |   Impact (R m) |   …of which relabelling |
|:----------------------------------------------------------|:----------|:--------------|---------------:|--------------:|---------------:|------------------------:|
| Construction of roads & stormwater - Olievenhoutbosch X60 | 77 → 77   | Black → Black |           39.5 |           4.0 |           35.5 |                     0.0 |
| Construction of roads & stormwater - Soshanguve South X12 | 37 → 37   | Black → Black |           23.2 |           6.2 |           17.0 |                     0.0 |
| Region 3 (Public Lighting)                                | 55 → 55   | Other → Other |            4.0 |          19.1 |           15.1 |                     0.0 |
| Upgrading of Road from gravel to tar in Ekangala Ward 105 | 105 → 105 | Black → Black |           15.0 |           0.0 |           15.0 |                     0.0 |
| and Flooding 5 backlog: Ramotse (Network 1A, 1C & 1F)     | 73 → 73   | Black → Black |           22.5 |           7.5 |           15.0 |                     0.0 |
| Internal Roads Mabopane Block R (Phase 2)                 | 22 → 22   | Black → Black |           15.0 |           0.0 |           15.0 |                     0.0 |
| Denneboom Intermodal facility                             | 28 → 28   | Black → Black |           38.5 |          25.5 |           13.0 |                     0.0 |
| Upgrading of roads and stormwater systems in Refilwe      | 99 → 99   | Black → Black |           23.0 |          10.0 |           13.0 |                     0.0 |

Largest moves *toward* Black wards:

| Project                                                           | Ward    | Group         |   Before (R m) |   After (R m) |   Impact (R m) |   …of which relabelling |
|:------------------------------------------------------------------|:--------|:--------------|---------------:|--------------:|---------------:|------------------------:|
| Water reticulation - Andeon X37                                   | 55 → –  | Other → –     |           20.8 |           0.0 |           20.8 |                     0.0 |
| Turnaround of Municipal Water Service - Reduction of Water losses | 58 → 58 | Black → Black |           50.0 |          65.3 |           15.3 |                     0.0 |
| Sewer reticulation - Booysens X4                                  | 55 → 55 | Other → Other |           12.0 |           0.0 |           12.0 |                     0.0 |
| Upgrade Refilwe Stadium                                           | 99 → 99 | Black → Black |           16.0 |          22.2 |            6.2 |                     0.0 |
| Acquisition and Refurbishment of Midtown Building                 | – → 81  | – → Black     |            0.0 |           2.3 |            2.3 |                     0.0 |
| Water reticulation - Booysens X4                                  | 55 → –  | Other → –     |            2.0 |           0.0 |            2.0 |                     0.0 |
| Townlands Project - Construction of 1,200 social housing units    | – → 81  | – → Black     |            0.0 |           0.6 |            0.6 |                     0.0 |

**2025/26 adjusted → 2026/27 original**

Largest moves *against* Black wards (Black ↓ or other ↑):

| Project                                                                | Ward    | Group         |   Before (R m) |   After (R m) |   Impact (R m) |   …of which relabelling |
|:-----------------------------------------------------------------------|:--------|:--------------|---------------:|--------------:|---------------:|------------------------:|
| Turnaround of Municipal Water Service - Reduction of Water losses      | 58 → 58 | Black → Black |           65.3 |          20.0 |           45.3 |                     0.0 |
| Water reticulation - Andeon X37                                        | – → 55  | – → Other     |            0.0 |          36.5 |           36.5 |                     0.0 |
| Sewer provision - Rama City                                            | 32 → 32 | Black → Black |           30.6 |           5.9 |           24.7 |                     0.0 |
| Replacement of obsolete of meter test bench ( Electricity Distribution | 29 → –  | Black → –     |           20.0 |           0.0 |           20.0 |                     0.0 |
| Upgrade Refilwe Stadium                                                | 99 → 99 | Black → Black |           22.2 |           4.0 |           18.2 |                     0.0 |
| Stormwater Drainage Mahube Valley                                      | 17 → –  | Black → –     |           15.0 |           0.0 |           15.0 |                     0.0 |
| Water reticulation - Booysens X4                                       | – → 55  | – → Other     |            0.0 |           9.7 |            9.7 |                     0.0 |
| Sewer reticulation - Booysens X4                                       | 55 → 55 | Other → Other |            0.0 |           9.0 |            9.0 |                     0.0 |

Largest moves *toward* Black wards:

| Project                                                        | Ward    | Group                         |   Before (R m) |   After (R m) |   Impact (R m) |   …of which relabelling |
|:---------------------------------------------------------------|:--------|:------------------------------|---------------:|--------------:|---------------:|------------------------:|
| Construction of roads & stormwater - Olievenhoutbosch X60      | 77 → 77 | Black → Black                 |            4.0 |          50.3 |           46.3 |                     0.0 |
| Temba and Hammanskraal - Upgrading of Existing Gravel Road     | 74 → 74 | Black/not single-ward → Black |           20.6 |          49.3 |           29.3 |                     0.0 |
| Line 2B: Atterbury Rd (btw Lynnwood Rd to Lois Avenue)         | 82 → –  | Other → –                     |           27.5 |           0.0 |           27.5 |                     0.0 |
| (804000) - 16 Contributions Roads - Garsfontein Road           | 45 → 45 | Other → Other                 |           43.2 |          15.7 |           27.4 |                     0.0 |
| Construction of roads & stormwater - Soshanguve South X12      | 37 → 37 | Black → Black                 |            6.2 |          32.3 |           26.0 |                     0.0 |
| Wonderboom Intermodal Facility (Building Works)                | 3 → –   | Other → –                     |           20.4 |           0.0 |           20.4 |                     0.0 |
| Water reticulation - Mamelodi X6 erf 34041 (Phomolong) Phase 2 | 40 → 40 | Black → Black                 |            3.0 |          19.0 |           16.0 |                     0.0 |
| Region 3 (Public Lighting)                                     | 55 → 55 | Other → Other                 |           19.1 |           4.0 |           15.1 |                     0.0 |


#### 9.8 Were the 2024/25 cuts restored?

Traced by WBS programme code, with name as a fallback:

| Project                                                                     | Budget / spend                                              |   R m | Listed?    | Source                                                                         |
|:----------------------------------------------------------------------------|:------------------------------------------------------------|------:|:-----------|:-------------------------------------------------------------------------------|
| Thorntree View roads & stormwater                                           | 2023/24 original                                            |  90.2 | yes        | 12.-Proposed-2023-2024-Adjustments-Budget.pdf p133                             |
| Thorntree View roads & stormwater                                           | 2023/24 adjusted                                            |  84.2 | yes        | 12.-Proposed-2023-2024-Adjustments-Budget.pdf p133                             |
| Thorntree View roads & stormwater                                           | 2024/25 original (Brink)                                    |   1   | yes        | 02.-2024-2025-MTREF-for-the-City-of-Tshwane.pdf p59                            |
| Thorntree View roads & stormwater                                           | 2024/25 adjusted (adj. budget)                              |  18.6 | yes        | 07.-Proposed-2024-2025-Adjustment-Budget.pdf p136                              |
| Thorntree View roads & stormwater                                           | 2024/25 adjusted (App N, final)                             |  24.5 | yes        | 22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.pdf p510          |
| Thorntree View roads & stormwater                                           | 2024/25 actual (App N)                                      |  24.5 | yes        | 22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.pdf p510          |
| Thorntree View roads & stormwater                                           | 2025/26 original                                            |   0   | not listed |                                                                                |
| Thorntree View roads & stormwater                                           | 2025/26 adjusted                                            |   0   | not listed |                                                                                |
| Thorntree View roads & stormwater                                           | 2026/27 original (Mayco draft, reconciles to adopted SDBIP) |   0   | yes        | 02.-2026-2027-MTREF-for-CoT-Final-1.pdf p68                                    |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2023/24 original                                            |  68   | yes        | 12.-Proposed-2023-2024-Adjustments-Budget.pdf p137                             |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2023/24 adjusted                                            |  30   | yes        | 12.-Proposed-2023-2024-Adjustments-Budget.pdf p137                             |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2024/25 original (Brink)                                    |  20   | yes        | 02.-2024-2025-MTREF-for-the-City-of-Tshwane.pdf p64                            |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2024/25 adjusted (adj. budget)                              |  20   | yes        | 07.-Proposed-2024-2025-Adjustment-Budget.pdf p138                              |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2024/25 adjusted (App N, final)                             |  20   | yes        | 22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.pdf p509          |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2024/25 actual (App N)                                      |  21.2 | yes        | 22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.pdf p509          |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2025/26 original                                            |  20   | yes        | 02.-2025-2026-MTREF-for-the-City-of-Tshwane-Special-Council-29-05-2025.pdf p68 |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2025/26 adjusted                                            |  47   | yes        | 10.-2025-2026-Adjustment-Budget.pdf p149                                       |
| Electricity Distribution Loss (IDP 714008; programme 9.801645 from 2024/25) | 2026/27 original (Mayco draft, reconciles to adopted SDBIP) |  20   | yes        | 02.-2026-2027-MTREF-for-CoT-Final-1.pdf p70                                    |
| Zithobeni X8 sewer provision                                                | 2023/24 original                                            |  30.6 | yes        | 12.-Proposed-2023-2024-Adjustments-Budget.pdf p133                             |
| Zithobeni X8 sewer provision                                                | 2023/24 adjusted                                            |  30.6 | yes        | 12.-Proposed-2023-2024-Adjustments-Budget.pdf p133                             |
| Zithobeni X8 sewer provision                                                | 2024/25 original (Brink)                                    |   0   | not listed |                                                                                |
| Zithobeni X8 sewer provision                                                | 2024/25 adjusted (adj. budget)                              |   0   | not listed |                                                                                |
| Zithobeni X8 sewer provision                                                | 2024/25 adjusted (App N, final)                             |   0   | not listed |                                                                                |
| Zithobeni X8 sewer provision                                                | 2024/25 actual (App N)                                      |   0   | not listed |                                                                                |
| Zithobeni X8 sewer provision                                                | 2025/26 original                                            |   0   | not listed |                                                                                |
| Zithobeni X8 sewer provision                                                | 2025/26 adjusted                                            |   0   | not listed |                                                                                |
| Zithobeni X8 sewer provision                                                | 2026/27 original (Mayco draft, reconciles to adopted SDBIP) |   0   | not listed |                                                                                |
| Timberlands social housing                                                  | 2023/24 original                                            |  26   | yes        | 12.-Proposed-2023-2024-Adjustments-Budget.pdf p134                             |
| Timberlands social housing                                                  | 2023/24 adjusted                                            |   5   | yes        | 12.-Proposed-2023-2024-Adjustments-Budget.pdf p134                             |
| Timberlands social housing                                                  | 2024/25 original (Brink)                                    |   0   | not listed |                                                                                |
| Timberlands social housing                                                  | 2024/25 adjusted (adj. budget)                              |   0   | not listed |                                                                                |
| Timberlands social housing                                                  | 2024/25 adjusted (App N, final)                             |   0   | not listed |                                                                                |
| Timberlands social housing                                                  | 2024/25 actual (App N)                                      |   0   | not listed |                                                                                |
| Timberlands social housing                                                  | 2025/26 original                                            |   0   | yes        | 02.-2025-2026-MTREF-for-the-City-of-Tshwane-Special-Council-29-05-2025.pdf p65 |
| Timberlands social housing                                                  | 2025/26 adjusted                                            |   0   | yes        | 10.-2025-2026-Adjustment-Budget.pdf p146                                       |
| Timberlands social housing                                                  | 2026/27 original (Mayco draft, reconciles to adopted SDBIP) |   0   | not listed |                                                                                |

**Findings:**
- **Thorntree View roads & stormwater (ward 36): not restored in the budgets.**
  - 2024/25 under Moya: R18.6m in the adjustment budget (p136); App N records R24.5m adjusted and actual.
  - 2025/26: not listed in the MTREF or the adjustment budget.
  - 2026/27: listed at R0 (p68).
  - **No document says the project was completed.** AR 2022/23 p179 reports progress ("Thorntree view project achieved a total of 15.8km"). AR 2023/24 p432 attributes under-expenditure on it to "underperformance by the contractor". AR 2024/25 p464 lists "Phase 2 – Construction of bulk stormwater channel – Thorntree View (Soshanguve South Extension 7)", ward 36, as not complete.
  - The 2025/26 MTREF procurement plan (p1727) schedules "Appointment of a Contractor for the Completion and remedial works of 2.2 KM stormwater channel at Thorntreeview" at R14,000,000 (MIG), with consultant (R2m) and health-and-safety (R1m) appointments (p1739). That work is not identifiable by name in the 2025/26 or 2026/27 capital annexures.
- **Electricity Distribution Loss (ward 29): held at R20m, partly restored in 2025/26 adjusted.**
  - R20m in the 2024/25 adjusted, 2025/26 original and 2026/27 original budgets.
  - The 2025/26 adjustment added **R27m** "from Urban Development Financing Grant" (adj. budget p62), for **R47m** in total (p149). Still below the R68m of 2023/24.
  - From 2024/25 the programme is re-coded as 9.801645, with "Revenue Enhancement" sub-items.
- **Zithobeni X8 sewer provision (ward 105): not restored.** It hasn't been listed in any budget since 2023/24, which cites contractor underperformance (AR 2023/24 p432). Zithobeni X8&9 bulk water main and roads lines do continue, and the 2025/26 adjustment added R4.4m for "Zithobeni x8 &9" (p61). These are separate projects.
- **Timberlands social housing (ward 81): not restored.** It's listed at a token R1,000 in the 2025/26 original and adjusted budgets (MTREF p65; adj. p146), against an estimated total project cost of R394,550,000 (MTREF p65). Not listed in 2026/27.
- **Correction to §7:** that section said Timberlands was "budgeted R0 in 2024/25". The 2024/25 MTREF has no Timberlands line at all; the R0 came from a code collision with the overprinted Sunnyside/Townlands row. The conclusion (dropped) is unchanged.

#### 9.9 Reading

**Location basis, (b):**

| Step | Black-ward share | R/resident ratio |
|---|---|---|
| 2024/25 adjusted (Moya's first adjustment) | 53.7% | 0.38 |
| 2025/26 original | 69.4% | 0.74 |
| 2025/26 adjusted | 63.5% | 0.57 |
| 2026/27 original | 72.1% | 0.84 |

- **Comparison with earlier budgets.** The 2025/26 and 2026/27 originals are above every Brink-era budget (2023/24 original 61.5%, 2024/25 original 57.1%). They are below the 2022/23 adjusted budget (77.4%), and the 2026/27 original is below the 2022/23 original (73.1%).
- **Service-area basis** gives the same up-down pattern at a higher level: 72.4% → 79.1% → 75.9% → 79.6%.
- **Per resident:** Black wards still receive less than other wards in every Moya-era budget on the location basis (ratio 0.4–0.8). On the service-area basis the ratio is 0.9–1.3.
- **The 2024/25 dip comes first.** The low point is Moya's first adjustment. Its biggest adverse moves (excluding bulk) are cuts or deferrals in Black wards plus increases in other wards: Sewer provision - Rama City (ward 32, −R25.5m); New Clinic Lusaka (ward 10, −R17.0m); Pretorious Park: sewer provision (ward 91, +R14.4m); Denneboom Depot (ward 38, −R14.0m); Upgrading of roads and stormwater systems in Rayton (ward 100, −R12.0m); Flooding Backlogs: Stinkwater & New Eersterust Area (ward 14, −R12.0m).
- **Within years, adjustments cut Black-ward shares.** Both Moya-era adjustment budgets lower the Black-ward share relative to that year's original (57.1% → 53.7%; 69.4% → 63.5%). So the in-year pattern ActionSA described for Brink also appears under Moya.
- **Caveats that limit these comparisons:**
  1. From 2025/26 the wards are carried forward, not stated in the documents.
  2. New projects can only be placed by region (region-only share up to 18% in 2026/27).
  3. There is no Moya-era actual spend below citywide level.
  4. Option B, which uses no ward information, is nearly flat. The larger ward-level swings rest on the City's own ward attributions.

