# Rare Disease, Real Kid: MVA Hackathon 2026

**Team:** kavya5cloud 
**Track:** 1 (Variant Prediction) + 2 (Drug Repurposing) 
**Track 1 leaderboard result (historical):** 100.0 Rank Points / 1.000 F-max

> ## ⚠️ STATUS — read before using any result in this repository
>
> A post-submission coordinate audit found a **genome-build error in the Track 1
> extraction step**. The variants reported in the original Track 1 submission are
> genuine proband variants but **are not in *BUB1B***. See
> [Track 1 Provenance Erratum](#track-1-provenance-erratum) below and
> [`analysis/TRACK1_SUBMISSION_ERRATUM.md`](analysis/TRACK1_SUBMISSION_ERRATUM.md).
>
> The two variants now under analysis (`p.Leu737*`, `p.Asn1002Lys`) **have been
> verified present in the proband VCF** (see [Verified Findings](#verified-findings)).
> **Their phase has NOT been determined.** They must not be described as
> compound heterozygous, biallelic, or in trans.
>
> **Track 2 outcome: mechanism UNRESOLVED; no drug candidate is justified.**

## Overview

This repository contains our analysis for identifying candidate causal variants in
a child with Mosaic Variegated Aneuploidy (MVA), and a Track 2 mechanistic and
drug-repurposing assessment of those variants.

## Verified Findings

Both variants below were confirmed **directly in the proband VCF**
(`WGS_EX2312012`, GRCh38) on 2026-09-16 using
[`analysis/scripts/step0_verify_provenance.py`](analysis/scripts/step0_verify_provenance.py):

| Variant | GRCh38 | REF>ALT | FILTER | GT | DP | GQ | AD | VAF |
|---|---|---|---|---|---|---|---|---|
| NM_001211.6:c.2210T>G (p.Leu737\*) | chr15:40,209,701 | T>G | PASS | 0/1 | 46 | 99 | 21,25 | 0.543 |
| NM_001211.6:c.3006T>G (p.Asn1002Lys) | chr15:40,220,612 | T>G | PASS | 0/1 | 28 | 99 | 15,13 | 0.464 |

**Phase status: UNDETERMINED.** Both genotypes are unphased (`0/1`); no GATK
PGT/PID phasing group links them. The two sites are **10,911 bp apart**, which
short-read fragments (~350–550 bp) cannot span. Trio genotyping or long-read
sequencing is required before any biallelic interpretation.

- **p.Leu737\*** — ClinVar VCV000533901, **Pathogenic/Likely pathogenic**, 2-star, multiple submitters, no conflicts, for MVA syndrome 1.
- **p.Asn1002Lys** — dbSNP rs2542593804; **no ClinVar record for this exact allele**; gnomAD AF 6.195e-7. **No functional evidence of any kind exists for this variant.**

## Track 1 Provenance Erratum

**HISTORICAL RECORD.** The Track 1 methods document states the analysis used
**GRCh38** and records this extraction command:

```bash
bcftools view -r 15:40400000-40500000 WGS_EX2312012_HGWCNDSX7.vcf.gz -o bub1b_region.vcf
```

**CORRECTED INTERPRETATION.** The proband VCF **is** GRCh38 (verified: `##reference=…GCA_000001405.15_GRCh38_no_alt_analysis_set…`; chr15 contig length 101,991,189). However, the interval `40,400,000–40,500,000` is the ***BUB1B* locus in GRCh37**, not GRCh38:

| Build | *BUB1B* span | Overlap with the extraction window |
|---|---|---|
| **GRCh38** (the VCF's build) | chr15:40,160,984–40,221,137 | **0 bp — no overlap** |
| GRCh37 | chr15:40,453,224–40,513,337 | 46,770 bp |

That window returns **36 variants** from the proband VCF — matching the count in
the methods document exactly, confirming the pipeline ran as described. But in
GRCh38 those variants lie in **IVD, BAHD1 and CHST14**, not *BUB1B*. The three
prioritised candidates are **real, PASS-quality proband variants in the wrong
genes**:

| Original candidate | Gene in GRCh38 (the VCF's build) | Gene in GRCh37 |
|---|---|---|
| chr15:40,425,440 C>CTATA | **IVD** | *no gene* |
| chr15:40,488,950 C>CA | lncRNA ENSG00000259536 | *BUB1B* |
| chr15:40,447,560 GAATAAATA>G | **BAHD1** | *no gene* |

**Consequently the original Track 1 interpretation — a compound-heterozygous
frameshift pair in *BUB1B* — is not supported.** Neither leading candidate is a
*BUB1B* variant under the VCF's actual build, and phase was never established for
any pair. The original submission is retained unmodified as a historical artifact
and is **not** treated as an established biological conclusion.

**Corrected extraction** (GRCh38 *BUB1B*, ±2 kb) returns **15** variants,
including both variants listed under [Verified Findings](#verified-findings):

```bash
bcftools view -r 15:40158984-40223137 WGS_EX2312012_HGWCNDSX7.vcf.gz
```

## Repository Layout

| Path | Contents |
|---|---|
| [`analysis/README.md`](analysis/README.md) | Track 2 reading order and status banner |
| [`analysis/kavya5cloud_track2_report.md`](analysis/kavya5cloud_track2_report.md) | Final Track 2 scientific report (16 sections) |
| [`analysis/round2_variant_characterisation.md`](analysis/round2_variant_characterisation.md) | Full evidence record, Rounds 1–3 |
| [`analysis/TRACK1_SUBMISSION_ERRATUM.md`](analysis/TRACK1_SUBMISSION_ERRATUM.md) | Formal erratum for the Track 1 submission CSVs |
| [`analysis/scripts/`](analysis/scripts/) | All analysis scripts, incl. `step0_verify_provenance.py` |
| [`analysis/data/provenance/`](analysis/data/) | VCF-derived provenance evidence |
| [`analysis/environment.txt`](analysis/environment.txt) | Software versions and documented absences |
| `MVA_Hackathon_2026_Track1_METHODS.md` | Historical Track 1 methods + build erratum |

## Pipeline (as originally run — see erratum)

1. Download VCF (315 MB compressed)
2. Extract BUB1B region — **used the GRCh37 interval on a GRCh38 VCF; see erratum**
3. Filter by quality and genotype
4. Prioritize by predicted functional impact
5. Generate ranked submission

## Reproduce the provenance check

```bash
python3 analysis/scripts/step0_verify_provenance.py /path/to/WGS_EX2312012_HGWCNDSX7.vcf.gz
```

## Tools Used

bcftools 1.24 · Python 3.12.7 · Biopython 1.88 · NumPy 1.26.4 · macOS (Apple Silicon). 
Full list, including documented *absences* (mkdssp, FoldX, MD engine): [`analysis/environment.txt`](analysis/environment.txt).

## Data Access

The dataset is gated. Request access at
<https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data>. 
Raw VCF/FASTQ are **not** committed (see `.gitignore`).

## License

CC BY 4.0 (as per hackathon rules)
