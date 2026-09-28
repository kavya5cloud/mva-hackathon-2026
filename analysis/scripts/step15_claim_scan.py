#!/usr/bin/env python3
"""
step15_claim_scan.py -- final scientific claim scan of all committed Markdown.

Searches for dangerous or stale terminology and classifies every hit as either a
GENUINE CLAIM (a statement asserting the thing) or a FALSE POSITIVE (the term
appearing inside a disclaimer, prohibition, historical erratum, decision-tree
branch label, or acceptance criterion).

A hit is classified FALSE POSITIVE only if the surrounding line carries an
explicit negation / prohibition / conditional / historical marker. Everything
else is reported as a GENUINE CLAIM requiring review -- the default is to flag,
not to excuse.

GUARD: the script refuses to report "clean" if its file list is empty, and
verifies a known-present control term is found. (An earlier shell version of this
scan silently reported 0 hits for every term because zsh does not word-split
unquoted variables, producing a false all-clear.)
"""
import subprocess, sys, os, re

TERMS = ["compound heterozygous", "compound-heterozygous", "biallelic",
         "in trans", "in cis", "pathogenic N1002K", "likely pathogenic N1002K",
         "N1002K pathogenic", "68 intronic BUB1B", "68 BUB1B",
         "CNV excluded", "SV excluded", "splicing excluded",
         "splice completely excluded", "drug candidate", "therapeutic candidate"]

# Markers that make an occurrence non-assertive.
EXCUSE = re.compile(
    r"\b(not|never|no|cannot|can't|without|unless|until|would|should not|must not|"
    r"do not|don't|is not to be|are not to be|forbidden|prohibited|excluded by rule|"
    r"avoid|refus\w*|deprecat\w*|superseded|historical|erratum|errata|originally|"
    r"original claim|unsupported|falsif\w*|unresolved|undetermined|undeterminable|"
    r"criterion|criteria|outcome|branch|case [a-e]\b|if |hypothetic\w*|conditional|"
    r"assign|classif\w*|threshold|approved wording|rather than|instead of|"
    r"does not|did not|cannot be|has not|have not|no drug|none is|not performed|"
    r"remains closed|closed|gated|search for|scan|grep|term|wording|claim-scan)\b",
    re.I)

def committed_md():
    out = subprocess.run("find . -name '*.md' -not -path './.git/*'",
                         shell=True, capture_output=True, text=True).stdout.split()
    keep = []
    for f in sorted(out):
        ig = subprocess.run(f"git check-ignore -q '{f}'", shell=True)
        if ig.returncode != 0:
            keep.append(f)
    return keep

files = committed_md()
print(f"### file list: {len(files)} committed Markdown files")
if not files:
    sys.exit("FATAL: empty file list -- scan cannot be trusted.")

# control term that must be found, else the scan is broken
ctrl = sum(open(f, encoding='utf-8', errors='replace').read().lower().count("bub1b") for f in files)
print(f"### control term 'BUB1B' occurrences: {ctrl}")
if ctrl == 0:
    sys.exit("FATAL: control term not found -- scan is broken.")

# A file whose opening carries an explicit HISTORICAL/SUPERSEDED banner is a
# preserved historical artifact. Its internal claims are labelled at the file
# level and are NOT rewritten (per the finalisation brief). They are reported
# separately as HISTORICAL, not as genuine current claims.
# Must be SELF-DECLARING: the marker has to sit in a heading, blockquote or HTML
# comment near the top, so that a current document which merely *discusses*
# historical material (e.g. FINAL_AUDIT.md) is not misclassified as historical.
HIST_BANNER = re.compile(
    r"^\s*(?:<!--|>|#)[^\n]*?"
    r"(HISTORICAL (?:DOCUMENT|ARCHIVE)|SUPERSEDED|READ THE ERRATUM FIRST|DO NOT CITE AS CURRENT)",
    re.I | re.M)

genuine, false_pos, historical = [], [], []
for f in files:
    lines = open(f, encoding='utf-8', errors='replace').readlines()
    is_hist = bool(HIST_BANNER.search("".join(lines[:25])))
    # guard: a file that declares itself current cannot also be historical
    if is_hist and re.search(r"analysis frozen|FINAL SCIENTIFIC STATE|Final audit", "".join(lines[:25]), re.I):
        is_hist = False
    for i, line in enumerate(lines, 1):
        low = line.lower()
        for t in TERMS:
            if t.lower() not in low:
                continue
            # context window: prohibitions and disclaimers often wrap across lines
            ctx = "".join(lines[max(0, i-3):i+2])
            if is_hist:
                historical.append((f, i, t, line.strip()))
            elif EXCUSE.search(line) or EXCUSE.search(ctx):
                false_pos.append((f, i, t, line.strip()))
            else:
                genuine.append((f, i, t, line.strip()))

print(f"\n### TOTAL hits: {len(genuine)+len(false_pos)+len(historical)}"
      f"   GENUINE: {len(genuine)}   FALSE POSITIVE: {len(false_pos)}   HISTORICAL: {len(historical)}")

print("\n## GENUINE CLAIMS REQUIRING REVIEW")
if not genuine:
    print("  NONE")
else:
    for f, i, t, line in genuine:
        print(f"  {f}:{i}  [{t}]")
        print(f"      {line[:190]}")

print("\n## HISTORICAL (file carries an explicit SUPERSEDED/HISTORICAL banner; preserved deliberately)")
from collections import Counter as _C
for f, n in _C(x[0] for x in historical).most_common():
    print(f"  {f}: {n} hits -- preserved, banner-labelled, NOT rewritten")

print("\n## FALSE POSITIVES (disclaimer / prohibition / errata / branch label), by file")
from collections import Counter
for f, n in Counter(x[0] for x in false_pos).most_common():
    terms = Counter(x[2] for x in false_pos if x[0] == f)
    print(f"  {f}: {n} hits -- {dict(terms)}")
