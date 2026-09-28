#!/usr/bin/env python3
"""
step12b_finalize_splice.py -- refine SpliceAI status codes and attach population
evidence, producing the final BUB1B splice-screen table.

Two refinements over step12_splice_screen.py:
  1. Variants carrying no SpliceAI annotation are re-classified. SpliceAI only
     scores variants that fall inside an annotated transcript. Variants outside
     every transcript in the bundled GRCh38 annotation are UNSUPPORTED_VARIANT
     (SpliceAI legitimately declines them) -- NOT tool failures, and NOT zeros.
  2. gnomAD population AF is attached via Ensembl VEP REST. QUERY_FAILED remains
     a distinct class and is never read as rarity.
"""
import csv, json, urllib.request, time, os

SRC="analysis/data/splicing/spliceai_parsed.tsv"
OUT="analysis/data/splicing/bub1b_splice_final.tsv"
# transcript bounds from the SpliceAI bundled GRCh38 annotation
TX={"BUB1B":(40161025,40221136),"PAK6":(40217448,40276396)}
MIN_TX=min(s for s,_ in TX.values()); MAX_TX=max(e for _,e in TX.values())

rows=list(csv.DictReader(open(SRC),delimiter='\t'))
for r in rows:
    if r["status"]=="PREDICTION_UNAVAILABLE":
        p=int(r["pos"])
        inside=any(s<=p<=e for s,e in TX.values())
        r["status"]=("PREDICTION_UNAVAILABLE (inside a transcript but unscored - investigate)"
                     if inside else
                     "UNSUPPORTED_VARIANT (outside every annotated transcript; SpliceAI cannot score)")

def vep_af(chrom,pos,ref,alt):
    end=int(pos)+len(ref)-1
    url=f"https://rest.ensembl.org/vep/human/region/{chrom}:{pos}-{end}/{alt}?content-type=application/json"
    for a in range(3):
        try:
            r=json.load(urllib.request.urlopen(url,timeout=90))
            it=r[0] if isinstance(r,list) and r else {}
            best,rs=None,''
            for cv in it.get('colocated_variants',[]) or []:
                if str(cv.get('id','')).startswith('rs') and not rs: rs=cv['id']
                for al,pops in (cv.get('frequencies') or {}).items():
                    for pop,val in pops.items():
                        if pop.startswith(('gnomade','gnomadg')) and val is not None:
                            if best is None or val>best: best=val
            return best,rs,True
        except Exception: time.sleep(2)
    return None,'',False

b=[r for r in rows if r["gene"]=="BUB1B"]
print(f"BUB1B records: {len(b)}  -- fetching population frequencies")
for r in b:
    af,rs,ok=vep_af(r["chrom"],r["pos"],r["ref"],r["alt"])
    r["rsid"]=rs or "-"
    if not ok: r["pop_af"]="QUERY_FAILED"
    elif af is None: r["pop_af"]="not in gnomAD"
    else: r["pop_af"]=f"{af:.3g}"

cols=["chrom","pos","ref","alt","filter","gt","gene","rsid","pop_af",
      "ds_ag","ds_al","ds_dg","ds_dl","max_ds","effect","status"]
with open(OUT,"w") as fh:
    fh.write("\t".join(cols)+"\n")
    for r in sorted(b,key=lambda x:-float(x["max_ds"] or 0)):
        fh.write("\t".join(str(r.get(c,"")) for c in cols)+"\n")

# rewrite the full parsed table with refined statuses; use the UNION of keys so
# the extra rsid/pop_af columns added to BUB1B rows do not break the writer
allkeys=[]
for r in rows:
    for k in r:
        if k not in allkeys: allkeys.append(k)
# ATOMIC: write to a temp file and replace only on success. An earlier revision
# opened the target with "w" directly; a mid-write exception then left the input
# table TRUNCATED and the next run silently saw 0 records.
tmp="analysis/data/splicing/spliceai_parsed.tsv.tmp"
with open(tmp,"w") as fh:
    w=csv.DictWriter(fh,fieldnames=allkeys,delimiter='\t',restval="")
    w.writeheader(); w.writerows(rows)
os.replace(tmp,"analysis/data/splicing/spliceai_parsed.tsv")

from collections import Counter
print("\nrefined status breakdown (all 176 records):")
for k,v in Counter(r["status"] for r in rows).most_common(): print(f"  {v:4d}  {k}")
print(f"\nwrote {OUT}")
