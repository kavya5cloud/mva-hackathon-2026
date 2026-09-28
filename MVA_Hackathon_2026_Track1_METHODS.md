> ## ⚠️ HISTORICAL DOCUMENT — READ THE ERRATUM FIRST
>
> This document is the **Track 1 methods record as originally submitted**. It is
> preserved unmodified for provenance. A post-submission audit found a
> **genome-build error**: the extraction interval `15:40400000-40500000` (§7.2) is
> the *BUB1B* locus in **GRCh37**, applied to a **GRCh38** VCF, and has **zero
> overlap** with *BUB1B* in GRCh38. The three prioritised candidates are real
> proband variants but lie in *IVD*, *BAHD1* and a lncRNA — **not *BUB1B***.
>
> **Every compound-heterozygous *BUB1B* statement in this document is therefore
> HISTORICAL and UNSUPPORTED.** See **§30 — Genome-Build / Provenance Erratum** at
> the end of this file, and `analysis/TRACK1_SUBMISSION_ERRATUM.md`.
>
> Separately: the two variants analysed in Track 2 (`p.Leu737*`, `p.Asn1002Lys`)
> **were verified present in the proband VCF** on 2026-09-16, but their **phase is
> undetermined**.

# MVA Hackathon 2026 — Track 1
# Research-Grade Methods & Analysis Report

**Team:** `kavya5cloud`  
**Model:** `model1`  
**Submission file:** `kavya5cloud_bub1b-compound-het-frameshift.csv`  
**Date:** 26 August 2026  
**Repository:** https://github.com/kavya5cloud/mva-hackathon-2026

---

## Abstract

Mosaic Variegated Aneuploidy (MVA) is a rare chromosomal-instability disorder in which constitutional mosaicism for chromosome gains and losses can occur across tissues. For this Track 1 analysis, we developed a phenotype-informed and inheritance-aware workflow to prioritize candidate variants from whole-genome sequencing (WGS) data.

The central design principle was to avoid treating the genome as an undifferentiated search space. The clinical phenotype was first used to establish an MVA-oriented disease model, after which **BUB1B** was selected as the primary candidate gene. Rather than processing the approximately 85 GB raw sequencing dataset, we operated on the provided WGS variant call file (VCF) and its index. An indexed genomic query was used to extract the BUB1B target interval on GRCh38, producing a manageable set of 36 variants for downstream analysis.

Variants were then filtered hierarchically according to technical quality, genotype compatibility, predicted functional consequence, and novelty/rarity. This reduced the candidate set to three high-priority variants. The two leading candidates — `chr15:40425440 C>CTATA` and `chr15:40488950 C>CA` — are heterozygous frameshift insertions and were prioritized as the primary compound-heterozygous hypothesis. `chr15:40447560 GAATAAATA>G`, a further frameshift candidate, was retained as an alternative pairing component.

The reported computational component required less than five minutes of compute time and incurred no direct compute cost on the local analysis environment. The workflow is deliberately compact, interpretable, and reproducible. However, the resulting variants should be considered **prioritized causal candidates rather than definitively validated pathogenic variants**, because phase/segregation and functional validation were not performed within this analysis.

---

# 1. Overview

## 1.1 Purpose of This Report

This document describes the complete methodology used to generate the Track 1 submission.

The goal is not simply to provide a list of variants. It is to document the reasoning chain that connects:

```text
Clinical phenotype
        ↓
Disease model
        ↓
Candidate gene
        ↓
Target genomic region
        ↓
Technical filtering
        ↓
Inheritance filtering
        ↓
Functional prioritization
        ↓
Novelty / rarity assessment
        ↓
Compound-heterozygous pairing
        ↓
Prioritized causal hypothesis
```

This structure makes the analysis easier to inspect, reproduce, critique, and extend.

---

## 1.2 Core Research Question

The analysis asks:

> **Which variants in the provided WGS data are most consistent with the proband's MVA phenotype under a BUB1B-associated, autosomal-recessive disease model?**

This question contains several sub-problems:

1. What disease model best fits the reported phenotype?
2. Which gene should be prioritized?
3. Where is that gene located in the reference genome?
4. Which variants occur in that region?
5. Which variants are technically credible?
6. Which variants fit the expected inheritance architecture?
7. Which variants are predicted to have severe functional consequences?
8. Which candidate pair provides the strongest combined explanation?

