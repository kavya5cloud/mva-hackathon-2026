#!/usr/bin/env python3
"""Task 3 - deep structural analysis of N1002 in the BUBR1 pseudokinase domain.
Structure: AlphaFold DB AF-O60566-F1-model_v6.pdb (full length, 1050 aa).
Computes: (1) pairwise spatial clustering of the known MVA missense positions,
(2) the N1002 contact shell and its cross-species conservation, (3) secondary
structure context, (4) distance of every MVA position to the pseudo-active site.
NOTE: human BUBR1 is a PSEUDOkinase. UniProt's 'Active site 882' is annotated by
similarity only; no residue here is described as catalytic on that basis."""
import sys, json, itertools
import numpy as np
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import three_to_index, index_to_one

PDB  = sys.argv[1] if len(sys.argv) > 1 else "AF-O60566-F1-model_v6.pdb"
HOM  = sys.argv[2] if len(sys.argv) > 2 else "homol.json"
MVA  = {727:"R727C", 814:"R814H", 844:"L844F", 909:"I909T",
        921:"Q921H", 1002:"N1002K", 1012:"L1012P"}
REF  = {795:"K795 (ATP, UniProt binding site)",
        882:"D882 (UniProt 'active site', by similarity - pseudokinase)",
        911:"D911 (tested in PMID 33207204)"}

ch = PDBParser(QUIET=True).get_structure("b", PDB)[0]["A"]
def one(r):
    try: return index_to_one(three_to_index(r.get_resname()))
    except Exception: return "X"
def mind(a, b):
    ra, rb = ch[(" ",a," ")], ch[(" ",b," ")]
    return min(x-y for x in ra for y in rb)
def plddt(p):
    r = ch[(" ",p," ")]; return sum(a.get_bfactor() for a in r)/len(r)

print("="*74)
print("1. PAIRWISE MINIMUM HEAVY-ATOM DISTANCES BETWEEN MVA MISSENSE POSITIONS (A)")
print("="*74)
ps = sorted(MVA)
print("        " + "".join(f"{MVA[p]:>9}" for p in ps))
for a in ps:
    print(f"{MVA[a]:>8}" + "".join(f"{mind(a,b):9.1f}" if a!=b else f"{'-':>9}" for b in ps))

print("\nContact-level pairs (<8 A, i.e. plausibly same structural neighbourhood):")
any8 = False
for a,b in itertools.combinations(ps,2):
    d = mind(a,b)
    if d < 8.0:
        print(f"   {MVA[a]} <-> {MVA[b]} : {d:.1f} A"); any8 = True
if not any8: print("   NONE - the MVA missense positions are spatially dispersed.")

print("\n" + "="*74)
print("2. DISTANCE OF EACH MVA POSITION TO REFERENCE SITES (A)")
print("="*74)
print(f"{'variant':>10} " + "".join(f"{k:>10}" for k in REF))
for p in ps:
    print(f"{MVA[p]:>10} " + "".join(f"{mind(p,k):10.1f}" for k in REF))
for k,v in REF.items(): print(f"   {k} = {v}")

print("\n" + "="*74)
print("3. N1002 CONTACT SHELL (<=4.5 A, any atom) AND ITS CONSERVATION")
print("="*74)
n = ch[(" ",1002," ")]
shell = {}
for res in ch:
    if res.id[1] == 1002 or res.id[0] != " ": continue
    d = min(x-y for x in n for y in res)
    if d <= 4.5: shell[res.id[1]] = (one(res), d)

hom = json.load(open(HOM))["data"][0]["homologies"]
def residue_at(s,t,pos):
    k=0
    for i,c in enumerate(s):
        if c!="-":
            k+=1
            if k==pos: return t[i]
    return None
SPP = ["pan_troglodytes","mus_musculus","rattus_norvegicus",
       "canis_lupus_familiaris","gallus_gallus","xenopus_tropicalis"]
cons = {}
for h in hom:
    sp = h["target"]["species"]
    if sp not in SPP: continue
    s,t = h["source"]["align_seq"], h["target"]["align_seq"]
    for p in list(shell)+[1002]:
        cons.setdefault(p,{})[sp] = residue_at(s,t,p)

print(f"{'pos':>6} {'aa':>3} {'dist':>6} {'pLDDT':>7}  conservation (chimp/mouse/rat/dog/chicken/xenopus)")
for p in sorted(shell):
    aa,d = shell[p]
    orth = [cons.get(p,{}).get(sp) for sp in SPP]
    ident = sum(1 for o in orth if o == aa)
    print(f"{p:>6} {aa:>3} {d:6.2f} {plddt(p):7.1f}  {''.join(str(o) for o in orth)}  -> {ident}/6 identical")
orth = [cons.get(1002,{}).get(sp) for sp in SPP]
print(f"{1002:>6} {'N':>3} {'--':>6} {plddt(1002):7.1f}  {''.join(str(o) for o in orth)}  -> "
      f"{sum(1 for o in orth if o=='N')}/6 identical   <-- N1002 itself")

print("\n" + "="*74)
print("4. SECONDARY STRUCTURE CONTEXT (pydssp, 975-1015)")
print("="*74)
try:
    import pydssp, torch  # noqa
    import numpy as _np
    coords = []
    idx = []
    for res in ch:
        if res.id[0]!=" ": continue
        try: coords.append([res["N"].coord,res["CA"].coord,res["C"].coord,res["O"].coord]); idx.append(res.id[1])
        except KeyError: pass
    ss = pydssp.assign(_np.array(coords), out_type="c3")
    m = {i:s for i,s in zip(idx,ss)}
    line = "".join(m.get(p,"?") for p in range(975,1016))
    print("   pos 975" + " "*(len(line)-10) + "1015")
    print("   " + line)
    print("   (H = helix, E = strand, - = loop/coil)")
    print(f"   N1002 secondary structure = '{m.get(1002)}'")
except Exception as e:
    print("   pydssp unavailable/failed:", e)
