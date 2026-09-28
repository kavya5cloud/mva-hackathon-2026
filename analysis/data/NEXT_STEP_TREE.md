# Follow-up branch tree — after the phase result

**Written 2026-09-24.** Entry state: phase **UNPHASED**, CNV/SV **unresolved from
available data**, splice screen **negative**, *BUB1B* **not confirmed**,
mechanism **C — UNKNOWN**, therapeutic gate **CLOSED**.

Outcome definitions and acceptance criteria: `phase/MINIMUM_DECISIVE_TEST.md`.
Route comparison: `phase/PHASE_EXPERIMENT_SPEC.md`.

```
PHASE RESULT
|
+-- IN TRANS
|   +-- evaluate whether N1002K has functional effect
|   +-- retain BUB1B genetic hypothesis
|   +-- therapeutic gate remains closed until mechanism established
|
+-- IN CIS
|   +-- N1002K functional work is deprioritised/stopped
|   +-- search for second BUB1B allele via CNV/SV/noncoding evidence
|   +-- do not conclude BUB1B is excluded
|
+-- UNRESOLVED
    +-- BUB1B remains unresolved
    +-- pursue exon-dosage/CNV testing if feasible
    +-- do not interpret N1002K mechanistically as a causal allele
```

---

## Branch 1 — IN TRANS

**What is established.** The allele architecture: `p.Leu737*` and `p.Asn1002Lys`
sit on opposite parental chromosomes. `p.Leu737*` retains its strong pathogenic
evidence (ClinVar 2-star Pathogenic/Likely pathogenic). ACMG **PM3 supporting**
evidence is now available for `p.Asn1002Lys`.

**What remains unknown.**
- Whether `p.Asn1002Lys` has **any** functional effect. It remains a **prioritised VUS**; *trans* configuration is supporting evidence, not proof.
- Whether *BUB1B* causes this proband's phenotype. MVA itself is asserted in our records rather than evidenced — no karyotype or PCS data exists (`phenotype/PHENOTYPE.md`).
- The mechanism, which remains **C — UNKNOWN**: destabilisation is falsified, direct PP2A-B56 disruption is unsupported, and the helix-cap model is computational only and was weakened by the φ/ψ result.
- Whether an additional, unrelated genetic contributor exists.

**Next experiment.** Functional assessment of `p.Asn1002Lys`, in this order, with
`L1012P` as destabilised positive control and `Q921H` as stable/WT-like negative
control, all at **WT-matched expression** (otherwise abundance and function are
confounded):
1. Steady-state abundance — quantitative immunoblot vs WT.
2. Protein half-life — cycloheximide chase.
3. If abundance and half-life are WT-like: SAC/alignment function, then KARD pS670/pS676 and kinetochore PP2A-B56 recruitment.

**What would close the therapeutic gate further.** Functional results showing
`p.Asn1002Lys` is **WT-like on every axis** — normal abundance, normal half-life,
normal checkpoint function. That would indicate it is not the disease allele even
in *trans*, returning the project to an unresolved molecular diagnosis and
removing the remaining rationale for mechanism-directed therapeutic work.

**What would reopen therapeutic analysis.** A **defined, targetable molecular
defect** — not merely "abnormal". Concretely: reduced abundance **and** shortened
half-life **and** demonstrated proteasome dependence **and** restoration of
function when abundance is restored. That combination would revive the
destabilisation mechanism and justify re-running the proteostasis drug search.
A specific, druggable interaction defect identified by IP-MS would be an
alternative route. **Generic checkpoint dysfunction would not qualify.**

---

## Branch 2 — IN CIS

**What is established.** Both variants lie on one parental chromosome. Under the
recessive model, **`p.Asn1002Lys` is not the second pathogenic allele**, and the
biallelic hypothesis as currently framed is **falsified**. `p.Leu737*` remains a
pathogenic null allele — now apparently monoallelic.