---

# 2. Clinical Phenotype Analysis

## 2.1 Reported Phenotype

The following HPO terms were provided for the proband:

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

The supplied clinical material describes this constellation as compatible with a classic MVA presentation.

---

## 2.2 Why Phenotype-First Prioritization Was Used

A whole-genome VCF can contain a very large number of variants. Treating every variant equally would create an unnecessarily broad prioritization problem.

The phenotype provides an information-rich prior.

In this analysis, the phenotype was therefore used to establish an MVA-oriented disease hypothesis before examining variants.

This is particularly useful for a rare disorder because the phenotype can substantially constrain the candidate-gene search.

The strategy can be summarized as:

```text
Phenotype → Disease → Gene → Region → Variant
```

rather than:

```text
All variants → Generic ranking → Attempted interpretation
```

The former approach is intentionally knowledge-driven.

---

# 3. Disease Model

## 3.1 Mosaic Variegated Aneuploidy

The analysis treats MVA as a chromosomal-instability disorder characterized by mosaic chromosome abnormalities and a clinically heterogeneous phenotype.

The supplied report associates the phenotype with:

- Mosaic aneuploidies
- Cancer predisposition
- Growth restriction
- Developmental abnormalities
- Ocular abnormalities
- Renal abnormalities

The clinical presentation supplied for the challenge was therefore used as a strong prior for an MVA-associated genetic mechanism.

---

## 3.2 Candidate Gene: BUB1B

The primary candidate gene selected for this analysis is:

```text
BUB1B
```

The gene encodes BUBR1, a component of the spindle assembly checkpoint.

The working biological model is:

```text
BUB1B loss of function
        ↓
Spindle assembly checkpoint dysfunction
        ↓
Abnormal chromosome segregation
        ↓
Chromosomal instability
        ↓
Mosaic aneuploidy
        ↓
MVA phenotype
```

This provides the biological rationale for prioritizing predicted loss-of-function variants.

---

## 3.3 Alternative MVA Genes

The supplied analysis identifies additional MVA-associated genes including:

- `CEP57`
- `TRIP13`

However, these genes were not evaluated in the same depth during this Track 1 targeted analysis.

This is an important limitation: the workflow deliberately prioritizes BUB1B rather than claiming that BUB1B is the only possible molecular explanation.

---

# 4. Disease Architecture and Inheritance Model

The working inheritance model is:

```text
Autosomal recessive
```

Under this model, a causal genotype may consist of two pathogenic variants affecting the two copies of the gene.

A compound-heterozygous configuration can be represented as:

```text
Allele 1 → Variant A
Allele 2 → Variant B
```

Therefore, the analysis does not stop after finding one damaging heterozygous variant.

Instead, it explicitly searches for combinations of candidate variants that could jointly explain the phenotype.

---

# 5. Data Acquisition

## 5.1 Input Dataset

The analysis used the gated MVA Hackathon dataset.

The relevant data components were:

| File | Approximate size | Purpose |
|---|---:|---|
| `WGS_EX2312012_HGWCNDSX7.vcf.gz` | 315 MB | Whole-genome variant calls |
| `WGS_EX2312012_HGWCNDSX7.vcf.gz.tbi` | 2.3 MB | Tabix index |
| `Challenge_Clinical_Phenotype_1.docx` | 16 KB | Clinical phenotype |

---

## 5.2 Why Raw FASTQ Data Was Not Used

The challenge environment also contained approximately 85 GB of raw sequencing data.

The workflow deliberately avoided downloading and processing the raw FASTQ data because the provided VCF already contains the called variants required for the targeted candidate-identification task.

This decision provides several advantages:

- Lower storage requirements
- Lower data-transfer requirements
- Faster analysis
- No read alignment required
- No variant calling required
- Lower computational complexity

The strategy therefore operates at the **variant-call layer** rather than the **read-processing layer**.

---

# 6. Reference Genome and Target Region

The analysis uses the GRCh38 reference coordinate system.

The BUB1B target region was defined as:

```text
GRCh38
chr15:40,400,000–40,500,000
```

The selected interval represents a focused 100 kb window around the BUB1B locus.

This window was used as the operational target for variant extraction.

---

# 7. Indexed VCF Extraction

## 7.1 Why Indexed Access Matters

The VCF was accompanied by a tabix index.

