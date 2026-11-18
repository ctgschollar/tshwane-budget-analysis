import csv, sys

AR22 = "City-of-Tshwane-Audited-Annual-Report-for-2022_23-FY.txt"
AR23 = "13.-The-Consolidated-Annual-Report-for-the-City-of-Tshwane_2023_24.txt"
AR24 = "22.-The-Consolidated-Audited-Annual-Report-for-CoT-2024-2025.txt"
MT23 = "02.-2023-2024-MTREF-for-the-City-of-Tshwane.txt"

RW = "Rooiwal WWTW Phase 1: Upgrading of Existing Infrastructure"
RW_N = "Same project also listed as 'Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture' (typo variant)."
KG = "Klipgat WWTW: Upgrading of existing infrastructure to 40Ml/d"
KG_N = "Same project also listed as 'Klipgat WWTW: Upgrading of existing infrastrature to 40Ml/d'."
SR = "Sunderland Ridge WWTW Phase1: Upgrade of existing infrastructure"
SR_N = "Variants: 'Sunderland Ridge WWTW Phase1: Upgrade of existing' and '...infrastructure Bavia' (truncated/merged name)."
PK = "New Parkmore LL Reservoir and HL Reservoir"
BB = "Bronkhorstbaai: Refurbishment and upgrade of Water Purification Plant"
M11 = "Mamelodi Ext 11 water (Bulk and reticulation) and sanitation services"
M11_N = "Variants: '...sanitation services ' (trailing space) and '...sanitation Nelmapius'."

rows = []
def r(p, t, areas, kind, quote, f, pg, conf, notes=""):
    assert len(quote) <= 350, (p, len(quote))
    rows.append(dict(project_name=p, statement_type=t, beneficiary_areas=areas, area_kind=kind,
                     quote=quote, source_file=f, pdf_page=pg, confidence=conf, notes=notes))

# ---- Rooiwal Phase 1
r(RW,"narrative","Temba; Hammanskraal; Marokolong; Region 2","township/suburb",
  "Rooiwal Wastewater Treatment Works (WWTW) Upgrade: ... A total of R450,500,000.00 was allocated to this project and as at 30 June 2023, the progress was at 68% and once completed, it will benefit the communities of Temba, Hammanskraal and Marokolong in Region 2.",
  AR22,77,"high",RW_N+" R450.5m matches Phase 1 allocation.")
r(RW,"narrative","Temba; Hammanskraal; Marokolong; Region 2","township/suburb",
  "A total of R450,500,000.00 was allocated for Phase 1 project on the 2023/24 Medium Term Revenue and Expenditure Framework (MTREF). ... As at 30 June 2024, the progress was at 78% progress and once completed, it will benefit the communities of Temba, Hammanskraal and Marokolong in Region 2.",
  AR23,90,"high",RW_N)
r(RW,"narrative","Hammanskraal","township/suburb",
  "The City gave heightened attention to the refurbishment of the Rooiwal Wastewater Treatment Works (WWTW) as part of the efforts to address the Hammanskraal’s water challenges. ... affecting the quality of drinking water in Hammanskraal.",
  AR24,94,"high",RW_N+" Text says 'refurbishment of the Rooiwal WWTW' (phase not named).")
r(RW,"narrative","farmers in the area (unnamed)","other",
  "These upgrades will benefit the farmers in the area, who have long suffered from poor sludge management which severely affected their land.",
  AR24,94,"medium",RW_N+" Beneficiary is a group, area not named.")
r(RW,"narrative","Region 2","region",
  "During the community consultation process, various service delivery issues were raised of which water and sanitation was a concern at Region 2. Following this process funding was reprioritized towards the upgrading of the Rooiwal Wastewater Treatment plant.",
  MT23,2,"medium",RW_N+" Indirect: funding response to a Region 2 concern, not an explicit 'serves' statement.")

