#!/usr/bin/env python3
"""
rank_genomewide_ar.py -- apply population-frequency filtering to the genome-wide
AR gene list, so that common polymorphisms are removed before any gene is
compared with BUB1B.

Focus: genes carrying HOM_pLoF or TWO_pLoF (models STRONGER than BUB1B's
pLoF_plus_MIS). If none survive frequency filtering with a phenotype-compatible
disease association, BUB1B is not being out-competed.

Population AF: Ensembl VEP REST GET (gnomAD). Query failures are recorded as
QUERY_FAILED and are NEVER treated as evidence of rarity.
Retrieved 2026-09-16.
"""
import json, urllib.request, time, csv, sys
from collections import defaultdict

SRC="analysis/data/genomewide/genomewide_ar_genes.tsv"
OUT="analysis/data/genomewide/genomewide_ar_rare.tsv"
ROW=[r for r in csv.DictReader(open(SRC),delimiter='\t')]
STRONG=[r for r in ROW if r['AR_model'] in ('HOM_pLoF','TWO_pLoF')]
print(f"genes with HOM_pLoF or TWO_pLoF: {len(STRONG)}")

def parse(v):
    out=[]
    for item in v.split(';'):
        if not item: continue
        loc,rest=item.split(':',1)
        import re
        m=re.match(r'(\d+)([ACGT]+)>([ACGT]+)\((.*?),(.*?)\)',rest)
        if m: out.append((loc,m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)))
    return out

def vep_af(chrom,pos,ref,alt):
    end=int(pos)+len(ref)-1
    url=f"https://rest.ensembl.org/vep/human/region/{chrom}:{pos}-{end}/{alt}?content-type=application/json"
    for a in range(4):
        try:
            r=json.load(urllib.request.urlopen(url,timeout=120))
            item=r[0] if isinstance(r,list) and r else {}
            best,rs=None,''
            for cv in item.get('colocated_variants',[]) or []:
                if str(cv.get('id','')).startswith('rs') and not rs: rs=cv['id']
                for al,pops in (cv.get('frequencies') or {}).items():
                    for pop,val in pops.items():
                        if pop.startswith(('gnomade','gnomadg')) and val is not None:
                            if best is None or val>best: best=val
            return best,rs,True
        except Exception:
            time.sleep(3*(a+1))
    return None,'',False

res=[]
for i,r in enumerate(STRONG,1):
    keep=[]
    for loc,pos,ref,alt,eff,gt in parse(r['variants']):
        af,rs,ok=vep_af(loc,pos,ref,alt)
        if not ok: cls='QUERY_FAILED'
        elif af is None: cls='ABSENT_from_gnomAD'
        elif gt in ('1/1','1|1') and af>=0.005: cls='COMMON'
        elif af>=0.01: cls='COMMON'
        else: cls='RARE'
        keep.append(dict(loc=loc,pos=pos,ref=ref,alt=alt,eff=eff,gt=gt,
                         af='NA' if af is None else f'{af:.3g}',rs=rs or '-',cls=cls))
    rare=[k for k in keep if k['cls'] in ('RARE','ABSENT_from_gnomAD')]
    res.append((r,keep,rare))
    if i%10==0: print(f"  {i}/{len(STRONG)}")

with open(OUT,'w') as fh:
    fh.write("gene\tAR_model\tn_pLoF_total\tn_pLoF_rare\tstatus\tdetail\n")
    for r,keep,rare in sorted(res,key=lambda x:-len(x[2])):
        status = 'RARE_pLoF_RETAINED' if rare else 'all_pLoF_common_or_unverified'
        det=";".join(f"{k['loc']}:{k['pos']}{k['ref']}>{k['alt']}({k['eff']},{k['gt']},AF={k['af']},{k['cls']},{k['rs']})" for k in keep)
        fh.write(f"{r['gene']}\t{r['AR_model']}\t{len(keep)}\t{len(rare)}\t{status}\t{det}\n")

surv=[(r,rare) for r,keep,rare in res if rare]
print(f"\nGenes retaining >=1 RARE pLoF after frequency filtering: {len(surv)}")
for r,rare in sorted(surv,key=lambda x:-len(x[1])):
    print(f"  {r['gene']:12s} {r['AR_model']:10s} rare_pLoF={len(rare)}")
    for k in rare: print(f"      {k['loc']}:{k['pos']} {k['ref']}>{k['alt']} {k['eff']} {k['gt']} AF={k['af']} {k['cls']} {k['rs']}")
print(f"\nwrote {OUT}")