An indexed VCF allows genomic regions to be queried without reading the entire file sequentially.

This is important because the input VCF is hundreds of megabytes in compressed form, while only a small genomic interval is relevant to the current hypothesis.

---

## 7.2 Extraction Command

The target region was extracted using `bcftools`:

```bash
bcftools view \
  -r 15:40400000-40500000 \
  WGS_EX2312012_HGWCNDSX7.vcf.gz \
  -o bub1b_region.vcf
```

The extraction returned:

> **36 variants**

These 36 variants became the starting set for targeted prioritization.

---

# 8. Variant Prioritization Pipeline

The workflow uses hierarchical filtering.

## 8.1 Pipeline Overview

```text
36 BUB1B-region variants
          │
          ▼
Quality filtering
          │
          ▼
36 variants
          │
          ▼
Genotype filtering
          │
          ▼
11 variants
          │
          ▼
Functional filtering
          │
          ▼
3 variants
          │
          ▼
Novelty / rarity assessment
          │
          ▼
3 prioritized candidates
          │
          ▼
Compound-heterozygous pairing
          │
          ▼
Primary + alternative hypotheses
```

The exact counts reported above are those supplied by the analysis.

---

# 9. Quality Control

## 9.1 Quality Criteria

The first filtering stage prioritized variants meeting:

```text
FILTER = PASS
GQ >= 99
```

The purpose of this stage was to prevent low-confidence variant calls from dominating the downstream interpretation.

The supplied analysis reports that all 36 variants in the extracted region met the stated quality-stage criterion.

---

## 9.2 Why Genotype Quality Matters

Genotype quality provides a measure of confidence in the assigned genotype.

Because the downstream analysis relies on distinguishing heterozygous and compound-heterozygous configurations, genotype confidence is especially relevant.

A weak genotype call could otherwise create a false inheritance hypothesis.

---

# 10. Genotype and Inheritance Filtering

The next stage applied the recessive disease model.

Variants were prioritized when represented as:

```text
0/1
```

or in compound-heterozygous representation:

```text
1/2
```

Variants that did not fit the desired inheritance architecture were deprioritized.

The reported number of candidates after this stage was:

> **11 variants**

---

## 10.1 Why Heterozygous Variants Were Retained

A single heterozygous variant is not necessarily sufficient to explain an autosomal-recessive phenotype.

However, two damaging heterozygous variants affecting the same gene can form a compound-heterozygous hypothesis.

Therefore, heterozygous variants were retained rather than discarded.

---

# 11. Functional Consequence Filtering

## 11.1 Functional Priority

The workflow then prioritized variants according to predicted functional consequence.

High-priority changes included:

- Frameshift
- Truncating variants
- Other severe loss-of-function candidates

The reasoning is straightforward:

```text
More severe predicted functional disruption
                ↓
Greater candidate priority
```

After functional filtering:

> **3 candidates remained**

---

## 11.2 Why Frameshifts Were Prioritized

A frameshift changes the reading frame downstream of an insertion or deletion.

For a coding sequence, this can lead to:

- Altered downstream amino acids
- Premature termination
- Loss of essential protein domains
- Reduced or absent functional protein

Because the working BUB1B disease model involves loss of function, frameshift candidates receive particularly high priority.

---

# 12. Novelty and Population-Frequency Considerations

The analysis also incorporated variant novelty.

Candidates without an established dbSNP identifier were prioritized relative to variants with known population identifiers.

This is not equivalent to proving pathogenicity.

A novel variant can be:

- Pathogenic
- Benign
- Rare because of technical or demographic reasons
- Previously unreported

Therefore, novelty was used as a **prioritization feature**, not as a standalone pathogenicity criterion.

---

# 13. Final Candidate Set

Three candidates survived the principal filtering stages.

| Rank | Position | Alleles | Type | Genotype |
|---:|---|---|---|---|
| **1** | `chr15:40425440` | `C>CTATA` | 4 bp frameshift insertion | `0/1` |
| **2** | `chr15:40488950` | `C>CA` | 1 bp frameshift insertion | `0/1` |
| **3** | `chr15:40447560` | `GAATAAATA>G` | Complex deletion / frameshift | `1/2` |

---

# 14. Candidate 1: chr15:40425440 C>CTATA

## 14.1 Variant Description

```text
chr15:40425440 C>CTATA
```

The reported interpretation is:

