# MVA Hackathon 2026 — Track 2 Final Report

**Team:** kavya5cloud 
**Subject:** Mechanistic and therapeutic assessment of *BUB1B* variants in a proband with Mosaic Variegated Aneuploidy 
**Report first issued:** 2026-09-16 · **Evidence frozen and audited:** 2026-09-26 
**Full evidence record:** `analysis/round2_variant_characterisation.md` · **Final audit:** `analysis/FINAL_AUDIT.md`

*Dates given inline against individual queries and results are the dates those
queries were run (2026-09-15 → 2026-09-24) and are historical; they are not
updated.*

**Evidence labels used throughout:** 
**ESTABLISHED** — directly observed here or in primary literature · **SUPPORTED** — strong converging evidence, not directly demonstrated · **HYPOTHESIZED** — coherent model, computational only · **UNKNOWN** — not determined · **FALSIFIED** — tested and rejected

---

> ## PROVENANCE STATUS — verified 2026-09-16
>
> Both variants were confirmed **directly in the gated proband VCF**
> (`WGS_EX2312012_HGWCNDSX7.vcf.gz`, md5 `a04ea354141cfb032872d67a11c8d2d8`,
> sample `WGS_EX2312012`, **GRCh38**) using `analysis/scripts/step0_verify_provenance.py`:
>
> | Variant | GRCh38 | REF>ALT | FILTER | GT | DP | GQ | AD | VAF |
> |---|---|---|---|---|---|---|---|---|
> | c.2210T>G p.Leu737\* | 15:40,209,701 | T>G ✓ | PASS | 0/1 | 46 | 99 | 21,25 | 0.543 |
> | c.3006T>G p.Asn1002Lys | 15:40,220,612 | T>G ✓ | PASS | 0/1 | 28 | 99 | 15,13 | 0.464 |
>
> **Patient attribution: ESTABLISHED.** Both variants are legitimately the proband's.
>
> **Phase: UNPHASED** (formal classification, `step13_phase_audit.py`). Both
> genotypes use the unphased `/` separator; GATK `PGT`/`PID` are declared but empty
> at both variants; no `PS` field exists; no shared phase set. The sites are
> 10,911 bp apart, beyond short-read reach. **Not compound heterozygous.**
>
> A **genome-build error** in the original Track 1 extraction is confirmed and
> corrected — see `analysis/TRACK1_SUBMISSION_ERRATUM.md`. It does **not** affect
> the two variants above.

---

## 1. Executive Summary

A child with Mosaic Variegated Aneuploidy features carries **two heterozygous
*BUB1B* variants**, both verified present in the proband's own WGS:
**NM_001211.6:c.2210T>G (p.Leu737\*)** and **NM_001211.6:c.3006T>G
(p.Asn1002Lys)**.

**`p.Leu737*` has strong pathogenic evidence** — ClinVar Pathogenic/Likely
pathogenic at two-star review (multiple submitters, no conflicts) for MVA
syndrome 1, a nonsense variant 746 nt upstream of the final exon–exon junction
and therefore predicted (not measured) to trigger nonsense-mediated decay.

**`p.Asn1002Lys` remains a prioritised VUS.** It is ultra-rare (gnomAD AF
6.195e-7), invariant from human to *Xenopus*, and scores highly on
AlphaMissense — but these are **supporting observations, not evidence of
pathogenicity**, and no functional data of any kind exist for it. Our own
mechanistic work argues against the obvious hypothesis: a ΔΔG predictor
calibrated against four *BUB1B* variants with published abundance phenotypes —
and correct on all four — scores N1002K as **neutral**, clustering it with the
known stable, WT-like Q921H rather than the destabilised group. A structural
helix-cap model was proposed as an alternative, but a subsequent backbone φ/ψ
check removed one of its supports. **The mechanism is UNRESOLVED.**

**Within the analyzed phenotype-driven panel and genome-wide autosomal-recessive
screen, independent genomic screening did not identify a better-supported
alternative explanation.** After discovering a genome-build error in our
own Track 1 pipeline, we re-derived the candidate gene from scratch: a
phenotype-driven PanelApp panel (selected from the proband's rhabdomyosarcoma HPO
term) plus an unbiased genome-wide autosomal-recessive screen over 5.02 M
variants. After population-frequency filtering, *BUB1B* was the only surviving
candidate, and no other MVA or mitotic-checkpoint gene carried a qualifying
genotype.

**Splice analysis found no computationally supported hidden *BUB1B* splice hit.**
SpliceAI and Pangolin, run independently over the locus ±50 kb, scored all 14
*BUB1B* records NO SIGNAL (maximum ΔS 0.03, complete concordance). The *BUB1B* set
is **12 deep-intronic variants + 2 coding controls = 14 records**; a further 56
variants in the same window are annotated to the adjacent gene **PAK6** and are
**not** counted as *BUB1B*. Both tools are **computational predictors (Tier 3)**;
this does **not** exclude branchpoint, pseudoexon, or structural mechanisms.

**Phase remains unresolved (UNPHASED).** Both variants are heterozygous with
unphased genotypes, no shared phase set exists, and the 10,911 bp separation
cannot be spanned by short reads. **CNV/SV status remains unresolved from
available data** — an audit across ten evidence classes found no dosage or
structural-variant information of any kind.

