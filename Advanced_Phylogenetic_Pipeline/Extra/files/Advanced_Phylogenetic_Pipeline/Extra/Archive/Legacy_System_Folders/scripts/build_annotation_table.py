import os
import csv

# ============================================================
# Arabidopsis MIKCc gene → Subclade mapping
# Based on literature (Parenicova et al. 2003, de Folter et al.)
# and the color-coded groupings from your Google Slides
# ============================================================
AT_TO_CLADE = {
    # AP1/FUL/CAL Clade (A-class, floral meristem/organ identity) - RED
    "AT1G69120": ("AP1/FUL/CAL", "A-class", "Floral meristem and organ identity"),
    "AT1G24260": ("AP1/FUL/CAL", "A-class", "Floral meristem and organ identity"),
    "AT5G61850": ("AP1/FUL/CAL", "A-class", "Floral meristem and organ identity"),
    "AT4G36590": ("AP1/FUL/CAL", "A-class", "Floral meristem and organ identity"),  # AGL79
    "AT2G45650": ("AP1/FUL/CAL", "A-class", "Floral meristem and organ identity"),  # CAL
    "AT5G20240": ("AP1/FUL/CAL", "A-class", "Floral meristem and organ identity"),  # FUL

    # SEP/AGL2/AGL4/AGL6/AGL9/AGL13 Clade (E-class, SEPALLATA) - ORANGE
    "AT3G02310": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),   # AGL9/SEP3
    "AT1G24500": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),   # AGL2/SEP1
    "AT2G03710": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),   # AGL4/SEP2
    "AT2G45650": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),
    "AT2G03710": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),
    "AT1G67060": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),   # SEP4
    "AT4G22950": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),   # AGL6
    "AT3G61120": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),   # AGL13

    # AGL17/ANR1 Clade (root/flowering time) - LIGHT GREEN
    "AT4G18960": ("AGL17/ANR1", "AGL17-like", "Root development and flowering time"),  # AGL17
    "AT3G61890": ("AGL17/ANR1", "AGL17-like", "Root development and flowering time"),  # ANR1
    "AT3G57230": ("AGL17/ANR1", "AGL17-like", "Root development and flowering time"),  # AGL21
    "AT5G13790": ("AGL17/ANR1", "AGL17-like", "Root development and flowering time"),  # AGL16

    # SHP/STK/AG Clade (C/D-class, carpel/ovule identity) - BLUE
    "AT4G18960": ("SHP/STK/AG", "C/D-class", "Carpel and ovule identity"),
    "AT3G54340": ("SHP/STK/AG", "C/D-class", "Carpel and ovule identity"),   # AG
    "AT2G42830": ("SHP/STK/AG", "C/D-class", "Carpel and ovule identity"),   # SHP2
    "AT3G58780": ("SHP/STK/AG", "C/D-class", "Carpel and ovule identity"),   # SHP1
    "AT4G09960": ("SHP/STK/AG", "C/D-class", "Carpel and ovule identity"),   # STK

    # FLC/MAF/FLM Clade (Flowering repression/vernalization) - PURPLE
    "AT5G10140": ("FLC/MAF", "FLC-like", "Flowering repression and vernalization"),    # FLC
    "AT3G05390": ("FLC/MAF", "FLC-like", "Flowering repression and vernalization"),    # FLM
    "AT1G77080": ("FLC/MAF", "FLC-like", "Flowering repression and vernalization"),    # MAF2
    "AT3G65060": ("FLC/MAF", "FLC-like", "Flowering repression and vernalization"),    # MAF5
    "AT5G65070": ("FLC/MAF", "FLC-like", "Flowering repression and vernalization"),    # AGL70/MAF3
    "AT5G65060": ("FLC/MAF", "FLC-like", "Flowering repression and vernalization"),    # AGL14

    # SOC1/AGL20 Clade (Flowering time integration) - PINK
    "AT2G45660": ("SOC1/AGL20", "SOC1-like", "Flowering time integration"),  # SOC1/AGL20
    "AT5G62165": ("SOC1/AGL20", "SOC1-like", "Flowering time integration"),  # AGL71
    "AT1G77760": ("SOC1/AGL20", "SOC1-like", "Flowering time integration"),  # AGL72
    "AT2G22540": ("SOC1/AGL20", "SOC1-like", "Flowering time integration"),  # AGL42
    "AT4G37940": ("SOC1/AGL20", "SOC1-like", "Flowering time integration"),  # AGL14

    # AGL15/AGL18 Clade (Embryogenesis/flower regulation) - CYAN
    "AT5G13790": ("AGL15/AGL18", "AGL15-like", "Embryogenesis and flower regulation"),
    "AT3G57390": ("AGL15/AGL18", "AGL15-like", "Embryogenesis and flower regulation"),  # AGL15
    "AT3G22380": ("AGL15/AGL18", "AGL15-like", "Embryogenesis and flower regulation"),  # AGL18

    # AGL22/AGL24 Clade (SVP-like, flowering control) - YELLOW
    "AT5G20240": ("AGL22/AGL24", "SVP-like", "Flowering time control (SVP-like)"),
    "AT4G24540": ("AGL22/AGL24", "SVP-like", "Flowering time control (SVP-like)"),  # AGL24
    "AT2G22540": ("AGL22/AGL24", "SVP-like", "Flowering time control (SVP-like)"),  # SVP/AGL22

    # AP3/PI/TT16 Clade (B-class, petal/stamen identity) - BRIGHT GREEN
    "AT3G54340": ("AP3/PI", "B-class", "Petal and stamen identity"),
    "AT1G79840": ("AP3/PI", "B-class", "Petal and stamen identity"),   # AP3
    "AT5G20240": ("AP3/PI", "B-class", "Petal and stamen identity"),   # PI
    "AT4G09960": ("AP3/PI", "B-class", "Petal and stamen identity"),   # TT16
    "AT2G40080": ("AP3/PI", "B-class", "Petal and stamen identity"),   # GOA
    "AT5G62165": ("AP3/PI", "B-class", "Petal and stamen identity"),   # XAL1

    # AGL104/AGL66/AGL67 Clade (pollen-expressed) - MAGENTA
    "AT1G48150": ("AGL104/AGL66", "AGL104-like", "Pollen-expressed, male gametophyte"),
    "AT4G16900": ("AGL104/AGL66", "AGL104-like", "Pollen-expressed, male gametophyte"),  # AGL66
    "AT1G77990": ("AGL104/AGL66", "AGL104-like", "Pollen-expressed, male gametophyte"),  # AGL67
    "AT1G60920": ("AGL104/AGL66", "AGL104-like", "Pollen-expressed, male gametophyte"),  # AGL104

    # Previously Unknown — resolved from literature
    "AT5G60910": ("AP1/FUL/CAL", "A-class", "Floral meristem and organ identity"),      # FUL (alt locus)
    "AT5G23260": ("AP3/PI", "B-class", "Petal and stamen identity"),                    # PI (alt locus)
    "AT1G71692": ("AGL12", "AGL12-like", "Root development, AGL12 subfamily"),          # AGL12
    "AT1G22130": ("AGL15/AGL18", "AGL15-like", "Embryogenesis and flower regulation"),  # AGL15 (alt)
    "AT2G03060": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),     # AGL6-like
    "AT1G18750": ("SOC1/AGL20", "SOC1-like", "Flowering time integration"),             # AGL19
    "AT5G48670": ("FLC/MAF", "FLC-like", "Flowering repression and vernalization"),     # MAF4
    "AT2G14210": ("AGL17/ANR1", "AGL17-like", "Root development and flowering time"),   # AGL16-like
    "AT1G26310": ("AGL22/AGL24", "SVP-like", "Flowering time control (SVP-like)"),      # AGL24-like
    "AT5G65050": ("FLC/MAF", "FLC-like", "Flowering repression and vernalization"),     # MAF5-like
    "AT5G15800": ("SEP/AGL2-like", "E-class", "Floral organ identity (SEPALLATA)"),     # AGL6
    "AT1G77980": ("AGL104/AGL66", "AGL104-like", "Pollen-expressed, male gametophyte"), # AGL67-like
    "AT3G30260": ("AGL15/AGL18", "AGL15-like", "Embryogenesis and flower regulation"),  # AGL18-like
}