- 4 bp insertion
- Frameshift
- Heterozygous
- `PASS`
- `GQ = 99`
- `DP = 36`
- `QD = 17.71`
- No rsID reported
- Balanced allele support

Reported allele counts:

```text
Reference: 14
Alternate: 11
```

---

## 14.2 Interpretation

The insertion changes the downstream reading frame and is predicted to result in premature termination.

The supplied analysis therefore considers it a strong loss-of-function candidate.

Its combination of:

- Severe predicted functional consequence
- High genotype quality
- Novelty
- Heterozygous state
- BUB1B biological relevance

makes it one of the two leading candidates.

---

# 15. Candidate 2: chr15:40488950 C>CA

## 15.1 Variant Description

```text
chr15:40488950 C>CA
```

Reported characteristics:

- 1 bp insertion
- Frameshift
- Heterozygous
- `PASS`
- `GQ = 99`
- `DP = 26`
- `QD = 6.91`
- No rsID reported

Reported allele counts:

```text
Reference: 11
Alternate: 15
```

---

## 15.2 Interpretation

The single-base insertion changes the reading frame and is predicted to cause premature termination.

This provides a second strong loss-of-function candidate in the same gene.

Its heterozygous state makes it particularly relevant when evaluated jointly with the other heterozygous BUB1B frameshift.

---

# 16. Candidate 3: chr15:40447560 GAATAAATA>G

## 16.1 Variant Description

```text
chr15:40447560 GAATAAATA>G
```

Reported characteristics:

- Complex deletion
- Predicted frameshift
- `PASS`
- `GQ = 99`
- `DP = 53`
- `QD = 39.68`
- No rsID reported
- Compound-heterozygous representation reported as `1/2`

---

## 16.2 Interpretation

The predicted frameshift makes this variant biologically compatible with the loss-of-function hypothesis.

However, within the supplied ranking it was not selected as the primary pair.

Instead, it is retained as an alternative component of the compound-heterozygous hypothesis.

---

# 17. Compound-Heterozygous Pair Ranking

The candidate-pair framework generated three possible pairings.

| Rank | Pair | EPCR | Interpretation |
|---:|---|---:|---|
| **1** | `40425440 + 40488950` | `0.95` | Primary hypothesis |
| **2** | `40447560 + 40425440` | `0.85` | Alternative |
| **3** | `40447560 + 40488950` | `0.80` | Alternative |

---

# 18. EPCR Scoring Framework

The analysis uses an Estimated Probability of Causal Relationship (EPCR) framework.

The conceptual formula is:

```text
EPCR =
    w1 × Functional Severity
  + w2 × Novelty
  + w3 × Quality
  + w4 × Biological Plausibility
```

The supplied weights are:

| Evidence dimension | Weight |
|---|---:|
| Functional severity | `0.40` |
| Novelty | `0.25` |
| Quality | `0.20` |
| Biological plausibility | `0.15` |

---

## 18.1 Functional Severity

Functional severity receives the highest weight.

This reflects the disease model: BUB1B loss of function is expected to be more compelling than variants with minimal predicted impact.

---

## 18.2 Novelty

Novel variants receive greater prioritization because established common variants are less likely to explain an ultra-rare Mendelian phenotype.

However, novelty is not proof of pathogenicity.

---

## 18.3 Technical Quality

High-quality calls are preferred because a biologically compelling variant is not useful if the underlying genotype call is unreliable.

---

## 18.4 Biological Plausibility

The candidate must make sense within the established disease model.

A severe variant in an unrelated gene would not receive the same biological-priority score as a similarly severe variant in BUB1B.

---

# 19. Primary Causal Hypothesis

The primary candidate pair is:

```text
chr15:40425440 C>CTATA
                +
chr15:40488950 C>CA
```

The supplied analysis assigns this pair:

```text
EPCR = 0.95
```

The rationale is that both variants:

- Occur in BUB1B
- Are heterozygous
- Are predicted frameshifts
- Are novel candidates
- Have high reported genotype quality
- Fit the recessive disease model
- Have strong biological plausibility

---

# 20. Alternative Causal Hypotheses

The analysis does not discard the third candidate.

Two alternative pairings are retained:

### Alternative 1

```text
chr15:40447560 GAATAAATA>G
                +
chr15:40425440 C>CTATA
```

Reported EPCR:

```text
0.85
```

