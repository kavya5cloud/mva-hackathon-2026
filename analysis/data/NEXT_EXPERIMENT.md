# Next experiment — stop/go rule

**Written 2026-09-24**, after the phase and CNV/SV audits. Supporting detail:
`phase/PHASE_REPORT.md`, `cnv_sv/CNV_SV_REPORT.md`, `DECISION_MATRIX_UPDATED.md`.

---

## 1. HIGHEST INFORMATION-GAIN EXPERIMENT

**Determine the phase of `NM_001211.6:c.2210T>G` (p.Leu737\*) and
`NM_001211.6:c.3006T>G` (p.Asn1002Lys).**

Two acceptable routes, in order of preference given that parental availability is
unknown:

| | Route | Why | Caveats |
|---|---|---|---|
| **1a** | **Trio genotyping** — Sanger sequencing of both sites in proband + both parents | Cheapest and fastest when parents are available and parentage is confirmed | Confounded by non-paternity, parental germline mosaicism, or a *de novo* event. Confirm parentage with a SNP identity panel. |
| **1b** | **Long-read sequencing of the proband** (PacBio HiFi or ONT) | Reads routinely exceed the 10,911 bp separation, so **one sample suffices — no parents needed**. Additionally resolves the CNV/SV question in the same experiment. | Higher cost; needs high-molecular-weight DNA. |

**If neither is obtainable:** allele-specific long-range PCR across 10,911 bp
followed by sequencing of the amplicon is a targeted, low-cost fallback that
directly demonstrates whether the two alternate alleles co-occur on one molecule.

**Explicitly NOT acceptable** as a substitute: statistical/population phasing
(both variants are ultra-rare and absent from reference panels), short-read
physical phasing (fragments ~350–550 bp cannot span 10.9 kb), or inference from
allele balance, genotype quality, or physical proximity.

---

## 2. WHY IT DISCRIMINATES THE MODELS

Phase is the **only** experiment that partitions the current hypothesis space in
a single step. Every other open question is downstream of it.

| Phase result | Case reached | What it does to the models |
|---|---|---|
| **in *trans*** | **CASE A** | Establishes the biallelic architecture required by the recessive model. N1002K becomes the rate-limiting unknown, and functional testing becomes justified. Satisfies ACMG PM3 for N1002K — supporting evidence, **not** proof of pathogenicity. |
| **in *cis*** | **CASE C** | **Falsifies the current biallelic framing.** N1002K is not the second pathogenic allele. Redirects effort to CNV/SV dosage and a wider noncoding search, and makes N1002K functional work largely unjustifiable. |
| **unresolvable** | **CASE B persists** | Forces the CNV/SV assay (below) as the next genetic step, since the *trans*/*cis* question cannot be settled directly. |

The discriminating power is asymmetric and that is precisely why it comes first:
a ***cis*** result would **stop** a whole line of work — N1002K structural and
functional investigation — that is currently the project's main forward momentum.
No other single experiment can do that. Running functional assays on N1002K
before phase risks expensively characterising a variant that may not sit on the
relevant allele.

---

## 3. WHAT RESULT WOULD TRIGGER THE NEXT STEP

| Result | Next step |
|---|---|
| **Phase = *trans*** (CASE A) | **Proceed to N1002K functional testing**, in this order: (i) steady-state abundance by quantitative immunoblot vs WT, with L1012P as destabilised positive control and Q921H as stable negative control; (ii) half-life by cycloheximide chase; (iii) if abundance and half-life are WT-like, SAC/alignment function and KARD pS670/pS676 + kinetochore PP2A-B56 at WT-matched expression. |
| **Phase = *cis*** (CASE C) | **Stop N1002K work.** Proceed directly to ***BUB1B* exon-dosage testing** (MLPA first-line, or qPCR/ddPCR) to search for a structural second hit. If negative, widen the noncoding search beyond the ±50 kb window and revisit alternative genes. |
| **Phase unobtainable** (CASE B persists) | **Proceed to *BUB1B* exon-dosage testing** as the next practical genetic experiment. It is cheap, needs only proband DNA, and addresses the one hidden-variant class that the current VCF cannot see at all. |
| **Exon-dosage positive** (CASE D) | Confirm the CNV is on the allele *not* carrying `p.Leu737*` — a dosage call alone does not establish phase. Then the genetic architecture is resolved and N1002K becomes a likely-incidental third allele. |
| **Phase resolved AND dosage negative** (CASE E) | Report an **unresolved molecular diagnosis.** Do not force a *BUB1B* attribution. Note explicitly that dosage assays miss balanced inversions and translocations, and that the screening window missed distal regulatory elements — "not found" is not "not there." |

### Gate that does not move

**The therapeutic gate remains CLOSED regardless of which branch is taken.** No
genetic result opens it. Mechanism is **C — UNKNOWN**, and the drug search is
gated on mechanism, not on genotype. Functional work (CASE A branch) is the only
path that could eventually change that, and only if it produces a defined,
targetable molecular defect.
