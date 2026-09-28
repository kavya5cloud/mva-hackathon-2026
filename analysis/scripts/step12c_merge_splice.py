#!/usr/bin/env python3
"""
step12c_merge_splice.py -- merge SpliceAI and Pangolin results into the final
BUB1B splice-screen table.

Pangolin CSV output format per gene entry:
    <ENSG>|<pos>:<largest_score_increase>|<pos>:<largest_score_decrease>|Warnings:
An empty Pangolin field means the variant was skipped ("not contained in a gene
body") -- recorded as UNSUPPORTED_VARIANT, never as a score of zero.

Gene IDs seen at this locus:
    ENSG00000156970 = BUB1B
    ENSG00000137843 = PAK6
    ENSG00000259288 = BUB1B-PAK6 readthrough
"""
import csv, re, os

SA  = "analysis/data/splicing/bub1b_splice_final.tsv"
PG  = "analysis/data/splicing/pangolin_out.csv"
OUT = "analysis/data/splicing/bub1b_splice_merged.tsv"
GENE = {"ENSG00000156970":"BUB1B","ENSG00000137843":"PAK6","ENSG00000259288":"BUB1B-PAK6"}

pang = {}
for r in csv.DictReader(open(PG)):
    key = (r["CHROM"], r["POS"], r["REF"], r["ALT"])
    raw = (r.get("Pangolin") or "").strip()
    if not raw:
        pang[key] = ("UNSUPPORTED_VARIANT", None, "-"); continue
    best, detail = 0.0, []
    for entry in raw.split(","):
        p = entry.split("|")
        if len(p) < 3: continue
        g = GENE.get(p[0].split(".")[0], p[0].split(".")[0])
        if g != "BUB1B": continue          # BUB1B transcript context only
        try:
            inc_pos, inc = p[1].split(":"); dec_pos, dec = p[2].split(":")
            inc, dec = float(inc), float(dec)
        except ValueError: continue
        detail.append(f"gain{float(inc):+.2f}@{inc_pos}nt / loss{float(dec):+.2f}@{dec_pos}nt")
        best = max(best, abs(inc), abs(dec))
    pang[key] = ("scored", round(best, 3), "; ".join(detail) or "-") if detail \
                else ("no BUB1B transcript context", None, "-")

rows = list(csv.DictReader(open(SA), delimiter="\t"))
cols = ["chrom","pos","ref","alt","filter","gt","gene","rsid","pop_af",
        "spliceai_max_ds","spliceai_effect","pangolin_max_abs","pangolin_detail",
        "concordant","status"]
out = []
for r in rows:
    key = (r["chrom"], r["pos"], r["ref"], r["alt"])
    pstat, pmax, pdet = pang.get(key, ("NOT_RUN", None, "-"))
    sa_max = float(r["max_ds"]) if r["max_ds"] not in ("", None) else None
    if sa_max is None or pmax is None:
        conc = "n/a"
    else:
        conc = "YES" if ((sa_max < 0.05) == (pmax < 0.05)) else "NO"
    # final prioritisation uses the HIGHER of the two tools (conservative)
    both = [x for x in (sa_max, pmax) if x is not None]
    mx = max(both) if both else None
    if mx is None:        cat = pstat
    elif mx < 0.05:       cat = "NO SIGNAL"
    elif mx < 0.20:       cat = "LOW PRIORITY"
    elif mx < 0.50:       cat = "REVIEW"
    else:                 cat = "HIGH-PRIORITY SPLICE CANDIDATE"
    out.append(dict(chrom=r["chrom"], pos=r["pos"], ref=r["ref"], alt=r["alt"],
                    filter=r["filter"], gt=r["gt"], gene=r["gene"], rsid=r["rsid"],
                    pop_af=r["pop_af"], spliceai_max_ds=r["max_ds"],
                    spliceai_effect=r["effect"],
                    pangolin_max_abs="" if pmax is None else pmax,
                    pangolin_detail=pdet, concordant=conc, status=cat))

tmp = OUT + ".tmp"
with open(tmp, "w") as fh:
    fh.write("\t".join(cols) + "\n")
    for r in sorted(out, key=lambda x: -(float(x["spliceai_max_ds"] or 0))):
        fh.write("\t".join(str(r[c]) for c in cols) + "\n")
os.replace(tmp, OUT)

from collections import Counter
print(f"merged records: {len(out)}")
print("status:", dict(Counter(r['status'] for r in out)))
print("concordance:", dict(Counter(r['concordant'] for r in out)))
print(f"wrote {OUT}")