# ---- Klipgat
r(KG,"narrative","several wards to the south of Ga-Rankuwa, Mabopane and parts of Winterveldt and Soshanguve; Region 1","township/suburb",
  "The refurbishment of the Klipgat Wastewater Treatment Works: ... As at 30 June 2024, the project was 100% completed and is now servicing the communities of several wards to the south of Ga-Rankuwa, Mabopane and parts of Winterveldt and Soshanguve in Region 1.",
  AR23,91,"high",KG_N+" Phrase is ambiguous: 'wards to the south of' may govern only Ga-Rankuwa or all listed places.")
r(KG,"narrative","several wards to the south of Ga-Rankuwa, Mabopane, Winterveldt and Soshanguve","township/suburb",
  "Refurbishment of the Klipgat Wastewater Treatment Works ... Project was completed at the end of 2024 year and now servicing communities of several wards to the south of Ga-Rankuwa, Mabopane, Winterveldt and Soshanguve.",
  AR24,93,"high",KG_N+" Same ambiguity as 2023/24 wording.")
r(KG,"location","Region 1","region",
  "The refurbishment of the Klipgat Wastewater Treatment Works: Situated in Region 1, the project scope includes the construction of the civil works...",
  AR22,77,"high",KG_N+" Location of the works, not beneficiaries.")
r(KG,"location","Region 1; alongside the Tolwane River","region",
  "The refurbishment of the Klipgat Wastewater Treatment Works: Situated in Region 1 alongside the Tolwane River, the project scope entailed the construction of the civil works...",
  AR23,91,"high",KG_N)

# ---- Sunderland Ridge
r(SR,"narrative","Ward 24 and sorrounding areas; Region 6","ward",
  "Refurbishment of Sunderland Ridge WWTW - Scope of the project entailed: Increased existing infrastructure capacity with a total of 70 Mℓ/d to accomodate the current rate of development. Project was completed at the end of 2024 year and now servicing communities of Ward 24 and sorrounding areas in, Region 6.",
  AR24,93,"high",SR_N+" Verbatim (typos in source). Note: the budget tables' 'Ward Location' column lists this project under Region 4: South / ward 70, so 'Region 6' here may be a drafting error; flag before use.")

# ---- Bronkhorstbaai
r(BB,"narrative","Bronkhorstbaai; Summerplace; Kungwini Country Estate; Ward 102; Region 7","township/suburb",
  "The project will benefit the community of Bronkhorstbaai, Summerplace and Kungwini Country Estate in Ward 102, Region 7.",
  AR22,27,"high","Narrative names 'Refurbishment of Bronkhorstbaai and Summerplace Water Purification Plant'.")
r(BB,"narrative","Bronkhorstbaai; Summerplace; Kungwini Country Estate; Ward 102; Region 7","township/suburb",
  "to be completed at the end of December 2023. The project will benefit the community of Bronkhorstbaai, Summerplace and Kungwini Country Estate in Ward 102, Region 7.",
  AR22,73,"high","Continuation of p72 'Refurbishment of Bronkhorstbaai and Summerplace Water Purification Plant' paragraph.")
r(BB,"narrative","Bronkhorstbaai; Summerplace; Kungwini Country Estate; Ward 107; Region 7; surrounding areas","township/suburb",
  "The project was completed on 03 November 2023 and the plant is operating optimally servicing the communities of Bronkhorstbaai, Summerplace and Kungwini Country Estate in Ward 107, Region 7 and surrounding areas.",
  AR23,83,"high","Ward given as 107 here vs 102 in 2022/23 AR; same wording also on p31-32.")
r(BB,"location","Region 7","region",
  "The Refurbishment of Bronkhorstbaai and Summerplace Water Purification Plant: This intervention is in Region 7.",
  AR22,27,"high","Location statement (also p72).")

# ---- Parkmore
r(PK,"narrative","Parkmore Low Level Reservoir service area; Region 6","region",
  "The scope of the project entails the construction of an additional 10 Mℓ to meet the increased demand in the water supply for the Parkmore Low Level Reservoir service area ... The Parkmore LL system will connect to the Garsfontein system that will service more than 20 000 households in Region 6.",
  AR22,72,"medium","Narrative is about the Parkmore LL reservoir/pipework; the 20 000 households are served by the connected Garsfontein system. HL reservoir not mentioned. Same wording on p27.")