### Alternative 2

```text
chr15:40447560 GAATAAATA>G
                +
chr15:40488950 C>CA
```

Reported EPCR:

```text
0.80
```

Maintaining alternative hypotheses is important because variant prioritization is not the same as proof.

---

# 21. Secondary Finding

The supplied analysis reports a secondary variant:

```text
chr15:40492443 C>CTTATTA
```

### Characteristics

- 6 bp in-frame insertion
- `rs59250073`
- Present in dbSNP
- Lower prioritization
- EPCR: `0.30`

The variant was retained for completeness but not promoted to the primary causal hypothesis.

This illustrates the difference between:

```text
Detected variant
```

and:

```text
Prioritized candidate variant
```

Not every detected variant is expected to contribute to disease.

---

# 22. Evidence Hierarchy

The analysis can be understood as an evidence hierarchy:

```text
                 Clinical phenotype
                         │
                         ▼
                 Disease association
                         │
                         ▼
                   Gene relevance
                         │
                         ▼
                Variant call quality
                         │
                         ▼
               Inheritance compatibility
                         │
                         ▼
              Functional consequence
                         │
                         ▼
                Novelty / rarity
                         │
                         ▼
               Candidate pair ranking
```

No single layer is intended to establish pathogenicity by itself.

The strongest candidate is the one supported across multiple independent dimensions.

---

# 23. Computational Environment

The reported analysis used:

| Tool | Version / Environment | Function |
|---|---|---|
| `bcftools` | `1.24` | Indexed VCF extraction |
| Python | `3.x` | Analysis / prioritization |
| macOS | Apple Silicon | Local compute environment |

The workflow intentionally avoids dependency on a large cloud-compute environment.

---

# 24. Runtime and Cost Analysis

| Operation | Reported time |
|---|---:|
| WGS VCF download | ~5 minutes |
| BUB1B region extraction | <2 seconds |
| Manual curation | ~30 minutes |
| **Compute time** | **<5 minutes** |
| **Direct compute cost** | **$0** |

The distinction between compute time and manual curation is intentional.

Manual review requires human reasoning and is therefore not equivalent to machine execution time.

---

# 25. Efficiency Analysis

The workflow demonstrates an important computational principle:

> **Reduce the search space using domain knowledge before applying expensive analysis.**

Instead of:

```text
~85 GB raw sequencing
        ↓
Alignment
        ↓
Variant calling
        ↓
Millions of variants
        ↓
Genome-wide annotation
        ↓
Prioritization
```

the workflow operates as:

```text
Provided WGS VCF
        ↓
BUB1B target interval
        ↓
36 variants
        ↓
11 genotype-compatible candidates
        ↓
3 functional candidates
        ↓
3 prioritized candidates
        ↓
Compound-heterozygous ranking
```

This is why the workflow can be executed rapidly on a local machine.

---

# 26. Strengths

## 26.1 Rapid

The targeted extraction avoids unnecessary genome-wide computation.

## 26.2 Low Resource Requirements

The analysis operates directly on the provided VCF rather than raw reads.

## 26.3 Clinically Informed

The phenotype drives gene selection.

## 26.4 Inheritance Aware

The workflow explicitly models compound heterozygosity.

## 26.5 Biologically Interpretable

Each filtering stage has a clear biological or technical rationale.

## 26.6 Reproducible

The target region and extraction command are explicitly documented.

## 26.7 Generalizable Concept

The framework can be adapted to other disorders when:

- The phenotype is sufficiently informative
- A candidate gene can be prioritized
- The inheritance model is known
- A suitable variant-call dataset is available

---

# 27. Limitations

## 27.1 Prior Knowledge Dependency

The workflow assumes a strong disease-to-gene association.

If the true gene is unknown, the targeted strategy could miss the causal locus.

---

## 27.2 Single-Gene Focus

The primary analysis focuses on BUB1B.

Alternative genes such as CEP57 and TRIP13 were not analyzed with the same depth.

---

## 27.3 No Phasing

The most important unresolved question is whether the leading variants are located on opposite alleles.

A true compound-heterozygous interpretation requires variants to be in trans.

The current analysis does not establish this.

---

## 27.4 No Functional Validation

The predicted frameshift consequences are computational interpretations.

No laboratory experiment was performed to demonstrate loss of BUBR1 function.

---

## 27.5 Manual Interpretation

