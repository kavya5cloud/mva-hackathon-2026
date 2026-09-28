#!/usr/bin/env python3
"""
check_strong_ar_genes.py -- frequency-check the genome-wide HOM_pLoF / TWO_pLoF
genes that are plausibly disease-relevant.

RATIONALE (stated so the triage is auditable, not hidden):
The 99 genes carrying an AR model stronger than BUB1B's are dominated by gene
families that are well known to carry common loss-of-function alleles or to be
alignment-problematic in short-read WGS:
  olfactory receptors (OR*), HLA class I/II, MUC*, KRTAP*, PSG*, NPIPB*, ZNF*,
  LILRB*, GOLGA6L*, AGAP*, DEFB*, TYW1B, POMZP3, ZDHHC11B
Homozygous pLoF in these is expected in a healthy genome and none is a credible
cause of rhabdomyosarcoma + IUGR + chromosomal instability.

This script frequency-checks the REMAINDER -- genes with a recognised human
disease association -- so that the comparison against BUB1B rests on data rather
than on that triage argument alone. Genes excluded by family are listed
explicitly in the output so the decision is reviewable.

Population AF: Ensembl VEP REST GET (gnomAD), retrieved 2026-09-16.
QUERY_FAILED is never treated as evidence of rarity.
"""
import json, urllib.request, time, csv, re, sys

SRC="analysis/data/genomewide/genomewide_ar_genes.tsv"
OUT="analysis/data/genomewide/strong_ar_disease_genes_af.tsv"
FAMILY=re.compile(r"^(OR\d|HLA-|MUC\d|KRTAP|PSG\d|NPIPB|LILRB|GOLGA6L|AGAP\d|DEFB|ZNF\d|TRIM51|PCDH|MICA|GSTT|SIGLEC|MS4A|SLC22A2[0-9]|FOLR3|PATE|CYLC|ZAN|HRNR|TYW1B|POMZP3|ZDHHC11B|SCRN3|C\d+orf)")
rows=[r for r in csv.DictReader(open(SRC),delimiter='\t') if r['AR_model'] in ('HOM_pLoF','TWO_pLoF')]
fam=[r for r in rows if FAMILY.match(r['gene'])]
keep=[r for r in rows if not FAMILY.match(r['gene'])]
print(f"HOM_pLoF/TWO_pLoF genes total : {len(rows)}")
print(f"  excluded by gene family     : {len(fam)}  -> {' '.join(sorted(x['gene'] for x in fam))}")
print(f"  frequency-checked here      : {len(keep)} -> {' '.join(sorted(x['gene'] for x in keep))}\n")

def parse(v):
    out=[]
    for item in v.split(';'):
        if not item: continue
        loc,rest=item.split(':',1)
        m=re.match(r'(\d+)([ACGTN]+)>([ACGTN]+)\((.*?),(.*?)\)',rest)
        if m: out.append((loc,m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)))
    return out

def vep_af(chrom,pos,ref,alt):
    end=int(pos)+len(ref)-1
    url=f"https://rest.ensembl.org/vep/human/region/{chrom}:{pos}-{end}/{alt}?content-type=application/json"
    for a in range(3):
        try:
            r=json.load(urllib.request.urlopen(url,timeout=60))
            it=r[0] if isinstance(r,list) and r else {}
            best,rs=None,''
            for cv in it.get('colocated_variants',[]) or []:
                if str(cv.get('id','')).startswith('rs') and not rs: rs=cv['id']
                for al,pops in (cv.get('frequencies') or {}).items():
                    for pop,val in pops.items():
                        if pop.startswith(('gnomade','gnomadg')) and val is not None:
                            if best is None or val>best: best=val
            return best,rs,True
        except Exception:
            time.sleep(2)
    return None,'',False

with open(OUT,'w') as fh:
    fh.write("gene\tAR_model\tvariant\tgt\teffect\tgnomad_popmax_AF\trsid\tclass\n")
    survivors=set()
    for r in keep:
        for loc,pos,ref,alt,eff,gt in parse(r['variants']):
            af,rs,ok=vep_af(loc,pos,ref,alt)
            if not ok: cls='QUERY_FAILED'
            elif af is None: cls='ABSENT_from_gnomAD'
            elif gt in ('1/1','1|1') and af>=0.005: cls='COMMON'
            elif af>=0.01: cls='COMMON'
            else: cls='RARE'
            if cls in ('RARE','ABSENT_from_gnomAD'): survivors.add(r['gene'])
            line=f"{r['gene']}\t{r['AR_model']}\t{loc}:{pos}{ref}>{alt}\t{gt}\t{eff}\t{'NA' if af is None else f'{af:.3g}'}\t{rs or '-'}\t{cls}"
            fh.write(line+"\n"); print("  "+line, flush=True)

print(f"\nGenes retaining a RARE/ABSENT pLoF: {sorted(survivors) or 'NONE'}")
print(f"wrote {OUT}")
