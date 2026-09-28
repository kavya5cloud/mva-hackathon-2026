#!/usr/bin/env python3
"""
step12_splice_screen.py -- SpliceAI screen of the BUB1B locus intronic variants,
to test for a hidden cryptic-splice second hit.

CONTEXT
  BUB1B is CASE B: p.Leu737* is a strong pathogenic allele; p.Asn1002Lys is a
  prioritised VUS; phase is UNKNOWN; CNV/SV is unavailable from this VCF. A
  cryptic-splice second hit is one of the two remaining hidden-variant classes
  (the other being CNV/SV, which this data cannot address at all).

IMPORTANT CORRECTION carried into this script
  The Round 4 record described "68 intronic BUB1B variants". Re-checking the
  snpEff gene assignment shows only **12** of those 68 are annotated to BUB1B;
  the other **56 are PAK6** (the adjacent gene -- BUB1B and PAK6 overlap at the
  3' end and form the BUB1B-PAK6 readthrough locus). All 68 are screened here
  for completeness, but the gene column distinguishes them and the BUB1B
  conclusion rests on the 12.

INPUT   the gated proband VCF (GRCh38, GATK 4.2.4.0), locus chr15:40,110,984-40,271,137
OUTPUT  analysis/data/splicing/

METHOD
  1. Extract locus variants from the gated VCF (exact CHROM/POS/REF/ALT preserved).
  2. Left-align and normalize with `bcftools norm -f <chr15 FASTA>`; record any change.
  3. Run SpliceAI against the bundled GRCh38 gene annotation.
  4. Parse the SPLICEAI INFO field and classify by max delta score.

  Failure handling (explicit, per the brief): a variant with no SPLICEAI field is
  recorded as PREDICTION_UNAVAILABLE and is NEVER scored as zero. Tool crashes are
  recorded as TOOL_FAILURE. Variants SpliceAI declines (e.g. outside any annotated
  gene, or ref mismatch) are recorded as UNSUPPORTED_VARIANT.

PRIORITISATION CATEGORIES (these are triage buckets, NOT pathogenicity calls)
  max DS  < 0.05                 NO SIGNAL
  0.05 <= max DS < 0.20          LOW PRIORITY
  0.20 <= max DS < 0.50          REVIEW
  max DS >= 0.50                 HIGH-PRIORITY SPLICE CANDIDATE
  (SpliceAI authors' reference points: 0.2 high recall, 0.5 recommended, 0.8 high precision)
"""
import subprocess, sys, os, gzip, json, shutil

VCF   = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/WGS_EX2312012_HGWCNDSX7.vcf.gz")
FASTA = sys.argv[2] if len(sys.argv) > 2 else "chr15.fa"
OUT   = "analysis/data/splicing"
PY    = "/opt/anaconda3/bin/python3"
REG   = "15:40110984-40271137"
os.makedirs(OUT, exist_ok=True)

def run(cmd, **kw):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)
    return p

print("### 1. Extract locus variants (exact CHROM/POS/REF/ALT preserved)")
raw = f"{OUT}/locus_raw.vcf"
run(f"bcftools view -r {REG} {VCF} -Ov -o {raw}")
n_raw = int(run(f"bcftools view -H {raw} | wc -l").stdout.strip())
print(f"  variants extracted: {n_raw}")

print("\n### 2. Normalize (left-align, split multiallelics)")
norm = f"{OUT}/locus_normalized.vcf"
r = run(f"bcftools norm -f {FASTA} -m -any {raw} -Ov -o {norm}")
print("  bcftools norm stderr:", (r.stderr or "").strip().replace("\n", " | ")[:300])
n_norm = int(run(f"bcftools view -H {norm} | wc -l").stdout.strip())
print(f"  variants after normalization: {n_norm}  ({'changed' if n_norm != n_raw else 'no change in count'})")

print("\n### 3. Run SpliceAI")
sa_out = f"{OUT}/spliceai_output.vcf"
log    = f"{OUT}/spliceai_run.log"
PARSE_ONLY = "--parse-only" in sys.argv and os.path.exists(sa_out)
if PARSE_ONLY:
    print(f"  --parse-only: reusing existing {sa_out} (model not re-run)")
cmd = (f"{PY} -m spliceai -I {norm} -O {sa_out} -R {FASTA} -A grch38 -D 500 -M 0")
print(f"  command: {cmd}")
env = dict(os.environ, TF_CPP_MIN_LOG_LEVEL="3", TF_USE_LEGACY_KERAS="1")
if PARSE_ONLY and os.path.exists(sa_out):
    class _R: returncode=0; stdout=""; stderr=""
    r=_R()
else:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
if not (PARSE_ONLY and os.path.exists(sa_out)):
    open(log, "w").write((r.stdout or "") + "\n--- STDERR ---\n" + (r.stderr or ""))