Human review remains part of the final ranking process.

This creates an opportunity for subjective interpretation.

---

## 27.6 Limited Automated Annotation

The workflow does not currently include comprehensive automated annotation using tools such as VEP or SnpEff.

---

## 27.7 Novelty Is Not Pathogenicity

A novel variant is not automatically disease-causing.

Novelty should be treated as supporting evidence only.

---

# 28. Validation Plan

The next stage of the analysis would be validation of the prioritized hypothesis.

## 28.1 Phase Confirmation

Determine whether:

```text
Variant A
```

and

```text
Variant B
```

are located on opposite parental chromosomes.

---

## 28.2 Parental Segregation

Where parental samples are available, test whether each candidate variant segregates as expected under the recessive model.

A simplified expectation would be:

```text
Parent 1 → Variant A carrier
Parent 2 → Variant B carrier
Proband  → Variant A + Variant B
```

---

## 28.3 Independent Variant Confirmation

Orthogonal confirmation could be used to verify the candidate variants independently of the original variant-calling process.

---

## 28.4 Functional Assessment

Where appropriate, functional assays could assess whether the variants produce the expected disruption of BUBR1 function.

---

## 28.5 Broader Genomic Analysis

A comprehensive follow-up should also evaluate alternative MVA-associated genes rather than assuming BUB1B is the sole possible explanation.

---

# 29. Future Improvements

The workflow could be extended in several directions.

### Automated Annotation

Integrate:

- VEP
- SnpEff
- ClinVar
- Population-frequency resources
- Gene/transcript annotations

### Automated Phenotype Matching

Introduce HPO-based gene prioritization so that candidate genes can be ranked without manually selecting BUB1B.

### Multi-Gene Analysis

Extend the targeted approach from one gene to a panel of MVA-associated genes.

### Automated Compound-Het Search

Generate all compatible heterozygous candidate pairs and rank them automatically.

### Phase-Aware Ranking

Incorporate read-backed or pedigree-based phasing into candidate scoring.

### Evidence Integration

Combine:

```text
Phenotype
+
Population frequency
+
Functional consequence
+
Splicing prediction
+
Conservation
+
Clinical databases
+
Segregation
+
Phasing
```

into a more comprehensive ranking system.

---

# 30. Reproducibility

## Primary Input

```text
WGS_EX2312012_HGWCNDSX7.vcf.gz
```

## Index

```text
WGS_EX2312012_HGWCNDSX7.vcf.gz.tbi
```

## Reference Genome

```text
GRCh38
```

## Target

```text
chr15:40,400,000–40,500,000
```

## Extraction

```bash
bcftools view \
  -r 15:40400000-40500000 \
  WGS_EX2312012_HGWCNDSX7.vcf.gz \
  -o bub1b_region.vcf
```

## Submission

```text
kavya5cloud_bub1b-compound-het-frameshift.csv
```

## Repository

```text
https://github.com/kavya5cloud/mva-hackathon-2026
```

## AI-assisted analysis

AI-assisted analysis disclosure: Anthropic Claude Opus 5 and Claude Opus 5.5 were
used via the Claude API with a Pro plan. Data sharing for model training was disabled.
AI-assisted outputs were independently checked against the project's source data and
evidence record.

---

# 31. Reproducibility Checklist

- [x] Clinical phenotype reviewed
- [x] MVA-oriented disease model established
- [x] BUB1B selected as primary candidate gene
- [x] GRCh38 coordinate system used
- [x] Indexed VCF accessed directly
- [x] BUB1B target region extracted
- [x] 36 regional variants identified
- [x] Quality filtering applied
- [x] Genotype filtering applied
- [x] Functional prioritization applied
- [x] Novelty considered
- [x] Three final candidates retained
- [x] Compound-heterozygous pair ranking performed
- [x] Secondary finding documented
- [x] Runtime and cost documented
- [x] Limitations documented
- [x] Validation requirements documented
- [x] Submission file identified
- [x] GitHub repository identified

---

# 32. Final Candidate Summary

| Category | Variant |
|---|---|
| **Primary candidate 1** | `chr15:40425440 C>CTATA` |
| **Primary candidate 2** | `chr15:40488950 C>CA` |
| **Alternative candidate** | `chr15:40447560 GAATAAATA>G` |
| **Secondary finding** | `chr15:40492443 C>CTTATTA` |
| **Primary pair** | `40425440 + 40488950` |
| **Primary EPCR** | `0.95` |
| **Alternative pair 1 EPCR** | `0.85` |
| **Alternative pair 2 EPCR** | `0.80` |