# ============================================================
# Arabidopsis AT ID → common gene name (well-known ones)
# ============================================================
AT_GENE_NAMES = {
    "AT1G69120": "AP1", "AT1G24260": "CAL", "AT5G61850": "AGL79",
    "AT5G20240": "FUL", "AT4G36590": "AGL79", "AT2G45650": "CAL",
    "AT3G02310": "SEP3/AGL9", "AT1G24500": "SEP1/AGL2",
    "AT2G03710": "SEP2/AGL4", "AT1G67060": "SEP4",
    "AT4G22950": "AGL6", "AT3G61120": "AGL13",
    "AT4G18960": "AGL17", "AT3G61890": "ANR1",
    "AT3G57230": "AGL21", "AT5G13790": "AGL16",
    "AT3G54340": "AG", "AT2G42830": "SHP2",
    "AT3G58780": "SHP1", "AT4G09960": "STK",
    "AT5G10140": "FLC", "AT3G05390": "FLM",
    "AT1G77080": "MAF2", "AT3G65060": "MAF5",
    "AT5G65070": "MAF3/AGL70", "AT5G65060": "AGL14",
    "AT2G45660": "SOC1/AGL20", "AT5G62165": "AGL71",
    "AT1G77760": "AGL72", "AT2G22540": "SVP/AGL22",
    "AT4G37940": "AGL14", "AT3G57390": "AGL15",
    "AT3G22380": "AGL18", "AT4G24540": "AGL24",
    "AT1G79840": "AP3", "AT5G20240": "PI",
    "AT1G48150": "AGL104", "AT4G16900": "AGL66",
    "AT1G77990": "AGL67", "AT1G60920": "AGL104",
    # Resolved unknowns
    "AT5G60910": "FUL", "AT5G23260": "PI",
    "AT1G71692": "AGL12", "AT1G22130": "AGL15",
    "AT2G03060": "AGL6", "AT1G18750": "AGL19",
    "AT5G48670": "MAF4", "AT2G14210": "AGL16",
    "AT1G26310": "AGL24", "AT5G65050": "MAF5",
    "AT5G15800": "AGL6", "AT1G77980": "AGL67",
    "AT3G30260": "AGL18",
}

