# BUB1B allele-architecture decision tree

**Updated 2026-09-24**, after the phase audit (`phase/PHASE_REPORT.md`), the
CNV/SV audit (`cnv_sv/CNV_SV_REPORT.md`) and the splice screen
(`splicing/README.md`). Supersedes the case list in `DECISION_MATRIX.md`.

This is a **decision tree, not a scoring exercise.** The cases are not ranked
best-to-worst; each is a distinct state of the world with distinct consequences.

---

## Current position

| Item | Status | Source |
|---|---|---|
| `p.Leu737*` (c.2210T>G) | **Strong pathogenic evidence** — ClinVar VCV000533901, Pathogenic/Likely pathogenic, 2-star, multiple submitters, no conflicts, MVA syndrome 1 | ClinVar, 2026-09-15 |
| `p.Asn1002Lys` (c.3006T>G) | **Prioritised VUS.** No functional evidence of any kind exists | Rounds 1–5 |
| Phase | **UNPHASED** — GT `0/1` both; PGT/PID both `.`; no `PS` field in this VCF; 10,911 bp apart | `step13_phase_audit.py` |
| CNV/SV | **Unresolved from available data** — no evidence of any type exists to assess it | `step14_cnv_sv_audit.py` |
| Cryptic splice | **Screened, no candidate** — 14/14 NO SIGNAL, max ΔS 0.03, two concordant tools. *Not* proof that no noncoding mechanism exists | `step12*` |
| Causality | **NOT established** | — |

**We are currently in CASE B.**

---

## CASE A — `p.Leu737*` and `p.Asn1002Lys` confirmed IN TRANS

**What it would support.** A biallelic *BUB1B* genotype: one definite null allele
plus one ultra-rare missense on the other chromosome, in a proband whose
phenotype includes rhabdomyosarcoma (HP:0002859), for which *BUB1B* is a
PanelApp GREEN, BIALLELIC gene. This is the configuration required by the
recessive MVA model, and it would satisfy ACMG PM3 for N1002K.

**What it would NOT prove.**
- It would **not** make N1002K pathogenic. *trans* configuration with a known null is supporting evidence (PM3), not proof of function. A rare benign missense can sit in *trans* with a pathogenic null by chance.
- It would **not** establish that *BUB1B* causes this patient's phenotype — MVA itself is asserted in our records, not evidenced (no karyotype, no PCS data).
- It would **not** exclude a second, unrelated genetic contributor.

**Does N1002K functional testing become higher priority?** **Yes — decisively.**
Under CASE A, N1002K is the only thing standing between "candidate" and "solved",
and its functional status becomes the rate-limiting question.

**Does BUB1B remain genetically unresolved?** Partially. The *architecture* would
be resolved; the *pathogenicity of the second allele* would not.

**Therapeutic/drug analysis gated?** **YES, still gated.** Mechanism remains
C — UNKNOWN. Phase is a genetic result, not a mechanistic one.

---

## CASE B — Phase remains unresolved *(current state)*

**What it would support.** Nothing beyond what is already established: two rare
heterozygous variants in a phenotype-matched recessive gene. A *candidate*
genotype.

**What it would NOT prove.** Everything. Without phase, the genotype is
compatible with (i) true compound heterozygosity, (ii) both variants in *cis* on
one chromosome with a wild-type second allele, or (iii) N1002K being an
incidental rare variant. **These cannot be distinguished.**

**Does N1002K functional testing become higher priority?** **No.** Functional
work on N1002K under unresolved phase risks characterising a variant that may not
be on the relevant allele at all. This is the concrete reason to resolve phase
before investing in functional assays.

**Does BUB1B remain genetically unresolved?** **Yes — fully.**

**Therapeutic/drug analysis gated?** **YES.**

---

## CASE C — `p.Leu737*` and `p.Asn1002Lys` confirmed IN CIS

**What it would support.** Both variants on one parental chromosome, leaving the
other *BUB1B* allele wild-type at these two positions. Under a recessive model,
**N1002K would not be the second pathogenic allele**, and the biallelic
hypothesis as currently framed would be falsified.

**What it would NOT prove.**
- It would **not** exclude *BUB1B*. A second hit could still exist as a CNV/SV, a deep-intronic or regulatory variant, or a variant outside the ±50 kb screening window.
- It would **not** make `p.Leu737*` benign — it remains a pathogenic null allele, just an apparently monoallelic one.
- It would **not** rule out a non-*BUB1B* explanation.

**Does N1002K functional testing become higher priority?** **No — it drops sharply.**
N1002K would become an incidental *cis* variant. Functional work would be hard to
justify.

**Does BUB1B remain genetically unresolved?** **Yes**, and the search reopens:
CNV/SV dosage testing becomes the priority, followed by a wider noncoding search
and reconsideration of alternative genes.

**Therapeutic/drug analysis gated?** **YES.**

---

## CASE D — A pathogenic/likely pathogenic *BUB1B* CNV/SV is found on the other allele

**What it would support.** A biallelic *BUB1B* genotype with two independently
credible loss-of-function alleles: `p.Leu737*` plus a structural null. This
would be the **strongest genetic evidence obtainable** for *BUB1B* causality —
stronger than CASE A, because both alleles would be LoF rather than one being a VUS.

**What it would NOT prove.**
- Phase would still need demonstrating — a CNV must be shown to be on the *other* chromosome, not the same one as `p.Leu737*`.
- It would **not** resolve N1002K, which would become a third, likely incidental, allele.
- It would **not** by itself establish the mechanism; it would establish the genetics.

**Does N1002K functional testing become higher priority?** **No — it becomes largely moot**
as a disease allele, though it would remain a curiosity.

**Does BUB1B remain genetically unresolved?** **No** — this is the case that would
resolve it, provided phase of the CNV is also established.

**Therapeutic/drug analysis gated?** **YES.** Even here, mechanism is
C — UNKNOWN and no E3 ligase for misfolded BUBR1 is known. Genetic resolution is
not mechanistic resolution.

---

## CASE E — No second *BUB1B* allele found after phase + CNV/SV assessment

**What it would support.** A single heterozygous pathogenic *BUB1B* null allele
with no demonstrable second hit. Under a strict recessive model this does **not**
explain the phenotype.

**What it would NOT prove.**
- It would **not** exclude *BUB1B*. Negative results from targeted assays are bounded by what those assays interrogate: dosage methods miss balanced inversions and translocations; the ±50 kb window misses distal regulatory elements; short reads miss repeat-mediated events. **"Not found" is not "not there."**
- It would **not** establish an alternative gene — the Round 4 genome-wide screen already found no competitor surviving frequency filtering.

**Does N1002K functional testing become higher priority?** **Situational.** If
phase showed *trans* but N1002K still looked benign, functional testing could
become the tie-breaker. If phase showed *cis*, no.

**Does BUB1B remain genetically unresolved?** **Yes**, and the honest report is
an **unresolved molecular diagnosis** — not a forced *BUB1B* attribution.

**Therapeutic/drug analysis gated?** **YES — absolutely.**

---

## Invariant across all five cases

**The therapeutic gate stays CLOSED in every case.** No genetic result — not even
CASE D — opens it. The gate is conditioned on *mechanism*, which remains
**C — UNKNOWN**: the destabilisation hypothesis is falsified, direct PP2A-B56
disruption is unsupported, the helix-cap model is computational only (and was
weakened by the φ/ψ result), and no E3 ligase for misfolded BUBR1 has ever been
identified.

Genetics constrains **which allele matters**. It does not tell us **what the
protein does**.
