# Decision Matrix — is BUB1B still the best-supported candidate?

**Executed:** 2026-09-16 · **Input:** `WGS_EX2312012_HGWCNDSX7.vcf.gz` (GRCh38, md5 `a04ea354141cfb032872d67a11c8d2d8`) 
**Deliberately independent of the Track 1 extraction**, which used a GRCh37 interval on a GRCh38 VCF and is not used as evidence anywhere below.

---

## Result: **CASE B**

> **BUB1B has one strong allele and one prioritised-but-unproven second allele,
> with phase unresolved. BUB1B remains plausible but UNRESOLVED.**

It is *not* CASE A (phase is unknown, so biallelic status is not demonstrated).
It is *not* CASE C (the two variants are not known to be in *cis*).
It is *not* CASE D (no other MVA gene has convincing biallelic evidence).
It is *not* CASE E (a credible genetic explanation does exist).

---

## How each case was tested

| Case | Condition | Verdict | Evidence |
|---|---|---|---|
| **A** | BUB1B has convincing biallelic evidence | ✗ | Two rare heterozygous alleles found, but **phase undetermined** and unobtainable from this data. Biallelic status is not demonstrated. |
| **B** | One strong allele, second allele unresolved | ✅ **SELECTED** | `p.Leu737*` is a ClinVar 2-star Pathogenic/Likely pathogenic pLoF (gnomAD popmax 9.98e-5). `p.Asn1002Lys` is an ultra-rare prioritised VUS with no functional evidence. Phase unknown. |
| **C** | Variants in *cis*, no second BUB1B hit | ✗ (not excluded) | *cis* is not demonstrated either. A full-locus scan (gene body ±50 kb, **all** variant classes, PASS and non-PASS) found **no third BUB1B variant** of any consequence. |
| **D** | Another MVA gene has convincing biallelic evidence | ✗ | Of BUB1B, CEP57, TRIP13, BUB1, CENATAC, KNL1, BUB3, MAD2L1, TTK, CENPE — **only BUB1B has any AR model at all** in the genome-wide screen. |
| **E** | No credible genetic explanation | ✗ | BUB1B remains credible. |

---

## What independently re-established BUB1B

1. **Phenotype-driven, not assumption-driven panel.** The proband's HPO includes Rhabdomyosarcoma (HP:0002859). Genomics England **PanelApp panel 290 "Familial rhabdomyosarcoma" v1.6** lists **BUB1B as GREEN (confidence 3), BIALLELIC**. The gene panel was selected from the phenotype, not from the Track 1 conclusion.

2. **Unbiased genome-wide AR screen recovered BUB1B with no gene-list prior.** 5.02 M variants → snpEff → 11,320 PASS HIGH/MODERATE → 203 genes with an AR model. BUB1B is among them (`pLoF_plus_MIS`).

3. **Frequency filtering eliminated essentially everything else.** Of 43 qualifying panel variants, **40 were common polymorphisms** (e.g. TP53 p.Pro72Arg AF 0.748; ERCC2 p.Asp312Asn AF 0.513; XPC p.Gln939Lys AF 0.729). Only **3** survived: BUB1B ×2 and a single ATM missense.

4. **Only two genes in the 80-gene phenotype panel retained any rare qualifying variant** — and only BUB1B retained a rare **pLoF plus a second rare allele**:

| Gene | Rare variants retained | Second allele? |
|---|---|---|
| **BUB1B** | `p.Leu737*` (AF 9.98e-5, HIGH/pLoF) + `p.Asn1002Lys` (ultra-rare) | **Yes — candidate biallelic genotype; phase unresolved** |
| ATM | `p.Ser978Pro` (AF 4.95e-3, rs139552233, MODERATE) | **No** — single allele, no qualifying second hit |