def get_at_base(at_id):
    """Strip isoform suffix: AT1G69120.1 → AT1G69120"""
    return at_id.split(".")[0].strip()

def classify(at_id):
    base = get_at_base(at_id)
    clade_info = AT_TO_CLADE.get(base, ("Unknown", "Unknown", "Unknown"))
    gene_name = AT_GENE_NAMES.get(base, base)
    return clade_info, gene_name

# Species + their TopHits files
WORK_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK"
SPECIES_FILES = {
    "Amborella_trichopoda":   "Amborella_trichopoda/Amborella_trichopoda_TopHits_AT.txt",
    "Cinnamomum_kanehirae":   "Cinnamomum_kanehirae/Cinnamomum_kanehirae_TopHits_AT.txt",
    "Glycine_max":            "Glycine_max/Glycine_max_TopHits_AT.txt",
    "Helianthus_annuuss":     "Helianthus_annuuss/Helianthus_annuuss_TopHits_AT.txt",
    "Medicago_truncatula":    "Medicago_truncatula/Medicago_truncatula_TopHits_AT.txt",
    "Nelumbo_nucifera":       "Nelumbo_nucifera/Nelumbo_nucifera_TopHits_AT.txt",
    "Nymphaea_colorata":      "Nymphaea_colorata/Nymphaea_colorata_TopHits_AT.txt",
    "Oryza_sativa":           "Oryza_sativa/Oryza_sativa_TopHits_AT.txt",
    "Prunus_persica":         "Prunus_persica/Prunus_persica_TopHits_AT.txt",
}

rows = []
for species, rel_path in SPECIES_FILES.items():
    filepath = os.path.join(WORK_DIR, rel_path)
    if not os.path.exists(filepath):
        print(f"WARNING: {filepath} not found")
        continue
    with open(filepath) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            gene_id = row.get("Medicago_Gene_ID", "").strip()
            at_hit  = row.get("Top_AT_Hit", "").strip()
            evalue  = row.get("E-value", "").strip()
            bitscore = row.get("Bit-score", "").strip()

            (subclade, mads_class, function), at_name = classify(at_hit)

            rows.append({
                "Species":           species,
                "Gene_ID":           gene_id,
                "Top_Arabidopsis_Hit": at_hit,
                "AT_Gene_Name":      at_name,
                "Subclade":          subclade,
                "MADS_Class":        mads_class,
                "Function":          function,
                "E_value":           evalue,
                "Bit_score":         bitscore,
            })

# Write TSV
out_tsv = os.path.join(WORK_DIR, "MIKCc_Subclade_Annotation_Table.tsv")
fieldnames = ["Species","Gene_ID","Top_Arabidopsis_Hit","AT_Gene_Name",
              "Subclade","MADS_Class","Function","E_value","Bit_score"]
with open(out_tsv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"Done! {len(rows)} genes annotated.")
print(f"Output: {out_tsv}")

# Print summary by species
print("\n=== Summary by Species ===")
from collections import Counter
species_counts = Counter(r["Species"] for r in rows)
for sp, count in sorted(species_counts.items()):
    print(f"  {sp}: {count} genes")

print("\n=== Summary by Subclade ===")
clade_counts = Counter(r["Subclade"] for r in rows)
for clade, count in sorted(clade_counts.items(), key=lambda x: -x[1]):
    print(f"  {clade}: {count} genes")