r(PK,"narrative","ward 50; ward 96; Region 6; Parkmore Low Level Reservoir Service Area","ward",
  "The project is about the construction of an additional capacity of 10 Megalitres (Mℓ) to meet the increased demand in the water supply for the Parkmore Low Level Reservoir Service Area ... The Parkmore LL system will connect to the Garsfontein system and will service more than 20 000 households in ward 50 and ward 96 across Region 6.",
  AR23,83,"medium","Same wording on p31. Served via the Garsfontein system. Budget table 'Ward Location' gives wards 44;45.")
r(PK,"narrative","Parkmore Low Level Reservoir Service Area","other",
  "the construction of an additional 10 Mℓ to meet the increased demand in the water supply for the Parkmore Low Level Reservoir Service Area, the installation of the associated pipework. The Parkmore LL system will connect to the Garsfontein system which will service more than 20 000 households.",
  AR24,90,"medium","No named area beyond the reservoir service area (also p35).")
r(PK,"location","Region 6; ward 50; ward 96","ward",
  "New Parkmore LL Reservoir associated pipework: The construction of the new Parkmore LL Reservoir associated pipework in Region 6, with work spanning over ward 50 and ward 96.",
  AR22,72,"high","Where the works run. Repeated in 2023/24 AR p31/p83 and 2024/25 AR p90.")

# ---- Mamelodi Ext 11
r(M11,"narrative","Mamelodi Ext 11; Ward 10; Region 6","township/suburb",
  "Mamelodi Ext 11 - (Ward 10, Region 6): The scope of the project includes the installation of a new sewer and water reticulation network, a bulk supply pipeline and house connections to service a total of 1 859 households.",
  AR23,90,"high",M11_N)
r(M11,"title","Mamelodi Ext 11","township/suburb",
  "Mamelodi Ext 11 water (Bulk and reticulation) and sanitation services",
  AR24,464,"medium",M11_N+" The title names water/sanitation services for Mamelodi Ext 11.")

# ---- Electricity
r("Wildebees 400/132kV, 315MVA Infeed station","narrative","Region 5; Region 6; surrounding areas","region",
  "Wildebeest Infeed Station (Mooiplaats: Region 6) – The project involve construction of new 400/132KV, 250MVA Infeed Station to lessen the bulk capacity constraints in Region 5 and 6 including surrounding areas that are being serviced by the station.",
  AR22,83,"high","Text says 250MVA, budget title says 315MVA.")
r("Wildebees 400/132kV, 315MVA Infeed station","narrative","the city's grid","city-wide",
  "On the Wildebees Infeed Station, construction work has begun. This project will add significant new capacity to the city’s grid",
  AR24,36,"medium","Generic grid-capacity statement.")
r("Wildebees 400/132kV, 315MVA Infeed station","location","Mooiplaats; Region 6","region",
  "Wildebeest Infeed Station (Mooiplaats: Region 6)",
  AR22,83,"high","Location label (also Figure 6 caption p84).")
r("Wapadrand 132/11kV Substation","narrative","surrounding areas that are fed from this substation (unnamed)","other",
  "Wapadrand Substation (Pretoria East: Region 6) – ... This will assist in restoring the substation to strengthen capacity of a total of 105MVA supporting surrounding areas that are fed from this substation.",
  AR22,83,"medium","Beneficiary areas not named.")
r("Wapadrand 132/11kV Substation","narrative","these fast-growing areas (unnamed)","other",
  "Work continues on the Mooikloof, Monavoni, Pyramid and Wapadrand Substations, which will secure long-term supply in these fast-growing areas",
  AR24,36,"medium","Shared statement for 4 substations; areas not named.")