**Consequently, *BUB1B* remains a leading genetic hypothesis rather than a
confirmed molecular diagnosis.** No second pathogenic *BUB1B* allele has been
established. The genotype is best described as **two heterozygous variants of
interest in a recessive-model candidate gene**.

**No therapeutic candidate is proposed, and the therapeutic gate remains CLOSED.**
This is a deliberate scientific conclusion, not an omitted section: the gate is
conditioned on a defined, experimentally supported targetable mechanism, and no
such mechanism exists. No drug search was performed.

**The highest-value next experiment is genetic, not mechanistic**: resolution of
phase (proband long-read sequencing preferred, or trio genotyping where parents
are available) and/or *BUB1B* exon-dosage/SV testing. Functional work on
`p.Asn1002Lys` should follow only once the allele architecture is constrained —
a *cis* result would make that work unjustifiable.

---

## 2. Patient Variant Context

| | Variant 1 | Variant 2 |
|---|---|---|
| HGVS | NM_001211.6:c.2210T>G | NM_001211.6:c.3006T>G |
| Protein | p.Leu737* | p.Asn1002Lys |
| GRCh38 | chr15:40,209,701 T>G | chr15:40,220,612 T>G |
| GRCh37 | chr15:40,501,902 T>G | chr15:40,512,813 T>G |
| dbSNP | rs759242053 | **rs2542593804** |
| ClinVar (exact allele) | VCV000533901 — **Pathogenic/Likely pathogenic, 2-star** | **no record** |
| gnomAD | exomes 7.87e-5 / genomes 3.29e-5 | combined **6.195e-7**, 0 hom, SAS AC=0 |
| **Current status** | **strong pathogenic evidence** | **prioritised VUS** |

Gene *BUB1B* (BUBR1), the spindle assembly checkpoint component whose biallelic
loss causes **Mosaic Variegated Aneuploidy syndrome 1** (MIM 257300).

**Critical distinction, maintained throughout:** a *different* nucleotide allele,
**c.3006T>A**, also produces p.Asn1002Lys and carries a 1-star VUS ClinVar record
(VCV004600147). **It is not the patient allele and no evidence is transferred
from it.**

**Numbering collision, resolved:** human **L1012** ≡ mouse **L1002**. The patient
variant is **human N1002K**, a different residue from the mouse L1002P / human
L1012P literature allele. No mouse evidence is transferred.

---

## 3. Variant Verification — **ESTABLISHED**

Independently verified against dbSNP, ClinVar, Ensembl VEP, gnomAD and UCSC
(all 2026-09-15).

- **N1002K is not novel.** It carries dbSNP **rs2542593804**, with no clinical significance assigned. ClinVar exact-allele search returns **0 records**; BUB1B has 2,093 ClinVar records overall. *(Absence from ClinVar is **UNKNOWN**, not benign.)*
- VEP confirms `missense_variant`, exon **23/23**, MANE/canonical transcript ENST00000287598.11.
- Verified directly from the Ensembl CDS: codon 1002 = **AAT**, c.3006 is base **3**, `AAT`(Asn) → **`AAG`**(Lys).
- **LOVD remains inaccessible** (IP/network block). Status **UNKNOWN**; no bypass attempted.

---

## 4. Leu737* Mechanism — **ESTABLISHED** (with one predicted step)

- Verified from CDS: codon 737 = **TTA**, c.2210 is base **2**, `TTA`(Leu) → **`TGA`**(opal stop).
- Located in **exon 17 of 23**.
- The final exon–exon junction is at **c.2957**; the PTC therefore lies **746 nt upstream** of it — far beyond the ~50–55 nt boundary.
- **NMD competence is PREDICTED, not demonstrated.** Patient RNA would be required to show transcript loss.
- If the transcript escapes NMD, the product would lack the entire pseudokinase domain (766–1050), resembling the **BUBR1-731X** truncation shown to lose KARD phosphorylation (PMID 33207204).

This allele is independently classified **Pathogenic/Likely pathogenic** at 2-star,
multi-submitter, no conflicts, for MVA syndrome 1. **It is the secure half of the
genotype.**

---

## 5. N1002K Structural Characterisation — **HYPOTHESIS-GENERATING** (computational)

*`p.Asn1002Lys` is a **prioritised VUS** throughout. Everything in this section is
computational, derived from a **predicted** structure, and is hypothesis-generating
only — none of it is functional or experimental evidence.*

Model: AlphaFold DB **AF-O60566-F1-model_v6** (v4 is retired — HTTP 404). Tier 3.

- **Numbering gate passed:** residue 1002 in the model is ASN; positions 737, 844, 909, 921, 1012 all match expectation.
- **pLDDT = 91.06** — high local confidence.
- **Residue RSA = 0.162** → buried by our pre-registered threshold (<0.20).
- **Per-atom analysis is more informative:** the residue-level RSA is driven by CB (10.87 Å²) and the *backbone* carbonyl (11.79 Å²). The functional amide is **fully buried — ND2 SASA = 0.00 Å²**, CG = 0.00 Å².
- **Three hydrogen bonds, all to main chain:** OD1 ← W978 N (2.83 Å); ND2 → V998 O (2.83 Å); ND2 → W978 O (2.95 Å). Packed against W973, F977, W978.

