#!/usr/bin/env python3
"""
step14_cnv_sv_audit.py -- determine whether ANY evidence exists in the available
project inputs to assess copy-number or structural variation at the BUB1B locus.

HARD RULE ENFORCED HERE:
  FORMAT/DP is NOT CNV evidence and is never used as such. Called-site depth is
  ascertainment-biased (it exists only where a variant was called), there is no
  matched reference panel or control cohort, and this is a single sample. The
  script records DP's presence for completeness and then explicitly refuses to
  derive dosage from it.

The audit is a search for evidence, not an analysis. If the evidence is absent,
the script says so and stops -- it does not substitute a weaker proxy.

Usage:
  python3 analysis/scripts/step14_cnv_sv_audit.py [proband.vcf.gz]
"""
import subprocess, sys, os, re, glob, datetime

VCF = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/WGS_EX2312012_HGWCNDSX7.vcf.gz")
OUT = "analysis/data/cnv_sv"
SEARCH_ROOTS = [os.path.expanduser("~"), os.path.expanduser("~/mva-hackathon-2026"),
                os.path.expanduser("~/mva-hackathon-2026-1"), os.path.expanduser("~/Downloads")]
BUB1B = ("15", 40160984, 40221137)
os.makedirs(OUT, exist_ok=True)

log = []
def emit(s=""):
    print(s); log.append(s)

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

if not os.path.exists(VCF):
    sys.exit(f"FATAL: VCF not found: {VCF}")