**What remains unknown.**
- Whether a second *BUB1B* allele exists at all, as a CNV/SV, a deep-intronic or regulatory variant, or a variant outside the ±50 kb screening window.
- Whether *BUB1B* is the right gene. **A *cis* result does not exclude *BUB1B*** — it excludes this particular pair as the biallelic explanation.
- Whether the phenotype has a non-*BUB1B* cause.

**Next experiment.** ***BUB1B* exon-dosage testing** — MLPA first-line across all
23 exons, or qPCR/ddPCR for targeted exons. This is the one hidden-variant class
the current VCF cannot see at all. If negative, widen the noncoding search beyond
the ±50 kb window (distal regulatory elements, which the screen did not cover)
and revisit alternative genes — noting that the Round 4 genome-wide screen already
found no competitor surviving frequency filtering.

**What would close the therapeutic gate further.** A dosage assay that is negative
**and** a broadened noncoding search that finds nothing. The correct output is
then an **unresolved molecular diagnosis**, not a forced *BUB1B* attribution — and
with no established causal gene, there is no mechanism to target.

**What would reopen therapeutic analysis.** Identification of a genuine second
pathogenic *BUB1B* allele (CNV/SV or noncoding) **plus** subsequent mechanistic
characterisation. Genetics alone would not suffice: the gate is conditioned on
mechanism.

**Explicitly stopped in this branch.** `p.Asn1002Lys` functional work, and any
further structural modelling of N1002. Characterising a variant on the wrong
allele would not inform the diagnosis.

---

## Branch 3 — UNRESOLVED

**What is established.** Nothing new. The entry state stands: two rare
heterozygous variants in a phenotype-matched recessive gene, phase undetermined.
`p.Leu737*` = strong pathogenic evidence; `p.Asn1002Lys` = **prioritised VUS**.
This is **CASE B** in `DECISION_MATRIX_UPDATED.md`.

**What remains unknown.** Everything the other branches would have settled. The
genotype remains compatible with (i) true compound heterozygosity, (ii) both
variants in *cis* with a wild-type second allele, or (iii) `p.Asn1002Lys` being
incidental. **These cannot be distinguished**, and the project must not pick one.

**Next experiment.** ***BUB1B* exon-dosage testing** — it needs only proband DNA,
does not depend on parental availability, and addresses the CNV/SV gap
independently of phase. In parallel, re-examine whether long-read sequencing can
be obtained, since it would resolve phase **and** CNV/SV together
(`phase/PHASE_EXPERIMENT_SPEC.md`, recommended route).

**What would close the therapeutic gate further.** Exhausting the accessible
genetic evidence — phase unobtainable, dosage negative, noncoding search negative
— which would make an **unresolved molecular diagnosis** the honest reported
outcome.

**What would reopen therapeutic analysis.** Nothing available in this branch.
Therapeutic work requires a mechanism, a mechanism requires a causal allele, and
a causal allele requires the genetic architecture to be constrained first.

**Explicitly prohibited in this branch.** Interpreting `p.Asn1002Lys`
mechanistically **as a causal allele**. Structural or functional work may be
described as *conditional* on a future *trans* result, but no output may treat
N1002K as established to be on the relevant allele, and none may describe it as
pathogenic or likely pathogenic.

---

## Invariant across all three branches

**The therapeutic gate stays CLOSED.** No phase result opens it. The gate is
conditioned on **mechanism** — currently **C — UNKNOWN** — and phase is a genetic
result, not a mechanistic one. Additionally, no E3 ligase for misfolded BUBR1 has
ever been identified, so even the destabilisation route would lack a defined
molecular target.

**`p.Asn1002Lys` is not to be called pathogenic or likely pathogenic in any
branch**, and the terms **compound heterozygous**, **biallelic**, **in trans** and
**in cis** are not to be used to describe the proband's genotype until the
corresponding criterion in `phase/MINIMUM_DECISIVE_TEST.md` is met.
