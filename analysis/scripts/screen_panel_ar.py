#!/usr/bin/env python3
"""
screen_panel_ar.py -- autosomal-recessive / candidate-biallelic screen of the
MVA + childhood-tumour gene panel in the proband VCF.

INPUT : analysis/data/panel/panel_annotated.vcf.gz  (snpEff 5.4c, GRCh38.mane.1.2.refseq, -canon)
OUTPUT: analysis/data/panel/ar_screen_candidates.tsv
        analysis/data/panel/gene_evidence_summary.tsv

=================== DOCUMENTED THRESHOLDS (all explicit) ===================
QUALITY
  FILTER            must be PASS  (non-PASS retained separately and COUNTED,
                    never silently dropped -- see the 'excluded' report)
  GQ                >= 20
  DP                >= 10
  allele balance    het calls with VAF < 0.20 or > 0.80 are flagged LOW_AB
                    (retained, flagged -- not dropped)

GENOTYPE HANDLING
  1/1 or 1|1        homozygous alternate      -> AR model A
  0/1 or 0|1        heterozygous              -> AR model B/C, de novo candidate
  1/2               multiallelic non-ref het  -> RETAINED and explicitly flagged
                    MULTIALLELIC; counts as TWO alternate alleles at one site and
                    is treated as a candidate biallelic genotype IN ITSELF
  ./. or .          missing genotype          -> EXCLUDED and COUNTED
  0/0               homozygous reference      -> not a candidate

CONSEQUENCE CLASSES (snpEff impact)
  HIGH      stop_gained, frameshift, splice_acceptor, splice_donor, start_lost,
            stop_lost  -> treated as putative loss-of-function (pLoF)
  MODERATE  missense, inframe indel, etc.     -> potentially damaging
  LOW/MODIFIER (synonymous, UTR, intronic, upstream/downstream) -> NOT counted
            toward the AR models here, but ARE exported for the BUB1B deep dive
            (scan_bub1b_locus.py) so nothing is lost.

ALLELE FREQUENCY -- IMPORTANT LIMITATION
  The VCF's INFO/AF is the GATK per-site allele fraction for THIS SINGLE SAMPLE
  (0.5 for a het). It is NOT a population frequency and is NEVER used as one.
  Population AF is obtained separately, per candidate, from gnomAD via the
  Ensembl VEP REST API (see annotate_candidates_af.py). Rarity thresholds are
  therefore applied AFTER this script, not inside it.

PHASE
  This script NEVER asserts phase. Two qualifying heterozygous variants in one
  gene are reported as "candidate biallelic genotype; phase unresolved".
============================================================================
"""
import gzip, re, sys, os, json
from collections import defaultdict

VCF = sys.argv[1] if len(sys.argv) > 1 else "analysis/data/panel/panel_annotated.vcf.gz"
OUT = "analysis/data/panel"
MIN_GQ, MIN_DP = 20, 10
HIGH_LOF = {"stop_gained","frameshift_variant","splice_acceptor_variant",
            "splice_donor_variant","start_lost","stop_lost"}

panel = {g["symbol"]: g for g in json.load(open(f"{OUT}/gene_panel.json"))["genes"]}

stats = defaultdict(int)
by_gene = defaultdict(list)
excluded = defaultdict(int)

def parse_ann(annstr):
    """Return (impact, effect, gene, hgvsc, hgvsp, feature) of the most severe ANN entry."""
    best = None
    rank = {"HIGH":0,"MODERATE":1,"LOW":2,"MODIFIER":3}
    for a in annstr.split(","):
        f = a.split("|")
        if len(f) < 11: continue
        eff, imp, gene, feat, hgvsc, hgvsp = f[1], f[2], f[3], f[6], f[9], f[10]
        if best is None or rank.get(imp,9) < rank.get(best[0],9):
            best = (imp, eff, gene, hgvsc, hgvsp, feat)
    return best

