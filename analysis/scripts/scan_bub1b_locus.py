#!/usr/bin/env python3
"""
scan_bub1b_locus.py -- exhaustive scan of the BUB1B locus in the proband VCF.

Deliberately NOT restricted to coding PASS SNVs. Every variant class is reported:
coding, synonymous, splice-region, canonical splice, UTR, upstream/downstream
(promoter-proximal), deep intronic, and indels. Non-PASS calls are RETAINED and
flagged, because a true second hit could sit behind a marginal filter.

COORDINATES (authoritative, Ensembl REST, retrieved 2026-09-16):
  BUB1B GRCh38 = chr15:40,160,984-40,221,137  (ENSG00000156970, + strand)
SCREENING WINDOW
  gene body +/- 50 kb  ->  chr15:40,110,984-40,271,137
  NOTE: +/-50 kb is a CHOSEN screening window, not a claim that it captures all
  BUB1B regulatory elements. Distal enhancers outside it would be missed.
TRANSCRIPT
  NM_001211.6 is retained as the reference transcript for Leu737*/Asn1002Lys,
  consistent with all prior interpretation in this repository.
"""
import subprocess, sys, os, re
from collections import Counter, defaultdict

VCF   = sys.argv[1] if len(sys.argv)>1 else os.path.expanduser("~/WGS_EX2312012_HGWCNDSX7.vcf.gz")
OUT   = "analysis/data/bub1b_locus"
GENE  = ("15", 40160984, 40221137)
FLANK = 50000
SE    = "/opt/anaconda3/share/snpeff-5.4.0c-0/snpEff.jar"
DB    = "GRCh38.mane.1.2.refseq"
os.makedirs(OUT, exist_ok=True)
REG = f"{GENE[0]}:{GENE[1]-FLANK}-{GENE[2]+FLANK}"
print(f"window: {REG}  (gene body +/- {FLANK//1000} kb)")

raw = f"{OUT}/bub1b_locus_raw.vcf.gz"
ann = f"{OUT}/bub1b_locus_annotated.vcf.gz"
subprocess.run(f"bcftools view -r {REG} {VCF} -Oz -o {raw}", shell=True, check=True)
subprocess.run(f"bcftools index -f -t {raw}", shell=True, check=True)
subprocess.run(f"java -Xmx4g -jar {SE} ann -noStats -canon {DB} {raw} 2>{OUT}/snpeff.log | bgzip -c > {ann}",
               shell=True, check=True)
subprocess.run(f"tabix -f -p vcf {ann}", shell=True, check=True)

q = subprocess.run(
    f"bcftools query -f '%CHROM\\t%POS\\t%REF\\t%ALT\\t%FILTER\\t%INFO/ANN\\t[%GT\\t%DP\\t%GQ\\t%AD]\\n' {ann}",
    shell=True, capture_output=True, text=True).stdout

rank={"HIGH":0,"MODERATE":1,"LOW":2,"MODIFIER":3}
rows=[]; cls=Counter(); filt=Counter(); ingene=0
for line in q.strip().split("\n"):
    if not line: continue
    f=line.split("\t")
    chrom,pos,ref,alt,fl,annstr,gt,dp,gq,ad = f[:10]
    if gt in ("./.",".","0/0","0|0"): continue
    best=None
    for a in annstr.split(","):
        p=a.split("|")
        if len(p)<11: continue
        if p[3]!="BUB1B": continue
        if best is None or rank.get(p[2],9)<rank.get(best[2],9): best=p
    if best is None:
        for a in annstr.split(","):
            p=a.split("|")
            if len(p)>=11 and (best is None or rank.get(p[2],9)<rank.get(best[2],9)): best=p
    if best is None: continue
    eff,imp,gene,feat,hgvsc,hgvsp = best[1],best[2],best[3],best[6],best[9],best[10]
    if gene=="BUB1B": ingene+=1
    inside = GENE[1] <= int(pos) <= GENE[2]
    vtype = "SNV" if len(ref)==1 and len(alt)==1 else "INDEL"
    # coarse class for reporting
    e0=eff.split("&")[0]
    if   e0 in ("stop_gained","frameshift_variant","splice_acceptor_variant","splice_donor_variant","start_lost","stop_lost"): k="pLoF"
    elif e0=="missense_variant": k="missense"
    elif e0=="synonymous_variant": k="synonymous"
    elif "splice_region" in eff: k="splice_region"
    elif "5_prime_UTR" in eff: k="5UTR"
    elif "3_prime_UTR" in eff: k="3UTR"
    elif e0=="intron_variant": k="intronic"
    elif e0 in ("upstream_gene_variant",): k="upstream"
    elif e0 in ("downstream_gene_variant",): k="downstream"
    else: k=e0
    cls[k]+=1; filt[fl]+=1
    rows.append(dict(chrom=chrom,pos=int(pos),ref=ref,alt=alt,filter=fl,gene=gene,
                     impact=imp,effect=eff,klass=k,vtype=vtype,hgvsc=hgvsc,hgvsp=hgvsp,
                     gt=gt,dp=dp,gq=gq,ad=ad,in_gene_body="yes" if inside else "flank"))

cols=["chrom","pos","ref","alt","filter","gene","impact","effect","klass","vtype",
      "hgvsc","hgvsp","gt","dp","gq","ad","in_gene_body"]
with open(f"{OUT}/bub1b_locus_all_variants.tsv","w") as fh:
    fh.write("\t".join(cols)+"\n")
    for r in sorted(rows,key=lambda x:x["pos"]):
        fh.write("\t".join(str(r[c]) for c in cols)+"\n")

print(f"\nnon-ref variants in window : {len(rows)}")
print(f"  annotated to BUB1B       : {ingene}")
print(f"  in gene body             : {sum(1 for r in rows if r['in_gene_body']=='yes')}")
print("\nby class:")
for k,v in cls.most_common(): print(f"  {k:16s} {v}")
print("\nby FILTER:")
for k,v in filt.most_common(): print(f"  {k:24s} {v}")
print("\nPotentially-consequential (pLoF / missense / splice_region / UTR), ANY filter:")
print(f"  {'pos':>10} {'ref>alt':<14}{'filter':<12}{'class':<14}{'gt':<6}{'DP':>4}{'GQ':>4}  {'hgvsp/hgvsc'}")
for r in sorted(rows,key=lambda x:x["pos"]):
    if r["klass"] in ("pLoF","missense","splice_region","5UTR","3UTR") or r["impact"] in ("HIGH","MODERATE"):
        print(f"  {r['pos']:>10} {r['ref']+'>'+r['alt']:<14}{r['filter']:<12}{r['klass']:<14}{r['gt']:<6}{r['dp']:>4}{r['gq']:>4}  {r['hgvsp'] or r['hgvsc']}")
print(f"\nwrote {OUT}/bub1b_locus_all_variants.tsv")