r("Wapadrand 132/11kV Substation","location","Pretoria East; Region 6","region",
  "Wapadrand Substation (Pretoria East: Region 6)",AR22,83,"high","Location label.")
r("Wapadrand 132/11kV Substation","location","Ward 101; Region 6","ward",
  "Wapadrand 132/11kV substation, Ward 101, Region 6",AR24,101,"high","Location label in project status graphic.")
r("Refurbishment of Mooikloof Substation","narrative","the surrounding areas (unnamed)","other",
  "Mooikloof Substation refurbishment (Pretoria East: Region 6) – ... The aim of restoring the substation is to enable a maximum capacity of 105MVA to address the capacity constraints in the surrounding areas.",
  AR22,83,"medium","Beneficiary areas not named.")
r("Refurbishment of Mooikloof Substation","narrative","these fast-growing areas (unnamed)","other",
  "Work continues on the Mooikloof, Monavoni, Pyramid and Wapadrand Substations, which will secure long-term supply in these fast-growing areas",
  AR24,36,"medium","Shared statement for 4 substations.")
r("Refurbishment of Mooikloof Substation","location","Pretoria East; Region 6","region",
  "Mooikloof Substation refurbishment (Pretoria East: Region 6)",AR22,83,"high","Location label.")
r("Refurbishment of Mooikloof Substation","location","Ward 91; Region 6","ward",
  "Construction of Mooikloof 132/11kV substation, Ward 91, Region 6",AR23,97,"high","Location label (multi-column layout).")
r("Refurbishment of Pyramid Sub Station","narrative","these fast-growing areas (unnamed)","other",
  "Work continues on the Mooikloof, Monavoni, Pyramid and Wapadrand Substations, which will secure long-term supply in these fast-growing areas",
  AR24,36,"medium","Shared statement for 4 substations.")
r("Refurbishment of Pyramid Sub Station","location","Rooiwal; Region 2","region",
  "Pyramid Substation refurbishment Project (Rooiwal: Region 2)",AR22,83,"high","Location label.")
r("Refurbishment of Pyramid Sub Station","location","Ward 96; Region 2","ward",
  "Construction of Pyramid 132/11kv Substation, Ward 96,Region 2",AR23,97,"high","Location label (multi-column layout).")
r("Monavoni 132/11KV Substation","narrative","these fast-growing areas (unnamed)","other",
  "Work continues on the Mooikloof, Monavoni, Pyramid and Wapadrand Substations, which will secure long-term supply in these fast-growing areas",
  AR24,36,"medium","Shared statement for 4 substations; the only statement found for Monavoni.")
r("Kentron 132/11kV Substation","location","Rooihuiskraal; Region 4","region",
  "Kentron Substation refurbishment Project (Rooihuiskraal: Region 4)",AR22,83,"high","Location label. No serving statement found.")
r("Kentron 132/11kV Substation","location","Ward 48; Region 4","ward",
  "Kentron 132/11kV substation, Ward 48, Region 4",AR24,101,"high","Location label (also Figure 5 caption p102).")
r("Refurbishment of Rosslyn Sub Station","narrative","the automotive sector and neighboring communities (unnamed)","other",
  "The Rosslyn Substation refurbishment is advancing and will bring relief to the automotive sector and neighboring communities",
  AR24,36,"medium","Beneficiaries are a sector and unnamed neighbouring communities.")
r("Soshanguve - JJ 132KV Power Line","narrative","new developments (unnamed)","other",
  "Upgrading of Soshanguve 132/11kV ... Project scope include the refurbishment of the transformer to increase the capacity of the substation to allow the City to supply new developments with energy needs",
  AR23,97,"medium","Text is about the Soshanguve 132/11kV SUBSTATION, not explicitly the JJ power line project; multi-column layout; beneficiaries unnamed. Use with caution.")
r("Soshanguve - JJ 132KV Power Line","location","Ward 33; Region 1","ward",
  "Upgrading of Soshanguve JJ 132/11kV Substation, Ward 33, Region 1",AR24,101,"high","Location of the JJ substation the line connects to (Figure 6 p102: 'Power Lines from Soshanguve JJ 132KV Substation'); budget ward for the line is 26.")
