#!/usr/bin/env python3
"""
step11_phi_psi.py -- single decisive backbone-geometry check at BUBR1 N1002.

WHY: Asn is over-represented at helix C-caps partly because it tolerates
POSITIVE phi. If N1002 sits at positive phi, most residues (including Lys) are
sterically disfavoured there and substitution is more likely to perturb local
backbone geometry. If phi is normal/negative, that particular argument does not
apply and the helix-cap model loses one of its supports.

This is a bounded sanity check, NOT a new modelling campaign.
Structure: AlphaFold AF-O60566-F1-model_v6.pdb (pLDDT at 1002 = 91.06).
No experimental structure of the human BUBR1 pseudokinase domain covering
residue 1002 was identified (PDB checked 2026-09-16, see analysis notes).
"""
import sys, math
from Bio.PDB import PDBParser, PPBuilder
from Bio.PDB.Polypeptide import three_to_index, index_to_one

PDB = sys.argv[1] if len(sys.argv)>1 else "AF-O60566-F1-model_v6.pdb"
s = PDBParser(QUIET=True).get_structure("b", PDB)
model = s[0]
ppb = PPBuilder()

angles = {}
for pp in ppb.build_peptides(model["A"]):
    phipsi = pp.get_phi_psi_list()
    for res,(phi,psi) in zip(pp, phipsi):
        angles[res.id[1]] = (
            math.degrees(phi) if phi else None,
            math.degrees(psi) if psi else None,
            res.get_resname(),
            sum(a.get_bfactor() for a in res)/len(res))

print(f"{'pos':>6} {'aa':>4} {'phi':>9} {'psi':>9} {'pLDDT':>7}  region")
for p in range(995, 1011):
    if p not in angles: continue
    phi,psi,aa,pl = angles[p]
    try: one = index_to_one(three_to_index(aa))
    except Exception: one = aa
    reg = ""
    if phi is not None and psi is not None:
        if phi > 0: reg = "POSITIVE PHI (left-handed / alphaL)"
        elif -160 <= phi <= -20 and -120 <= psi <= 50: reg = "alpha / helical"
        elif -180 <= phi <= -40 and (psi > 90 or psi < -150): reg = "beta / extended"
        else: reg = "other"
    mark = "   <== N1002" if p == 1002 else ""
    print(f"{p:>6} {one:>4} {str(round(phi,1)) if phi else 'NA':>9} "
          f"{str(round(psi,1)) if psi else 'NA':>9} {pl:7.1f}  {reg}{mark}")

phi,psi,aa,pl = angles[1002]
print(f"\nN1002: phi={phi:.1f} deg, psi={psi:.1f} deg, pLDDT={pl:.1f}")
if pl < 70:
    print("VERDICT: C -- unresolved; local model confidence too low.")
elif phi > 0:
    print("VERDICT: A -- POSITIVE PHI / unusual geometry.")
    print("  Positive phi is sterically restrictive: Gly, Asn and Asp populate it")
    print("  readily; most other residues (Lys included) do not. This SUPPORTS the")
    print("  view that Asn is specifically favoured here.")
else:
    print("VERDICT: B -- normal negative phi.")
    print("  The 'only Asn/Gly tolerate this backbone conformation' argument does")
    print("  NOT apply. Any steric case against Lys must rest on side-chain packing")
    print("  and hydrogen bonding, not on backbone geometry.")