### The helix C-cap finding

Secondary structure: β-strand **978–980**, α-helix **990–1001**, loop **1002–1007**,
α-helix **1008–1015**. **N1002 is the first residue of the loop — the C′ position
of a helix C-cap.** ND2→V998 O is the canonical Asn capping bond (V998 is *i*−4,
its carbonyl otherwise unsatisfied at the helix terminus); the reciprocal W978 pair
staples the helix end to the β-strand.

**Caveat added after a subsequent backbone check (Round 4).** A φ/ψ measurement at
N1002 returned **φ = −126.6°, ψ = +37.3°** — a *normal negative* φ in the bridge
region, **not** the positive-φ conformation that only Asn and Gly populate
readily. The argument that the backbone conformation itself excludes Lys
therefore **does not apply**, and the helix-cap model loses one of its supports.
Any steric case against Lys now rests solely on side-chain hydrogen bonding and
packing. (Separately verified: residue 1002 is **not modelled in any experimental
structure** — the two cryo-EM entries mapping *BUB1B* resolve only residues
~19–345 — so AlphaFold remains the sole structural source.)

Asn is the most favoured residue at helix C-caps because its short amide can
substitute for backbone hydrogen bonding. **Lysine cannot do this:** NZ is a donor
only and cannot accept from W978 N; it is longer and flexible; and it buries a
formal positive charge at a position with zero solvent exposure.

### N1002 is NOT a nucleotide-pocket residue — **ESTABLISHED (from the model)**

N1002 is **28.6 Å from K795** (UniProt ATP site) and **18.4 Å from D882** — the
**furthest of all seven MVA positions** from the degenerate pocket (I909T, by
contrast, is 4.1 Å from D911). Human BUBR1 is a **pseudokinase** with no
phosphotransfer activity; UniProt's "Active site 882" is annotated *by similarity*
only. **N1002 is not positioned within the annotated pseudo-catalytic/nucleotide-associated region in the AlphaFold model.**

### The MVA missense positions do not form one cluster

Only R727–Q921 (4.8 Å) and R814–Q921 (7.9 Å) are within contact range. **N1002 is
≥19.7 Å from every MVA position except L1012 (10.3 Å, still not a contact).**
There is no single MVA hotspot onto which N1002K can be mapped.

---

## 6. Stability Calibration — **hypothesis A DISFAVOURED as primary mechanism**

DynaMut2 — a **computational ΔΔG predictor (Tier 3, not experimental evidence)** —
on the excised pseudokinase domain (766–1050), calibrated **before** interpreting
the variant of interest:

| variant | ΔΔG (kcal/mol) | published experimental phenotype | predictor correct? |
|---|---|---|---|
| I909T | **−3.48** | reduced abundance, ↑turnover, rescued by re-expression | ✅ |
| L1012P | **−1.80** | reduced abundance, ↑degradation, rescued by re-expression | ✅ |
| L844F | **−1.70** | reduced abundance (+ residual defect) | ✅ |
| Q921H | **−0.15** | **stable, indistinguishable from WT** | ✅ |
| **N1002K** | **−0.01** | **no data exists** | — |

The predictor separates the destabilised group from the stable control by 1.6–3.3
kcal/mol on this exact structure — it is demonstrably sensitive here. **N1002K
clusters with Q921H.** This cannot be dismissed as predictor insensitivity.

**Attempted replication FAILED:** DDMut accepted all five jobs but its results
endpoint returned `Internal Server Error` on every poll. **No DDMut values were
obtained and none are reported.** FoldX is not licensed in our environment.
Per protocol, predictors are reported separately and **never averaged**.

**Orthogonal metric, also calibrated:** AlphaMissense scores N1002K **0.9229
(likely_pathogenic)** — highest in the panel. But AlphaMissense **fails the
abundance calibration**: it cannot separate stable Q921H (0.49) from destabilised
I909T (0.45), and calls destabilised L844F "likely benign". SIFT and PolyPhen-2
call every panel member damaging, including WT-like Q921H, and are uninformative.

**The two axes give different answers, and both stand:** N1002K is **assigned a
high pathogenicity prior by AlphaMissense but is not predicted to be
thermodynamically destabilising by calibrated DynaMut2; neither constitutes
functional evidence.** The
helix-cap model (§5) offers a way these could be compatible — though that model is computational only, and the φ/ψ result in §5 weakens it.

---

## 7. Conservation — **ESTABLISHED**

- **N1002 is invariant** across all six species with an alignable residue (human, chimpanzee, mouse, rat, dog, chicken, *Xenopus*).
- It is conserved in *Xenopus* **where three benchmark positions have diverged**: L844→I, I909→L, **Q921→Y**. N1002 is therefore **more deeply conserved than Q921**, the residue whose variant is experimentally WT-like.
- **phyloP100way = 4.7967** (track range −20 to 7.532); **phastCons100way = 1.000** (ceiling) at the exact mutated nucleotide. *These are measured comparative-genomics scores — a **supporting observation**, not functional evidence.*
- **A conserved micro-core surrounds it:** W978, I1000, L1001, N1002, A1003 are all **6/6 identical**, embedded in a variable surround (F977 1/6, N1004 1/6). Selection acts sharply on this specific set.