r("Refurbishment Of Kwagga Infeed Substation","narrative","the municipality (85% of purchased electricity via 3 infeed stations)","city-wide",
  "The municipality purchases 100% of its electricity from ESKOM at transmission and distribution levels, 85% is purchased through the 3 infeed stations (Njala, Kwagga and Reitvel) at 175kV transmission levels and 15% at distribution levels.",
  AR22,539,"medium","About the station's role, not the refurbishment project; also 2023/24 AR p560.")

# ---- Water/other
r("Zithobeni X8&9 - Bulk water main line","table","Zithobeni X8&9","township/suburb",
  "(710863) Zithobeni X8&9 - Bulk water main line | 102 | R 500 000 | Connection to bulk water supply for Zithobeni X8&9 completed.",
  AR22,330,"high","Planned Annual Deliverable column of the SDBIP project table (cells joined with |).")
r("Refurbishment Of Laudium Bulk Pipeline","narrative","Laudium reservoir; Atteridgeville HL reservoir","other",
  "Additionally, a new dual-supply network was introduced for Laudium and Atteridgeville HL reservoirs, where a new 700mm diameter pipeline was installed for Laudium, while the existing 500mm pipeline was reconnected to Atteridgeville HL.",
  AR24,91,"medium","The text does NOT name the budget project 'Refurbishment Of Laudium Bulk Pipeline'; the link to that project is not stated. Beneficiary is a reservoir, not an area. Variant: '...Cathodic protection to all Stee'.")
r("Tshwane Automotive SEZ Phase 1 Bulk Infrastructure Roll out","title","Tshwane Automotive SEZ Phase 1","other",
  "(714048) Tshwane Automotive SEZ Phase 1 Bulk Infrastructure Roll out | 86 | R 113 492 828 | Provision of bulk engineering infrastructure for phase 1 (water, sewer, roads, storm water and electricity)",
  AR22,324,"medium","Title plus deliverable: bulk services for SEZ Phase 1 (the zone itself, no residential area named).")
r("Chantelle detail design and bulk infrastructure upgrade","location","Chantelle ext. 39","township/suburb",
  "Furthermore, commendable progress in the upgrade of bulk infrastructure in Chantelle ext. 39 is also accounted for.",
  AR22,92,"high","Where the works are (social housing project); no serving statement found.")

# ---- Titles with service verb
titles = [
 ("Water provision – Winterveldt 20ML Reservoir","Winterveldt","Also 'Water provision - Winterveldt 20ML Reservoir' (hyphen variant)."),
 ("Water Provision - Winterveldt Bulk water line","Winterveldt",""),
 ("Water provision - Hammanskraal West X10 (Bulk water line)","Hammanskraal West X10",""),
 ("Water provision - Rama City (20 ML Reservoir)","Rama City",""),
 ("Sewer provision - New Eersterust X8 (Tswaing) (Bulk sewer infrastructu","New Eersterust X8 (Tswaing)","maxR 0."),
 ("Sewer provision - Garsfontein - Bulk","Garsfontein","maxR 0."),
 ("Contributions Water- Louwlardia Ext 57 ( Pretoriusrand Reservoir)","Louwlardia Ext 57","Contribution for a township development; full title in 2024/25 AR p513: 'Township Water and Sanitation Services Development: Tshwane Contributions (City Wide) - Louwlardia Ext 57 ( Pretoriusrand Reservoir)'."),
 ("Township Water and Sanitation Services Development: Tshwane Contributi","Louwlardia Ext 57","Truncated name; full title (2024/25 AR p513) ends '- Louwlardia Ext 57 ( Pretoriusrand Reservoir)'. Probably the same project as the Louwlardia row."),
]
for name, area, note in titles:
    r(name,"title",area,"township/suburb",name.strip(),"bulk_projects.csv","","medium" if "Contribut" in name or "Township" in name else "high",
      "Title uses 'provision'/'services' with a named area. "+note)
