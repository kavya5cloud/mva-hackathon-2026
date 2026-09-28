#!/usr/bin/env python3
"""
step0_verify_provenance.py  --  BLOCKING PRE-REQUISITE for this repository.

WHY THIS EXISTS
---------------
The extraction command recorded in MVA_Hackathon_2026_Track1_METHODS.md:

    bcftools view -r 15:40400000-40500000 WGS_EX2312012_HGWCNDSX7.vcf.gz

cannot have returned either variant of interest, under EITHER genome build:

    BUB1B  GRCh38 chr15:40,160,984-40,221,137   overlap with that window =      0 bp
    BUB1B  GRCh37 chr15:40,453,224-40,513,337   overlap with that window = 46,770 bp
    c.2210T>G  GRCh38 40,209,701 | GRCh37 40,501,902  -> OUTSIDE the window in both
    c.3006T>G  GRCh38 40,220,612 | GRCh37 40,512,813  -> OUTSIDE the window in both

This script therefore verifies provenance directly against the proband VCF:
 1. prints header provenance (##reference, ##contig, GATK command line)
 2. infers the genome build from the chr15 contig length
 3. extracts the CORRECT BUB1B interval for that build
 4. reports presence/absence, REF/ALT, FILTER, GT, DP, GQ, AD for both variants
 5. reports phasing tags and states the phase conclusion

chr15 contig lengths (Ensembl REST, verified 2026-09-15):
    GRCh38 = 101,991,189
    GRCh37 = 102,531,392

PHASING TAGS -- IMPORTANT
-------------------------
GATK HaplotypeCaller emits physical phasing as FORMAT/PGT + FORMAT/PID.
It does NOT emit FORMAT/PS (that is WhatsHap/HapCUT2 convention).
An earlier revision of this script queried %PS unconditionally; because PS is not
declared in this VCF's header, `bcftools query` exited non-zero with an empty
stdout, which was misread as "variant not present" -- a FALSE NEGATIVE.
This version queries only tags that are actually declared in the header, and
surfaces bcftools stderr instead of swallowing it.

Usage:
    python3 analysis/scripts/step0_verify_provenance.py <proband.vcf.gz>

Requires bcftools on PATH (developed and run against bcftools 1.24).
"""
import subprocess, sys, re, os, hashlib

VCF = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
OUT = "analysis/data/provenance"
os.makedirs(OUT, exist_ok=True)

# build -> (chr15 length, BUB1B start, BUB1B end, pos c.2210T>G, pos c.3006T>G)
BUILDS = {
    "GRCh38": (101991189, 40160984, 40221137, 40209701, 40220612),
    "GRCh37": (102531392, 40453224, 40513337, 40501902, 40512813),
}
TARGETS = [("c.2210T>G p.Leu737*", "T", "G", 3), ("c.3006T>G p.Asn1002Lys", "T", "G", 4)]
MARGIN = 2000

def sh(cmd, required=True):
    """Run cmd; return stdout. Raise loudly on failure rather than returning ''."""
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        msg = f"COMMAND FAILED (exit {p.returncode}): {cmd}\nstderr: {p.stderr.strip()}"
        if required:
            sys.exit("ERROR: " + msg)
        print("  WARNING: " + msg)
    return p.stdout

print("### 0. Input file")
print(f"  path : {VCF}")
print(f"  size : {os.path.getsize(VCF):,} bytes")
h = hashlib.md5()
with open(VCF, "rb") as fh:
    for chunk in iter(lambda: fh.read(1 << 20), b""):
        h.update(chunk)
print(f"  md5  : {h.hexdigest()}")
print(f"  bcftools: {sh('bcftools --version').splitlines()[0]}")

print("\n### 1. VCF header provenance")
hdr = sh(f"bcftools view -h {VCF}")
prov = [l for l in hdr.splitlines()
        if re.match(r"^##(reference|source|fileformat)", l)
        or re.match(r"^##contig=<ID=(chr)?15,", l)]
print("\n".join("  " + l for l in prov))
gatk = [l for l in hdr.splitlines() if l.startswith("##GATKCommandLine")]
samples = sh(f"bcftools query -l {VCF}").split()
print(f"  sample(s): {samples}")
open(f"{OUT}/header_provenance.txt", "w").write("\n".join(prov + gatk + [f"samples={samples}"]))

print("\n### 2. Infer genome build from chr15 contig length")
m = re.search(r"^##contig=<ID=(chr)?15,.*?length=(\d+)", hdr, re.M)
if not m:
    sys.exit("ERROR: no chr15 contig line in header - cannot infer build.")
length, chrprefix = int(m.group(2)), (m.group(1) or "")
build = next((b for b, v in BUILDS.items() if v[0] == length), None)
print(f"  chr15 length = {length:,}   contig naming = '{chrprefix}15'")
if build is None:
    sys.exit(f"ERROR: chr15 length {length:,} matches neither build. Resolve manually.")