**Limitation:** the zebrafish orthologue is **gapped at every benchmarked
position** — this region is not alignable. Conservation is established **human →
*Xenopus***, not to teleosts. **Conservation is not pathogenicity**; it is
supporting evidence only.

---

## 8. Competing Mechanisms

| Hypothesis | Confidence | Status |
|---|---|---|
| **A** — reduced abundance / destabilisation | **LOW** | **Actively disfavoured.** Calibrated ΔΔG neutral. |
| **G→A** — local helix-cap-loss defect, normal global stability | **MEDIUM** | **Working hypothesis; computational only.** Consistent with the observations; no experimental support. |
| **D** — impaired allosteric KARD S670/S676 phosphorylation → ↓kinetochore PP2A-B56 | **MEDIUM** | **Downstream testable model; untested.** Residue 1002 never tested. |
| **E** — SAC weakness despite normal abundance | MEDIUM-LOW | Untested. |
| **H** — incidental / not the second pathogenic allele | **LOW-MEDIUM** | **Cannot be excluded** while phase and provenance are unresolved. |
| **C** — altered partner interaction | LOW | Contradicted: ND2 SASA = 0.00 Å², not an accessible interface. |
| **F** — altered localization | LOW | Kinetochore targeting maps ~800 residues away. |
| **B** — intramolecular autoregulation | LOW | Speculative; no supporting contact. |
| **G** — altered dynamics only | LOW-MEDIUM | **Untested — no MD was performed.** |

### Direct PP2A-B56 disruption is FALSIFIED

Gama Braga *et al.* (*Cell Reports* 2020, **PMID 33207204**) show **PP2A-B56 binds
the KARD (S670/S676), not the pseudokinase domain**; the domain's contribution is
**allosteric**. N1002 is **51–85 Å** from the KARD, which is disordered in the
model (pLDDT ~30). **"N1002K directly disrupts PP2A-B56 binding" is not supported
and is not claimed.**

Crucially, that same work shows **abundance and allosteric function are
dissociable**: the *hyperstable* 731X and the *unstable* DKD **both** lose KARD
phosphorylation. A normally abundant protein can therefore still be functionally
defective — which is precisely the scenario the helix-cap model predicts.

---

## 9. Provenance (**ESTABLISHED**) and Phase (**UNPHASED**)

**We do not claim compound heterozygosity.**

- **Existing data cannot establish phase.** Single-sample WGS VCF; genotypes recorded as unphased `0/1`; no parental samples described anywhere in the methods record.
- **Read-backed phasing is physically impossible here.** The variants are **10,911 bp apart**. Illumina fragments (~350–550 bp) fall more than an order of magnitude short. This is a hard limit, not a tooling choice.
- **Population/statistical phasing is not acceptable** for two ultra-rare variants (AF 6.2e-7 and 7.9e-5) absent from reference panels.
- **Trio genotyping can establish inheritance-based phase when both parents are available and informative; proband long-read sequencing can directly resolve physical phase and may additionally detect structural variation.** Trio caveats: parentage, parental germline mosaicism, and *de novo* events.
- **Long-read sequencing (PacBio HiFi / ONT) is definitive and needs only the proband** — the preferred route if parents are unavailable.
- **Linked-read (10x Chromium) would work in principle but the platform is discontinued**; Hi-C/Pore-C is the modern equivalent.

**Pre-registered threshold — any one of:** (T1) trio showing each variant from a
different parent with confirmed parentage; (T2) ≥5 long reads spanning both sites
with ≥90% of informative reads assigning the alternates to opposite haplotypes in
one phase block; (T3) allele-specific long-range PCR across 10.9 kb showing the
alternates never co-occur on one molecule.

**Approved wording until then:**

> The proband carries two heterozygous *BUB1B* variants, c.2210T>G (p.Leu737\*)
> and c.3006T>G (p.Asn1002Lys). **Phase has not been determined.** They are
> reported as two heterozygous variants of interest in a recessive-model candidate
> gene, **not** as a confirmed compound-heterozygous genotype.

### Variant provenance — **ESTABLISHED** (resolved 2026-09-16)

Verified directly against the gated proband VCF: both variants are present, with
matching REF/ALT, `PASS` filter, `0/1` genotype, GQ 99, adequate depth and clean
heterozygous allele balance (VAF 0.543 and 0.464). See the Provenance Status block
above and §R3.11 of the evidence record.

Separately, the **Track 1 build error is confirmed**: the documented window is the
GRCh37 *BUB1B* locus applied to a GRCh38 VCF, so the three original Track 1
candidates — though real, PASS-quality proband variants — lie in *IVD*, *BAHD1*
and a lncRNA, **not *BUB1B***. That erratum does not affect the two variants
analysed in this report. Full detail: `analysis/TRACK1_SUBMISSION_ERRATUM.md`.

---

## Genetic Resolution Status

*Synthesis of the genetic evidence as of 2026-09-24, ahead of the mechanism
decision below. Supporting detail: `data/phase/`, `data/cnv_sv/CNV_SV_REPORT.md`,
`data/splicing/README.md`, `data/DECISION_MATRIX_UPDATED.md`.*