with gzip.open(VCF, "rt") as fh:
    for line in fh:
        if line.startswith("#"):
            continue
        c = line.rstrip("\n").split("\t")
        chrom, pos, _id, ref, alt, qual, filt, info, fmt, smp = c[:10]
        stats["total"] += 1
        keys = fmt.split(":"); vals = smp.split(":")
        g = dict(zip(keys, vals))
        gt = g.get("GT", "./.")
        if gt in ("./.", ".", "0/0", "0|0"):
            excluded["missing_or_homref"] += 1; continue
        m = re.search(r"ANN=([^;\t]+)", info)
        if not m:
            excluded["no_annotation"] += 1; continue
        pa = parse_ann(m.group(1))
        if pa is None:
            excluded["unparseable_ann"] += 1; continue
        impact, effect, gene, hgvsc, hgvsp, feat = pa
        if gene not in panel:
            excluded["off_panel_gene"] += 1; continue
        if impact not in ("HIGH","MODERATE"):
            excluded[f"impact_{impact}"] += 1; continue
        if filt != "PASS":
            excluded["non_PASS"] += 1; continue
        try: dp = int(g.get("DP","0"))
        except ValueError: dp = 0
        try: gq = int(g.get("GQ","0"))
        except ValueError: gq = 0
        if gq < MIN_GQ: excluded["low_GQ"] += 1; continue
        if dp < MIN_DP: excluded["low_DP"] += 1; continue

        flags = []
        if "," in alt or gt in ("1/2","1|2","2/1"): flags.append("MULTIALLELIC")
        ad = g.get("AD","")
        vaf = None
        try:
            parts = [int(x) for x in ad.split(",")]
            if len(parts) >= 2 and sum(parts) > 0:
                vaf = sum(parts[1:]) / sum(parts) if "1/2" in gt else parts[1]/(parts[0]+parts[1])
        except Exception: pass
        zyg = "HOM_ALT" if gt in ("1/1","1|1") else ("MULTIALLELIC_HET" if "2" in gt else "HET")
        if zyg == "HET" and vaf is not None and not (0.20 <= vaf <= 0.80):
            flags.append("LOW_AB")
        if impact == "HIGH" and effect.split("&")[0] in HIGH_LOF: flags.append("pLoF")

        rec = dict(chrom=chrom, pos=int(pos), ref=ref, alt=alt, filter=filt, gene=gene,
                   impact=impact, effect=effect, hgvsc=hgvsc, hgvsp=hgvsp, feature=feat,
                   gt=gt, zyg=zyg, dp=dp, gq=gq, ad=ad,
                   vaf=round(vaf,3) if vaf is not None else "NA",
                   flags=";".join(flags) or "-")
        by_gene[gene].append(rec); stats["qualifying"] += 1

# ---- write candidate table -------------------------------------------------
cols = ["gene","chrom","pos","ref","alt","zyg","gt","impact","effect","hgvsc","hgvsp",
        "feature","dp","gq","ad","vaf","filter","flags"]
with open(f"{OUT}/ar_screen_candidates.tsv","w") as fh:
    fh.write("\t".join(cols)+"\n")
    for gene in sorted(by_gene):
        for r in sorted(by_gene[gene], key=lambda x:x["pos"]):
            fh.write("\t".join(str(r[c]) for c in cols)+"\n")

# ---- per-gene AR model assignment -----------------------------------------
with open(f"{OUT}/gene_evidence_summary.tsv","w") as fh:
    fh.write("gene\tn_qualifying\tn_HIGH_pLoF\tn_MODERATE\tn_hom_alt\tn_multiallelic\tAR_model\tnote\n")
    for gene in sorted(panel):
        v = by_gene.get(gene, [])
        nh  = sum(1 for r in v if "pLoF" in r["flags"])
        nm  = sum(1 for r in v if r["impact"]=="MODERATE")
        nho = sum(1 for r in v if r["zyg"]=="HOM_ALT")
        nma = sum(1 for r in v if "MULTIALLELIC" in r["flags"])
        if   nho and nh:  model, note = "A_hom_pLoF", "homozygous putative LoF"
        elif nho:         model, note = "A_hom", "homozygous rare coding variant"
        elif nma:         model, note = "B_multiallelic", "two alt alleles at one site; phase unresolved"
        elif nh >= 2:     model, note = "B_two_pLoF", "candidate biallelic genotype; phase unresolved"
        elif nh == 1 and nm >= 1: model, note = "C_pLoF_plus_missense", "candidate biallelic genotype; phase unresolved"
        elif nh == 1:     model, note = "single_pLoF", "one pLoF allele only; no qualifying second allele"
        elif nm >= 2:     model, note = "B_two_missense", "candidate biallelic genotype; phase unresolved"
        elif nm == 1:     model, note = "single_missense", "one qualifying allele only"
        else:             model, note = "none", "no qualifying variant identified under the documented filters"
        fh.write(f"{gene}\t{len(v)}\t{nh}\t{nm}\t{nho}\t{nma}\t{model}\t{note}\n")

print(f"variants examined          : {stats['total']:,}")
print(f"qualifying panel variants  : {stats['qualifying']:,}")
print("\nEXCLUSION ACCOUNTING (nothing dropped silently):")
for k,v in sorted(excluded.items(), key=lambda x:-x[1]):
    print(f"  {k:24s} {v:,}")
print(f"\nwrote {OUT}/ar_screen_candidates.tsv")
print(f"wrote {OUT}/gene_evidence_summary.tsv")
