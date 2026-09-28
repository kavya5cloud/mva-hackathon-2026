# Proband phenotype — extracted, not invented

**Status: PHENOTYPE AVAILABLE.** (A `PHENOTYPE_MISSING.md` was therefore **not**
created; the brief instructed that such a file be produced only if phenotype data
were absent.)

**Source:** `MVA_Hackathon_2026_Track1_METHODS.md` §2.1 "Reported Phenotype",
lines 98–112. Extracted verbatim 2026-09-16. The methods document states these
HPO terms "were provided for the proband".

| Clinical feature | HPO identifier |
|---|---|
| Rhabdomyosarcoma | `HP:0002859` |
| Nephrocalcinosis | `HP:0000121` |
| Short stature | `HP:0004322` |
| Failure to thrive | `HP:0001508` |
| Skeletal muscle atrophy | `HP:0003202` |
| Premature birth | `HP:0001622` |
| Small for gestational age | `HP:0001518` |
| Recurrent spontaneous abortion | `HP:0200067` |

## Provenance limitation

These terms are recorded **second-hand**, inside our own Track 1 methods
document. The primary clinical source file supplied by the hackathon was not
located in this repository. The terms are used as given and none has been added,
removed, or reinterpreted.

## Fields that are NOT available and would be required for a full analysis

- Consanguinity status (materially changes the prior on homozygous-by-descent AR models)
- Parental phenotypes and parental samples
- **Cytogenetic confirmation of mosaic aneuploidy** — no karyotype, FISH, or
  chromosome-count data is present in this repository
- **Premature chromatid separation (PCS)** status — a key MVA discriminator, absent
- Sex of the proband
- Age at onset / age at sampling
- Tumour histology and somatic profiling of the rhabdomyosarcoma
- Microcephaly / head-circumference measurements
- Growth parameters beyond the qualitative HPO terms

## How the phenotype was used in this analysis

The HPO set includes **Rhabdomyosarcoma (HP:0002859)**. This was used to select
the gene panel **objectively** — Genomics England PanelApp panel 290 "Familial
rhabdomyosarcoma" — rather than assuming an MVA/*BUB1B* model a priori. See
`analysis/scripts/build_gene_panel.py`.

**Important caveat recorded honestly:** the HPO set as given contains **no term
for mosaic aneuploidy, variegated aneuploidy, PCS, or microcephaly.** The
MVA diagnosis is therefore *asserted* in the Track 1 document rather than
*evidenced* by the HPO list available to us. Rhabdomyosarcoma, IUGR/SGA, short
stature and failure to thrive are compatible with MVA but are not specific to it.
