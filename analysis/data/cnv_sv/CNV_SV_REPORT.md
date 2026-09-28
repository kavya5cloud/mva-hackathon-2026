# BUB1B CNV / SV EVIDENCE AUDIT

run date   : 2026-09-24 23:12
input VCF  : WGS_EX2312012_HGWCNDSX7.vcf.gz  (315,153,971 bytes)
bcftools   : bcftools 1.24
BUB1B      : GRCh38 chr15:40,160,984-40,221,137

## 1. Symbolic ALT alleles declared in the VCF header (`##ALT`)
    declared: NONE

## 2. Symbolic ALT alleles actually present in records (<DEL>, <DUP>, <CNV>, <INV>, <INS>)
    records with a symbolic ALT: 0

## 3. Breakend (BND) records
    BND-style records: 0

## 4. SV/CNV INFO keys (SVTYPE, SVLEN, END, CIPOS, CIEND, IMPRECISE, CN, ...)
    SVTYPE       ABSENT
    SVLEN        ABSENT
    END          ABSENT
    CIPOS        ABSENT
    CIEND        ABSENT
    IMPRECISE    ABSENT
    CN           ABSENT
    CNQ          ABSENT
    CNV          ABSENT
    NUMSNP       ABSENT
    BC           ABSENT
    FOLD_CHANGE  ABSENT

## 5. gVCF reference blocks (<NON_REF>)
    <NON_REF> records in first 200k: 0
    => NOT a gVCF (site-level VCF only; no reference-block depth)

## 6. Read-depth / dosage FORMAT fields usable for CNV
    FORMAT keys declared: ['AD', 'DP', 'GQ', 'GT', 'PGT', 'PID', 'PL']
    DP is present, but:
      *** FORMAT/DP IS NOT CNV EVIDENCE AND IS NOT USED HERE. ***
      Called-site depth is ascertainment-biased (present only where a variant
      was called), has no matched control cohort or reference panel, and this
      is a single sample. Any 'CNV' derived from it would be uninterpretable.

## 7. Split-read / discordant-pair evidence
    Requires aligned reads. Checked for BAM/CRAM below.
    No SR/PE/PR-style FORMAT fields are declared in this VCF: NONE

## 8. Aligned reads / raw data on disk
    searched: ['kavyashree', 'mva-hackathon-2026', 'mva-hackathon-2026-1', 'Downloads']
    patterns: ['*.bam', '*.cram', '*.fastq.gz', '*.fq.gz', '*.fastq', '*.fq']
    found   : NONE

## 9. Pre-computed CNV / SV call sets in the project
    patterns: ['*cnv*', '*CNV*', '*sv*.vcf*', '*SV*.vcf*', '*manta*', '*delly*', '*lumpy*', '*gcnv*', '*cnvnator*', '*.seg', '*.cns', '*.cnr']
    found   : NONE

## 10. Variant content at the BUB1B locus (for completeness only)
    records in BUB1B gene body : 14
    of which symbolic/SV       : 0
    (small SNV/indel records only; these cannot reveal exon-level dosage)

## VERDICT
    evidence types found: NONE

    >>> CNV/SV status unresolved from available data. <<<

    No symbolic alleles, no SV/CNV INFO keys, no gVCF reference blocks,
    no usable depth track, no split-read/discordant-pair fields, no BAM/CRAM,
    no FASTQ, and no pre-computed CNV or SV call sets were found.
    A CNV or SV second hit in BUB1B -- for example a single- or multi-exon
    deletion on the allele not carrying p.Leu737* -- CANNOT BE EXCLUDED.

## Minimum practical assay to test BUB1B exon dosage
    NONE OF THE FOLLOWING HAS BEEN PERFORMED. This is a recommendation only.

| Assay | What it measures | Resolution | Practicality | Notes |
|---|---|---|---|---|
| **MLPA** (e.g. a custom BUB1B probemix) | relative copy number, exon by exon | single-exon | Established clinical method; needs ~100 ng DNA; a BUB1B-specific probemix may need custom design | **Most practical first-line dosage test.** Covers all 23 exons in one reaction. |
| **qPCR** (relative dosage vs 2-copy reference) | copy number at selected exons | per-amplicon | Cheapest; any lab with a qPCR machine | Needs 2-3 reference loci and replicate design; only interrogates the exons assayed, so a deletion elsewhere is missed. |
| **ddPCR** | absolute copy number | per-amplicon | More precise than qPCR, less common | Best when a specific exon is already suspected. |
| **Targeted / exome CNV calling from reads** | read-depth ratio | multi-exon | Requires BAM/CRAM, which do not exist here | Would need re-alignment of the ~85 GB raw data, if obtainable. |
| **Long-read WGS** | SV breakpoints AND phase | base-level | Highest cost | **Resolves CNV/SV and phase in one experiment.** |

    Practical note: a dosage assay only interrogates the region it targets. A
    negative MLPA/qPCR result narrows the space; it does not exclude every SV
    class (balanced inversions and translocations disrupting BUB1B would be
    missed by dosage methods entirely).
