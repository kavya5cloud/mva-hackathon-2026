# Track 1 Submission Erratum

**Date of correction:** 2026-09-16 
**Raised by:** post-submission coordinate and provenance audit (Round 3) 
**Verification script:** [`scripts/step0_verify_provenance.py`](scripts/step0_verify_provenance.py) 
**Evidence:** [`data/provenance/`](data/provenance/) · full record in [`round2_variant_characterisation.md`](round2_variant_characterisation.md) §R3.1

> **Both original submission CSVs are preserved byte-for-byte**, in place at the
> repository root and archived under `analysis/data/provenance/*_original.csv`.
> **Nothing has been overwritten.** This document records what the original
> artifacts claimed, why those claims are unsupported, and what the corrected
> interpretation is.

---

## 1. Provenance verification result (the basis for this erratum)

Run 2026-09-16 against the gated proband VCF.

| Item | Value |
|---|---|
| Source VCF | `WGS_EX2312012_HGWCNDSX7.vcf.gz` |
| VCF md5 | `a04ea354141cfb032872d67a11c8d2d8` |
| Size | 315,153,971 bytes |
| Sample | `WGS_EX2312012` |
| `##reference` | `GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta` |
| chr15 contig | `<ID=15,length=101991189>` → **GRCh38** (GRCh37 would be 102,531,392) |
| Contig naming | no `chr` prefix |
| Caller | GATK 4.2.4.0 `VariantFiltration` |
| Phasing tags declared | `PGT`, `PID` (GATK physical phasing). **`PS` is not declared.** |
| bcftools | 1.24 |

### Variants verified present in the proband

| Variant | GRCh38 | REF>ALT | FILTER | GT | DP | GQ | AD | VAF | PGT/PID |
|---|---|---|---|---|---|---|---|---|---|
| c.2210T>G p.Leu737\* | 15:40,209,701 | T>G ✓ | PASS | 0/1 | 46 | 99 | 21,25 | 0.543 | `.` / `.` |
| c.3006T>G p.Asn1002Lys | 15:40,220,612 | T>G ✓ | PASS | 0/1 | 28 | 99 | 15,13 | 0.464 | `.` / `.` |

**Both variants are legitimately attributable to the proband.** REF/ALT match the
expected alleles, both are `PASS`, both have GQ 99, adequate depth and clean
heterozygous allele balance. **Normalization is not at issue** — both are SNVs.

**Phase: UNDETERMINED.** Both genotypes are unphased (`0/1`) and neither carries a
PGT/PID phasing group. GATK physical phasing links only variants within a single
read/fragment; these sites are **10,911 bp** apart, far beyond short-read reach
(~350–550 bp).

---

## 2. Artifact 1 — `kavya5cloud_bub1b-compound-het-frameshift.csv`

**Original record (preserved verbatim):**

```csv
proband_id,chrom_1,pos_1,ref_1,alt_1,chrom_2,pos_2,ref_2,alt_2,epcr,finding_type,notes
PROBAND01,chr15,40425440,C,CTATA,chr15,40488950,C,CA,0.95,primary,"Compound heterozygous frameshift variants in BUB1B causing MVA"
```

**Original claim:** two frameshift variants **in *BUB1B***, **compound
heterozygous**, **causing MVA**, EPCR 0.95.

**Why it is unsupported — three independent failures:**

1. **Wrong gene (genome-build error).** The VCF is GRCh38. The extraction window `15:40,400,000–40,500,000` is the *BUB1B* locus in **GRCh37** and has **zero overlap** with *BUB1B* in GRCh38 (chr15:40,160,984–40,221,137). In GRCh38 these positions are:
   - `chr15:40,425,440` → **IVD**
   - `chr15:40,488,950` → lncRNA **ENSG00000259536**
   
   Neither is a *BUB1B* variant.
2. **Phase never demonstrated.** No trio, no long-read, and the variants are unphased. The Track 1 methods document itself concedes this at §27.3.
3. **Causality never demonstrated.** "causing MVA" asserts a causal relationship established by no experiment or segregation evidence.

