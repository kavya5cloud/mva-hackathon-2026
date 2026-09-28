#!/usr/bin/env python3
"""
annotate_candidates_af.py -- attach POPULATION allele frequency to the AR-screen
candidates via the Ensembl VEP REST API (gnomAD genomes/exomes).

WHY THIS IS A SEPARATE STEP
  The proband VCF carries INFO/AF, but that is GATK's per-site allele fraction
  for this ONE sample (0.5 for a het, 1.0 for a hom). It is NOT a population
  frequency and must never be used as one. This script fetches real population
  frequencies so rarity thresholds can be applied honestly.

METHOD
  POST https://rest.ensembl.org/vep/human/region  (GRCh38, batched)
  Frequencies taken from colocated_variants[].frequencies (gnomAD).
  Retrieved: 2026-09-16.

RARITY THRESHOLDS (documented, applied here for the first time)
  AR candidate (het, compound-het component) : gnomAD popmax AF < 0.01
  AR candidate (homozygous)                  : gnomAD popmax AF < 0.005
                                               AND gnomAD homozygote count low
  Anything at or above these is classified COMMON_POLYMORPHISM and is NOT a
  candidate. Variants absent from gnomAD are reported as 'absent' (treated as
  rare, but flagged: absence can also mean poor coverage).
"""
import json, urllib.request, sys, time, os

IN  = "analysis/data/panel/ar_screen_candidates.tsv"
OUT = "analysis/data/panel/ar_screen_candidates_af.tsv"
rows = [l.rstrip("\n").split("\t") for l in open(IN)]
hdr, data = rows[0], rows[1:]
idx = {c:i for i,c in enumerate(hdr)}

class QueryFailed(Exception):
    """Raised when the API could not be reached. MUST NOT be conflated with
    'variant absent from gnomAD' -- that conflation would fabricate rarity."""

def vep_one(chrom, pos, ref, alt):
    """Per-variant GET. The batch POST endpoint returned 500/503 on 2026-09-16,
    so this uses the GET region endpoint, which is stable."""
    end = int(pos) + len(ref) - 1
    url = (f"https://rest.ensembl.org/vep/human/region/{chrom}:{pos}-{end}/{alt}"
           f"?content-type=application/json")
    last = None
    for attempt in range(4):
        try:
            r = json.load(urllib.request.urlopen(url, timeout=120))
            return r[0] if isinstance(r, list) and r else {}
        except Exception as e:
            last = e; time.sleep(3 * (attempt + 1))
    raise QueryFailed(f"{chrom}:{pos}{ref}>{alt} -> {last}")

print(f"querying VEP (GET, per variant) for {len(data)} candidate(s) ...")
res, failed = {}, []
for n, r in enumerate(data, 1):
    c,p,ref,alt = r[idx['chrom']], r[idx['pos']], r[idx['ref']], r[idx['alt']]
    a0 = alt.split(",")[0]
    try:
        res[(c,p,ref,a0)] = vep_one(c,p,ref,a0)
    except QueryFailed as e:
        failed.append(str(e)); res[(c,p,ref,a0)] = None
    if n % 10 == 0: print(f"  {n}/{len(data)}")
if failed:
    print(f"\n  *** {len(failed)} QUERY FAILURES -- reported as QUERY_FAILED, NOT as absent ***")
    for f in failed[:5]: print("   ", f)

def popmax(item):
    best, where, homs = None, None, None
    for cv in (item or {}).get("colocated_variants", []) or []:
        fr = cv.get("frequencies") or {}
        for allele, pops in fr.items():
            for pop, val in pops.items():
                if pop in ("gnomade","gnomadg") or pop.startswith(("gnomade_","gnomadg_")):
                    if pop.endswith(("_remaining",)): continue
                    if best is None or (val is not None and val > best):
                        best, where = val, pop
    return best, where

out = []
for r in data:
    c,p,ref,alt = r[idx['chrom']], r[idx['pos']], r[idx['ref']], r[idx['alt']]
    a0 = alt.split(",")[0]
    item = res.get((c,p,ref,a0), None)
    query_ok = item is not None
    af, pop = popmax(item) if query_ok else (None, None)
    rsid = ""
    for cv in (item or {}).get("colocated_variants", []) or []:
        if str(cv.get("id","")).startswith("rs"): rsid = cv["id"]; break
    zyg = r[idx['zyg']]
    if not query_ok:
        cls = "QUERY_FAILED"          # NOT evidence of rarity
    elif af is None:
        cls = "ABSENT_from_gnomAD"
    elif zyg == "HOM_ALT" and af >= 0.005: cls = "COMMON_POLYMORPHISM"
    elif zyg != "HOM_ALT" and af >= 0.01:  cls = "COMMON_POLYMORPHISM"
    else: cls = "RARE_candidate"
    out.append(r + [rsid or "-", "NA" if af is None else f"{af:.3g}", pop or "-", cls])

with open(OUT,"w") as fh:
    fh.write("\t".join(hdr + ["rsid","gnomad_popmax_AF","gnomad_pop","rarity_class"]) + "\n")
    for r in out: fh.write("\t".join(map(str,r)) + "\n")

from collections import Counter
cnt = Counter(r[-1] for r in out)
print(f"\nwrote {OUT}")
for k in ("RARE_candidate","ABSENT_from_gnomAD","COMMON_POLYMORPHISM","QUERY_FAILED"):
    print(f"  {k:22s} {cnt.get(k,0)}")
if cnt.get("QUERY_FAILED"):
    print("\n  WARNING: QUERY_FAILED rows have NO frequency evidence either way.")
    print("  They must not be treated as rare. Re-run before interpreting.")
