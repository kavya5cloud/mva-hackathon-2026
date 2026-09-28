# Structural variant / CNV analysis — availability assessment

**Determination date:** 2026-09-16 
**Conclusion: SV/CNV analysis is NOT POSSIBLE from the currently available input.**

No SV or CNV analysis was performed, and no SV/CNV result is reported anywhere in
this repository.

## What was checked

| Evidence type | Present? | Verification |
|---|---|---|
| SV records in the VCF (`<DEL>`, `<DUP>`, `<INV>`, `<INS>`, BND) | **NO** | `bcftools view -h` declares **no `##ALT`** lines; `awk '$5 ~ /^</'` over all records returns nothing |
| gVCF / reference blocks (`<NON_REF>`) | **NO** | no `NON_REF` alleles present — this is a filtered site-level VCF, not a gVCF |
| Per-base depth / coverage track | **NO** | only per-variant `FORMAT/DP` at called sites; no genome-wide depth signal |
| BAM / CRAM | **NO** | filesystem search found no `*.bam` / `*.cram` |
| FASTQ | **NO** | filesystem search found no `*.fastq*` / `*.fq*` (the ~85 GB raw dataset was never downloaded, per Track 1 methods line 229) |
| Pre-computed CNV calls | **NO** | none in the repository or the gated data directory |
| Pre-computed SV calls | **NO** | none |

## What the VCF actually is

GATK 4.2.4.0 `VariantFiltration` output: single-sample, site-level SNV and small
indel calls on GRCh38, ~5.02 million records. INFO fields are GATK annotation
metrics (`QD`, `FS`, `MQ`, `SOR`, `MQRankSum`, `ReadPosRankSum`, `ExcessHet`,
`InbreedingCoeff`, `AC`, `AF`, `AN`, `DP`, `DB`, `MLEAC`, `MLEAF`).

## Why per-variant DP cannot substitute

A crude depth-based CNV inference from `FORMAT/DP` at called sites was considered
and **rejected**: called-site depth is ascertainment-biased (it exists only where
a variant was called), there is no matched reference panel or control cohort for
normalisation, and a single sample gives no baseline. Any "CNV" derived this way
would be uninterpretable. It was not attempted.

## Consequence for the scientific conclusions

This is a **material limitation**, and it is carried explicitly into the decision
matrix:

- A **CNV or SV second hit in *BUB1B*** — for example a single-exon deletion on the
  allele not carrying `p.Leu737*` — **cannot be excluded**. This is a recognised
  mechanism in recessive disease and would not appear in this VCF.
- The same applies to every other gene screened.
- Therefore "no qualifying variant identified under the documented filters" must
  never be read as "gene excluded".

## What would resolve it

1. Access to the aligned reads (BAM/CRAM) → read-depth CNV calling (e.g. CNVnator, GATK gCNV) and split-read/discordant-pair SV calling (Manta, DELLY).
2. A gVCF with reference blocks → depth-based CNV inference.
3. Exon-level dosage assay targeted at *BUB1B* (MLPA or qPCR) → directly tests the single most important open possibility.
4. Long-read WGS → resolves SV **and** phase simultaneously.