Both variants **are** real, PASS-quality heterozygous proband variants — the error
is in gene assignment and interpretation, not in variant calling.

**Corrected interpretation:** *Two heterozygous frameshift insertions in the
proband at chr15:40,425,440 (IVD) and chr15:40,488,950 (lncRNA ENSG00000259536),
GRCh38. Not *BUB1B* variants. Phase undetermined. No causal relationship to MVA is
established.*

**Status:** **SUPERSEDED.** Retained as a historical submission artifact only.

---

## 3. Artifact 2 — `kavya5cloud_submission3_bub1b_compoundhet.csv`

**Original record (preserved verbatim):**

```csv
proband_id,chrom_1,pos_1,ref_1,alt_1,chrom_2,pos_2,ref_2,alt_2,epcr,finding_type,notes
PROBAND01,chr15,40209701,T,G,chr15,40220612,T,G,0.95,primary,"BUB1B compound-heterozygous candidate: NM_001211.6:c.2210T>G (p.Leu737*) + c.3006T>G (p.Asn1002Lys)"
```

**Original claim:** a *BUB1B* **compound-heterozygous candidate**, EPCR 0.95.

**What is CORRECT in this artifact:**
- ✅ Both coordinates are correct GRCh38 positions **within** *BUB1B*.
- ✅ Both variants are **verified present** in the proband (§1 above).
- ✅ REF/ALT, gene, transcript and HGVS are all correct.

**What is unsupported:**
- ❌ **"compound-heterozygous"** — phase has never been determined and cannot be determined from the existing short-read data.
- ⚠️ **EPCR 0.95** — difficult to defend for a pair whose phase is unknown and where one allele (p.Asn1002Lys) has **no ClinVar record and no functional evidence of any kind**. The value is not corrected here because the hackathon's EPCR semantics are not defined in this repository; it is flagged for review.

**Corrected interpretation (approved wording):**

> *Two heterozygous *BUB1B* variants of interest in a recessive-model candidate
> gene: NM_001211.6:c.2210T>G (p.Leu737\*) and c.3006T>G (p.Asn1002Lys).
> **Phase undetermined.** Not established as compound heterozygous.*

**Status:** **COORDINATES AND VARIANTS CONFIRMED; INTERPRETATION CORRECTED.**

---

## 4. Relationship between original and corrected artifacts

```
kavya5cloud_bub1b-compound-het-frameshift.csv   (Track 1, earlier)
        │  SUPERSEDED - wrong gene (GRCh37 window on a GRCh38 VCF)
        ▼
kavya5cloud_submission3_bub1b_compoundhet.csv   (Track 1, submission 3)
        │  coordinates and variants CONFIRMED against the proband VCF
        │  interpretation CORRECTED: "compound heterozygous" -> "phase undetermined"
        ▼
analysis/kavya5cloud_track2_report.md                 (Track 2)
           mechanism UNRESOLVED; therapeutic gate CLOSED
```

**Neither CSV has been modified.** The corrected interpretation lives in this
erratum, in `README.md`, and in the Track 2 report. If the hackathon permits a
resubmission, the `notes` field of submission 3 should read:

```
"BUB1B: two heterozygous variants of interest, phase undetermined: NM_001211.6:c.2210T>G (p.Leu737*) + c.3006T>G (p.Asn1002Lys)"
```

We did not apply that edit unilaterally, because altering a scored submission
artifact after the fact would itself destroy provenance.

---

## 5. Claims that must not be made on the basis of these artifacts

- ❌ "compound heterozygous" · "biallelic" · "in trans"
- ❌ "frameshift variants in *BUB1B*" (for the first artifact — they are in *IVD* and a lncRNA)
- ❌ "causing MVA"
- ❌ any statement that phase, segregation, or causality has been demonstrated

**Permitted:** "two heterozygous *BUB1B* variants of interest, phase undetermined",
for the second artifact only.