---

# 33. Overall Conclusion

The Track 1 workflow demonstrates how a rare-disease genomic problem can be approached using a combination of **clinical phenotype interpretation, disease-gene knowledge, targeted genomic extraction, quality control, inheritance modeling, functional prioritization, and candidate-pair analysis**.

The strategy deliberately avoids treating the entire genome as an undifferentiated search space. Instead, the phenotype is used to establish an MVA-oriented prior, BUB1B is selected as the primary candidate gene, and an indexed WGS VCF is queried directly for the relevant genomic region.

This produces a compact set of 36 variants, which is subsequently reduced through sequential filtering to three high-priority candidates.

The leading hypothesis is:

```text
BUB1B
│
├── chr15:40425440 C>CTATA
│       └── heterozygous frameshift
│
└── chr15:40488950 C>CA
        └── heterozygous frameshift
```

Together, these variants form the primary compound-heterozygous hypothesis, with an EPCR of `0.95` under the supplied scoring framework.

The third frameshift candidate,

```text
chr15:40447560 GAATAAATA>G
```

remains important as an alternative explanation and prevents the analysis from overcommitting to a single pair without additional evidence.

The main methodological contribution is therefore the **integration of disease knowledge with inheritance-aware computational filtering**.

The workflow shows that a targeted strategy can dramatically reduce the amount of data that must be processed while maintaining an interpretable connection between phenotype and candidate variants.

At the same time, the analysis has clear scientific boundaries. The current results do **not** establish definitive pathogenicity, nor do they prove that the two leading variants are in trans. Confirmation would require appropriate phase/segregation analysis, independent variant confirmation, and potentially functional testing.

The resulting work should therefore be viewed as a **high-priority computational hypothesis generation pipeline** that provides a clear and reproducible starting point for downstream validation.

---

# 34. Acknowledgements

This work was made possible through the Hackathon, organized by **Sage Bionetworks** in partnership with the **MVA Society, Hugging Face, and BEACON**, with prize sponsorship from **AWS and Anthropic**.

We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease.

---

# 35. Scientific Interpretation Note

This document describes the methodology and candidate prioritization performed for the MVA Hackathon Track 1 analysis.

The candidate variants and causal interpretation reported here are derived from the supplied analysis and should be understood as **research hypotheses generated from genomic and clinical evidence**.

They should not be interpreted as independent clinical confirmation of a diagnosis or as definitive proof of pathogenicity.

Further evidence — particularly phasing, segregation, orthogonal confirmation, and functional validation — would be required for definitive causal assignment.

---

## Citation / Project Information

**Project:** MVA Hackathon 2026 — Track 1  
**Team:** `kavya5cloud`  
**Model:** `model1`  
**Submission:** `kavya5cloud_bub1b-compound-het-frameshift.csv`  
**Repository:** https://github.com/kavya5cloud/mva-hackathon-2026

---

# 30. Genome-Build / Provenance Erratum

**Added 2026-09-16, after submission.** Nothing above this line has been altered.
All original commands, tables and interpretations are preserved as the
**HISTORICAL RECORD**. This section supplies the **CORRECTED INTERPRETATION**.

Verification script: `analysis/scripts/step0_verify_provenance.py`. 
Evidence: `analysis/data/provenance/`. Full record: `analysis/round2_variant_characterisation.md` §R3.1.

## 30.1 HISTORICAL RECORD

**Documented build** (§6, §Reference Genome, Reproducibility checklist):

```text
GRCh38
```

**Documented extraction command** (§7.2):

```bash
bcftools view \
  -r 15:40400000-40500000 \
  WGS_EX2312012_HGWCNDSX7.vcf.gz \
  -o bub1b_region.vcf
```

**Documented result:** 36 variants; three prioritised candidates
(`chr15:40425440 C>CTATA`, `chr15:40488950 C>CA`, `chr15:40447560 GAATAAATA>G`);
primary hypothesis = a compound-heterozygous frameshift pair in *BUB1B* (EPCR 0.95).

## 30.2 CORRECTED INTERPRETATION

### The VCF is GRCh38 — the build statement was right

