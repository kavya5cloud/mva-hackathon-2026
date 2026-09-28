#!/usr/bin/env python3
"""
screen_genomewide_ar.py -- unbiased genome-wide AR screen (no gene-list prior).

INPUT : analysis/data/genomewide/genomewide_high_moderate.tsv
        (snpEff 5.4c GRCh38.mane.1.2.refseq -canon, PASS only, HIGH|MODERATE)
OUTPUT: analysis/data/genomewide/genomewide_ar_genes.tsv

Thresholds identical to screen_panel_ar.py: GQ>=20, DP>=10, PASS.
Population AF is NOT available at this stage and is applied afterwards to the
shortlist only (annotate_candidates_af.py). Counts here are therefore
PRE-frequency-filter and must not be read as rare-variant counts.

AR models scored:
  HOM_pLoF      >=1 homozygous HIGH-impact pLoF          (strongest)
  TWO_pLoF      >=2 heterozygous HIGH-impact pLoF
  pLoF_plus_MIS  1 HIGH pLoF + >=1 MODERATE
"""
import sys, re
from collections import defaultdict

SRC = "analysis/data/genomewide/genomewide_high_moderate.tsv"
OUT = "analysis/data/genomewide/genomewide_ar_genes.tsv"
HIGH_LOF = {"stop_gained","frameshift_variant","splice_acceptor_variant",
            "splice_donor_variant","start_lost","stop_lost"}
MIN_GQ, MIN_DP = 20, 10

genes = defaultdict(lambda: dict(hom_plof=[], het_plof=[], mis=[]))
n_in = n_keep = 0
for line in open(SRC):
    f = line.rstrip("\n").split("\t")
    if len(f) < 10: continue
    n_in += 1
    chrom,pos,ref,alt,filt,ann,gt,dp,gq,ad = f[:10]
    if gt in ("./.",".","0/0","0|0"): continue
    try:
        if int(gq) < MIN_GQ or int(dp) < MIN_DP: continue
    except ValueError: continue
    best=None; rank={"HIGH":0,"MODERATE":1,"LOW":2,"MODIFIER":3}
    for a in ann.split(","):
        p=a.split("|")
        if len(p)<11: continue
        if best is None or rank.get(p[2],9)<rank.get(best[2],9): best=p
    if best is None: continue
    eff,imp,gene = best[1],best[2],best[3]
    if not gene: continue
    n_keep += 1
    rec=(chrom,pos,ref,alt,eff,gt,dp,gq,best[10] or best[9])
    hom = gt in ("1/1","1|1")
    if imp=="HIGH" and eff.split("&")[0] in HIGH_LOF:
        (genes[gene]["hom_plof"] if hom else genes[gene]["het_plof"]).append(rec)
    elif imp=="MODERATE":
        genes[gene]["mis"].append(rec)

rows=[]
for g,d in genes.items():
    hp,tp,mi = len(d["hom_plof"]), len(d["het_plof"]), len(d["mis"])
    if   hp>=1: model="HOM_pLoF"
    elif tp>=2: model="TWO_pLoF"
    elif tp==1 and mi>=1: model="pLoF_plus_MIS"
    else: continue
    rows.append((g,model,hp,tp,mi,d))

order={"HOM_pLoF":0,"TWO_pLoF":1,"pLoF_plus_MIS":2}
rows.sort(key=lambda r:(order[r[1]],-r[2],-r[3]))
with open(OUT,"w") as fh:
    fh.write("gene\tAR_model\tn_hom_pLoF\tn_het_pLoF\tn_moderate\tvariants\n")
    for g,model,hp,tp,mi,d in rows:
        v=";".join(f"{r[0]}:{r[1]}{r[2]}>{r[3]}({r[4]},{r[5]})"
                   for r in d["hom_plof"]+d["het_plof"])
        fh.write(f"{g}\t{model}\t{hp}\t{tp}\t{mi}\t{v}\n")

print(f"records read           : {n_in:,}")
print(f"passing GQ/DP/genotype : {n_keep:,}")
print(f"genes with an AR model : {len(rows):,}")
from collections import Counter
for k,v in Counter(r[1] for r in rows).most_common(): print(f"  {k:16s} {v}")
print(f"wrote {OUT}")
