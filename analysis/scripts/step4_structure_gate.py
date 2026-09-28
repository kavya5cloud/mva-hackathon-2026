#!/usr/bin/env python3
"""
Step 4 - BUBR1 N1002 structural gate.

Structure : AlphaFold DB AF-O60566-F1-model_v6.pdb (BUBR1 / O60566, full length 1050 aa)
            NOTE: model_v4 referenced in the project brief is retired (HTTP 404 on
            2026-09-15); v6 is the current AlphaFold DB release and is used instead.

Method deviation: mkdssp is not installable in this environment (no conda/salilab
build for darwin-arm64, no system binary). SASA is therefore computed with
Biopython's Shrake-Rupley implementation (Bio.PDB.SASA), and RSA is derived using
the Tien et al. 2013 (PLoS ONE 8:e80635) theoretical maximum ASA values.
Secondary structure is taken from pydssp.

PRE-REGISTERED THRESHOLDS (fixed before inspecting any result):
    RSA < 0.20  -> substantially buried  -> supports destabilisation hypothesis (A)
    RSA > 0.40  -> exposed               -> weakens A, strengthens interface hypothesis (B)
    0.20-0.40   -> equivocal
Hard stop: residue 1002 in the model MUST be ASN, else numbering/mapping is wrong.
"""
import sys, json
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley
from Bio.PDB.Polypeptide import three_to_index, index_to_one

PDB = sys.argv[1] if len(sys.argv) > 1 else "AF-O60566-F1-model_v6.pdb"

# Tien et al. 2013, theoretical maximum ASA (A^2)
MAXASA = {"A":129,"R":274,"N":195,"D":193,"C":167,"Q":225,"E":223,"G":104,"H":224,
          "I":197,"L":201,"K":236,"M":224,"F":240,"P":159,"S":155,"T":172,"W":285,
          "Y":263,"V":174}

def one(res):
    try: return index_to_one(three_to_index(res.get_resname()))
    except Exception: return "X"

struct = PDBParser(QUIET=True).get_structure("bubr1", PDB)
model = struct[0]
chain = model["A"]

# ---- hard numbering gate -------------------------------------------------
r1002 = chain[(" ", 1002, " ")]
aa1002 = one(r1002)
print(f"[GATE] residue 1002 in model = {r1002.get_resname()} ({aa1002})")
if aa1002 != "N":
    sys.exit("STOP: residue 1002 is not ASN - numbering/model mapping is wrong.")
for pos, exp in [(1012,"L"), (909,"I"), (921,"Q"), (844,"L"), (737,"L")]:
    got = one(chain[(" ", pos, " ")])
    print(f"[GATE] residue {pos} = {got} (expected {exp}) {'OK' if got==exp else 'MISMATCH'}")

# ---- pLDDT (AlphaFold stores per-atom pLDDT in the B-factor column) -------
def plddt(res):
    b = [a.get_bfactor() for a in res]
    return sum(b)/len(b)

print("\n[pLDDT] local confidence")
for p in range(995, 1016):
    print(f"  {p:5d} {one(chain[(' ',p,' ')])}  pLDDT={plddt(chain[(' ',p,' ')]):6.2f}")
p1002 = plddt(r1002)
win = [plddt(chain[(" ",p," ")]) for p in range(992, 1013)]
print(f"\n  pLDDT(1002)            = {p1002:.2f}")
print(f"  mean pLDDT(992-1012)   = {sum(win)/len(win):.2f}")

# ---- SASA / RSA, full-length context --------------------------------------
ShrakeRupley().compute(model, level="R")
full = {p: chain[(" ",p," ")].sasa for p in range(1, 1051) if (" ",p," ") in chain}

# ---- SASA / RSA, isolated pseudokinase domain (UniProt 766-1050) ----------
import copy
dom = copy.deepcopy(model)
for res in list(dom["A"]):
    if not (766 <= res.id[1] <= 1050):
        dom["A"].detach_child(res.id)
ShrakeRupley().compute(dom, level="R")
domsasa = {r.id[1]: r.sasa for r in dom["A"]}

print("\n[RSA] res aa  SS   SASA_full  RSA_full   SASA_dom  RSA_dom")
rows = []
for p in range(995, 1016):
    res = chain[(" ",p," ")]; aa = one(res)
    rf = full[p]/MAXASA[aa]; rd = domsasa[p]/MAXASA[aa]
    rows.append(dict(pos=p, aa=aa, plddt=round(plddt(res),2),
                     sasa_full=round(full[p],2), rsa_full=round(rf,3),
                     sasa_dom=round(domsasa[p],2), rsa_dom=round(rd,3)))
    print(f"      {p:4d} {aa}       {full[p]:8.2f}  {rf:7.3f}   {domsasa[p]:8.2f}  {rd:7.3f}")

print("\n[BENCHMARK] known MVA / control positions")
bench = {727:"R",814:"R",844:"L",909:"I",921:"Q",1002:"N",1012:"L"}
bm = []
for p, exp in bench.items():
    res = chain[(" ",p," ")]; aa = one(res)
    rf = full[p]/MAXASA[aa]; rd = domsasa[p]/MAXASA[aa] if p in domsasa else float("nan")
    bm.append(dict(pos=p, aa=aa, plddt=round(plddt(res),2),
                   rsa_full=round(rf,3), rsa_dom=round(rd,3)))
    print(f"      {p:4d} {aa}  pLDDT={plddt(res):6.2f}  RSA_full={rf:6.3f}  RSA_dom={rd:6.3f}")

# ---- verdict against PRE-REGISTERED thresholds ----------------------------
rsa = rows[[r['pos'] for r in rows].index(1002)]['rsa_dom']
print("\n[VERDICT] using pre-registered thresholds on domain-context RSA")
print(f"  N1002 RSA_dom = {rsa:.3f}")
if p1002 < 70:
    v = "UNRESOLVED - local pLDDT < 70, structure unreliable"
elif rsa < 0.20: v = "BURIED -> supports destabilisation hypothesis (A)"
elif rsa > 0.40: v = "EXPOSED -> weakens A, strengthens interface hypothesis (B)"
else:            v = "EQUIVOCAL (0.20-0.40)"
print(f"  {v}")

json.dump(dict(structure=PDB, plddt_1002=p1002,
               plddt_mean_992_1012=sum(win)/len(win),
               window=rows, benchmark=bm, verdict=v),
          open("step4_results.json","w"), indent=2)
