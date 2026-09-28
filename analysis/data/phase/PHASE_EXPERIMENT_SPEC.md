# Phase experiment specification — *BUB1B* c.2210T>G and c.3006T>G

**Written 2026-09-24.** Prepared after the phase audit classified the two
variants **UNPHASED** (`step13_phase_audit.py`; report gitignored — contains
genotypes).

**Target question.** Are `NM_001211.6:c.2210T>G` (p.Leu737\*, chr15:40,209,701)
and `NM_001211.6:c.3006T>G` (p.Asn1002Lys, chr15:40,220,612) on the same
parental chromosome or on opposite ones?

**Governing physical fact.** The two sites are **10,911 bp apart**. Any method
whose evidence footprint is shorter than that cannot link them directly.

> **No laboratory performance figures, turnaround times, success rates or prices
> appear in this document.** None were available from a verifiable source, and
> inventing them would misrepresent the comparison. Where cost or feasibility is
> mentioned it is strictly relative and qualitative.

---

## Option 1 — Trio genotyping

| Item | Detail |
|---|---|
| **Material required** | Proband DNA **plus DNA from both biological parents**. Targeted assay (e.g. Sanger sequencing) at the two positions in all three individuals. |
| **Parents required?** | **Yes — both.** This is the option's defining constraint. |
| **Resolves *cis*/*trans* directly?** | **Indirectly, by inheritance.** It does not observe the two alleles on one molecule; it infers their parental origin. Informative only when each parent carries one and only one of the two variants. |
| **Genomic scale of evidence** | Two independent single-nucleotide observations. **No physical linkage is measured at all** — the 10,911 bp gap is never spanned. |
| **Reveals CNV/SV simultaneously?** | **No.** A targeted genotyping assay gives no dosage or structural information. |
| **Major limitations** | Uninformative if one parent carries both variants or if neither carries one. Confounded by **non-paternity/non-maternity** (mitigate with a SNP identity panel), **parental germline mosaicism**, and a ***de novo*** event in the proband — any of which converts a clean answer into an ambiguous one. Requires parental availability and consent. |
| **Decisive result** | Parent 1 heterozygous for `c.2210T>G` and reference at `c.3006T>G`; Parent 2 heterozygous for `c.3006T>G` and reference at `c.2210T>G`; proband heterozygous for both; parentage confirmed. That pattern is decisive for ***trans***. The mirror pattern — both variants in one parent, the other parent reference at both — is decisive for ***cis***. |

---

## Option 2 — Proband long-read sequencing (PacBio HiFi or ONT)

| Item | Detail |
|---|---|
| **Material required** | **High-molecular-weight proband DNA only.** Can be whole-genome, or targeted to the locus via adaptive sampling / enrichment. HMW extraction is the main sample-quality constraint. |
| **Parents required?** | **No.** This is the option's principal advantage when parents are unavailable, deceased, or parentage is uncertain. |
| **Resolves *cis*/*trans* directly?** | **Yes — directly and physically.** Individual reads spanning both positions show, molecule by molecule, whether the two alternate alleles co-occur. |
| **Genomic scale of evidence** | Read lengths in routine use for HiFi and ONT comfortably exceed the 10,911 bp separation, so single reads can span both sites. Phase blocks typically extend well beyond the locus. |
| **Reveals CNV/SV simultaneously?** | **Yes.** This is the only option here that addresses **both** open genetic questions — phase *and* the unresolved CNV/SV status — in one experiment. It detects deletions, duplications, insertions, inversions and translocations, including balanced events that dosage assays miss entirely. |
| **Major limitations** | Highest cost of the three. Requires HMW DNA and a sequencing provider. Coverage at any single locus is stochastic, so a **pre-specified minimum number of spanning reads must be set in advance** (see `MINIMUM_DECISIVE_TEST.md`). Repetitive or low-complexity sequence between the sites could reduce confident spanning alignment. |
| **Decisive result** | A phase block containing both positions, with at least the pre-specified number of independent spanning reads, and a clear majority of informative reads assigning the two alternate alleles either to **opposite** haplotypes (*trans*) or to the **same** haplotype (*cis*). |

---

