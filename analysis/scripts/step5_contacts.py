#!/usr/bin/env python3
"""Step 5 - N1002 side-chain contact environment and H-bond inventory.
Structure: AF-O60566-F1-model_v6.pdb. Geometric H-bond criterion (no H atoms in
the AlphaFold model): heavy-atom donor-acceptor distance <= 3.5 A between a
plausible N/O donor and an N/O acceptor. Contacts listed to 4.0 A."""
import sys
from Bio.PDB import PDBParser, NeighborSearch
from Bio.PDB.SASA import ShrakeRupley
from Bio.PDB.Polypeptide import three_to_index, index_to_one

PDB = sys.argv[1] if len(sys.argv) > 1 else "AF-O60566-F1-model_v6.pdb"
m = PDBParser(QUIET=True).get_structure("b", PDB)[0]
ch = m["A"]
r = ch[(" ", 1002, " ")]
assert r.get_resname() == "ASN", "numbering gate failed"

# per-atom SASA to see whether the amide tip itself is exposed
ShrakeRupley().compute(m, level="A")
print("[per-atom SASA of N1002]")
for a in r:
    print(f"   {a.get_id():4s} SASA={a.sasa:6.2f} A^2  pLDDT={a.get_bfactor():.1f}")
print(f"   side-chain (CB,CG,OD1,ND2) total = {sum(a.sasa for a in r if a.get_id() in ('CB','CG','OD1','ND2')):.2f} A^2")
print(f"   amide tip (OD1+ND2) total        = {sum(a.sasa for a in r if a.get_id() in ('OD1','ND2')):.2f} A^2")

atoms = [a for a in m.get_atoms()]
ns = NeighborSearch(atoms)
def one(res):
    try: return index_to_one(three_to_index(res.get_resname()))
    except Exception: return "X"

print("\n[contacts <= 4.0 A of N1002 OD1 / ND2]")
seen = set()
for aname in ("OD1", "ND2"):
    src = r[aname]
    for nb in sorted(ns.search(src.coord, 4.0), key=lambda x: (x-src)):
        pr = nb.get_parent()
        if pr is r: continue
        d = nb - src
        pol = nb.element in ("N", "O") 
        hb = "H-BOND (<=3.5A, N/O-N/O)" if (pol and d <= 3.5) else ("polar" if pol else "vdW")
        role = ("acceptor" if aname == "ND2" else "donor") + "@1002" if pol else "-"
        print(f"   {aname} -- {one(pr)}{pr.id[1]:<5d} {nb.get_id():4s} d={d:5.2f} A  {hb:26s} {role}")
        seen.add((pr.id[1], one(pr)))

print("\n[residues with any atom within 4.0 A of the N1002 side chain]")
env = {}
for aname in ("CB","CG","OD1","ND2"):
    for nb in ns.search(r[aname].coord, 4.0):
        pr = nb.get_parent()
        if pr is r: continue
        d = nb - r[aname]
        key = (pr.id[1], one(pr))
        if key not in env or d < env[key][0]: env[key] = (d, nb.get_id(), aname)
for k in sorted(env):
    d, nba, sa = env[k]
    print(f"   {k[1]}{k[0]:<5d} closest {nba:4s} to {sa:4s} d={d:5.2f} A")
