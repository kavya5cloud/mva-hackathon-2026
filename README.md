# Rare Disease, Real Kid: MVA Hackathon 2026

**Team:** kavya5cloud  
**Track:** 1 (Variant Prediction) + 2 (Drug Repurposing)  
**Score:** 100.0 Rank Points / 1.000 F-max  

## Overview

This repository contains our complete analysis pipeline for identifying the causal variants in a child with Mosaic Variegated Aneuploidy (MVA). Our approach combines targeted genomic analysis of the BUB1B gene with clinical phenotype interpretation to identify a compound heterozygous frameshift mutation pair.

## Key Findings

| Variant | Position (GRCh38) | Type | Impact |
|---------|------------------|------|--------|
| C>CTATA | chr15:40425440 | 4bp insertion | Frameshift |
| C>CA | chr15:40488950 | 1bp insertion | Frameshift |

## Pipeline

1. Download VCF (315 MB compressed)
2. Extract BUB1B region (chr15:40,400,000–40,500,000)
3. Filter by quality and genotype
4. Prioritize by predicted functional impact
5. Generate ranked submission

## Run Time

- **Compute:** < 5 minutes
- **Cost:** $0 (local machine)
- **Storage:** ~350 MB

## Tools Used

- bcftools 1.24
- Python 3.x
- macOS (Apple Silicon)

## Data Access

The dataset is gated. Request access at:
https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data

## License

CC BY 4.0 (as per hackathon rules)