for name in ["Installation of telemetry, bulk meters and control equipment at reserv",
             "Relining/upgrading reservoirs (City Wide)","Replace reservoir fencing (City Wide)",
             "Waste Water Treatment facilities upgrades Minor Capital Projects (City"]:
    r(name,"title","City Wide","city-wide",name,"bulk_projects.csv","","medium",
      "'(City Wide)' is a scope label, not a service verb. Budget tables mark these 'Whole of the Metro'/'City Wide'.")

covered = {x["project_name"] for x in rows}
variants = {"Rooiwal WWTW Phase 1: Upgrading of Existing Infrastruture","Klipgat WWTW: Upgrading of existing infrastrature to 40Ml/d",
            "Sunderland Ridge WWTW Phase1: Upgrade of existing","Sunderland Ridge WWTW Phase1: Upgrade of existing infrastructure Bavia",
            "Mamelodi Ext 11 water (Bulk and reticulation) and sanitation services ","Mamelodi Ext 11 water (Bulk and reticulation) and sanitation Nelmapius",
            "Water provision - Winterveldt 20ML Reservoir","Refurbishment Of Laudium Bulk Pipeline Cathodic protection to all Stee"}
none_notes = {
 "Bronkhorstspruit Water Purification Plant Refurbishment":"Different project from Bronkhorstbaai (711921F vs 711921E). The narrative about Bronkhorstbaai/Summerplace does not apply. 2024/25 AR p179 mentions maintenance at Bronkhorstspruit plant with no service area.",
 "Bronkhorstspruit and Rietvlei Water Purification Plant Refurbishment":"See Bronkhorstspruit WPP note.",
 "Rooiwal WWTW Phase 2 : 80Ml/d Extensions and Extension of Sludge facil":"Only budget-table rows. The Rooiwal statements refer to Phase 1 / refurbishment.",
 "Temba and Babelegi WWTW upgrade of existing infrastucture":"Only budget/SDBIP tables (ward 74). The Rooiwal narrative's 'Temba' beneficiary is about Rooiwal, not this project.",
 "Temba and Babelegi WWTW upgrade of existing infrastructure":"See typo variant.",
 "Waltloo to Nyala Power Lines":"Only ward-list tables (wards 16;18;23;28;38;43;67). No text says it supplies Mamelodi or any other area.",
 "Network Control Centre Reconfiguration":"SDBIP deliverable is control-room equipment; no area.",
 "Olievenhoutbosch ext 60 bulk water line":"2024/25 AR p31/32/109 lists Olievenhoutbosch ext 60 among areas where stands were connected to water, but does not link this to the bulk line project.",
 "Olievenhoutbosch X60 Bulk Water":"See Olievenhoutbosch ext 60 note.",
 "Bulk Reservoir - Fort West X4&5":"SDBIP (2022/23 AR p330) describes 'bulk water line and 8,5Ml reservoir' with no service area.",
 "Booysens X4 (30ML Reservoir)":"Only SDBIP/budget tables.",
 "Bulk water pipeline - Booysens X4":"Only SDBIP/budget tables.",
 "Refilwe Manor 10ml reservoir":"SDBIP: 'Completion of the Refilwe Manor 10ML reservoir' with no service area.",
 "Chantelle detail design and bulk infrastructure upgrade":"",
}
out=[]
seen=set()
for row in csv.DictReader(open(sys.argv[1])):
    n=row["project_name"]
    if n in seen: continue
    seen.add(n)
    if n in covered or n in variants: continue
    out.append(dict(project_name=n,statement_type="none",beneficiary_areas="",area_kind="",quote="",source_file="",pdf_page="",
                    confidence="",notes=(none_notes.get(n,"") + (" maxR 0.0 in input; checked briefly." if float(row["maxR"])==0 else "")).strip()))
with open(sys.argv[2],"w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows+out)
print(len(rows),"statements;",len(out),"none rows")
