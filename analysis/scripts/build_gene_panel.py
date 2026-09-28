#!/usr/bin/env python3
"""
build_gene_panel.py -- assemble the screening gene panel and fetch GRCh38 coordinates.

GENE LIST PROVENANCE (no gene was invented):
  1. Genomics England PanelApp panel 290 "Familial rhabdomyosarcoma" v1.6
     (updated 2025-11-23) -- GREEN (confidence_level 3) genes only.
     Chosen because the proband's HPO includes Rhabdomyosarcoma (HP:0002859).
  2. Genomics England PanelApp panel 259 "Childhood solid tumours cancer
     susceptibility" v1.30 (updated 2025-10-13) -- GREEN genes only.
  3. The MVA / mitotic-checkpoint gene set specified in the analysis brief:
     BUB1B CEP57 TRIP13 BUB1 CCDC84(CENATAC) KNL1 BUB3 MAD2L1 TTK CENPE
     NOTE: PanelApp has no dedicated "mosaic variegated aneuploidy" panel
     (searched 2026-09-16); this set is therefore carried from the brief and is
     labelled as such in the output, NOT as a PanelApp-derived list.

Coordinates: Ensembl REST POST /lookup/symbol/homo_sapiens (GRCh38).
Retrieved: 2026-09-16.
"""
import json, urllib.request, sys, os

OUT = "analysis/data/panel"
os.makedirs(OUT, exist_ok=True)

def panel_green(pid):
    d = json.load(open(f"{OUT}/panelapp_{pid}.json"))
    meta = dict(id=d["id"], name=d["name"], version=d["version"],
                version_created=d["version_created"])
    genes = sorted({g["gene_data"]["gene_symbol"] for g in d["genes"]
                    if str(g.get("confidence_level")) == "3"})
    return meta, genes

m290, g290 = panel_green(290)
m259, g259 = panel_green(259)
MVA_BRIEF = ["BUB1B","CEP57","TRIP13","BUB1","CCDC84","KNL1","BUB3","MAD2L1","TTK","CENPE"]

sources = {}
for g in g290: sources.setdefault(g, []).append("PanelApp290_rhabdomyosarcoma_GREEN")
for g in g259: sources.setdefault(g, []).append("PanelApp259_childhood_solid_tumour_GREEN")
for g in MVA_BRIEF: sources.setdefault(g, []).append("MVA_gene_set_from_brief")

symbols = sorted(sources)
print(f"panel 290 GREEN: {len(g290)} | panel 259 GREEN: {len(g259)} | MVA brief: {len(MVA_BRIEF)}")
print(f"UNION: {len(symbols)} genes")

# Ensembl batch symbol lookup (GRCh38)
req = urllib.request.Request(
    "https://rest.ensembl.org/lookup/symbol/homo_sapiens",
    data=json.dumps({"symbols": symbols}).encode(),
    headers={"Content-Type": "application/json", "Accept": "application/json"})
info = json.load(urllib.request.urlopen(req, timeout=180))

rows, missing = [], []
for s in symbols:
    d = info.get(s)
    if not d or d.get("seq_region_name") not in [str(i) for i in range(1, 23)] + ["X", "Y", "MT"]:
        missing.append(s); continue
    rows.append(dict(symbol=s, ensembl_id=d["id"], chrom=d["seq_region_name"],
                     start=d["start"], end=d["end"], strand=d["strand"],
                     assembly=d.get("assembly_name"), sources=sources[s]))

rows.sort(key=lambda r: (r["chrom"].zfill(2), r["start"]))
json.dump(dict(panels=[m290, m259], mva_brief=MVA_BRIEF, retrieved="2026-09-16",
               genes=rows, unresolved=missing),
          open(f"{OUT}/gene_panel.json", "w"), indent=2)

FLANK = 50000
with open(f"{OUT}/panel_regions_flank50kb.bed", "w") as fh:
    for r in rows:
        fh.write(f"{r['chrom']}\t{max(0,r['start']-1-FLANK)}\t{r['end']+FLANK}\t{r['symbol']}\n")

print(f"resolved: {len(rows)}   unresolved: {missing or 'none'}")
print(f"wrote {OUT}/gene_panel.json and panel_regions_flank50kb.bed (+/-{FLANK//1000} kb)")
