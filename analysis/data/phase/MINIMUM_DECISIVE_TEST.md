# Minimum decisive genetic test — *BUB1B* phase

**Written 2026-09-24.** Pre-registered acceptance criteria, fixed **before** any
data are generated, so the classification cannot be argued after the fact.

**Question.** Assign one of exactly three outcomes to
`NM_001211.6:c.2210T>G` (p.Leu737\*) and `NM_001211.6:c.3006T>G` (p.Asn1002Lys),
which lie **10,911 bp** apart on GRCh38 chr15:

- **A — IN TRANS** (opposite parental chromosomes)
- **B — IN CIS** (same parental chromosome)
- **C — UNRESOLVED**

**C is the default.** A or B is assigned **only** when the corresponding
criterion below is met in full. Anything short of it stays C.

---

## What is NOT phase evidence

These are excluded by rule. None may contribute to an A or B call, alone or in
combination:

| Excluded | Why |
|---|---|
| **Allele balance / VAF** | Both variants are clean heterozygotes (VAF 0.543 and 0.464). This is expected for a het call and carries **no** information about which chromosome an allele sits on. |
| **DP / GQ** | Read depth and genotype quality describe confidence in the *genotype*, not its *phase*. Both are GQ 99 here; that is irrelevant to the question. |
| **Physical proximity** | 10,911 bp is not evidence. Two het variants in one gene are not "probably in *trans*". |
| **Statistical / population phasing** | May be reported as weak, indirect, supporting context **only**, explicitly labelled as such. It must **never** be presented as definitive clinical phase. Both variants are ultra-rare (gnomAD AF 9.98e-5 and 6.195e-7) and absent from reference haplotype panels, so a panel can only place them onto a scaffold, not support them directly. |
| **Short-read physical phasing** | Fragments of ~350–550 bp cannot span 10,911 bp. This is a physical impossibility, not a tooling limitation. |
| **ACMG PM3-style reasoning** | "A rare variant *in trans* with a pathogenic allele" is a *consequence* of knowing phase. It cannot be used to *establish* phase. |
| **Phenotype fit** | That the proband's phenotype matches *BUB1B* disease says nothing about which chromosome carries which allele. |

**Missing phase fields stay missing.** The current VCF declares `PGT`/`PID` but
both are `.` at both variants, and `PS` is not declared at all. These empty
fields are **not** to be imputed, defaulted, or interpreted. `UNPHASED` is the
audited classification and it stands until new data replace it.

---

## Criterion for **A — IN TRANS**

Any **one** of the following, in full:

**A1 — Long-read physical phasing**
- Both positions fall inside a **single phase block**.
- At least **5 independent reads span both positions** (pre-registered minimum; duplicates and supplementary alignments excluded).
- **≥90%** of informative spanning reads assign the two alternate alleles to **opposite** haplotypes.
- Mapping quality at both positions is adequate and neither sits in a region flagged as unreliable by the aligner.

**A2 — Trio genotyping**
- One parent is heterozygous for `c.2210T>G` and homozygous reference at `c.3006T>G`.
- The other parent is heterozygous for `c.3006T>G` and homozygous reference at `c.2210T>G`.
- The proband is heterozygous at both.
- **Parentage is confirmed** by an independent SNP identity panel.
- No evidence of parental germline mosaicism at either site.

**A3 — Allele-specific long-range PCR**
- Allele-specific amplification anchored on one variant, sequenced at the other, showing consistently the **reference** base.
- **Reciprocal** experiment (anchor swapped) gives the concordant result.
- Controls demonstrate allele-specific priming worked and **no allele dropout** occurred.
- Equivalent: single-molecule sequencing of a bulk ~10.9 kb amplicon showing a clean haplotype split.

---

## Criterion for **B — IN CIS**

The mirror of the above:

**B1 — Long-read:** same phase-block and ≥5-spanning-read requirement; **≥90%** of informative spanning reads assign both alternate alleles to the **same** haplotype.

**B2 — Trio:** one parent heterozygous for **both** variants; the other parent homozygous reference at **both**; proband heterozygous at both; parentage confirmed.

**B3 — Long-range PCR:** allele-specific amplification anchored on one variant shows consistently the **alternate** base at the other, reciprocally confirmed, with dropout controls clean.

---

## Everything else is **C — UNRESOLVED**

Explicitly including:

- Fewer than 5 spanning reads, or the two positions falling in different phase blocks.
- Informative reads split between 10% and 90% — an ambiguous ratio is **not** rounded to the nearer call. (A genuinely mixed ratio should also prompt review for mosaicism or mismapping rather than being forced into A or B.)
- Trio data where one parent carries both variants **and** the other carries one — uninformative.
- Trio data where neither parent carries a variant the proband has (***de novo***) — phase still requires A1 or A3.
- Parentage unconfirmed or discordant.
- Long-range PCR that amplifies but without reciprocal confirmation, or with failed/absent dropout controls.
- Any result resting on excluded evidence from the table above.

---

## Reporting rules

1. State the assigned outcome (**A**, **B** or **C**) and the criterion met, by its identifier (A1/A2/A3/B1/B2/B3).
2. Report the underlying counts — spanning reads, informative reads, haplotype split — not just the conclusion.
3. While the outcome is **C**, the approved wording remains: *"two heterozygous *BUB1B* variants of interest; phase undetermined."* The terms **compound heterozygous**, **biallelic**, **in trans** and **in cis** are not to be used.
4. **A does not make `p.Asn1002Lys` pathogenic.** *Trans* configuration with a known null allele is ACMG **supporting** evidence (PM3); it is not proof of a functional effect. The variant remains a **prioritised VUS** until functional data exist.
5. **No phase result opens the therapeutic gate.** The gate is conditioned on mechanism, which remains **C — UNKNOWN**.