print(f"  exit code: {r.returncode}   (log: {log})")
if r.returncode != 0:
    print("  *** SpliceAI FAILED. Last stderr lines: ***")
    print("\n".join("    " + l for l in (r.stderr or "").strip().split("\n")[-12:]))
    print("\n  TOOL_FAILURE recorded. No scores are fabricated. Stopping.")
    sys.exit(1)

print("\n### 4. Parse SPLICEAI annotations")
# SPLICEAI=ALLELE|SYMBOL|DS_AG|DS_AL|DS_DG|DS_DL|DP_AG|DP_AL|DP_DG|DP_DL
rows = []
for line in open(sa_out):
    if line.startswith("#"): continue
    f = line.rstrip("\n").split("\t")
    chrom, pos, _id, ref, alt, qual, filt, info = f[:8]
    smp = f[9] if len(f) > 9 else ""
    gt = smp.split(":")[0] if smp else "NA"
    sa = None
    for kv in info.split(";"):
        # SpliceAI v1.3.1 writes the key as "SpliceAI=" (mixed case). Match
        # case-insensitively so a casing change can never silently produce a
        # file full of PREDICTION_UNAVAILABLE.
        if kv.upper().startswith("SPLICEAI="):
            sa = kv.split("=", 1)[1]; break
    base = dict(chrom=chrom, pos=int(pos), ref=ref, alt=alt, filter=filt, gt=gt)
    if sa is None:
        rows.append(dict(base, gene="NA", ds_ag=None, ds_al=None, ds_dg=None, ds_dl=None,
                         dp_ag=None, dp_al=None, dp_dg=None, dp_dl=None,
                         max_ds=None, status="PREDICTION_UNAVAILABLE", effect="-"))
        continue
    for entry in sa.split(","):
        p = entry.split("|")
        if len(p) < 10:
            rows.append(dict(base, gene="NA", ds_ag=None, ds_al=None, ds_dg=None, ds_dl=None,
                             dp_ag=None, dp_al=None, dp_dg=None, dp_dl=None,
                             max_ds=None, status="UNSUPPORTED_VARIANT", effect="-")); continue
        _a, sym = p[0], p[1]
        try:
            ds = [float(x) for x in p[2:6]]; dp = [int(x) for x in p[6:10]]
        except ValueError:
            rows.append(dict(base, gene=sym, ds_ag=None, ds_al=None, ds_dg=None, ds_dl=None,
                             dp_ag=None, dp_al=None, dp_dg=None, dp_dl=None,
                             max_ds=None, status="PREDICTION_UNAVAILABLE", effect="-")); continue
        labels = ["acceptor_gain","acceptor_loss","donor_gain","donor_loss"]
        mx = max(ds); eff = labels[ds.index(mx)] if mx > 0 else "none"
        if   mx < 0.05: cat = "NO SIGNAL"
        elif mx < 0.20: cat = "LOW PRIORITY"
        elif mx < 0.50: cat = "REVIEW"
        else:           cat = "HIGH-PRIORITY SPLICE CANDIDATE"
        rows.append(dict(base, gene=sym, ds_ag=ds[0], ds_al=ds[1], ds_dg=ds[2], ds_dl=ds[3],
                         dp_ag=dp[0], dp_al=dp[1], dp_dg=dp[2], dp_dl=dp[3],
                         max_ds=round(mx,4), status=cat,
                         effect=f"{eff}@{dp[ds.index(mx)]:+d}nt" if mx > 0 else "none"))

cols = ["chrom","pos","ref","alt","filter","gt","gene","ds_ag","ds_al","ds_dg","ds_dl",
        "dp_ag","dp_al","dp_dg","dp_dl","max_ds","effect","status"]
with open(f"{OUT}/spliceai_parsed.tsv","w") as fh:
    fh.write("\t".join(cols)+"\n")
    for r_ in sorted(rows, key=lambda x: (-(x["max_ds"] if x["max_ds"] is not None else -1), x["pos"])):
        fh.write("\t".join("" if r_[c] is None else str(r_[c]) for c in cols)+"\n")

from collections import Counter
print(f"  annotation records parsed: {len(rows)}")
print("\n  status breakdown:")
for k,v in Counter(x["status"] for x in rows).most_common():
    print(f"    {k:34s} {v}")
print("\n  by gene:")
for k,v in Counter(x["gene"] for x in rows).most_common():
    print(f"    {k:12s} {v}")
n_ok = sum(1 for x in rows if x["max_ds"] is not None)
if n_ok == 0 and rows:
    print("\n  *** GUARD TRIPPED: 0/%d records carry a usable score. ***" % len(rows))
    print("  This is a PARSING or TOOL problem, not evidence of 'no splice effect'.")
    print("  Inspect the INFO key casing in the SpliceAI output before interpreting.")
json.dump(rows, open(f"{OUT}/spliceai_parsed.json","w"), indent=2)
print(f"\nwrote {OUT}/spliceai_parsed.tsv and .json")
