# MVA Hackathon 2026 — Track 1 Methods Report

**Team:** kavya5cloud  
**Model:** model1  
**Submission File:** kavya5cloud_bub1b-compound-het-frameshift.csv  
**Date:** 26 August 2026  
**GitHub:** https://github.com/kavya5cloud/mva-hackathon-2026  

---

## Abstract

We identified compound heterozygous frameshift variants in **BUB1B** (BUB1 mitotic checkpoint serine/threonine kinase B) as the likely cause of Mosaic Variegated Aneuploidy (MVA) in the proband. Our approach combined targeted genomic region extraction with biological knowledge of MVA genetics, completing analysis in under 5 minutes of compute time at zero cost.

---

## Approach

### 1. Clinical Phenotype Analysis
- Reviewed HPO terms: rhabdomyosarcoma (HP:0002859), nephrocalcinosis (HP:0000121), short stature (HP:0004322), failure to thrive (HP:0001508), skeletal muscle atrophy (HP:0003202), premature birth (HP:0001622), small for gestational age (HP:0001518), recurrent spontaneous abortion (HP:0200067)
- Recognized constellation as classic MVA presentation
- Identified BUB1B as established causal gene (OMIM #257300)

### 2. Data Acquisition
- Downloaded WGS VCF (315 MB compressed) + index (2.3 MB)
- Avoided 85 GB raw sequencing data
- Used gated Hugging Face dataset access

### 3. Region Extraction
- Extracted BUB1B region: GRCh38 chr15:40,400,000–40,500,000
- Command: `bcftools view -r 15:40400000-40500000`
- Result: 36 variants in region

### 4. Variant Filtering

| Filter | Criterion | Variants Remaining |
|--------|-----------|-------------------|
| Quality | PASS, GQ≥99 | 36 |
| Genotype | 0/1 or 1/2 | 11 |
| Functional | Frameshift/truncating | 3 |
| Novelty | No rsID or rare | 3 |

### 5. Final Candidates

| Rank | Position | Variant | Type | Genotype |
|------|----------|---------|------|----------|
| 1 | chr15:40425440 | C>CTATA | 4bp frameshift insertion | 0/1 |
| 2 | chr15:40488950 | C>CA | 1bp frameshift insertion | 0/1 |
| 3 | chr15:40447560 | GAATAAATA>G | Complex deletion | 1/2 |

---

## Rationale

1. **Biological plausibility**: BUB1B encodes BUBR1, essential for spindle assembly checkpoint. Biallelic loss causes chromosomal instability → cancer predisposition + growth failure.

2. **Variant severity**: Both top candidates are novel frameshift insertions predicted to cause premature stop codons → complete loss of function.

3. **Inheritance pattern**: Compound heterozygous (0/1 for each) consistent with autosomal recessive MVA.

4. **Quality metrics**: All PASS, GQ=99, balanced allele depth, high QD.

---

## Compound Heterozygous Pair Output

Our approach explicitly outputs compound heterozygous pairs (chrom_2/pos_2/ref_2/alt_2 columns populated), essential for recessive disease architecture.

---

## Secondary Findings

One secondary finding included: chr15:40492443 C>CTTATTA (6bp in-frame insertion, rs59250073). Classified as secondary with low EPCR (0.30).

---

## Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| bcftools | 1.24 | VCF extraction |
| Python | 3.x | Prioritization |
| macOS | Apple Silicon | Compute |

---

## Run Time & Cost

| Metric | Value |
|--------|-------|
| VCF download | ~5 minutes |
| Region extraction | <2 seconds |
| Manual curation | ~30 minutes |
| **Total compute** | **<5 minutes** |
| **Total cost** | **$0** |

---

## Strengths

1. **Rapid**: Under 5 minutes compute time
2. **Zero cost**: Local machine only
3. **Clinically informed**: Leveraged MVA-BUB1B association
4. **Scalable**: Applicable to any monogenic disease
5. **Reproducible**: Full code on GitHub
6. **Compound het aware**: Explicitly handles recessive architecture

## Limitations

1. **Prior knowledge required**: Assumes causal gene known
2. **Manual curation**: Final ranking needs human review
3. **Single-gene focus**: May miss variants in other genes
4. **No automated annotation**: VEP/SnpEff not used

---

## Acknowledgements

*"This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON, with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease."*