| Evidence | Value |
|---|---|
| `##reference` | `GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta` |
| `##contig=<ID=15,...>` | `length=101991189` → **GRCh38** (GRCh37 chr15 = 102,531,392) |
| Contig naming | no `chr` prefix |

### The extraction interval was GRCh37 — this is the error

| Build | *BUB1B* span (Ensembl, verified 2026-09-15) | Overlap with `40,400,000–40,500,000` |
|---|---|---|
| **GRCh38** — the VCF's actual build | chr15:**40,160,984–40,221,137** | **0 bp — NO OVERLAP** |
| GRCh37 | chr15:**40,453,224–40,513,337** | 46,770 bp |

**The documented interval is the *BUB1B* locus in GRCh37, applied to a GRCh38
VCF.** The pipeline executed exactly as written — re-running that command returns
**36 variants**, matching §7.2 precisely — but the window does not contain *BUB1B*
in GRCh38.

### What the three candidates actually are

All three are genuine, `PASS`-quality heterozygous variants in the proband. Their
gene assignment in GRCh38 is not *BUB1B*:

| Candidate | GRCh38 gene (VCF's build) | GRCh37 gene |
|---|---|---|
| `chr15:40425440 C>CTATA` | **IVD** | *no gene* |
| `chr15:40488950 C>CA` | lncRNA **ENSG00000259536** | *BUB1B* |
| `chr15:40447560 GAATAAATA>G` | **BAHD1** | *no gene* |

**Why the original interpretation was problematic:** the primary hypothesis
(§13, §17) required both leading candidates to be frameshift variants in *BUB1B*.
Under the VCF's actual build, **neither is a *BUB1B* variant**. The
compound-heterozygous *BUB1B* frameshift conclusion therefore does not follow from
the data, independently of the separate fact that phase was never established
(correctly conceded at §27.3).

### The gated VCF resolves the issue — for the currently analysed variants

Corrected extraction:

```bash
bcftools view -r 15:40158984-40223137 WGS_EX2312012_HGWCNDSX7.vcf.gz
```

returns **15** variants in the GRCh38 *BUB1B* locus, including both variants under
analysis in Track 2:

| Variant | GRCh38 | REF>ALT | FILTER | GT | DP | GQ | AD | VAF |
|---|---|---|---|---|---|---|---|---|
| c.2210T>G p.Leu737\* | 15:40,209,701 | T>G | PASS | 0/1 | 46 | 99 | 21,25 | 0.543 |
| c.3006T>G p.Asn1002Lys | 15:40,220,612 | T>G | PASS | 0/1 | 28 | 99 | 15,13 | 0.464 |

## 30.3 Provenance status

| Item | Status |
|---|---|
| **p.Leu737\* provenance** | ✅ **VERIFIED PRESENT** in the proband VCF. REF/ALT match, PASS, GT 0/1, DP 46, GQ 99, VAF 0.543. |
| **p.Asn1002Lys provenance** | ✅ **VERIFIED PRESENT** in the proband VCF. REF/ALT match, PASS, GT 0/1, DP 28, GQ 99, VAF 0.464. |
| **Phase** | ❌ **UNDETERMINED.** Both unphased (`0/1`); no GATK PGT/PID phasing group links them; sites are 10,911 bp apart, beyond short-read reach. Trio or long-read sequencing required. |
| **Original three candidates** | ✅ present in the VCF, but ❌ **not *BUB1B* variants** in GRCh38. |
| **Original compound-het *BUB1B* frameshift conclusion** | ❌ **NOT SUPPORTED.** Superseded. |

## 30.4 Lesson for the pipeline

Add an assertion between the region query and any downstream interpretation:
confirm the build from `##reference` / contig lengths, and confirm that the
queried interval actually overlaps the intended gene **in that build**, before
attributing any returned variant to that gene. `step0_verify_provenance.py`
implements this check.

## 30.5 Correction to the verification script itself

An earlier revision of `step0_verify_provenance.py` queried `FORMAT/PS`
unconditionally. `PS` is not declared in this VCF (GATK emits `PGT`/`PID`), so
`bcftools query` exited non-zero with empty stdout, which the script misread as
**"variant not present"** — a false negative that briefly and incorrectly
suggested both variants were absent. The script now queries only FORMAT tags
declared in the header and surfaces `bcftools` stderr instead of discarding it.
The result above is from the corrected script.
