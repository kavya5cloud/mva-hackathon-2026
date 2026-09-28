#!/usr/bin/env python3
"""
step13_phase_audit.py -- exhaustive audit of what phasing information the source
VCF does and does not contain for the two BUB1B variants of interest.

SCIENTIFIC CONSTRAINTS (enforced in code, not just prose):
  * Phase is NEVER inferred from allele balance, genotype quality, read depth, or
    physical proximity. Only explicit phasing encodings count:
      - a '|' separator in GT, AND
      - a shared phase-set identifier (PS, or GATK's PID) across BOTH variants.
  * A missing phase field is UNPHASED / INSUFFICIENT_DATA. It is never silently
    read as cis or trans.
  * If an expected field is absent from the VCF header, the script says so loudly
    rather than substituting a default.

VARIANTS AUDITED (GRCh38):
  chr15:40,209,701 T>G   NM_001211.6:c.2210T>G   p.Leu737*
  chr15:40,220,612 T>G   NM_001211.6:c.3006T>G   p.Asn1002Lys

CLASSIFICATION (exactly one is emitted):
  PHASED_IN_TRANS    both '|' , shared phase set, alt alleles on opposite haplotypes
  PHASED_IN_CIS      both '|' , shared phase set, alt alleles on the same haplotype
  UNPHASED           variants present and callable, but no phase encoding links them
  INSUFFICIENT_DATA  a variant is absent, or the data cannot support the question

Usage:
  python3 analysis/scripts/step13_phase_audit.py [proband.vcf.gz]
"""
import subprocess, sys, os, re, hashlib, datetime

VCF = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/WGS_EX2312012_HGWCNDSX7.vcf.gz")
OUT = "analysis/data/phase"
os.makedirs(OUT, exist_ok=True)

TARGETS = [
    dict(label="p.Leu737*",     hgvs="NM_001211.6:c.2210T>G", chrom="15", pos=40209701, ref="T", alt="G"),
    dict(label="p.Asn1002Lys",  hgvs="NM_001211.6:c.3006T>G", chrom="15", pos=40220612, ref="T", alt="G"),
]
# FORMAT/INFO keys that could conceivably carry phase information
PHASE_KEYS = ["PS", "PGT", "PID", "HP", "PQ", "PW", "PHASE", "PSET", "HAP", "BX", "MI"]

def sh(cmd, required=True):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0 and required:
        sys.exit(f"FATAL: command failed (exit {p.returncode}): {cmd}\nstderr: {p.stderr.strip()}")
    return p.stdout

if not os.path.exists(VCF):
    sys.exit(f"FATAL: VCF not found: {VCF}")

log = []
def emit(s=""):
    print(s); log.append(s)

