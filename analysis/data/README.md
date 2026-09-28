# Round 2 data artefacts

- `BUBR1_kinase_766_1050.pdb` — BUBR1 pseudokinase domain (UniProt O60566 residues
  766-1050) excised from AlphaFold DB `AF-O60566-F1-model_v6.pdb`
  (MD5 of source full-length model: 943e5596717db0424b1a020ae429e174).
  This exact file was the input to all DynaMut2 ddG submissions.
- `step4_results.json` — machine-readable output of `../scripts/step4_structure_gate.py`
  (pLDDT, per-residue SASA/RSA 995-1015, benchmark panel, pre-registered verdict).
- `homol.json` — raw Ensembl REST Compara orthologue response (aligned protein
  sequences) used by `../scripts/step6_conservation.py`. Retrieved 2026-09-15.

The full-length AlphaFold model is not committed (691 KB, retrievable):
  curl -O https://alphafold.ebi.ac.uk/files/AF-O60566-F1-model_v6.pdb

---

## Provenance artifacts (`provenance/`) and data governance

Written by `../scripts/step0_verify_provenance.py` on 2026-09-16.

**Committed (no individual genotype data):**

| File | Contents |
|---|---|
| `header_provenance_redacted.txt` | `##reference` / `##contig` metadata — the evidence for the GRCh38 build call |
| `kavya5cloud_*_original.csv` | byte-for-byte archives of the two submission CSVs |
| `README_original_pre-erratum.md` | `README.md` as it stood before the 2026-09-16 correction |
| `gitignore_original.txt` | `.gitignore` before the scope fix |

**Deliberately gitignored — patient genotype-level data from the GATED dataset:**

| File | Why withheld |
|---|---|
| `bub1b_region_GRCh38.vcf.gz` (+`.tbi`) | 15 individual genotypes at the *BUB1B* locus |
| `bub1b_locus_variants.tsv` | same, as POS/REF/ALT/FILTER/GT/DP/GQ/AD |
| `track1_window_GRCh38.tsv` | 36 genotypes from the erroneous Track 1 window |
| `header_provenance.txt` | full header incl. GATK command line with internal `/home/dnanexus` paths |

All four are **fully reproducible** from the gated source:

```bash
python3 analysis/scripts/step0_verify_provenance.py /path/to/WGS_EX2312012_HGWCNDSX7.vcf.gz
```

**Note on `.gitignore`:** the original pattern `data/` matched `analysis/data/` at
any depth and silently excluded every evidence artifact here. It is now scoped to
`/data/` (top level), with `analysis/data/**` re-included and the genotype-level
files listed explicitly. Verify with `git check-ignore -v <path>` before committing.