**`p.Leu737*` (NM_001211.6:c.2210T>G)** carries strong pathogenic evidence. It is
recorded in ClinVar as **Pathogenic/Likely pathogenic** at two-star review status
(criteria provided, multiple submitters, no conflicts) for Mosaic Variegated
Aneuploidy syndrome 1, and was verified present in the proband (PASS, GT 0/1,
DP 46, GQ 99). The nonsense codon arises in exon 17 of 23, 746 nt upstream of the
final exon–exon junction; nonsense-mediated decay is therefore **predicted**, but
has not been measured in patient material.

**`p.Asn1002Lys` (NM_001211.6:c.3006T>G)** remains a **prioritised VUS**. It is
ultra-rare (gnomAD v4.1.1 AF 6.195e-7, no homozygotes), absent from ClinVar as
this exact allele, and falls at an invariant position (human to *Xenopus*;
phyloP 4.80, phastCons 1.00). No functional evidence of any kind exists for it —
no published assay, and no deep mutational scan of *BUB1B*. Rarity and
conservation are supporting observations; **neither is used here as evidence of
pathogenicity**.

**Computational splice analysis** of the *BUB1B* locus (gene body ±50 kb) did not
identify a plausible hidden intronic splice event. SpliceAI 1.3.1 and Pangolin
were run independently on the same normalised variants: all 14 *BUB1B* records —
**12 deep-intronic variants** plus the two coding variants as controls (the other
**56 variants in the window belong to the adjacent gene *PAK6*** and are not
counted as *BUB1B*) — scored
**NO SIGNAL**, with a maximum ΔS of 0.03 and complete concordance between the two
tools. No canonical `splice_acceptor`, `splice_donor` or `splice_region` variant
exists anywhere in the analysed interval. **This does not establish the absence of
all possible noncoding mechanisms**: these tools have limited sensitivity for
branchpoints and pseudoexon activation, neither detects structural variation, and
distal regulatory elements outside the screening window were not examined.

**Phase is unresolved.** A formal audit classified the two variants **UNPHASED**.
Both are heterozygous with the unphased `/` separator; the VCF declares GATK
`PGT`/`PID` but both are empty at both positions, and no `PS` field exists. No
shared phase set links them. The variants are **10,911 bp apart**, which
short-read fragments cannot span, so physical phasing is unobtainable from these
data. Phase was not inferred from allele balance, genotype quality, read depth, or
physical proximity.

**CNV/SV status remains unresolved** because suitable dosage or structural-variant
data are unavailable. An audit across ten evidence classes returned nothing: no
symbolic ALT alleles, no breakend records, no SV/CNV INFO or FORMAT keys, no gVCF
reference blocks, no usable depth track, no split-read or discordant-pair fields,
no BAM/CRAM or FASTQ, and no pre-computed CNV or SV call sets. `FORMAT/DP` was not
used as a dosage proxy. A structural second hit in *BUB1B* — for example a
single-exon deletion on the allele not carrying `p.Leu737*` — **cannot be
excluded**.

**Current causal interpretation.** *BUB1B* was independently re-established as the
leading candidate by an unbiased, phenotype-driven, frequency-filtered
genome-wide screen, and no competing gene survived that screen. However,
**no second pathogenic *BUB1B* allele has been established.** *BUB1B* therefore
remains a **leading genetic hypothesis rather than a confirmed molecular
diagnosis**. The proband's two variants are reported as **two heterozygous
variants of interest in a recessive-model candidate gene**, and not as a
compound-heterozygous, biallelic, *cis* or *trans* genotype.

**Therapeutic gate.** Analysis remains **gated pending resolution of both genotype
and mechanism**. The gate is conditioned on mechanism, which is classified
**C — UNKNOWN**; no genetic result alone would open it. No drug search has been
performed and no candidate is proposed.

---

## 10. Mechanism Decision: **C — UNKNOWN / UNRESOLVED**

- **Not A:** the calibrated stability prediction is neutral, and burial is shallower than in the destabilised alleles.
- **Not B-as-stated:** N1002 is buried and 51–85 Å from the KARD; PP2A-B56 does not bind this domain.
- **Not D (incidental) — but not excluded:** conservation and rarity are too strong to dismiss; phase and provenance are unresolved.
- **Working model (HYPOTHESIZED; computational only):** loss of a buried helix C-cap perturbs the 1002–1007 loop and the register of helix 1008–1015, degrading the pseudokinase domain's allosteric support for KARD phosphorylation — **without** reducing abundance. This is the pre-registered "WT-like abundance, impaired function" scenario, and it must be tested before being believed.

---

## 11. Experimental Falsification Plan

Priority-ordered. Full table with expected results per hypothesis in
`analysis/round2_variant_characterisation.md` §R3.7.