## Option 3 — Allele-specific long-range PCR

| Item | Detail |
|---|---|
| **Material required** | **Proband DNA only.** Primers flanking both sites, amplifying across the ~10.9 kb interval; long-range polymerase; sequencing of the amplicon (Sanger, or short-read/long-read of the product). |
| **Parents required?** | **No.** |
| **Resolves *cis*/*trans* directly?** | **Yes — physically**, because a single amplicon molecule derives from a single parental chromosome. Either allele-specific priming at one site followed by sequencing at the other, or cloning/single-molecule sequencing of the bulk amplicon to read haplotypes individually. |
| **Genomic scale of evidence** | One ~10.9 kb amplicon — sized specifically to span the gap. Evidence is confined to that interval. |
| **Reveals CNV/SV simultaneously?** | **Only incidentally and unreliably.** A large deletion inside the amplified interval might show as an altered product size, and total amplification failure of one allele is uninterpretable on its own. **This is not a dosage assay and must not be reported as one.** |
| **Major limitations** | Long-range PCR across ~10.9 kb requires optimisation and may fail for sequence-composition reasons. **Allele dropout is the central hazard**: preferential amplification of one chromosome can mimic *cis*. Bulk-amplicon Sanger sequencing averages both haplotypes and is **not** sufficient — haplotypes must be separated (allele-specific priming, cloning, or single-molecule reads). PCR chimeras/recombination between templates can create false haplotypes. Requires positive and negative controls to demonstrate allele-specific priming actually worked. |
| **Decisive result** | Allele-specific amplification anchored on one variant, with sequencing at the other position showing consistently the reference base (*trans*) or consistently the alternate base (*cis*), **in both reciprocal directions**, with controls demonstrating no allele dropout. Single-molecule reads of the amplicon showing a clear haplotype split are equivalent. |

---

## Comparison at a glance

| | Trio | Long-read | Long-range PCR |
|---|---|---|---|
| Parents required | **Yes** | No | No |
| Direct physical linkage | No (inheritance-based) | **Yes** | **Yes** |
| Spans 10,911 bp | No | **Yes** | **Yes** |
| Also answers CNV/SV | No | **Yes** | No |
| Principal failure mode | uninformative parents; non-paternity; *de novo*; mosaicism | locus coverage stochastic | allele dropout; amplification failure |
| Relative cost | lowest | highest | intermediate |

---

## RECOMMENDED ROUTE

**Proband long-read sequencing (Option 2), with trio genotyping (Option 1) as the
route of choice if — and only if — both parents are available and parentage can
be confirmed.**

The recommendation rests on information gained relative to the project's actual
open questions, not on cost.

**Two questions are open, not one.** Phase is UNPHASED and CNV/SV is *unresolved
from available data* — the CNV/SV audit found no evidence of any type: no
symbolic alleles, no gVCF, no depth track, no split-read or discordant-pair
fields, no BAM/CRAM/FASTQ, and no pre-computed calls. **Long-read sequencing is
the only one of the three options that addresses both.** Trio genotyping and
long-range PCR each answer phase alone and leave the CNV/SV question exactly
where it is.

**It does not depend on material we do not know we have.** Parental availability
is not recorded anywhere in this project — `PHENOTYPE.md` lists it among the
missing clinical fields. Long-read requires the proband only, so it cannot be
blocked by that unknown.

**Its failure mode is the most benign.** Insufficient spanning coverage yields
*unresolved* — the status quo — and is remediable by sequencing more deeply. By
contrast, trio genotyping can return a genuinely uninformative parental
configuration, and long-range PCR can return a **positively misleading** result
through allele dropout, which mimics *cis*.

**If long-read is not obtainable**, use trio genotyping when parents are
available, and reserve long-range PCR for the case where neither is possible —
recognising that it answers only the phase question and carries the highest risk
of a confidently wrong answer.

**One caveat that applies to every route: resolving phase does not resolve
causality.** A *trans* result would establish the allele architecture. It would
**not** establish that `p.Asn1002Lys` is pathogenic, and it would **not** open
the therapeutic gate, which is conditioned on mechanism (**C — UNKNOWN**).