print(f"  ==> INFERRED BUILD: {build}")
ref = [l for l in hdr.splitlines() if l.startswith("##reference")]
print(f"  cross-check ##reference: {ref[0] if ref else 'ABSENT'}")

_, gs, ge, p1, p2 = BUILDS[build]
region = f"{chrprefix}15:{gs-MARGIN}-{ge+MARGIN}"

print(f"\n### 3. Correct BUB1B extraction for {build}")
print(f"  bcftools view -r {region} {VCF}")
n = sh(f"bcftools view -H -r {region} {VCF} | wc -l").strip()
print(f"  variants in the BUB1B locus: {n}")
sh(f"bcftools view -r {region} {VCF} -Oz -o {OUT}/bub1b_region_{build}.vcf.gz")
sh(f"bcftools index -f -t {OUT}/bub1b_region_{build}.vcf.gz")
print(f"  written: {OUT}/bub1b_region_{build}.vcf.gz (+ .tbi)")
sh(f"bcftools query -r {region} -f '%POS\\t%REF\\t%ALT\\t%FILTER\\t[%GT\\t%DP\\t%GQ\\t%AD]\\n' "
   f"{VCF} > {OUT}/bub1b_locus_variants.tsv")
print(f"  written: {OUT}/bub1b_locus_variants.tsv")

# Only query FORMAT tags that are actually declared, so an undeclared tag can
# never turn into a silent false negative (see module docstring).
declared = set(re.findall(r"^##FORMAT=<ID=([A-Za-z0-9_]+)", hdr, re.M))
phase_tags = [t for t in ("PS", "PGT", "PID") if t in declared]
fmt = "%POS\\t%REF\\t%ALT\\t%FILTER\\t[%GT\\t%DP\\t%GQ\\t%AD" + \
      "".join(f"\\t[%{t}]" if False else f"\\t[%{t}]" for t in []) + "]"
extra = "".join(f"\\t[%{t}]" for t in phase_tags)
print(f"\n  FORMAT tags declared: {sorted(declared)}")
print(f"  phasing tags present in header: {phase_tags or 'NONE'}"
      f"   (GATK uses PGT/PID; PS is WhatsHap/HapCUT2 convention)")

print(f"\n### 4. Are the two variants of interest present?  (build {build})")
results = {}
for label, eref, ealt, _ in TARGETS:
    pos = p1 if "2210" in label else p2
    q = sh(f"bcftools query -r {chrprefix}15:{pos}-{pos} "
           f"-f '%POS\\t%REF\\t%ALT\\t%FILTER\\t[%GT\\t%DP\\t%GQ\\t%AD]{extra}\\n' {VCF}",
           required=False).strip()
    print(f"\n  --- {label}  (expected {chrprefix}15:{pos} {eref}>{ealt})")
    if not q:
        print("      ** NOT PRESENT AT THIS POSITION **")
        results[label] = None
        continue
    for line in q.splitlines():
        f = line.split("\t")
        rec = dict(zip(["POS","REF","ALT","FILTER","GT","DP","GQ","AD"] + phase_tags, f))
        match = (rec["REF"] == eref and rec["ALT"] == ealt)
        print(f"      POS={rec['POS']}  REF={rec['REF']}  ALT={rec['ALT']}  "
              f"{'<-- REF/ALT MATCH' if match else '<-- REF/ALT MISMATCH'}")
        print(f"      FILTER={rec['FILTER']}  GT={rec['GT']}  DP={rec['DP']}  GQ={rec['GQ']}  AD={rec['AD']}")
        for t in phase_tags:
            print(f"      {t}={rec.get(t)}")
        try:
            r_, a_ = (int(x) for x in rec["AD"].split(",")[:2])
            print(f"      VAF={a_/(r_+a_):.3f}  (allele balance)")
        except Exception:
            pass
        results[label] = rec

print("\n### 5. VERDICT")
present = [k for k, v in results.items() if v]
if len(present) == len(TARGETS):
    print("  Both variants ARE present in the proband VCF -> PROVENANCE RESOLVED.")
    gts = {k: v["GT"] for k, v in results.items()}
    print(f"  Genotypes: {gts}")
    unphased = all("/" in g for g in gts.values())
    print("\n  PHASE:")
    if unphased:
        print("    Both genotypes use '/' (unphased). No shared phasing group links them.")
        print("    ==> PHASE IS UNKNOWN from this VCF.")
    else:
        print("    At least one genotype is '|'-delimited - inspect the phasing group carefully.")
    print("    The two sites are 10,911 bp apart. GATK PGT/PID physical phasing only")
    print("    links variants within a single read/fragment (~350-550 bp here), so it")
    print("    CANNOT span this pair. Trio genotyping or long-read sequencing is required.")
    print("\n  Do NOT write 'compound heterozygous', 'biallelic' or 'in trans'.")
else:
    print("  ** AT LEAST ONE VARIANT IS ABSENT. Downstream claims about it are void. **")