| Pri | Experiment | Decisive because |
|---|---|---|
| ~~0~~ | ~~Variant provenance~~ — **DONE 2026-09-16** | ✅ Both variants confirmed present in the proband (PASS, 0/1, GQ 99) |
| **1** | **Phase** — trio Sanger or proband long-read | ***cis* → N1002K is not the second allele** |
| **2** | **Abundance** (immunoblot) + **half-life** (CHX chase) vs WT, with L1012P and Q921H controls | **Normal → hypothesis A falsified; abundance rescue is not a therapeutic route** |
| **3** | **SAC/alignment function at WT-matched expression** | Impaired with normal abundance → local-defect model; WT-like → possibly incidental |
| **3** | **KARD pS670/pS676 + kinetochore PP2A-B56** at WT-matched abundance | **The direct test of the allosteric model** |
| **4** | **Purified 766–1050 biophysics**: nanoDSF Tm + limited proteolysis / HDX-MS | **ΔTm ≈ 0 with altered local proteolysis/HDX in 998–1015 → confirms helix-cap model.** ΔTm ≪ 0 → revives A |

All functional readouts require expression titrated to WT-matched levels, or
abundance and function are confounded.

---

## 12. Therapeutic Decision Gate: **CLOSED**

| Gate condition | Observed |
|---|---|
| Reduced abundance | **no data — never measured** |
| Shortened half-life | **no data** |
| Proteasome-dependent loss | **no data** |
| Rescue by stabilisation demonstrated | **no data** |
| *or* a precise defective signalling node identified | **no data** — residue 1002 was never tested |

Independently sufficient additional reasons the gate stays closed:

- Mechanism is **UNRESOLVED**; the working model is entirely computational.
- **No E3 ligase for misfolded BUBR1 has ever been identified** — even under hypothesis A there would be no defined target.
- **Phase is undetermined** — N1002K is not established as a pathogenic allele in this patient (provenance is now established; phase is not).
- The one plausible node (PLK1/CDK1 → KARD) is **not safely druggable in the required direction**: inhibitors would *reduce* KARD phosphorylation and worsen the predicted defect.

---

## 13. Drug Repurposing Result: **NOT PERFORMED**

**No drug search was conducted. No candidate is named, ranked or scored.**

Proposing a compound here would mean retrofitting a therapy to an unsupported
mechanism. The following remain excluded, and nothing found in this work overturns
that: **HSP90 inhibitors** (would *reduce* BUBR1), **broad proteasome inhibitors**,
**MPS1/TTK inhibitors**, **Aurora inhibitors**, **KIF11/Eg5 inhibitors**,
**classical antimitotics**, **APC/C activators** — all would be expected to
**worsen** missegregation in a patient who already has MVA.

**Condition to reopen:** Experiments 2 + 3 + 4 showing reduced abundance,
shortened half-life and proteasome-dependent loss, **plus** Experiment 1 showing
*trans*. (Experiment 0, provenance, is complete.)

---

## 14. Limitations

1. **Phase undetermined**, and unresolvable with the existing short-read data (the two sites are 10,911 bp apart). *(Provenance was a limitation in earlier drafts; it is now ESTABLISHED — see the Provenance Status block.)*
2. **CNV/SV status is unresolved from the available data** — no structural-variant caller
   output, read-depth/coverage track, array or MLPA result was available. This is an
   **absence of evidence, not evidence of absence**: a second hit of this class is neither
   demonstrated nor excluded.
3. **No experimental functional assays were performed in this work.** Every mechanistic
   statement about N1002K is computational (Tier 3). No abundance, half-life, degradation,
   kinetochore-localisation, PP2A-B56-binding or SAC-function assay was carried out.
4. **No cryptic-splice second hit was detected**, but prediction is not exclusion — 14/14
   *BUB1B* intronic records returned NO SIGNAL from two concordant computational predictors.
5. **No functional evidence for N1002K exists anywhere** — no publication, no assay, and **no deep mutational scan** (MaveDB returns no BUB1B score-set).
6. **All structural conclusions rest on a *predicted* model** (AlphaFold), not an experimental structure. No experimental structure of the human BUBR1 pseudokinase domain was used.
7. **Only one ΔΔG predictor returned values.** DDMut's API failed; FoldX is unlicensed. A single-predictor result, however well calibrated, is weaker than a consensus.
8. **NMD for Leu737\* is predicted, not measured.**
9. **No molecular dynamics was performed** — the protein-dynamics hypothesis is untested.
10. **DSSP was unavailable**; SASA came from Shrake–Rupley with Tien 2013 max-ASA. Values are not identical to DSSP output.
11. **Conservation established only to *Xenopus*** — zebrafish is gapped.
12. **LOVD is inaccessible** — status UNKNOWN, not negative.
13. **The AlphaFold KARD coordinates are unreliable** (pLDDT ~30); the 51–85 Å distances are qualitative. The conclusion does not depend on them.

---

## 15. Reproducibility

Repository: <https://github.com/kavya5cloud/mva-hackathon-2026> — this report is
`analysis/kavya5cloud_track2_report.md`; the full evidence record is
`analysis/round2_variant_characterisation.md`; `analysis/README.md` gives the reading
order and the reproduction commands.