emit("# BUB1B CNV / SV EVIDENCE AUDIT")
emit(f"\nrun date   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
emit(f"input VCF  : {os.path.basename(VCF)}  ({os.path.getsize(VCF):,} bytes)")
emit(f"bcftools   : {sh('bcftools --version').splitlines()[0]}")
emit(f"BUB1B      : GRCh38 chr{BUB1B[0]}:{BUB1B[1]:,}-{BUB1B[2]:,}")

hdr = sh(f"bcftools view -h {VCF}")
findings = {}

emit("\n## 1. Symbolic ALT alleles declared in the VCF header (`##ALT`)")
alts = re.findall(r"^##ALT=<ID=([^,>]+)", hdr, re.M)
emit(f"    declared: {alts or 'NONE'}")
findings["symbolic_alt_declared"] = bool(alts)

emit("\n## 2. Symbolic ALT alleles actually present in records (<DEL>, <DUP>, <CNV>, <INV>, <INS>)")
n_sym = sh(f"bcftools view -H {VCF} | awk '$5 ~ /^</' | wc -l").strip()
emit(f"    records with a symbolic ALT: {n_sym}")
findings["symbolic_alt_records"] = int(n_sym or 0) > 0

emit("\n## 3. Breakend (BND) records")
n_bnd = sh(f"bcftools view -H {VCF} | awk '$5 ~ /\\[|\\]/' | wc -l").strip()
emit(f"    BND-style records: {n_bnd}")
findings["bnd_records"] = int(n_bnd or 0) > 0

emit("\n## 4. SV/CNV INFO keys (SVTYPE, SVLEN, END, CIPOS, CIEND, IMPRECISE, CN, ...)")
sv_keys = ["SVTYPE","SVLEN","END","CIPOS","CIEND","IMPRECISE","CN","CNQ","CNV","NUMSNP","BC","FOLD_CHANGE"]
info_keys = set(re.findall(r"^##INFO=<ID=([A-Za-z0-9_]+)", hdr, re.M))
fmt_keys  = set(re.findall(r"^##FORMAT=<ID=([A-Za-z0-9_]+)", hdr, re.M))
for k in sv_keys:
    where = []
    if k in info_keys: where.append("INFO")
    if k in fmt_keys:  where.append("FORMAT")
    emit(f"    {k:12s} {'declared in ' + '/'.join(where) if where else 'ABSENT'}")
findings["sv_info_keys"] = any(k in info_keys or k in fmt_keys for k in sv_keys)

emit("\n## 5. gVCF reference blocks (<NON_REF>)")
n_nonref = sh(f"bcftools view -H {VCF} | head -200000 | awk '$5 ~ /NON_REF/' | wc -l").strip()
emit(f"    <NON_REF> records in first 200k: {n_nonref}")
emit(f"    => {'gVCF' if int(n_nonref or 0) > 0 else 'NOT a gVCF (site-level VCF only; no reference-block depth)'}")
findings["gvcf"] = int(n_nonref or 0) > 0

emit("\n## 6. Read-depth / dosage FORMAT fields usable for CNV")
emit(f"    FORMAT keys declared: {sorted(fmt_keys)}")
emit("    DP is present, but:")
emit("      *** FORMAT/DP IS NOT CNV EVIDENCE AND IS NOT USED HERE. ***")
emit("      Called-site depth is ascertainment-biased (present only where a variant")
emit("      was called), has no matched control cohort or reference panel, and this")
emit("      is a single sample. Any 'CNV' derived from it would be uninterpretable.")
findings["usable_depth_track"] = False

emit("\n## 7. Split-read / discordant-pair evidence")
emit("    Requires aligned reads. Checked for BAM/CRAM below.")
emit("    No SR/PE/PR-style FORMAT fields are declared in this VCF: "
     f"{[k for k in ('SR','PE','PR','RP','RR') if k in fmt_keys] or 'NONE'}")
findings["split_read_fields"] = any(k in fmt_keys for k in ("SR","PE","PR","RP","RR"))

emit("\n## 8. Aligned reads / raw data on disk")
pats = ["*.bam","*.cram","*.fastq.gz","*.fq.gz","*.fastq","*.fq"]
hits = []
for root in SEARCH_ROOTS:
    if not os.path.isdir(root): continue
    for p in pats:
        hits += glob.glob(os.path.join(root, p)) + glob.glob(os.path.join(root, "*", p))
hits = sorted(set(hits))
emit(f"    searched: {[os.path.basename(r) or r for r in SEARCH_ROOTS]}")
emit(f"    patterns: {pats}")
emit(f"    found   : {hits or 'NONE'}")
findings["aligned_reads"] = bool(hits)

emit("\n## 9. Pre-computed CNV / SV call sets in the project")
cnv_pats = ["*cnv*","*CNV*","*sv*.vcf*","*SV*.vcf*","*manta*","*delly*","*lumpy*","*gcnv*","*cnvnator*","*.seg","*.cns","*.cnr"]
chits = []
for root in SEARCH_ROOTS:
    if not os.path.isdir(root): continue
    for p in cnv_pats:
        chits += [x for x in glob.glob(os.path.join(root, p)) + glob.glob(os.path.join(root, "*", p))
                  if os.path.isfile(x)]
chits = sorted(set(chits))
emit(f"    patterns: {cnv_pats}")
emit(f"    found   : {chits or 'NONE'}")
findings["precomputed_calls"] = bool(chits)

emit("\n## 10. Variant content at the BUB1B locus (for completeness only)")
n_locus = sh(f"bcftools view -H -r {BUB1B[0]}:{BUB1B[1]}-{BUB1B[2]} {VCF} | wc -l").strip()
n_sym_locus = sh(f"bcftools view -H -r {BUB1B[0]}:{BUB1B[1]}-{BUB1B[2]} {VCF} | awk '$5 ~ /^</' | wc -l").strip()
emit(f"    records in BUB1B gene body : {n_locus}")
emit(f"    of which symbolic/SV       : {n_sym_locus}")
emit("    (small SNV/indel records only; these cannot reveal exon-level dosage)")

emit("\n## VERDICT")
avail = [k for k, v in findings.items() if v]
emit(f"    evidence types found: {avail or 'NONE'}")
if not any(findings.values()):
    emit("\n    >>> CNV/SV status unresolved from available data. <<<")
    emit("\n    No symbolic alleles, no SV/CNV INFO keys, no gVCF reference blocks,")
    emit("    no usable depth track, no split-read/discordant-pair fields, no BAM/CRAM,")
    emit("    no FASTQ, and no pre-computed CNV or SV call sets were found.")
    emit("    A CNV or SV second hit in BUB1B -- for example a single- or multi-exon")
    emit("    deletion on the allele not carrying p.Leu737* -- CANNOT BE EXCLUDED.")
else:
    emit("\n    Some evidence types were detected; review them before concluding.")

emit("\n## Minimum practical assay to test BUB1B exon dosage")
emit("    NONE OF THE FOLLOWING HAS BEEN PERFORMED. This is a recommendation only.")
emit("""
| Assay | What it measures | Resolution | Practicality | Notes |
|---|---|---|---|---|
| **MLPA** (e.g. a custom BUB1B probemix) | relative copy number, exon by exon | single-exon | Established clinical method; needs ~100 ng DNA; a BUB1B-specific probemix may need custom design | **Most practical first-line dosage test.** Covers all 23 exons in one reaction. |
| **qPCR** (relative dosage vs 2-copy reference) | copy number at selected exons | per-amplicon | Cheapest; any lab with a qPCR machine | Needs 2-3 reference loci and replicate design; only interrogates the exons assayed, so a deletion elsewhere is missed. |
| **ddPCR** | absolute copy number | per-amplicon | More precise than qPCR, less common | Best when a specific exon is already suspected. |
| **Targeted / exome CNV calling from reads** | read-depth ratio | multi-exon | Requires BAM/CRAM, which do not exist here | Would need re-alignment of the ~85 GB raw data, if obtainable. |
| **Long-read WGS** | SV breakpoints AND phase | base-level | Highest cost | **Resolves CNV/SV and phase in one experiment.** |

    Practical note: a dosage assay only interrogates the region it targets. A
    negative MLPA/qPCR result narrows the space; it does not exclude every SV
    class (balanced inversions and translocations disrupting BUB1B would be
    missed by dosage methods entirely).""")

open(f"{OUT}/CNV_SV_REPORT.md", "w").write("\n".join(log) + "\n")
print(f"\nwrote {OUT}/CNV_SV_REPORT.md")
