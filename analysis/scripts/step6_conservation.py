#!/usr/bin/env python3
"""Step 6 - cross-species residue identity at human BUBR1 positions of interest.
Source: Ensembl REST Compara homology endpoint (pairwise protein alignments,
aligned=1) for human BUB1B / ENSG00000156970. Each homology record supplies the
human and target sequences already aligned to each other, so the human residue
index is mapped through the gapped human string to read off the target residue."""
import json, sys
POS = [727, 737, 814, 844, 909, 921, 1002, 1012]
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "homol.json"))["data"][0]["homologies"]

def residue_at(src_aln, tgt_aln, pos):
    """pos = 1-based ungapped index into src_aln; return aligned tgt char."""
    n = 0
    for i, c in enumerate(src_aln):
        if c != "-":
            n += 1
            if n == pos:
                return tgt_aln[i]
    return None

rows = {}
human_ref = None
for h in d:
    sp = h["target"]["species"]
    if h["type"] != "ortholog_one2one" and sp == "danio_rerio" and h["target"]["perc_id"] < 30:
        continue  # drop the low-identity second zebrafish paralogue
    s, t = h["source"]["align_seq"], h["target"]["align_seq"]
    if human_ref is None:
        human_ref = {p: residue_at(s, s, p) for p in POS}
    rows.setdefault(sp, {})
    for p in POS:
        rows[sp][p] = residue_at(s, t, p)
    rows[sp]["_id"] = h["target"]["id"]
    rows[sp]["_pid"] = h["target"]["perc_id"]

order = ["homo_sapiens", "pan_troglodytes", "mus_musculus", "rattus_norvegicus",
         "canis_lupus_familiaris", "gallus_gallus", "xenopus_tropicalis", "danio_rerio"]
rows["homo_sapiens"] = dict(human_ref, _id="ENSG00000156970", _pid=100.0)

hdr = "species".ljust(26) + "".join(f"{p:>7}" for p in POS) + "   %id"
print(hdr); print("-" * len(hdr))
for sp in order:
    if sp not in rows: continue
    r = rows[sp]
    print(sp.ljust(26) + "".join(f"{str(r[p]):>7}" for p in POS) + f"  {r['_pid']:5.1f}")

print("\nconservation vs human (identical / n species compared):")
for p in POS:
    comp = [rows[sp][p] for sp in order if sp in rows and sp != "homo_sapiens"]
    same = sum(1 for c in comp if c == human_ref[p])
    print(f"  {human_ref[p]}{p:<5d} {same}/{len(comp)} identical   others: "
          + ",".join(sorted({c for c in comp if c != human_ref[p]}) ) or "  -")