Scripts (`analysis/scripts/`, 21 files — 19 Python, 2 shell, all syntax-validated):
`step0_verify_provenance.py`, `step1_database_queries.sh`, `step4_structure_gate.py`,
`step5_contacts.py`, `step5b_ddg_panel.sh`, `step6_conservation.py`,
`step9_structural_network.py`, `step11_phi_psi.py`, `step12_splice_screen.py`,
`step12b_finalize_splice.py`, `step12c_merge_splice.py`, `step13_phase_audit.py`,
`step14_cnv_sv_audit.py`, `step15_claim_scan.py`, `build_gene_panel.py`,
`screen_panel_ar.py`, `annotate_candidates_af.py`, `screen_genomewide_ar.py`,
`check_strong_ar_genes.py`, `scan_bub1b_locus.py`, and `rank_genomewide_ar.py`
(superseded, retained for provenance). 
Data (`analysis/data/`): domain PDB, `step4_results.json`, raw Compara response, README. 
Environment: `analysis/environment.txt` — Python 3.12.7, Biopython 1.88, NumPy 1.26.4,
bcftools 1.24; **documented absences**: mkdssp, FoldX, MD engine.

Structure: `AF-O60566-F1-model_v6.pdb`, MD5 `943e5596717db0424b1a020ae429e174`.
Pre-registered thresholds (RSA <0.20 / >0.40; pLDDT ≥70; ASN-at-1002 hard gate;
gnomAD popmax >0.001 and ClinVar B/LB ≥2-star stop criteria) were fixed before
results were inspected and **were not altered afterwards**.

Failed queries, access limitations and invalid query syntaxes are recorded in
§R3.10 rather than omitted. **Open reproducibility gaps are listed there and are
not yet closed** — most importantly, the DynaMut2 calls and the database queries
were made ad-hoc and still need to be captured as scripts with saved raw responses.

### AI-assisted analysis

AI-assisted analysis disclosure: Anthropic Claude Opus 5 and Claude Opus 5.5 were
used via the Claude API with a Pro plan. Data sharing for model training was disabled.
AI-assisted outputs were independently checked against the project's source data and
evidence record.

---

## 16. Final Conclusion

The proband carries a securely classified pathogenic *BUB1B* null allele
(**p.Leu737\***, ClinVar 2-star Pathogenic/Likely pathogenic) and a second,
ultra-rare missense variant (**p.Asn1002Lys**, rs2542593804) that remains a
**prioritised VUS** with no functional evidence of any kind.

**The hypothesis we set out to support is disfavoured.** N1002K does not behave
like the destabilised MVA alleles under a predictor that correctly classifies all
four of them. A structural helix-cap model was proposed as an alternative, but it
is computational only and a subsequent backbone φ/ψ measurement removed one of
its supports. **The mechanism is UNRESOLVED.**

**We then tested the gene itself rather than assuming it.** Prompted by a
genome-build error we found in our own Track 1 pipeline, we re-derived the
candidate from a phenotype-driven PanelApp panel and an unbiased genome-wide
recessive screen. *BUB1B* was the only candidate surviving frequency filtering —
an independent re-establishment, not a carried-forward assumption. A subsequent
two-tool splice screen found no computationally supported hidden intronic hit.

**Two genetic questions remain open, and they are now the rate-limiting ones.**
Phase is **UNPHASED** — the variants are 10,911 bp apart and short reads cannot
span them. **CNV/SV status is unresolved from available data** — no dosage or
structural information of any kind exists in the inputs we have. **No second
pathogenic *BUB1B* allele has been established**, so *BUB1B* remains a **leading
genetic hypothesis rather than a confirmed molecular diagnosis**, and the
genotype is reported as two heterozygous variants of interest in a
recessive-model candidate gene — not as compound heterozygous, biallelic, *cis*
or *trans*.

The next experiment is genetic, not mechanistic: resolve phase and/or exon dosage
first, because a *cis* result would make further N1002K work unjustifiable.

**We therefore report no drug candidate. The therapeutic gate remains closed until
genotype and mechanism are experimentally resolved.**

---

### References and data sources

**Primary literature** *(PMIDs verified in-session against PubMed/NCBI)*

- Suijkerbuijk SJE *et al.* Molecular causes for BUBR1 dysfunction in the human cancer predisposition syndrome mosaic variegated aneuploidy. *Cancer Res* 70:4891–4900 (2010). **PMID 20516114** — source for the I909T / L1012P / L844F / Q921H abundance phenotypes used to calibrate DynaMut2, and for the HSP90/proteasome dependence of MVA missense alleles.
- Gama Braga V *et al.* BUBR1 pseudokinase domain promotes kinetochore PP2A-B56 recruitment, spindle checkpoint silencing, and chromosome alignment. *Cell Rep* 33:108397 (2020). **PMID 33207204** — source for human BUBR1 being a pseudokinase, for PP2A-B56 binding the KARD rather than the pseudokinase domain, and for abundance and allosteric function being dissociable.

**Methods citations**