5. **No stronger competitor survived genome-wide.** 99 genes carried HOM_pLoF or TWO_pLoF (models stronger than BUB1B's). These are dominated by gene families with known common LoF or alignment difficulty (olfactory receptors, HLA, MUC, KRTAP, PSG, NPIPB, LILRB, ZNF). Every disease-relevant HOM_pLoF gene frequency-checked was **COMMON** (AF 0.36–1.00: WNK1, LRRK1, CEP89, TDRD12, MRPS34, DZANK1, TLR8, DIAPH2, GPR33, CCDC198, SERPINB11, VSIG10L, USP29, NUDT11).

   Three genes retained rare pLoF — **and all three show the same artifact signature**:

   | Gene | Rare pLoF | Span | Assessment |
   |---|---|---|---|
   | SERPINA1 | 4 frameshifts | **61 bp** | Clustered indels = misalignment signature. A1AT deficiency is caused by the common Z/S missense alleles, and the phenotype (liver/lung) does not match. |
   | POU6F2 | 2 frameshifts | **2 bp** | Clustered indels. A weak Wilms-tumour candidate locus; not an MVA/chromosomal-instability gene. |
   | ADAMTS1 | 2 frameshifts | **8 bp** | Clustered indels. No established Mendelian disease. |

   Four heterozygous frameshifts within 61 bp in one individual is not plausible true biallelic LoF; it is the classic signature of indel misalignment in low-complexity sequence. **This is an assessment from the variant pattern, not a read-level demonstration** — none of the three is formally excluded without inspecting the alignments, which are unavailable.

   By contrast BUB1B's two variants are a **stop_gained and a missense 10,911 bp apart** — not a clustered-indel artifact pattern.

---

## What remains unresolved — and why CASE B, not CASE A

| Open question | Status | What would resolve it |
|---|---|---|
| **Phase** | **UNKNOWN.** Both `0/1`, no GATK PGT/PID group. The variants are 10,911 bp apart; Illumina fragments (~350–550 bp) cannot span that. | Trio genotyping, or long-read (PacBio HiFi / ONT) on the proband alone |
| **CNV/SV second hit in BUB1B** | **CANNOT BE EXCLUDED.** No SV records, no gVCF, no BAM/CRAM, no depth track — see `SV_CNV_AVAILABILITY.md` | BAM-based CNV calling, exon-dosage MLPA/qPCR on BUB1B, or long-read WGS |
| **Deep-intronic / cryptic splice second hit** | **SCREENED 2026-09-24 — no candidate found.** SpliceAI 1.3.1 + Pangolin over the full locus: all 14 BUB1B records NO SIGNAL, 14/14 concordant, max ΔS 0.03 (vs 0.2 high-recall threshold). Note: 12 of the 68 catalogued "intronic" variants are BUB1B; 56 are PAK6. **Not proof of absence** — these tools have limited sensitivity for branchpoints and pseudoexon activation. | RNA-seq from patient cells (direct observation of transcript) |
| **N1002K pathogenicity** | **PRIORITISED VUS.** No functional evidence of any kind exists for it | Functional assay; phase |
| **MVA diagnosis itself** | **ASSERTED, NOT EVIDENCED** in available records. The HPO set contains no term for mosaic aneuploidy, variegated aneuploidy, PCS or microcephaly | Karyotype / chromosome-count data; PCS assay |

---

## Consequence for the ongoing work

**BUB1B mechanism work is NOT stopped, but it is NOT yet earned either.**

The data did not redirect us away from BUB1B — it is the only candidate that
survives an unbiased, phenotype-driven, frequency-filtered genome-wide screen.
That is a genuine, independent re-establishment and it removes the YELLOW-flag
concern that BUB1B was carried forward only because of a build-error artifact.

But CASE B explicitly means **unresolved**. The rate-limiting evidence is no
longer gene choice — it is **phase**, then **the possibility of a hidden second
hit (CNV/splice)**, then **functional data on N1002K**. Deeper structural or
mechanistic modelling of N1002K does not address any of those three and should
not be prioritised until at least the first is settled.