emit("# BUB1B PHASE AUDIT")
emit(f"\nrun date          : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
emit(f"input VCF         : {os.path.basename(VCF)}")
emit(f"input path        : (local path withheld from the committed record)")
emit(f"size              : {os.path.getsize(VCF):,} bytes")
h = hashlib.md5()
with open(VCF, "rb") as fh:
    for c in iter(lambda: fh.read(1 << 20), b""): h.update(c)
emit(f"md5               : {h.hexdigest()}")
emit(f"bcftools          : {sh('bcftools --version').splitlines()[0]}")
emit(f"python            : {sys.version.split()[0]}")

hdr = sh(f"bcftools view -h {VCF}")
samples = sh(f"bcftools query -l {VCF}").split()
emit(f"\nsample ID(s)      : {samples}")
if len(samples) != 1:
    emit(f"NOTE: expected a single-sample VCF; found {len(samples)}.")

fmt_keys = set(re.findall(r"^##FORMAT=<ID=([A-Za-z0-9_]+)", hdr, re.M))
info_keys = set(re.findall(r"^##INFO=<ID=([A-Za-z0-9_]+)", hdr, re.M))
emit(f"\nFORMAT keys declared : {sorted(fmt_keys)}")
emit(f"INFO keys declared   : {sorted(info_keys)}")

present_phase_fmt  = [k for k in PHASE_KEYS if k in fmt_keys]
present_phase_info = [k for k in PHASE_KEYS if k in info_keys]
emit(f"\nphase-related FORMAT keys present : {present_phase_fmt or 'NONE'}")
emit(f"phase-related INFO keys present   : {present_phase_info or 'NONE'}")
for k in PHASE_KEYS:
    if k not in fmt_keys and k not in info_keys:
        emit(f"  ABSENT (declared nowhere): {k}")

# Query only declared keys so an undeclared tag can never crash bcftools and be
# misread as 'variant not present' (this exact bug occurred in Round 3).
query_fmt = ["GT", "DP", "GQ", "AD"] + present_phase_fmt
fstr = "%CHROM\\t%POS\\t%REF\\t%ALT\\t%FILTER" + "".join(f"\\t[%{k}]" for k in query_fmt) + "\\n"

emit("\n## Per-variant record")
results = {}
for t in TARGETS:
    emit(f"\n### {t['label']}  ({t['hgvs']})")
    emit(f"    expected: chr{t['chrom']}:{t['pos']:,} {t['ref']}>{t['alt']}")
    raw = sh(f"bcftools query -r {t['chrom']}:{t['pos']}-{t['pos']} -f '{fstr}' {VCF}", required=False).strip()
    if not raw:
        emit("    ** VARIANT NOT PRESENT AT THIS POSITION **")
        results[t['label']] = None
        continue
    for line in raw.splitlines():
        vals = line.split("\t")
        rec = dict(zip(["CHROM","POS","REF","ALT","FILTER"] + query_fmt, vals))
        ok = rec["REF"] == t["ref"] and rec["ALT"] == t["alt"]
        emit(f"    observed: {rec['CHROM']}:{rec['POS']} {rec['REF']}>{rec['ALT']}  "
             f"{'REF/ALT MATCH' if ok else '** REF/ALT MISMATCH **'}")
        emit(f"    FILTER = {rec['FILTER']}")
        emit(f"    GT     = {rec['GT']}   ({'PHASED separator |' if '|' in rec['GT'] else 'UNPHASED separator /'})")
        emit(f"    DP     = {rec.get('DP')}    GQ = {rec.get('GQ')}    AD = {rec.get('AD')}")
        for k in present_phase_fmt:
            v = rec.get(k)
            emit(f"    {k:6s} = {v}   {'(no value -- this variant is not in a phase set)' if v in ('.', '', None) else ''}")
        for k in PHASE_KEYS:
            if k not in present_phase_fmt and k not in present_phase_info:
                emit(f"    {k:6s} = FIELD NOT PRESENT IN THIS VCF")
        results[t['label']] = rec

emit("\n## Distance between the two variants")
d = TARGETS[1]["pos"] - TARGETS[0]["pos"]
emit(f"    {TARGETS[1]['pos']:,} - {TARGETS[0]['pos']:,} = {d:,} bp")

emit("\n## Shared phase set?")
a, b = results[TARGETS[0]['label']], results[TARGETS[1]['label']]
shared = None
if a is None or b is None:
    emit("    Cannot evaluate: at least one variant is absent.")
else:
    for k in present_phase_fmt:
        va, vb = a.get(k), b.get(k)
        usable = va not in ('.', '', None) and vb not in ('.', '', None)
        emit(f"    {k}: variant1={va!r}  variant2={vb!r}  -> "
             f"{'SHARED' if usable and va == vb else ('both empty' if not usable else 'different')}")
        if usable and va == vb:
            shared = k
    if not present_phase_fmt:
        emit("    No phase-related FORMAT key exists in this VCF at all.")
    emit(f"    => shared phase set: {shared or 'NONE'}")

emit("\n## CLASSIFICATION")
both_present = a is not None and b is not None
both_bar = both_present and "|" in a["GT"] and "|" in b["GT"]
if not both_present:
    verdict = "INSUFFICIENT_DATA"
    why = "at least one variant is absent from the VCF"
elif both_bar and shared:
    ha = a["GT"].split("|"); hb = b["GT"].split("|")
    same = (ha.index("1") == hb.index("1")) if ("1" in ha and "1" in hb) else None
    verdict = "PHASED_IN_CIS" if same else "PHASED_IN_TRANS"
    why = f"both GT use '|' and share phase set {shared}"
else:
    verdict = "UNPHASED"
    reasons = []
    if not both_bar: reasons.append("GT uses the unphased '/' separator")
    if not shared:   reasons.append("no shared phase-set identifier links the two variants")
    why = "; ".join(reasons)

emit(f"\n    >>> {verdict} <<<")
emit(f"    reason: {why}")

if verdict in ("UNPHASED", "INSUFFICIENT_DATA"):
    emit("\n    Phase CANNOT be determined from this VCF.")
    emit("    Phase was NOT inferred from allele balance, GQ, DP, or physical proximity.")
    emit("\n    What would resolve it:")
    emit(f"      1. Parental/trio genotyping of both sites. Definitive when informative")
    emit(f"         (each variant from a different parent); confounded by non-paternity,")
    emit(f"         parental germline mosaicism, or a de novo event.")
    emit(f"      2. Long-read sequencing (PacBio HiFi / ONT). Reads routinely exceed")
    emit(f"         {d:,} bp, so a single proband sample suffices -- no parents needed.")
    emit(f"      3. Linked-read or Hi-C/Pore-C phasing (10x Chromium is discontinued;")
    emit(f"         Hi-C/Pore-C is the current equivalent).")
    emit(f"      4. Allele-specific long-range PCR across {d:,} bp followed by")
    emit(f"         sequencing of the amplicon.")
    emit("\n    NOT acceptable as evidence of phase:")
    emit("      - statistical/population phasing of two ultra-rare variants absent from panels")
    emit("      - short-read physical phasing (fragments ~350-550 bp cannot span 10.9 kb)")
    emit("      - ACMG PM3-style reasoning, or 'both are het so probably trans'")

open(f"{OUT}/PHASE_REPORT.md", "w").write("\n".join(log) + "\n")
print(f"\nwrote {OUT}/PHASE_REPORT.md")
sys.exit(0)