- Tien MZ *et al.* Maximum allowed solvent accessibilities of residues in proteins. *PLoS ONE* 8:e80635 (2013) — max-ASA values used for RSA normalisation.
- Rodrigues CHM, Pires DEV, Ascher DB. DynaMut2: assessing changes in stability and flexibility upon single and multiple point missense mutations. *Protein Sci* 30:60–69 (2021).
- Jaganathan K *et al.* Predicting splicing from primary sequence with deep learning. *Cell* 176:535–548 (2019) — SpliceAI.
- Zeng T, Li YI. Predicting RNA splicing from DNA sequence using Pangolin. *Genome Biol* 23:103 (2022).
- Cheng J *et al.* Accurate proteome-wide missense variant effect prediction with AlphaMissense. *Science* 381:eadg7492 (2023).
- Jumper J *et al.* Highly accurate protein structure prediction with AlphaFold. *Nature* 596:583–589 (2021); Varadi M *et al.* AlphaFold Protein Structure Database. *Nucleic Acids Res* 50:D439–D444 (2022).
- Cingolani P *et al.* A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff. *Fly* 6:80–92 (2012).
- McLaren W *et al.* The Ensembl Variant Effect Predictor. *Genome Biol* 17:122 (2016).
- Martin AR *et al.* PanelApp crowdsources expert knowledge to establish consensus diagnostic gene panels. *Nat Genet* 51:1560–1565 (2019).
- Danecek P *et al.* Twelve years of SAMtools and BCFtools. *GigaScience* 10:giab008 (2021).
- Cock PJA *et al.* Biopython. *Bioinformatics* 25:1422–1423 (2009).

**Databases and resources — versions and access dates verified in-session.**
*These version strings, not the citations above, are the authoritative provenance
record for every database claim in this report.*

| Resource | Version / identifier | Accessed | Used for |
|---|---|---|---|
| **ClinVar** (NCBI E-utilities) | **VCV000533901** `p.Leu737*` Pathogenic/Likely pathogenic, 2-star, last evaluated 2024-10-09 · **VCV004600147** `c.3006T>A` Uncertain significance, 1-star, last evaluated 2025-09-19 | 2026-09-15 | §3, §4; the T>G / T>A allele distinction |
| **gnomAD** | **v4.1.1** — `p.Asn1002Lys` (15-40220612-T-G): AC 1, AN 1,614,226, **AF 6.195e-7**, 0 hom, SAS AC 0 · `p.Leu737*`: exomes 7.87e-5, genomes 3.29e-5 | 2026-09-12 / 2026-09-15 | §2, §3 |
| **dbSNP** | **rs759242053** (`p.Leu737*`) · **rs2542593804** (`p.Asn1002Lys`, no clinical significance assigned) | 2026-09-15 | §2, §3 |
| **UniProt** | **O60566**, Swiss-Prot reviewed, sequence version 3, annotation updated 2026-09-02. Protein-kinase domain **766–1050** | 2026-09-15 | §5 |
| **AlphaFold DB** | **AF-O60566-F1-model_v6**, created 2025-08-01, md5 `943e5596717db0424b1a020ae429e174` (v4 retired, HTTP 404) | 2026-09-15 | §5, §6 |
| **Ensembl** | REST / VEP, transcript **ENST00000287598.11** (MANE), **GRCh38**; GRCh37 endpoint for the build erratum; Compara orthologues | 2026-09-15/16 | §3, §7, erratum |
| **UCSC** | `phyloP100way` **4.7967** · `phastCons100way` **1.000** at chr15:40,220,612 (hg38) | 2026-09-15 | §7 |
| **AlphaMissense** (via Ensembl VEP) | `p.Asn1002Lys` **0.9229** (likely_pathogenic) | 2026-09-15 | §6 |
| **DynaMut2** | web API; job IDs recorded in `analysis/scripts/step5b_ddg_panel.sh`. N1002K **−0.01**, L1012P −1.80, I909T −3.48, L844F −1.70, Q921H −0.15 kcal/mol | 2026-09-15 | §6 |
| **SpliceAI** | **1.3.1**, bundled GRCh38 annotation, `-D 500 -M 0`, TensorFlow 2.21.0 | 2026-09-24 | §Genetic Resolution Status |
| **Pangolin** | GitHub `tkzeng/Pangolin`, **GENCODE v44** annotation, `-d 500`, PyTorch 2.9.1 | 2026-09-24 | §Genetic Resolution Status |
| **snpEff** | **5.4c** (build 2026-02-23), db **GRCh38.mane.1.2.refseq**, `-canon` | 2026-09-16 | genome-wide and locus screens |
| **PanelApp** (Genomics England) | panel **290** "Familial rhabdomyosarcoma" **v1.6** (2025-11-23) · panel **259** "Childhood solid tumours cancer susceptibility" **v1.30** (2025-10-13) | 2026-09-16 | gene-panel selection |
| **PDBe** | **6tlj**, **5khu** — BUBR1 chains model only residues ~19–345/18–308; **residue 1002 is absent from both** | 2026-09-16 | §5 limitation |
| **MaveDB** | score-set search `BUB1B` → `{"detail":"Not Found"}` — **no deep mutational scan exists** | 2026-09-16 | §14 |
| **LOVD** | **inaccessible** (IP/network block). Status **UNKNOWN**, not negative | 2026-09-12 → 2026-09-24 | §14 limitation |
| **Proband VCF** | `WGS_EX2312012_HGWCNDSX7.vcf.gz`, md5 `a04ea354141cfb032872d67a11c8d2d8`, GRCh38, GATK 4.2.4.0 (gated; not committed) | 2026-09-16 → 2026-09-24 | all genotype claims |

**Failed or unavailable, recorded rather than omitted:** DDMut (result endpoint
returned server errors on all five jobs — **no values obtained, none reported**);
FoldX (not licensed); mkdssp (not installable on this platform — Shrake–Rupley
used instead); molecular dynamics (not performed); LOVD (network block).
