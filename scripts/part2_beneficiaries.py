"""Reviewed beneficiary statements for bulk-infrastructure projects (follow-up 2).
Quotes were verified against the pdftotext pages. kind: township | wards | regions. basis: narrative | title."""
import pandas as pd

AR22 = "City-of-Tshwane-Audited-Annual-Report-for-2022_23-FY.pdf"
AR23 = "13.-The-Consolidated-Annual-Report-for-the-City-of-Tshwane_2023_24.pdf"

ROWS = [
    # project_key (name prefix, matched after normalisation), kind, target, basis, source_file, pdf_page, quote, decision note
    ("Rooiwal WWTW Phase 1", "township", "Temba;Hammanskraal", "narrative", AR22, 77,
     "it will benefit the communities of Temba, Hammanskraal and Marokolong in Region 2",
     "also AR 2023/24 p90 (same words) and AR 2024/25 p94 ('to address the Hammanskraal's water challenges'). "
     "Marokolong is a separate Census Main Place not in the township mapping, so it is not allocated; "
     "'Hammanskraal' = the official Main Place (Rens Town, Kanana)."),
    ("Klipgat WWTW", "regions", "Region 1", "narrative", AR23, 91,
     "now servicing the communities of several wards to the south of Ga-Rankuwa, Mabopane and parts of Winterveldt and Soshanguve in Region 1",
     "wards not named ('several wards to the south of'); attributed at the stated region level. Similar wording AR 2024/25 p93."),
    ("Bronkhorstbaai", "regions", "Region 7", "narrative", AR22, 27,
     "will benefit the community of Bronkhorstbaai, Summerplace and Kungwini Country Estate in Ward 102, Region 7",
     "AR 2023/24 p83 says 'Ward 107, Region 7' for the same communities; ward conflicts, region agrees -> region level."),
    ("New Parkmore LL Reservoir", "regions", "Region 6", "narrative", AR23, 83,
     "will service more than 20 000 households in ward 50 and ward 96 across Region 6",
     "the City's e-GIS region layer places wards 50 and 96 in Region 2; ward/region conflict -> stated region used. "
     "Region 6 also in AR 2022/23 p72."),
    ("Mamelodi Ext 11 water (Bulk and reticulation)", "wards", "10", "narrative", AR23, 90,
     "Mamelodi Ext 11 - (Ward 10, Region 6): ... a bulk supply pipeline and house connections to service a total of 1 859 households",
     "ward 10 is in Region 6 on the e-GIS layer (consistent)."),
    ("Wildebees", "regions", "Region 5;Region 6", "narrative", AR22, 83,
     "Infeed Station to lessen the bulk capacity constraints in Region 5 and 6 including surrounding areas that are being serviced by the station", ""),
    ("Zithobeni X8&9 - Bulk", "township", "Zithobeni", "narrative", AR22, 330,
     "(710863) Zithobeni X8&9 - Bulk ... Connection to bulk water supply for Zithobeni X8&9",
     "project performance table (target text)."),
    # titles with a service verb naming a mapped township (variant only)
    ("Water provision - Winterveldt 20ML Reservoir", "township", "Winterveld", "title", "budget tables / Appendix N", "",
     "Water provision - Winterveldt 20ML Reservoir", "title states service ('Water provision') + area"),
    ("Water provision – Winterveldt 20ML Reservoir", "township", "Winterveld", "title", "budget tables / Appendix N", "",
     "Water provision – Winterveldt 20ML Reservoir", "title states service ('Water provision') + area"),
    ("Water Provision - Winterveldt Bulk water line", "township", "Winterveld", "title", "budget tables / Appendix N", "",
     "Water Provision - Winterveldt Bulk water line", "title states service ('Water provision') + area"),
]
NOT_USED = [
    ("Sunderland Ridge WWTW", "AR 2024/25 p93: 'now servicing communities of Ward 24 and sorrounding areas in, Region 6'",
     "internally inconsistent: ward 24 is Region 1 in every City source; budget tables place the plant in Region 4 / ward 70"),
    ("Water provision - Hammanskraal West X10 (Bulk water line)", "title", "Hammanskraal West X10 is not part of the official Hammanskraal Main Place; no mapping"),
    ("Water provision - Rama City (20 ML Reservoir)", "title", "Rama City not in the township mapping"),
    ("Wapadrand / Mooikloof / Pyramid / Monavoni / Rosslyn / Kwagga / Soshanguve JJ line / Laudium / Tshwane Automotive SEZ",
     "AR text", "beneficiary not named ('surrounding areas', 'these fast-growing areas', 'neighbouring communities') or link to the budget project not stated"),
]

if __name__ == "__main__":
    pd.DataFrame(ROWS, columns=["project_key", "kind", "target", "basis", "source_file", "pdf_page", "quote", "note"]).to_csv(
        "work/bulk_beneficiaries_final.csv", index=False)
    pd.DataFrame(NOT_USED, columns=["project", "statement", "why_not_used"]).to_csv("work/bulk_beneficiaries_not_used.csv", index=False)
    print("written", len(ROWS))
