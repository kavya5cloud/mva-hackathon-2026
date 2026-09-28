### 1.2 ClinVar — Protein-level search

Query:
`Asn1002Lys`

Query date:
2026-09-12

Result:
ClinVar returned 13 variants matching the protein-level term across
multiple genes.

A BUB1B record was identified, but it represents a DIFFERENT nucleotide
substitution from the patient's variant:

- Transcript: `NM_001211.6`
- Gene: `BUB1B`
- HGVS: `c.3006T>A`
- Protein: `p.Asn1002Lys`
- Variation ID: `4600147`
- Accession: `VCV004600147.1`
- GRCh38 location: `chr15:40220612`
- Classification: `Uncertain significance`
- Review status: `1 star`
- Submitter count: `1`

This record must not be treated as evidence directly classifying the
patient's `c.3006T>G` allele, because T>A and T>G are distinct
nucleotide substitutions despite producing the same amino-acid change.

### 1.3 ClinVar — Exact patient variant

Query:
`NM_001211.6:c.3006T>G`

Query date:
2026-09-12

Result:
0 variants found in the exact-HGVS search.

Interpretation:
No ClinVar record was identified for the exact `c.3006T>G` allele
through the exact-HGVS query. A separate BUB1B `c.3006T>A`
(p.Asn1002Lys) record exists, but it cannot be used to classify
the patient's `c.3006T>G` allele.
---

# Round 2 — Mechanistic characterisation of BUB1B N1002K

All work below executed 2026-09-15. Environment: macOS darwin 25.5.0, Python 3
(Anaconda), Biopython 1.88, NumPy 1.26.4. Scripts in `analysis/scripts/`.

**Headline: the destabilisation hypothesis (A) is NOT supported. The drug-search
gate FAILS. Mechanism is classified C (UNKNOWN), leaning towards a local /
allosteric pseudokinase-domain defect rather than global thermodynamic
destabilisation.**

---

## Step 1 — Variant reality check (GATE 1: PASSED)

| Resource | Version | Query date | Exact query | Result |
|---|---|---|---|---|
| Ensembl VEP REST | GRCh38, Ensembl REST (live) | 2026-09-15 | `NM_001211.6:c.3006T>G` | missense_variant, `ENST00000287598.11:c.3006T>G`, `ENSP00000287598.7:p.Asn1002Lys`, **exon 23/23**, MANE/canonical. `colocated_variants` = none returned by VEP. |
| dbSNP (NCBI E-utilities) | build current 2026-09-15 | 2026-09-15 | `15[CHR] AND 40220612[CHRPOS]` | **1 record: rs2542593804.** docsum HGVS includes `NC_000015.10:g.40220612T>G`, `NM_001211.6:c.3006T>G`, `NP_001202.5:p.Asn1002Lys`. `clinical_significance` = **empty (none assigned)**. |
| ClinVar (E-utilities esearch) | 2026-09-15 | 2026-09-15 | `BUB1B[gene] AND c.3006T>G` | **count = 0** |
| ClinVar | 2026-09-15 | 2026-09-15 | `BUB1B[gene] AND Asn1002Lys` | count = 1 → UID 4600147 = `c.3006T>**A**` (VCV004600147), Uncertain significance, *criteria provided, single submitter* (1 star), last evaluated 2025-09-19, SPDI `NC_000015.10:40220611:T:A`. **Different nucleotide allele — not transferable.** |
| ClinVar | 2026-09-15 | 2026-09-15 | `BUB1B[gene] AND 40220612` | count = 1 → UID 3221415 = `c.3007G>A` (p.Ala1003Thr), VUS, 1 star. **Neighbouring position, not the patient allele.** |
| gnomAD v4.1.1 | (carried from Round 1) | 2026-09-12 | `15-40220612-T-G` | AC=1, AN=1,614,226, AF=6.195e-7, 0 hom, PASS |
| LOVD | — | — | — | **ACCESS LIMITATION** — IP/network block. Status UNKNOWN. Not a negative result. |

**Key correction to the Round 1 record:** the exact T>G allele is **not novel**.
It carries **dbSNP rsID rs2542593804**. Absence from ClinVar ≠ absence from all
variant resources.

**Gate 1 evaluation (pre-registered stop criteria):**
- popmax AF > ~0.001? **No** (6.195e-7). 
- ClinVar Benign/Likely benign at ≥2 star? **No record at all for T>G.**

→ **GATE 1 PASSED — continue.** Evidence tier: Tier 1 (database records).

---

## Step 2 — Verification of p.Leu737* (c.2210T>G)

| Item | Result | Source |
|---|---|---|
| Consequence | `stop_gained`, `ENST00000287598.11:c.2210T>G`, `p.Leu737Ter` | Ensembl VEP REST, 2026-09-15 |
| Genomic (GRCh38) | chr15:40209701 T>G | VEP |
| rsID | **rs759242053** | VEP colocated_variants |
| ClinVar | **VCV000533901 — Pathogenic/Likely pathogenic**, review status *criteria provided, multiple submitters, no conflicts* (**2 star**), last evaluated 2024-10-09, trait: **Mosaic variegated aneuploidy syndrome 1**. SPDI `NC_000015.10:40209700:T:G` | ClinVar esummary, 2026-09-15 |
| gnomAD (via VEP) | exomes AF 7.867e-5; genomes AF 3.286e-5; SAS 0 | VEP colocated frequencies |
| Literature | PMIDs 29641532, 15475955, 21190457 | VEP colocated pubmed |

**Transcript / NMD analysis (ENST00000287598, 23 exons, CDS 3153 nt → 1050 aa):**

1. **Exon containing c.2210: exon 17** (of 23). 
2. **Total exon count: 23.** 
3. Stop codon created at CDS nt **2209–2211**. 
4. 5′UTR = 152 nt (CDS starts genomic 40161221; exon 1 = 40161069–40161255). Final
   exon–exon junction (exon 22 | exon 23) at transcript nt 3109 = **c.2957**. 
5. PTC last base (c.2211) lies **746 nt upstream** of the final exon–exon junction —
   far beyond the ~50–55 nt boundary. **NMD-competent by the canonical rule.** 
6. **Codon 737 = `TTA` (verified from Ensembl CDS)**; c.2210 is base **2** of that codon. 
7. **`TTA` (Leu) → `TGA` (opal stop) — confirmed.**

**Interpretation.** Leu737* is a *bona fide*, independently classified (2-star,
multi-submitter, no conflicts) pathogenic loss-of-function allele in the correct
disease gene and disease. The NMD prediction is structural/positional (Tier 3 for
the NMD step itself); the pathogenic classification is Tier 1. Stated without
overstatement: NMD is *predicted*, not measured in this patient — patient RNA
would be required to demonstrate transcript loss.

---

## Step 3 — BUBR1 domain boundaries (UniProt O60566)

Source: `https://rest.uniprot.org/uniprotkb/O60566.json`, Swiss-Prot reviewed,
sequence version 3, length **1050 aa**, last annotation update **2026-09-02**.
Retrieved 2026-09-15.

| Feature type | Range | Description |
|---|---|---|
| Domain | **62–226** | BUB1 N-terminal |
| Domain | **766–1050** | **Protein kinase** (pseudokinase in human — no phosphotransfer activity) |
| Motif | 111–118 | Nuclear localization signal |
| Motif | 224–232 | D-box |
| Active site | 882 | Proton acceptor *(annotated by similarity; human BUBR1 is catalytically dead)* |
| Binding site | 772–780 | ATP |
| Binding site | 795 | ATP |
| Site | 579–580 | Cleavage; by caspase-3 |
| Site | 610–611 | Cleavage; by caspase-3 |

**Annotations within ±15 residues of position 1002 (i.e. 987–1017): NONE.**

**Observed fact:** N1002 lies inside the pseudokinase domain (766–1050), near its
C-terminal end, and is **not** at any annotated ATP-binding, active-site, or
functional-site residue. **Inference:** any effect of N1002K is therefore a
*structural/packing* effect, not a direct catalytic- or ligand-site effect — which
is consistent with human BUBR1 being a pseudokinase. Tier 1 (curated annotation).

---

## Step 4 — Asn1002 burial / structure (PRIMARY GATE)

**Structure.** AlphaFold DB `AF-O60566-F1`, **model_v6** (`modelCreatedDate`
2025-08-01, `latestVersion` 6). 
**DEVIATION FROM BRIEF:** `AF-O60566-F1-model_v4.pdb` referenced in the project
brief is **retired — HTTP 404 on 2026-09-15**. v6 is the current AlphaFold DB
release and was used instead. Full-length, 1050 residues, single chain A.
MD5 of downloaded v6 PDB: `943e5596717db0424b1a020ae429e174`.

**DEVIATION FROM BRIEF (method).** `mkdssp`/`dssp` could not be installed in this
environment (no binary available for this platform; conda salilab channel and pip
both failed). SASA was therefore computed with **Biopython `Bio.PDB.SASA`
(Shrake–Rupley)**, and RSA derived with **Tien et al. 2013 (PLoS ONE 8:e80635)**
theoretical maximum ASA values. This is a documented substitution, not a silent one.

**Script:** `analysis/scripts/step4_structure_gate.py`

### 4a. Numbering gate — PASSED

```
[GATE] residue 1002 in model = ASN (N)
[GATE] residue 1012 = L (expected L) OK
[GATE] residue  909 = I (expected I) OK
[GATE] residue  921 = Q (expected Q) OK
[GATE] residue  844 = L (expected L) OK
[GATE] residue  737 = L (expected L) OK
```
UniProt O60566 numbering is in exact register with NM_001211.6 protein numbering.
**Residue 1002 IS asparagine — the mapping is correct.**

### 4b. pLDDT — PASSED

```
pLDDT(1002)          = 91.06
mean pLDDT(992-1012) = 91.45
```
Well above the pre-registered ≥70 threshold. **Local structure is high-confidence;
a burial conclusion is permitted.**

### 4c. RSA, residues 995–1015

Domain context = pseudokinase domain 766–1050 in isolation. (Values identical to
full-length context here, i.e. no other domain packs against this surface.)

| res | aa | pLDDT | SASA (Å²) | **RSA** |
|---|---|---|---|---|
| 995 | K | 92.4 | 108.02 | 0.458 |
| 996 | F | 94.9 | 3.62 | 0.015 |
| 997 | F | 93.9 | 2.42 | 0.010 |
| 998 | V | 92.3 | 45.75 | 0.263 |
| 999 | R | 93.8 | 56.60 | 0.207 |
| 1000 | I | 93.8 | 2.14 | 0.011 |
| 1001 | L | 91.6 | 7.64 | 0.038 |
| **1002** | **N** | **91.1** | **31.50** | **0.162** |
| 1003 | A | 88.0 | 3.39 | 0.026 |
| 1004 | N | 80.4 | 103.44 | 0.530 |
| 1005 | D | 82.2 | 136.05 | 0.705 |
| 1006 | E | 87.8 | 91.67 | 0.411 |
| 1007 | A | 91.1 | 67.92 | 0.527 |
| 1008 | T | 92.1 | 10.10 | 0.059 |
| 1009 | V | 93.9 | 41.99 | 0.241 |
| 1010 | S | 94.4 | 57.25 | 0.369 |
| 1011 | V | 94.7 | 0.00 | 0.000 |
| 1012 | L | 95.3 | 0.00 | 0.000 |
| 1013 | G | 94.2 | 25.21 | 0.242 |
| 1014 | E | 94.7 | 81.93 | 0.367 |
| 1015 | L | 95.7 | 8.32 | 0.041 |

### 4d. Benchmark against known MVA positions

| pos | aa | pLDDT | RSA (full) | RSA (domain) | published behaviour |
|---|---|---|---|---|---|
| 727 | R | 88.5 | 0.061 | n/a (outside 766–1050) | ↑turnover (~2×) |
| 814 | R | 90.3 | 0.156 | 0.156 | — |
| 844 | L | 85.9 | 0.006 | 0.006 | ↓abundance + extra defect |
| 909 | I | 87.0 | 0.029 | 0.029 | ↓abundance, rescued by re-expression |
| 921 | Q | 83.3 | 0.011 | **0.311** | **stable, WT-like** |
| **1002** | **N** | **91.1** | **0.162** | **0.162** | **unknown (this study)** |
| 1012 | L | 95.3 | 0.000 | 0.000 | ↓abundance, rescued by re-expression |

### 4e. Verdict against PRE-REGISTERED thresholds

Thresholds fixed before results were inspected: RSA <0.20 buried; >0.40 exposed;
0.20–0.40 equivocal.

**N1002 RSA = 0.162 → BURIED → formally supports hypothesis A.**

**Honest caveat (recorded, not suppressed):** N1002 is buried but at the *shallow*
end — markedly less deeply than L1012 (0.000), L844 (0.006) or I909 (0.029). Its
RSA is closer to R814 (0.156). Per-atom analysis (Step 5) refines this
considerably and is the more informative measurement.

**Gate 4 result: PASSED — continue to Step 5.** Evidence tier: Tier 3
(computational, on a predicted structure).

---

## Step 5 — Hydrogen bonds and ΔΔG

**Script:** `analysis/scripts/step5_contacts.py`. Same structure (v6). AlphaFold
models carry no hydrogens, so H-bonds are called on heavy-atom geometry:
N/O donor–acceptor pair at ≤3.5 Å. Contacts listed to 4.0 Å.

### 5a. Per-atom solvent exposure of N1002 — this is the key refinement

| atom | SASA (Å²) |
|---|---|
| N | 0.00 |
| CA | 2.42 |
| C | 0.00 |
| O | 11.79 |
| CB | 10.87 |
| CG | 0.00 |
| **OD1** | **6.43** |
| **ND2** | **0.00** |
| side chain (CB+CG+OD1+ND2) | 17.30 |
| **amide tip (OD1+ND2)** | **6.43** |

**Observed fact:** the residue-level RSA of 0.162 is driven almost entirely by CB
(10.87 Å²) and the *backbone* carbonyl O (11.79 Å²). The **functional amide group
is essentially fully buried** — ND2 has **zero** solvent exposure and CG is zero.

### 5b. H-bond inventory

| N1002 atom | role | partner | partner atom | distance | call |
|---|---|---|---|---|---|
| OD1 | acceptor | **Trp978** | backbone **N** | **2.83 Å** | **H-bond** |
| ND2 | donor | **Val998** | backbone **O** | **2.83 Å** | **H-bond** |
| ND2 | donor | **Trp978** | backbone **O** | **2.95 Å** | **H-bond** |
| OD1 | (weak/long) | Leu1001 | backbone O | 3.73 Å | polar, not called |
| ND2 | (long) | Trp978 | backbone N | 3.62 Å | polar, not called |

Residues packing the N1002 side chain (≤4.0 Å): **Phe977, Trp978, Val998, Leu1001, Ala1003.**

**Observed fact:** N1002 is a **buried asparagine making three hydrogen bonds,
all to main-chain atoms**, bridging the Phe977–Trp978 segment to the Val998–Leu1001
segment, inside an aromatic pocket (F977, W978).

**Inference (Tier 3, mechanistic):** Asn→Lys should be non-conservative here.
(i) Lysine NZ is a **donor only** and cannot replace OD1's role accepting the
W978 backbone amide. (ii) It buries a **formal positive charge** with no
compensating buried acceptor. (iii) Lys is longer and bulkier in a tightly packed
aromatic pocket. All three point towards a **local** structural penalty.

### 5c. ΔΔG prediction — and it CONTRADICTS the above

Tool: **DynaMut2** (Rodrigues, Pires & Ascher, *Protein Sci* 2021), web API
`https://biosig.lab.uq.edu.au/dynamut2/api/prediction_single`, queried 2026-09-15.
Input structure: pseudokinase domain 766–1050 excised from AF-O60566-F1-model_v6
(`BUBR1_kinase_766_1050.pdb`), chain A. Sign convention: negative = destabilising.

Crucially, the predictor was **calibrated on variants with published experimental
abundance phenotypes before the N1002K result was interpreted**:

| variant | DynaMut2 ΔΔG (kcal/mol) | published experimental behaviour | predictor correct? |
|---|---|---|---|
| I909T | **−3.48** | reduced abundance, ↑turnover, rescued by re-expression | ✅ |
| L1012P | **−1.80** | reduced abundance, ↑degradation, rescued by re-expression | ✅ |
| L844F | **−1.70** | reduced abundance (+ additional defect) | ✅ |
| Q921H | **−0.15** | **stable, functionally indistinguishable from WT** | ✅ |
| **N1002K** | **−0.01** | **unknown** | — |

**This is the pivotal result.** DynaMut2 correctly separates all four
known-outcome variants on this exact structure: the three destabilised alleles
score −1.7 to −3.5, the known-stable allele scores −0.15. The predictor is
demonstrably *sensitive* in this system. **N1002K scores −0.01 — clustering with
Q921H, the known-stable, WT-like negative control, and nowhere near the
destabilised group.** The neutral call cannot be dismissed as predictor
insensitivity.

**Attempted replication — FAILED (access limitation).** DDMut (same group,
independent model) accepted job submissions but its results endpoint returned
`{"message": "Internal Server Error"}` for all five jobs on repeated polling.
**No DDMut values were obtained. No number is reported for it.** FoldX is not
licensed/installed in this environment. Per instruction, predictors are reported
separately and **not averaged**.

### 5d. Orthogonal in-silico metric (also calibrated)

Ensembl VEP REST with AlphaMissense, 2026-09-15, transcript ENST00000287598:

| variant | AlphaMissense | AM class | SIFT | PolyPhen-2 |
|---|---|---|---|---|
| **N1002K** | **0.9229** | **likely_pathogenic** | deleterious | probably_damaging |
| L1012P | 0.8720 | likely_pathogenic | deleterious | probably_damaging |
| Q921H | 0.4913 | ambiguous | deleterious | probably_damaging |
| I909T | 0.4506 | ambiguous | deleterious | probably_damaging |
| L844F | 0.2917 | likely_benign | deleterious | probably_damaging |

**Reading this honestly:** AlphaMissense scores N1002K **highest in the entire
panel** — above the validated pathogenic L1012P. But AlphaMissense **fails the
abundance calibration**: it cannot separate the known-stable Q921H (0.49) from the
known-destabilised I909T (0.45), and calls the destabilised L844F "likely benign".
SIFT and PolyPhen-2 are uninformative here — they call every panel member damaging,
including the WT-like Q921H.

**Therefore the two tools are measuring different things, and both readings stand:**
- **Stability axis (DynaMut2, calibrated and correct 4/4): N1002K is NOT predicted to be destabilising.**
- **General function/fitness axis (AlphaMissense, not calibrated for abundance): N1002K is predicted deleterious.**

The convergent reading is that N1002K may well be **functionally deleterious
without being thermodynamically destabilising** — which is precisely the
distinction this investigation was designed to test, and it falls against
hypothesis A.

---

## Step 6 — Conservation

**Script:** `analysis/scripts/step6_conservation.py`. Source: Ensembl REST Compara
`/homology/symbol/human/BUB1B`, `type=orthologues; sequence=protein; aligned=1`,
retrieved 2026-09-15. Residues read directly from the Compara pairwise protein
alignments (no re-alignment step needed; MAFFT/Clustal not required).

| species | 727 | 737 | 814 | 844 | 909 | 921 | **1002** | 1012 | % id |
|---|---|---|---|---|---|---|---|---|---|
| *Homo sapiens* | R | L | R | L | I | Q | **N** | L | 100.0 |
| *Pan troglodytes* | R | L | R | L | I | Q | **N** | L | 95.7 |
| *Mus musculus* | R | L | R | L | I | Q | **N** | L | 74.9 |
| *Rattus norvegicus* | R | L | R | L | I | Q | **N** | L | 76.1 |
| *Canis lupus familiaris* | R | L | R | L | I | Q | **N** | L | 87.5 |
| *Gallus gallus* | R | L | R | L | I | Q | **N** | L | 49.6 |
| *Xenopus tropicalis* | H | L | R | **I** | **L** | **Y** | **N** | – | 44.0 |
| *Danio rerio* | – | – | – | – | – | – | – | – | 39.9 |

**Limitation (recorded):** the zebrafish orthologue (ENSDARG00000074927,
`ortholog_one2many`, 39.9% id) has **gaps at every benchmarked position** — this
region is not alignable. A second zebrafish paralogue (ENSDARG00000078825, 18.3%
id) was excluded as too divergent. **Conservation is therefore established from
human to *Xenopus*, not to teleosts.** Do not claim "conserved to zebrafish".

**Observed fact:** N1002 is **invariant across all 6 species with an alignable
residue (human → *Xenopus*)**. Notably, N1002 is conserved in *Xenopus*
**where three benchmark positions have diverged** (L844→I, I909→L, **Q921→Y**).

**Key discriminator:** N1002 is **more deeply conserved than Q921**, the residue
whose missense variant (Q921H) is experimentally stable and WT-like. This argues
against classification D (incidental).

**Nucleotide-level conservation** (UCSC REST API, hg38, chr15:40220611-40220612,
retrieved 2026-09-15):

| track | value | scale |
|---|---|---|
| **phyloP100way** | **4.7967** | track range −20 to 7.532 |
| **phastCons100way** | **1.000** | range 0 to 1 (maximum) |

GERP was not retrieved (track not queried via this endpoint) — recorded as not done.

**Interpretation:** the exact mutated nucleotide is under strong purifying
selection (phyloP 4.80; phastCons at ceiling 1.0). This is measured, not asserted.
Tier 1 (database-derived scores).

---

## Step 7 — PP2A-B56 surface (competing-hypothesis test)

**Source:** Gama Braga *et al.*, "BUBR1 Pseudokinase Domain Promotes Kinetochore
PP2A-B56 Recruitment, Spindle Checkpoint Silencing, and Chromosome Alignment,"
*Cell Reports* 33(7):108397, 17 Nov 2020 — **PMID 33207204**. Full text consulted
via the bioRxiv preprint (doi:10.1101/733378).

**Critical mechanistic finding — this reframes the hypothesis:**

> PP2A-B56 **does not bind the BUBR1 pseudokinase domain directly.** Recruitment
> occurs "mainly through direct interaction between one of several isoforms of the
> B56 adaptor subunit and the **Kinetochore Alignment Regulatory Domain (KARD)**
> of BUBR1", phosphorylated at **S670 and S676** by PLK1/CDK1. The pseudokinase
> domain acts **allosterically** to promote that KARD phosphorylation.

**Residues experimentally tested in the pseudokinase domain** (all attenuated
S670/S676 phosphorylation and reduced PP2A-B56 kinetochore recruitment):
**K795R** (SKD), **D882A**, **S884A**, **D911A**, **K795R+D911A** (DKD), **S913A**,
and **BUBR1-731X** (whole-domain deletion).

**N1002 is not among them, and no interface residues have been invented here.**

**Mapped distances** (AF-O60566-F1-model_v6, minimum heavy-atom distance from N1002):

| target | distance | note |
|---|---|---|
| Ser670 (KARD) | **71.9 Å** | pLDDT 30.2 — disordered, position unreliable |
| Ser676 (KARD) | **59.0 Å** | pLDDT 35.9 — disordered, position unreliable |
| Ser665 | 84.5 Å | pLDDT 29.5 |
| Ser682 | 51.0 Å | pLDDT 31.8 |
| Lys795 (ATP) | 28.6 Å | — |
| Asp882 (catalytic) | 18.4 Å | — |
| Asp911 | 23.4 Å | — |
| Ser913 | 24.9 Å | — |

**Classification: DISTANT / UNLIKELY** to be a direct PP2A-B56 interface residue.
Two independent reasons: (i) the KARD is ≥51 Å away in the model, and (ii) more
decisively and independent of the model, **PP2A-B56 does not bind this domain at
all** — so there is no pseudokinase-domain "PP2A-B56 interface" for N1002 to sit on.
The absolute KARD distances carry low confidence (pLDDT ~30, intrinsically
disordered linker) and should not be quoted as precise; the qualitative conclusion
does not depend on them.

**Consequence for hypothesis B.** Hypothesis B as literally stated — "disrupts a
PP2A-B56-related *surface*" — is **NOT SUPPORTED**. N1002 is buried (Step 4/5) and
is not on any PP2A-B56 binding surface.

**However, B is not thereby eliminated in its broader form.** Because the
pseudokinase domain's contribution is **allosteric and requires a correctly folded
domain**, a *local* fold perturbation at N1002 could impair KARD phosphorylation
and downstream PP2A-B56 recruitment **without** producing a measurable drop in
global stability or steady-state abundance. Notably, Gama Braga *et al.* report
that both the **hyperstable** BUBR1-731X and the **unstable** BUBR1-DKD lose KARD
phosphorylation — i.e. **abundance and allosteric function are dissociable in this
domain**. This is the mechanism most consistent with the full evidence set
(buried H-bonded Asn + high conservation + high AlphaMissense + **neutral ΔΔG**),
but it is **inferred, not demonstrated**.

---

## Step 8 — E3 ligase / degradation machinery

Searches run 2026-09-15 across PubMed/PMC/journal sources for: BUBR1 degradation
ubiquitin ligase; BUBR1 misfolded proteasome CHIP; BUB1B protein quality control;
BUBR1 HSP90 proteasome degradation; BUBR1 ubiquitination E3; BUBR1 turnover chaperone.

### DEMONSTRATED
- **MVA missense BUBR1 alleles are cleared by an HSP90-dependent, proteasome-dependent route.** Suijkerbuijk *et al.*, *Cancer Res* 70:4891–4900 (2010), **PMID 20516114**. U2OS cells stably expressing LAP-tagged WT, **I909T** or **L1012P** BUBR1 were challenged with **cycloheximide** (translation), **geldanamycin** (HSP90 folding) and **MG132** (proteasome). Mutants showed ~2-fold increased turnover (I909T, R727C) and sensitivity to HSP90 inhibition. **Forced overexpression of I909T and L1012P to WT-like levels fully restored function** — establishing that for *those* alleles the defect is abundance, not intrinsic function.
- **APC/C–CDH1 degrades BUB1 in G1 via KEN boxes**; BUBR1 is a core MCC component that *inhibits* APC/C towards cyclin B1 and securin (BUBR1's D-box is UniProt-annotated at 224–232).

### PLAUSIBLE (mechanistically reasonable, not shown for BUBR1 in human cells)
- **CHIP/STUB1** as the E3 coupling HSP70/HSP90 triage to ubiquitination — CHIP is the canonical chaperone-linked U-box E3 for misfolded clients, and the HSP90 dependence above makes it a reasonable candidate. **No publication was found demonstrating CHIP/STUB1 ubiquitinates BUBR1.**
- **CDC37** as the kinase-domain-specific HSP90 co-chaperone — BUBR1 carries a (pseudo)kinase domain, making CDC37 engagement plausible. **No BUBR1-specific evidence found.**
- Chaperone-assisted kinetochore quality control exists as a described system, but the identified components (**Hsp70, Bag102, Ubc4, Ubr11, San1**) are from **yeast**, not human, and BUBR1 was not the substrate.

### UNKNOWN
1. **Specific E3 ligase for misfolded human BUBR1: NOT IDENTIFIED.** This is a genuine, explicit gap in the literature.
2. **CHIP/STUB1 → BUBR1: no direct evidence.**
3. **CDC37/HSP70 → BUBR1: no direct evidence.**
4. **Evidence specifically for N1002K: NONE.** No functional, abundance, turnover or structural study of this variant exists.

**Limitation stated plainly:** because no E3 ligase for misfolded BUBR1 is known,
any therapeutic strategy aimed at blocking BUBR1 degradation currently has **no
defined molecular target**. This would be a blocker for the drug arm even if the
destabilisation mechanism had been supported.

---

## MECHANISM DECISION

### **C. UNKNOWN** — with hypothesis A (destabilisation) actively disfavoured.

**Evidence FOR a real functional effect (i.e. against D, incidental):**
- Amide group of N1002 is **fully buried** (ND2 SASA 0.00 Å²) and makes **three main-chain hydrogen bonds** (W978 N, V998 O, W978 O) bridging two secondary-structure elements. Asn→Lys cannot reproduce the OD1 acceptor role and buries a charge. *(Tier 3)*
- **phyloP 4.80 / phastCons 1.00** at the exact nucleotide — measured strong purifying selection. *(Tier 1)*
- **N1002 invariant human → *Xenopus***, and conserved where the WT-like control Q921 has diverged (Q→Y). *(Tier 1)*
- **AlphaMissense 0.9229, likely_pathogenic** — highest in the benchmark panel. *(Tier 3)*
- Extremely rare: gnomAD AF 6.195e-7, 0 homozygotes; no ClinVar classification; dbSNP rs2542593804 with no clinical significance assigned. *(Tier 1)*
- Found **in trans** with a 2-star **Pathogenic/Likely pathogenic** LoF allele (Leu737*) in a patient with the matching phenotype. *(Tier 1, genetics — though phase has not been demonstrated in this record; see below)*

**Evidence AGAINST hypothesis A (destabilisation) — this is the decisive contradiction:**
- **DynaMut2 ΔΔG = −0.01 kcal/mol**, i.e. neutral — and the predictor was **validated on the same structure against four variants with known experimental abundance phenotypes and got all four right** (I909T −3.48, L1012P −1.80, L844F −1.70 destabilised; Q921H −0.15 stable). **N1002K clusters with the known-stable Q921H negative control.** *(Tier 3, but calibrated)*
- N1002's residue-level burial (RSA 0.162) is **shallow** relative to the destabilising alleles L1012 (0.000), L844 (0.006), I909 (0.029).
- N1002 sits at the **C-terminal edge** of the pseudokinase domain with **no UniProt annotation within ±15 residues** and no packing against any other domain.

**Evidence AGAINST hypothesis B as literally stated (PP2A-B56 surface):**
- PP2A-B56 **does not bind the pseudokinase domain directly** (PMID 33207204); it binds the KARD (S670/S676), which is **51–85 Å away** and disordered. N1002 is buried, not on any interaction surface.

**Why not D (incidental)?** The conservation and AlphaMissense evidence is too
strong, and the allele frequency too low, to dismiss it — and dismissing it would
leave the patient's MVA with only one explained allele.

**Why C and not A or B?** The two strongest *stability-specific* lines point in
opposite directions and cannot be reconciled from computation alone: the
hydrogen-bond geometry says "this should hurt the local fold", while a
demonstrably-calibrated ΔΔG predictor says "this does not destabilise the domain".
**Declaring A supported would require ignoring the one computational result that
was explicitly validated against ground truth in this system.**

**Most consistent (but UNPROVEN) working model, stated as a hypothesis only:**
N1002K causes a **local** perturbation of the pseudokinase C-lobe that impairs the
domain's **allosteric** promotion of KARD S670/S676 phosphorylation, **without**
measurably reducing global stability or steady-state BUBR1 abundance. This is
explicitly the "WT-like abundance, impaired function" scenario that the brief
pre-registered as the **strong falsification** of the abundance-rescue model. It
is testable (Steps 1–8 of the experimental plan below) and must be tested before
being believed.

### Additional evidence gap flagged
**Phase has not been demonstrated in this record.** The compound-heterozygous
interpretation requires that N1002K and Leu737* are in *trans*. Nothing in the
evidence gathered here establishes that. Parental testing or read-backed phasing
is required. Recorded as an open gap, not an assumption.

---

## DRUG SEARCH: **NO — NOT JUSTIFIED. GATE FAILED.**

The brief conditions the drug search on the mechanism gate supporting the
**stabilisation** hypothesis. It does not.

1. The only **calibrated** stability prediction returns **neutral (−0.01 kcal/mol)**, clustering N1002K with the known-stable Q921H rather than with the destabilised alleles that the stabiliser rationale is built on.
2. There is **no evidence of any kind** — experimental or clinical — that N1002K reduces BUBR1 abundance. No functional study of this variant exists.
3. **No E3 ligase for misfolded BUBR1 has ever been identified** (Step 8), so a degradation-blocking strategy has no defined target.
4. The excluded-class list in the brief (HSP90 inhibitors, MPS1/TTK, Aurora, KIF11, antimitotics, proteasome inhibitors) removes essentially every well-characterised agent that touches this pathway — and correctly so, since HSP90 inhibition and proteasome inhibition would *reduce* BUBR1 or *impair* the checkpoint, which is the wrong direction.

**No drug candidates are proposed, and none are ranked.** Proposing a chaperone-
or degradation-directed compound here would be retrofitting a therapy to an
unsupported mechanism — explicitly prohibited by rule 11.

**Condition for re-opening the drug arm:** if experiment 2/3 below demonstrates
that N1002K has **reduced steady-state abundance and a shortened half-life** that
is **proteasome-dependent**, the destabilisation mechanism becomes supported and
the drug search should be re-run at that point — not before.

---

## FALSIFICATION EXPERIMENTS

Ordered so that the earliest experiments discriminate hardest between A, B/C and D.

| # | Experiment | Readout | Result that supports A | Result that falsifies A |
|---|---|---|---|---|
| 1 | Stable isogenic RPE-1 or U2OS lines: LAP/GFP-tagged **WT, N1002K, L1012P (pos. ctrl), Q921H (neg. ctrl)**, siRNA-resistant, on endogenous BUBR1 knockdown | expression established | — | — |
| 2 | **Steady-state abundance** by quantitative immunoblot vs WT, n≥3 | relative protein level | N1002K reduced like L1012P | **N1002K = WT, like Q921H** |
| 3 | **Half-life**: cycloheximide chase, 0–8 h | t½ | t½ shortened | **t½ = WT** |
| 4 | **Proteasome dependence**: MG132 rescue of abundance | fold rescue | mutant selectively rescued | no selective rescue |
| 5 | **Chaperone dependence**: geldanamycin/17-AAG at low dose, short exposure, with an HSP90-client positive control and a mitotic-arrest control to avoid confounding by checkpoint effects | abundance loss vs WT | mutant selectively lost | no selective loss |
| 6 | **SAC function**: nocodazole challenge, mitotic index + time-lapse mitotic duration; **chromosome alignment**: metaphase plate width; missegregation rate | checkpoint strength | impaired | — |
| 7 | **Abundance rescue test**: titrate N1002K expression to WT-matched levels (doxycycline-tunable), re-measure #6 | function restored? | **function restored → A confirmed, drug arm re-opens** | **function NOT restored → A falsified** |
| 8 | **If abundance is normal (the predicted outcome):** measure **KARD phospho-S670/S676** (phospho-specific immunoblot + kinetochore immunofluorescence) and **kinetochore PP2A-B56 / B56 isoform recruitment**, per PMID 33207204 | pS670/pS676, B56 intensity at kinetochores | — | **reduced pKARD + reduced B56 with WT-like abundance → allosteric/scaffolding defect (B-broad) confirmed** |
| 9 | **Phase determination**: parental testing or long-read/read-backed phasing of c.2210T>G and c.3006T>G | cis vs trans | — | **cis → N1002K is not the second pathogenic allele; reconsider D and re-open the search for a second hit** |
| 10 | **Thermal stability, orthogonal to cells**: purify pseudokinase domain 766–1050 WT vs N1002K; nanoDSF/DSF Tm and limited proteolysis | ΔTm | ΔTm ≪ 0 | **ΔTm ≈ 0 → independently confirms the neutral ΔΔG prediction** |

**Pre-registered decision rules:**
- WT-like abundance **+** WT-like half-life **+** impaired SAC/alignment → **abundance rescue is insufficient; B-broad (allosteric) becomes the leading hypothesis.**
- WT-like abundance **+** WT-like half-life **+** WT-like function → **reconsider D (incidental)** and treat experiment 9 as urgent.
- Reduced abundance **+** shortened t½ **+** MG132-rescued **+** function restored by re-expression → **A confirmed; re-open the drug search.**

---

## REPRODUCIBILITY RECORD

**Date of all Round 2 queries:** 2026-09-15.

**Structures**
- `AF-O60566-F1-model_v6.pdb` — AlphaFold DB, created 2025-08-01, `latestVersion` 6, MD5 `943e5596717db0424b1a020ae429e174`. URL: https://alphafold.ebi.ac.uk/files/AF-O60566-F1-model_v6.pdb
- `BUBR1_kinase_766_1050.pdb` — pseudokinase domain excised from the above (Biopython PDBIO + residue Select), used for all ΔΔG submissions.
- **model_v4 (named in the brief) is retired — HTTP 404 on 2026-09-15.**

**Software versions**
- Python 3 (Anaconda, /opt/anaconda3), Biopython **1.88**, NumPy **1.26.4**
- SASA: `Bio.PDB.SASA.ShrakeRupley`; max-ASA reference: Tien *et al.* 2013, PLoS ONE 8:e80635
- **mkdssp / dssp: NOT AVAILABLE** — install failed (conda salilab + pip). DSSP was not run. `pydssp` installed but provides secondary structure only, no SASA.
- **FoldX: NOT AVAILABLE** (not licensed/installed).

**Web services / APIs**
| Service | Endpoint | Outcome |
|---|---|---|
| AlphaFold DB API | `alphafold.ebi.ac.uk/api/prediction/O60566` | OK |
| UniProt REST | `rest.uniprot.org/uniprotkb/O60566.json` | OK |
| Ensembl REST VEP | `rest.ensembl.org/vep/human/hgvs/...` (+`AlphaMissense=1`) | OK |
| Ensembl REST lookup/sequence | `/lookup/id/ENST00000287598?expand=1`, `/sequence/id/...?type=cds` | OK |
| Ensembl REST Compara | `/homology/symbol/human/BUB1B?type=orthologues;sequence=protein;aligned=1` | OK |
| NCBI E-utilities | `esearch`/`esummary` on `clinvar`, `snp` | OK |
| UCSC REST | `api.genome.ucsc.edu/getData/track?genome=hg38;track=phyloP100way…` | OK |
| **DynaMut2** | `biosig.lab.uq.edu.au/dynamut2/api/prediction_single` | OK — 5/5 jobs returned |
| **DDMut** | `biosig.lab.uq.edu.au/ddmut/api/prediction_single` | **FAILED — `Internal Server Error` on all result polls. No values obtained.** |
| **LOVD** | — | **FAILED — IP/network block (carried from Round 1). Status UNKNOWN.** |

**Failed / null queries (recorded, not hidden)**
- `AF-O60566-F1-model_v4.pdb` → HTTP 404
- ClinVar `BUB1B[gene] AND c.3006T>G` → **0 results**
- DDMut result polling → Internal Server Error ×5 (two submission formats attempted)
- GERP score → not retrieved (not queried)
- Zebrafish orthologue → gaps at all 8 benchmarked positions; second paralogue excluded (18.3% id)

**Pre-registered thresholds (fixed before results; NOT altered afterwards)**
- RSA <0.20 buried / >0.40 exposed / 0.20–0.40 equivocal
- pLDDT ≥70 required for any burial conclusion
- Hard stop if residue 1002 in the model is not ASN (it is ASN — passed)
- gnomAD popmax AF >0.001 or ClinVar B/LB ≥2-star → stop (neither triggered)

**Assumptions**
- UniProt O60566 numbering ≡ NM_001211.6 / NP_001202.5 protein numbering — **verified** at 6 positions (737, 844, 909, 921, 1002, 1012).
- Human L1012 ≡ mouse L1002. The patient variant is **human N1002K** and is a different residue from the mouse L1002P / human L1012P literature allele. Kept distinct throughout.
- Human BUBR1 is a **pseudokinase** (no phosphotransfer activity). UniProt's "Active site 882" is annotated by similarity and is **not** evidence of catalysis.
- H-bonds called on heavy-atom geometry only (AlphaFold models contain no hydrogens).

**Scripts created**
- `analysis/scripts/step4_structure_gate.py` — numbering gate, pLDDT, Shrake-Rupley RSA, benchmark panel, pre-registered verdict → `step4_results.json`
- `analysis/scripts/step5_contacts.py` — per-atom SASA of N1002, 4 Å contact map, H-bond inventory
- `analysis/scripts/step6_conservation.py` — Compara alignment parsing, cross-species residue table

---

# Round 3 — Provenance, phase, structural network, and final gating

All work below executed **2026-09-15**. Scripts in `analysis/scripts/`.

> **HEADLINE CHANGE OF PRIORITY.** The highest-priority unresolved issue is **not
> phase**. It is **variant provenance**: the repository contains no documented
> pipeline step that produces c.2210T>G or c.3006T>G from the provided VCF, and the
> documented extraction command **cannot** have returned either variant in either
> genome build. Phase is the *second* question; provenance must be settled first.

---

## R3.1 — Variant provenance and a genome-build collision (NEW, CRITICAL)

> **✅ RESOLVED 2026-09-16 — see §R3.11.** The build collision documented below is
> **confirmed real** (the VCF is GRCh38; the documented window is the GRCh37
> *BUB1B* locus and returns variants in *IVD*/*BAHD1*/a lncRNA). However, direct
> verification against the gated proband VCF shows **both variants of interest ARE
> present** in the proband (PASS, 0/1, GQ 99). **Provenance is therefore RESOLVED
> POSITIVELY.** The "BLOCKING" status asserted below no longer applies to the two
> Track 2 variants; it still applies to the original Track 1 frameshift pair.

### Observed facts

`MVA_Hackathon_2026_Track1_METHODS.md` states the analysis uses **GRCh38**
(lines 246, 251, 1083, 1120) and documents exactly one extraction command (line ~280):

```bash
bcftools view -r 15:40400000-40500000 \
  WGS_EX2312012_HGWCNDSX7.vcf.gz -o bub1b_region.vcf
```

Authoritative gene coordinates (Ensembl REST, retrieved 2026-09-15):

| Build | BUB1B span | Overlap with window 40,400,000–40,500,000 |
|---|---|---|
| **GRCh38** (`rest.ensembl.org`) | chr15:**40,160,984–40,221,137** | **0 bp — NO OVERLAP** |
| **GRCh37** (`grch37.rest.ensembl.org`) | chr15:**40,453,224–40,513,337** | 46,770 bp — overlaps |

Genes actually located at **GRCh38** chr15:40,400,000–40,500,000 (Ensembl overlap
API): **IVD, BAHD1, CHST14** and several lncRNAs. **BUB1B is not among them.**

### The extraction window misses BOTH patient variants in BOTH builds

Coordinates from dbSNP (authoritative, retrieved 2026-09-15):

| Variant | rsID | GRCh38 (NC_000015.10) | GRCh37 (NC_000015.9) | In window? |
|---|---|---|---|---|
| c.2210T>G p.Leu737* | rs759242053 | 40,209,701 | **40,501,902** | **No** (GRCh38 far below; GRCh37 exceeds 40,500,000 by 1,902 bp) |
| c.3006T>G p.Asn1002Lys | rs2542593804 | 40,220,612 | **40,512,813** | **No** (GRCh38 far below; GRCh37 exceeds window by 12,813 bp) |

**Conclusion (ESTABLISHED):** the documented `bcftools -r 15:40400000-40500000`
extraction **could not have returned either patient variant under either genome
build.** The two variants now under analysis are therefore **undocumented in the
repository's pipeline** — there is no recorded step showing they were observed in
`WGS_EX2312012_HGWCNDSX7.vcf.gz`.

### The Track 1 candidates are not two BUB1B variants either

Gene assignment of the three Track 1 candidates (Ensembl overlap API, both builds):

| Position | Gene in GRCh38 | Gene in GRCh37 |
|---|---|---|
| chr15:40,425,440 (C>CTATA) | **IVD** | *no gene* |
| chr15:40,488,950 (C>CA) | ENSG00000259536 (lncRNA) | **BUB1B** |
| chr15:40,447,560 (GAATAAATA>G) | **BAHD1** | *no gene* |

**Only one** of the three is in BUB1B, and **only under a GRCh37 interpretation**.
The claim in `kavya5cloud_bub1b-compound-het-frameshift.csv` and in `README.md`
of a "compound heterozygous frameshift" pair **in BUB1B** is therefore **not
supported by the coordinates as recorded**.

### Repository inconsistency (observed fact)

| Artefact | Variants asserted | Status |
|---|---|---|
| `README.md` "Key Findings" | chr15:40,425,440 C>CTATA + chr15:40,488,950 C>CA | contradicts current analysis |
| `kavya5cloud_bub1b-compound-het-frameshift.csv` | same two | contradicts current analysis |
| `kavya5cloud_submission3_bub1b_compoundhet.csv` | chr15:40,209,701 T>G + chr15:40,220,612 T>G | current analysis; **undocumented provenance** |
| `MVA_Hackathon_2026_Track1_METHODS.md` | documents only the first pair | does not mention the second pair |

**Both submission CSVs additionally assert `"compound heterozygous"` in their
`notes` field with `epcr = 0.95`, while §27.3 of the methods document explicitly
states phase was never established.** These are mutually inconsistent.

### Required action (BLOCKING)

1. Re-extract using the **correct GRCh38 interval** for BUB1B, with margin:
   `bcftools view -r chr15:40160000-40222000` (or `15:...` depending on the VCF's
   contig naming — check with `bcftools view -h | grep contig | head`).
2. **Confirm the VCF's genome build** from its header (`##reference`, `##contig`
   lengths) before trusting any coordinate. Contig length chr15 = 102,531,392
   (GRCh38) vs 102,531,392… — use the `##reference` line and assembly-specific
   contig lengths, not assumption.
3. Confirm that c.2210T>G and c.3006T>G are actually present, with genotype `0/1`
   each, in the proband's VCF, and record the GT/DP/GQ/AD fields.
4. Until step 3 is done, **neither variant may be described as a patient variant.**

*Tier 1 (direct inspection of repository artefacts + authoritative coordinate
databases). This section supersedes the implicit assumption in Rounds 1–2 that
the two variants were established patient genotypes.*

---

## R3.2 — Phase / compound-heterozygosity analysis

### R3.2.1 Can the existing dataset establish phase? **NO.**

The provided data is a **single-sample WGS VCF** (`WGS_EX2312012_HGWCNDSX7.vcf.gz`,
315 MB + tabix index). Documented facts from the methods file: no parental samples
are described anywhere; raw FASTQ (~85 GB) exists in the gated dataset but was
deliberately **not** downloaded (line 229); genotypes are recorded as unphased
`0/1` (line 370, 463–465).

A `0/1` genotype carries **no phase information**. Unless the VCF contains
`|`-delimited phased genotypes with a shared `PS` (phase set) tag, phase cannot be
read out. **This must be checked before anything else:**

```bash
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t[%GT\t%PS\t%DP\t%GQ]\n' \
  -r chr15:40160000-40222000 WGS_EX2312012_HGWCNDSX7.vcf.gz
```
If `GT` shows `0/1` (slash) or `PS` is absent → **phase UNKNOWN from the VCF.**

### R3.2.2 Read-backed phasing: **NOT POSSIBLE with short reads.**

Distance between the two variants: **40,220,612 − 40,209,701 = 10,911 bp.**

The dataset is Illumina short-read WGS (filename `..._HGWCNDSX7` = NovaSeq S4
flowcell). Typical PCR-free short-read libraries have insert sizes of ~350–550 bp.
Even generous 1 kb inserts fall **more than an order of magnitude short** of the
10.9 kb separation. There is **no realistic probability** of a read pair or
fragment spanning both sites.

**Therefore read-backed phasing (WhatsHap, HapCUT2) on the existing short-read
data cannot resolve this pair.** This is a hard physical limitation, not a
software choice. *(Tier 1 — arithmetic on authoritative coordinates.)*

A partial workaround exists but is not guaranteed: **statistical/population
phasing** (SHAPEIT5, Beagle) using common heterozygous SNPs across the 10.9 kb
interval as a scaffold. Both variants are ultra-rare (AF 6.2e-7 and 7.9e-5) and
therefore absent from reference panels, so they can only be phased *onto* a
scaffold haplotype, with no direct panel support. **Population phasing of
ultra-rare variants is unreliable and is NOT an acceptable basis for a clinical
compound-het call.** It may be used as weak supporting evidence only.

### R3.2.3 Parental genotyping: **SUFFICIENT, and the cheapest definitive route.**

Under a standard autosomal-recessive model, trio Sanger sequencing of the two
sites resolves phase definitively in the informative case:

*(Hypothetical outcomes. No trio data exist for this proband; nothing in this
table has been observed.)*

| Father (hypothetical) | Mother (hypothetical) | Proband | Inference **if** observed |
|---|---|---|---|
| L737* het, N1002K ref | L737* ref, N1002K het | both het | *trans* configuration would be established |
| both variants in same parent | other parent ref/ref | both het | *cis* configuration would be established; N1002K would not be the second allele |
| neither parent carries one variant | — | proband het | ***de novo*** — phase still needs read-backed/long-read confirmation |

**Caveats that must be stated:** parental testing assumes correct stated
parentage (confirm with a SNP identity panel) and can be confounded by parental
germline mosaicism or by a *de novo* event. Non-paternity or a *de novo* variant
converts this from definitive to inconclusive.

### R3.2.4 Long-read sequencing: **DEFINITIVE, and works on the proband alone.**

PacBio HiFi or ONT reads routinely exceed 15–20 kb, comfortably spanning 10.9 kb.
A single proband HiFi genome (or targeted adaptive-sampling / amplicon of the
BUB1B locus) phases both variants directly onto the same or opposite haplotypes,
**without requiring parental samples** — which matters if parents are unavailable,
deceased, or parentage is uncertain. This is the preferred route when trio samples
cannot be obtained.

### R3.2.5 Linked-read (10x Genomics Chromium) data: **would work in principle, but the platform is discontinued.**

Linked reads generate barcoded molecules of ~50–100 kb and would readily span
10.9 kb. However, 10x Genomics **discontinued** the Chromium Genome/linked-read
product, so this is not a practical option for new sample generation in 2026. It
remains valid only if such data already exists for this proband. Contemporary
equivalents are long reads (R3.2.4) or **Hi-C / Pore-C**-based phasing, which can
phase across megabases from a single sample.

### R3.2.6 Evidence threshold before writing "compound heterozygous"

Adopt this **pre-registered** standard. ANY ONE of the following is sufficient:

- **(T1)** Trio genotyping showing each variant inherited from a different parent, with confirmed parentage; **or**
- **(T2)** Long-read (HiFi/ONT) data with ≥5 independent reads spanning both positions, ≥90% of informative reads assigning the two alternate alleles to **opposite** haplotypes, within a single phase block; **or**
- **(T3)** An equivalent orthogonal molecular demonstration of trans configuration (e.g. allele-specific long-range PCR across 10.9 kb followed by sequencing of the amplicon, showing the two alternate alleles never co-occur on one molecule).

**Not sufficient:** population/statistical phasing alone; short-read read-backed
phasing (physically impossible here); ACMG PM3 reasoning from the literature;
"both variants are het so they are probably in trans"; the fact that the phenotype
matches MVA.

### R3.2.7 Exact wording to use while phase is unresolved

> The proband carries two heterozygous *BUB1B* variants, NM_001211.6:c.2210T>G
> (p.Leu737\*) and NM_001211.6:c.3006T>G (p.Asn1002Lys). **Phase has not been
> determined.** The available data are single-sample short-read WGS, in which the
> two variants are separated by 10,911 bp — a distance that cannot be spanned by
> short-read fragments — and no parental samples were available. These variants are
> therefore reported as **two heterozygous variants of interest in a
> recessive-model candidate gene**, and **not** as a confirmed compound-heterozygous
> genotype. Determination of phase by trio genotyping or long-read sequencing is
> required before a biallelic interpretation can be made.

**Permitted short forms:** "two heterozygous *BUB1B* variants, phase undetermined";
"candidate biallelic configuration, unconfirmed". 
**Forbidden:** "compound heterozygous", "biallelic", "in trans", "recessive
diagnosis confirmed" — until T1, T2 or T3 is met.

---

## R3.3 — Deep structural analysis of N1002 (Task 3)

**Script:** `analysis/scripts/step9_structural_network.py`. Structure
AF-O60566-F1-model_v6.pdb; orthologue residues from `analysis/data/homol.json`.

### R3.3.1 The MVA missense positions do NOT form one cluster

Pairwise minimum heavy-atom distances (Å):

| | R727C | R814H | L844F | I909T | Q921H | N1002K | L1012P |
|---|---|---|---|---|---|---|---|
| **R727C** | – | 12.4 | 20.9 | 12.1 | **4.8** | 25.6 | 18.9 |
| **R814H** | 12.4 | – | 24.3 | 14.2 | **7.9** | 24.3 | 14.7 |
| **L844F** | 20.9 | 24.3 | – | 9.4 | 23.9 | 20.4 | 14.3 |
| **I909T** | 12.1 | 14.2 | 9.4 | – | 14.5 | 19.7 | 10.1 |
| **Q921H** | **4.8** | **7.9** | 23.9 | 14.5 | – | 24.0 | 18.0 |
| **N1002K** | 25.6 | 24.3 | 20.4 | 19.7 | 24.0 | – | **10.3** |
| **L1012P** | 18.9 | 14.7 | 14.3 | 10.1 | 18.0 | **10.3** | – |

Only two pairs are within contact range (<8 Å): **R727–Q921 (4.8 Å)** and
**R814–Q921 (7.9 Å)**. **N1002 is ≥19.7 Å from every MVA position except L1012
(10.3 Å)** — and even that is not a contact.

**Interpretation (SUPPORTED, Tier 3):** the MVA missense alleles occupy at least
two distinct structural neighbourhoods. N1002 sits in a **C-terminal
neighbourhood** with L1012, spatially separate from the R727/R814/Q921 group.
There is **no single "MVA hotspot"** onto which N1002K can be mapped by proximity.

### R3.3.2 N1002 is the MOST DISTANT MVA position from the nucleotide pocket

Minimum heavy-atom distance to reference sites (Å):

| variant | K795 (ATP, UniProt) | D882 (UniProt "active site", *by similarity*) | D911 (tested, PMID 33207204) |
|---|---|---|---|
| R727C | 7.9 | 9.3 | 8.2 |
| R814H | 17.2 | 15.8 | 15.2 |
| L844F | 14.6 | 9.9 | 11.0 |
| I909T | 8.9 | 6.7 | **4.1** |
| Q921H | 13.3 | 12.0 | 12.5 |
| **N1002K** | **28.6** | **18.4** | **23.4** |
| L1012P | 21.0 | 13.2 | 15.9 |

**ESTABLISHED (from the model):** N1002 is **28.6 Å from K795** and **18.4 Å from
D882** — the furthest of all seven positions from the degenerate nucleotide pocket.

**This formally excludes any ATP-pocket / pseudo-catalytic interpretation of
N1002K.** Restating the standing caution: human BUBR1 is a **pseudokinase** with
no phosphotransfer activity (PMID 33207204); UniProt's "Active site 882" is
annotated **by similarity only**. Residue 1002 is neither catalytic nor
nucleotide-binding, and must never be described as such.

### R3.3.3 N1002 sits in a conserved micro-core inside a variable surround

Contact shell (≤4.5 Å, any atom) with cross-species identity
(chimp/mouse/rat/dog/chicken/*Xenopus*):

| pos | aa | dist (Å) | pLDDT | orthologues | identity |
|---|---|---|---|---|---|
| 973 | W | 4.36 | 87.0 | W W W W Q Q | 4/6 |
| 977 | F | 3.46 | 87.4 | L L L V V | **1/6** |
| **978** | **W** | **2.83** | 88.4 | W W W W W W | **6/6** |
| 998 | V | 2.83 | 92.2 | V V V V R T | 4/6 |
| 999 | R | 3.62 | 93.8 | R R Q R Q K | 3/6 |
| **1000** | **I** | 3.33 | 93.8 | I I I I I I | **6/6** |
| **1001** | **L** | 1.34 | 91.6 | L L L L L L | **6/6** |
| **1003** | **A** | 1.34 | 88.0 | A A A A A A | **6/6** |
| 1004 | N | 3.14 | 80.4 | S S S D E | **1/6** |
| **1002** | **N** | — | 91.1 | N N N N N N | **6/6** |

**Observed fact:** a contiguous invariant micro-core — **W978 · I1000 · L1001 ·
N1002 · A1003** (all 6/6) — is embedded in a surround that tolerates substitution
(F977 1/6, N1004 1/6). Selection is acting sharply on this specific set of
residues, not on the region generally.

**Important nuance:** the two H-bond acceptors N1002 engages are **main-chain**
atoms of W978 and V998. Main-chain H-bonding does not require side-chain identity,
so V998's divergence in chicken/*Xenopus* (V→R/T) does **not** break the N1002
interaction. This strengthens rather than weakens the network argument.

### R3.3.4 N1002 is a buried helix C-cap — the key structural finding

Secondary structure (pydssp on the same model), residues 975–1015:

```
pos   975    980    985    990    995   1000   1005   1010   1015
       - - - E E E - - - H H H - - - H H H H H H H H H H H H - - - - - - H H H H H H H H
                 ^strand 978-980        ^------- helix 990-1001 -------^      ^helix 1008-1015
                                                              N1002 -^
```

- β-strand **978–980**
- α-helix **990–1001**
- loop **1002–1007**  ← **N1002 is the FIRST residue of this loop**
- α-helix **1008–1015**

**N1002 is the residue immediately C-terminal to helix 990–1001 — the C′ position
of a helix C-cap.** Its hydrogen bonds are exactly the capping geometry:

- **ND2 → V998 backbone O (2.83 Å)** — V998 is at *i*−4, i.e. the last turn of the helix. Its carbonyl has no *i*+4 backbone partner at the helix terminus; N1002's amide satisfies it. **This is the canonical Asn C-cap hydrogen bond.**
- **ND2 → W978 backbone O (2.95 Å)** and **OD1 ← W978 backbone N (2.83 Å)** — a reciprocal pair that **staples the helix C-terminus to the β-strand 978–980.**

Asn is statistically the most favoured residue at helix C-caps precisely because
its short amide can substitute for backbone hydrogen bonding. **Lysine cannot
perform this role:** NZ is a donor only (cannot accept from W978 N), it is longer
and conformationally flexible, and it carries a formal positive charge into a
position with zero solvent exposure (ND2 SASA = 0.00 Å²) packed against W973/F977/W978.

### R3.3.5 This resolves the ΔΔG / conservation paradox

The apparent contradiction in Round 2 — buried H-bonded residue + phyloP 4.80 +
AlphaMissense 0.92, but calibrated DynaMut2 ΔΔG = −0.01 — is **explained, not
explained away**, by the capping geometry:

> Helix capping is a **local geometric** constraint governing loop conformation
> and the register of an adjacent secondary-structure element. ΔΔG predictors are
> trained on **global unfolding free energies** (ΔΔG of denaturation) and
> systematically under-weight capping and loop-geometry losses, which can perturb
> local architecture while leaving the folded-state free energy of the domain
> essentially unchanged.

**Prediction that follows, and that is testable:** N1002K should show
**WT-like abundance and WT-like half-life** (consistent with DynaMut2) while
perturbing the **conformation of the 1002–1007 loop and the position of helix
1008–1015**. Since the pseudokinase domain acts **allosterically** on KARD
phosphorylation (PMID 33207204), a local conformational change is a coherent —
though **unproven** — route to functional loss without abundance loss.

**Status: HYPOTHESIZED (Tier 3).** This is an interpretation of a *predicted*
structure. It is not experimental evidence, and it must be tested (R3.5, Exp 2/3/7).

---

## R3.4 — Search for direct functional evidence on N1002K (Task 5)

All queries run 2026-09-15.

| Resource | Query | Result |
|---|---|---|
| PubMed / web | `BUB1B N1002K`, `Asn1002`, `c.3006T>G`, `rs2542593804` | **No publication reports this variant.** Results returned only general MVA1/BUB1B reviews and the known destabilised alleles. |
| ClinVar | exact allele `c.3006T>G` | **0 records** (BUB1B total: 2,093 records) |
| ClinVar | `c.3006T>A` (p.Asn1002Lys) | VCV004600147, VUS, 1-star — **different nucleotide allele, not transferable** |
| **MaveDB** | score-set search `BUB1B` | **`{"detail":"Not Found"}` — no deep mutational scan of BUB1B exists.** No MAVE functional score is available for any BUB1B residue. |
| Ensembl variation | chr15:40,220,610–40,220,615 | rs1222026369 (40220613, G>A, missense, VUS — this is c.3007G>A / A1003T); rs2037887083 (40220614, missense); rs2037887147 (40220615, synonymous). **Ensembl's variation track did not return rs2542593804 at 40220612**, although dbSNP does — a database-lag discrepancy, recorded. |
| LOVD | — | **ACCESS LIMITATION persists** (IP/network block). No bypass attempted. Status **UNKNOWN**, not negative. |

**Failed query (recorded):** ClinVar codon-level searches of the form
`BUB1B[gene] AND "p.*1012"` returned 0 for every codon including 1012, where
records are known to exist. **The query syntax is invalid; those zeros are
artefacts and carry no information.** They are not reported as results.

### Conclusion for Task 5

> **There is NO direct functional evidence of any kind for BUB1B p.Asn1002Lys.**
> No publication, no functional assay, no abundance measurement, no localization
> data, no checkpoint assay, no interaction data, and no deep mutational scan.
> Every mechanistic statement about N1002K in this report is therefore either
> computational prediction (Tier 3) or extrapolation from *other* BUB1B variants
> (explicitly flagged as such).

Per rule 15: **absence from these databases is UNKNOWN, not evidence of benignity.**

### Evidence from other BUB1B variants — applicability to N1002K

| Variant | Evidence | System | Applicable to N1002K? |
|---|---|---|---|
| I909T | ↑turnover ~2×, HSP90/proteasome-sensitive; **function fully restored by re-expression** (PMID 20516114) | U2OS, LAP-tagged | **NO** — different residue, different structural context (4.1 Å from D911, N1002 is 23.4 Å), and DynaMut2 separates them (−3.48 vs −0.01) |
| L1012P | ↓abundance, ↑degradation, rescued by re-expression (PMID 20516114) | U2OS | **NO** — nearest MVA position (10.3 Å) but not in contact; proline substitution in a buried position is a categorically different perturbation from an Asn→Lys cap loss |
| L844F | ↓abundance **plus a residual defect after re-expression** (PMID 20516114) | U2OS | **NO** — 20.4 Å away; but it is the precedent that abundance rescue can be insufficient |
| Q921H | stable, functionally **indistinguishable from WT** (PMID 20516114) | U2OS | **NO** — 24.0 Å away; relevant only as the ΔΔG calibration negative control |
| K795R, D882A, S884A, D911A, S913A, 731X | all ↓KARD pS670/pS676 and ↓kinetochore PP2A-B56 (PMID 33207204) | HeLa/RPE1 | **Indirectly** — establishes that the pseudokinase domain acts allosterically and that **abundance and allosteric function are dissociable** (hyperstable 731X and unstable DKD both lose pKARD). Does **not** implicate residue 1002. |

**Human/mouse numbering collision — resolved and restated:** human **L1012** ≡
mouse **L1002**. The patient variant is **human N1002K**, a *different residue*
from the mouse L1002P / human L1012P literature allele. No mouse L1002P evidence
is transferred to human N1002K anywhere in this report.

---

## R3.5 — Mechanism hypothesis matrix for a stable N1002K (Task 2)

| # | Hypothesis | Supporting evidence | Contradictory evidence | Confidence | Falsification experiment | Druggable target? |
|---|---|---|---|---|---|---|
| **A** | **Reduced abundance / destabilisation** | Burial (RSA 0.162); 3 H-bonds lost; precedent in I909T/L1012P/L844F | **Calibrated DynaMut2 = −0.01, clustering with the WT-like Q921H (4/4 controls correct)**; burial shallower than L1012/L844/I909 | **LOW** (actively disfavoured) | Exp 2+3: immunoblot + CHX chase vs WT | Would reopen proteostasis search — **currently closed** |
| **G→A** | **Local structural / helix-cap-loss defect with normal global stability** | N1002 is the C′ helix C-cap of helix 990–1001; ND2→V998 O is canonical capping geometry; invariant micro-core W978·I1000·L1001·N1002·A1003; Lys cannot accept H-bonds or tolerate burial of charge; **reconciles neutral ΔΔG with phyloP 4.80 / AlphaMissense 0.92** | Entirely computational, on a **predicted** structure; no experimental support; no BUBR1 capping mutant has ever been characterised | **MEDIUM** (leading hypothesis) | Exp 10: purified 766–1050 WT vs N1002K — nanoDSF Tm **and** limited proteolysis / HDX. Cap loss predicts **ΔTm ≈ 0 but altered protease susceptibility / HDX in the 998–1015 segment** | No — not directly actionable |
| **D** | **Reduced KARD S670/S676 phosphorylation → ↓kinetochore PP2A-B56, via allostery** | Pseudokinase domain demonstrably promotes KARD phosphorylation allosterically (PMID 33207204); every tested domain perturbation reduced pKARD; **abundance and pKARD are dissociable** (731X hyperstable yet pKARD-low) | N1002 is 51–85 Å from the KARD; no direct contact; residue 1002 was never tested in that study | **MEDIUM** (leading downstream readout) | Exp 7: phospho-S670/S676 immunoblot + kinetochore IF, and B56 kinetochore intensity, with WT-matched expression | Weakly — PLK1/CDK1 modulation is unsafe in a chromosome-instability disorder |
| **E** | **SAC weakness despite normal abundance** | MVA phenotype requires a segregation defect; L844F precedent shows abundance rescue can be insufficient | No N1002K data; SAC could equally be intact with only an alignment defect | **MEDIUM-LOW** | Exp 6: nocodazole mitotic index + time-lapse mitotic duration at WT-matched expression | No — generic SAC modulation is explicitly excluded |
| **C** | **Altered interaction with a non-PP2A partner** (BUB3, BUB1, CDC20, PLK1, KNL1) | N1002 is surface-adjacent within the C-lobe; pseudokinase domains commonly serve as scaffolds | **N1002's amide is fully buried (ND2 SASA 0.00 Å²)** — it is not on an accessible interface; no partner is known to bind this face | **LOW** | Exp 8: BUBR1 IP-MS, WT vs N1002K, quantitative | Only if a specific node emerged |
| **F** | **Altered kinetochore localization** | Any folding/scaffolding perturbation could affect recruitment | Kinetochore targeting maps to the N-terminal TPR/KEN/Bub3-binding regions, ~800 residues away — not to the pseudokinase domain | **LOW** | Exp 5: BUBR1 kinetochore IF intensity vs CREST | No |
| **B** | **Altered intramolecular autoregulation** | Pseudokinase domains can regulate in *cis*; N1002 is 18–29 Å from the degenerate pocket | No evidence of any intramolecular regulatory contact involving 1002; purely speculative | **LOW** | Exp 8/10: HDX-MS comparing WT vs mutant across the full-length protein | No |
| **G** | **Altered protein dynamics without static structural change** | Loop 1002–1007 conformational freedom would rise on losing the cap; ΔΔG-neutral is consistent | Untested; MD was **not** performed in this work (stated limitation) | **LOW-MEDIUM** | MD simulation (not performed here) + HDX-MS of 995–1015 | No |
| **H(=D-alt)** | **Incidental / not the second pathogenic allele** | No functional evidence exists; ClinVar has no record; phase unestablished; **provenance unestablished (R3.1)** | phyloP 4.80, phastCons 1.00, invariant to *Xenopus*, AlphaMissense 0.9229, AF 6.2e-7 | **LOW-MEDIUM — cannot be excluded** | Exp 1: phase determination. *cis* → this hypothesis becomes leading | n/a |

**Standing constraint:** every entry above rated MEDIUM or below rests on
computational prediction. **None of these is an established biological fact.**

---

## R3.6 — BUBR1 functional network and where a stable N1002K could act (Task 4)

Evidence stratified as required.

### DIRECTLY DEMONSTRATED (primary literature, human cells)
- BUBR1 is a core **MCC** component (with BUB3, CDC20, MAD2) that inhibits **APC/C^CDC20** toward cyclin B1 and securin. *(reviewed; PMID 21159489)*
- **PP2A-B56 is recruited via the KARD** (S670/S676, phosphorylated by PLK1/CDK1) — **not** via the pseudokinase domain. *(PMID 33207204)*
- The **pseudokinase domain promotes KARD phosphorylation allosterically**; K795R, D882A, S884A, D911A, S913A and 731X all reduce pS670/pS676 and kinetochore PP2A-B56, causing attenuated SAC silencing and chromosome-alignment errors. *(PMID 33207204)*
- **Human BUBR1 has no phosphotransfer activity** — it is a pseudokinase. *(PMID 33207204)*
- **Abundance and allosteric function are dissociable:** hyperstable 731X and unstable DKD both lose KARD phosphorylation. *(PMID 33207204)*
- Certain MVA missense alleles (**I909T, L1012P**) lower abundance via HSP90/proteasome-dependent turnover, and **forced re-expression to WT levels fully restores function**. *(PMID 20516114)*
- **L844F** retains a functional defect even after abundance rescue. *(PMID 20516114)*
- **Q921H** is stable and functionally indistinguishable from WT. *(PMID 20516114)*
- Biallelic *BUB1B* LoF causes **MVA syndrome 1** (MIM 257300), with mosaic aneuploidy and cancer predisposition.

### STRONGLY SUPPORTED
- BUBR1 hypomorphism → weakened SAC and/or impaired kinetochore–microtubule error correction → **missegregation → mosaic aneuploidy**, the MVA phenotype.
- **Leu737\*** removes the entire pseudokinase domain (766–1050) and the C-terminus; if the transcript escapes NMD, the product would resemble the 731X truncation shown to lose KARD phosphorylation.

### PLAUSIBLE
- A **stable** N1002K perturbs the C-lobe locally (helix-cap loss, R3.3.4), degrading the domain's allosteric support for KARD phosphorylation → reduced kinetochore PP2A-B56 → impaired SAC silencing and chromosome alignment. **This is the single most coherent route by which a normally abundant N1002K could cause MVA**, and it is the model the experimental plan is built to test.
- CHIP/STUB1 or CDC37 participation in BUBR1 quality control (**no BUBR1-specific demonstration exists**).

### SPECULATIVE
- N1002K altering a specific protein–protein interface (contradicted by ND2 SASA = 0.00 Å²).
- N1002K affecting kinetochore targeting (maps to the N-terminus, ~800 residues away).
- Any intramolecular autoregulatory role for residue 1002.

### Where a stable N1002K could plausibly disrupt the pathway

```
BUB1B (N1002K, stable, normal abundance)
        │
        ▼  [PLAUSIBLE — helix-cap loss perturbs C-lobe loop 1002-1007]
pseudokinase domain 766-1050 local conformation
        │
        ▼  [DIRECTLY DEMONSTRATED that this link exists for other domain perturbations]
allosteric promotion of KARD S670/S676 phosphorylation (PLK1/CDK1)
        │
        ▼  [DIRECTLY DEMONSTRATED]
kinetochore PP2A-B56 recruitment
        │
        ▼  [DIRECTLY DEMONSTRATED]
SAC silencing + kinetochore-microtubule error correction
        │
        ▼  [STRONGLY SUPPORTED]
chromosome missegregation -> mosaic variegated aneuploidy
```

**The weak link is the first arrow**, and it is the one with no experimental
support. Experiment 7 tests it directly.

---

## R3.7 — Experimental priority table (Task 6)

Cell system throughout: **hTERT-RPE1** (near-diploid, checkpoint-proficient) with
siRNA/CRISPRi depletion of endogenous BUBR1 and doxycycline-tunable, siRNA-resistant
LAP/GFP-tagged transgenes. **Controls on every plate: WT (normal), L1012P
(destabilised positive control), Q921H (stable/WT-like negative control), empty
vector.** Expression must be **titrated to WT-matched levels** before any functional
readout, or abundance and function are confounded.

| Pri | # | Experiment | Assay | Expected under A (destabilised) | Expected under G→A/D (stable, local defect) | Expected under H (incidental) | Falsification criterion | Cost | Time |
|---|---|---|---|---|---|---|---|---|---|
| **0** | **0** | **Variant provenance** (R3.1) | Re-extract GRCh38 chr15:40,160,000–40,222,000 from the proband VCF; confirm build from header; record GT/DP/GQ/AD | variants present, 0/1 | variants present, 0/1 | — | **Variants absent → the entire analysis is void** | ~£0 | hours |
| **1** | **1** | **Phase determination** | Trio Sanger (T1) **or** proband PacBio HiFi / targeted long-read (T2) | *trans* | *trans* | ***cis*** | ***cis* → N1002K is not the second allele; H becomes leading** | £–££ | 1–3 wk |
| **2** | **2** | **Steady-state abundance** | Quantitative immunoblot (LI-COR), n≥3, vs WT | **reduced**, like L1012P | **WT-like**, like Q921H | WT-like | **Reduced → A revives, drug gate may reopen** | £ | 1 wk |
| **2** | **3** | **Protein half-life** | Cycloheximide chase 0–8 h, densitometry | **t½ shortened** | **t½ = WT** | t½ = WT | **Shortened → A revives** | £ | 1 wk |
| **3** | **4** | **Proteasome / chaperone dependence** | MG132 rescue; low-dose short-exposure 17-AAG with an HSP90-client positive control **and** a mitotic-arrest control | selective rescue / selective loss | **no selective effect** | no effect | Selective MG132 rescue → A | £ | 1 wk |
| **3** | **6** | **SAC function** | Nocodazole mitotic index; live imaging of mitotic duration (NEBD→anaphase); alignment (metaphase plate width); missegregation rate | impaired (abundance-driven) | **impaired at WT-matched expression** | **WT-like** | **WT-like function at WT-matched abundance → N1002K may be incidental (H)** | ££ | 2–3 wk |
| **3** | **7** | **KARD phosphorylation & PP2A-B56** | phospho-S670 / phospho-S676 immunoblot **and** kinetochore IF; B56 kinetochore intensity vs CREST | reduced (secondary to low abundance) | **reduced at WT-matched abundance — the diagnostic result for D** | normal | **Normal pKARD + normal B56 at WT-matched abundance → D falsified** | ££ | 3–4 wk |
| **4** | **10** | **Biophysics of the isolated domain** | Purify 766–1050 WT vs N1002K: nanoDSF Tm, limited proteolysis, ideally HDX-MS of 990–1015 | **ΔTm ≪ 0** | **ΔTm ≈ 0 but altered proteolysis / HDX in 998–1015** — the direct test of the helix-cap model | ΔTm ≈ 0, no change | **ΔTm ≪ 0 → A revives; no local change → helix-cap model falsified** | ££ | 4–6 wk |
| **5** | **5** | **Localization** | BUBR1 kinetochore IF intensity vs CREST, prometaphase | reduced (low abundance) | WT-like | WT-like | Reduced at WT-matched abundance → F | £ | 1 wk |
| **5** | **8** | **Interactome** | BUBR1 IP-MS (BUB3, BUB1, CDC20, MAD2, B56 isoforms, PLK1), label-free quantitative | proportional loss | **selective loss of one node → identifies a specific target** | no change | No selective change → C falsified | £££ | 6–8 wk |
| **6** | **9** | **Patient-cell phenotype** | Patient PBMC/fibroblast karyotype or scKaryo-seq; % aneuploid cells | aneuploidy present | aneuploidy present | — | Confirms the disease phenotype; **does not discriminate hypotheses** | ££ | 2–4 wk |
| **6** | **11** | **Rescue with WT BUBR1** | Re-express WT in patient cells; re-measure Exp 9 | rescued | rescued | rescued | Rescue confirms *BUB1B*-attributable phenotype | ££ | 4 wk |

**Decision logic (pre-registered):**
- Exp 2 + 3 both normal, Exp 6 impaired → **hypothesis A FALSIFIED; abundance rescue is not a therapeutic route; G→A/D becomes leading.**
- Exp 2 reduced + Exp 3 shortened + Exp 4 MG132-rescued + function restored by re-expression → **A CONFIRMED; the proteostasis drug gate reopens.**
- Exp 2, 3 and 6 all WT-like → **reconsider H (incidental)**; Exp 1 becomes decisive.
- Exp 1 shows *cis* → **stop; N1002K is not the second pathogenic allele.**

---

## R3.8 — Therapeutic gate (Task 7): **CLOSED**

Applying the pre-registered gate:

| Gate condition | Required | Observed | Pass? |
|---|---|---|---|
| N1002K causes reduced abundance | experimental | **no data — never measured** | ✗ |
| Shortened half-life | experimental | **no data** | ✗ |
| Proteasome-dependent loss | experimental | **no data** | ✗ |
| Rescue by stabilisation demonstrated | experimental | **no data** | ✗ |
| *Alternatively:* a **precise** defective signalling node identified | experimental | **no data** — the KARD/PP2A-B56 route is PLAUSIBLE only, and residue 1002 was never tested | ✗ |
| *Alternatively:* only generic SAC dysfunction shown | — | not even this is demonstrated | n/a |

Additionally, and independently sufficient to keep the gate closed:

- **Mechanism is UNRESOLVED (C).** The leading hypothesis (helix-cap loss → altered local conformation → impaired allosteric KARD phosphorylation) is **entirely computational**.
- **No E3 ligase for misfolded BUBR1 has ever been identified**, so even under hypothesis A there is no defined molecular target for a degradation-blocking strategy.
- **Phase is undetermined** — it is not established that N1002K is a pathogenic allele in this patient at all.
- **Variant provenance is unestablished (R3.1)** — it is not established that the patient carries this variant as recorded.
- The one plausible node (PLK1/CDK1 → KARD phosphorylation) is **not safely druggable in the required direction**: PLK1 and CDK1 inhibitors *reduce* KARD phosphorylation, which would **worsen** the predicted defect, and both impair mitosis in a chromosome-instability disorder.

### **THERAPEUTIC CONCLUSION (final):**

> **No drug candidate is currently justified; experimental mechanism resolution is
> required before repurposing.**

---

## R3.9 — Drug repurposing (Task 8): **NOT PERFORMED — GATE CLOSED**

No drug search was conducted. No candidates are named, ranked, or scored.

Proposing any compound at this stage would require retrofitting a therapy to an
unsupported mechanism. The following remain **excluded** and their exclusion is
**not** overturned by anything found in this round: HSP90 inhibitors (would
*reduce* BUBR1), broad proteasome inhibitors (non-specific, mitotically toxic),
MPS1/TTK inhibitors, Aurora inhibitors, KIF11/Eg5 inhibitors, classical
antimitotics, and APC/C activators — every one of which would be expected to
**worsen** chromosome missegregation in a patient who already has MVA.

**Explicit condition to reopen:** Experiments 2 + 3 + 4 demonstrating reduced
abundance, shortened half-life and proteasome-dependent loss, **plus** Experiment
1 demonstrating *trans* configuration, **plus** Experiment 0 confirming the
variant is present in the proband. Until all four hold, the gate stays closed.

---

## R3.10 — Reproducibility audit (Task 9)

### Files that exist (verified 2026-09-16)

```
analysis/
├── round2_variant_characterisation.md      this document
├── environment.txt                         NEW - software versions + documented absences
├── scripts/
│   ├── step0_verify_provenance.py          NEW - BLOCKING provenance/build/phase check
│   ├── step4_structure_gate.py             pLDDT, Shrake-Rupley RSA, numbering gate
│   ├── step5_contacts.py                   per-atom SASA, 4 A contacts, H-bonds
│   ├── step6_conservation.py               Compara orthologue residue table
│   └── step9_structural_network.py         NEW - MVA clustering, contact shell, SS
└── data/
    ├── README.md                           provenance of the data artefacts
    ├── BUBR1_kinase_766_1050.pdb           domain model used for all ddG submissions
    ├── step4_results.json                  machine-readable Step 4 output
    └── homol.json                          raw Ensembl Compara response
```

### Gaps identified and closed in this round

| Gap | Action taken |
|---|---|
| No record of software versions | **`analysis/environment.txt` created**, including documented *absences* (mkdssp, FoldX, MD) |
| No script for the structural-network analysis | **`step9_structural_network.py` created** |
| No way to verify the variants came from the proband | **`step0_verify_provenance.py` created** — build inference from chr15 contig length, correct-interval extraction, GT/PS/DP/GQ/AD readout |
| ddG results not machine-readable | see table below — **still open** |

### Gaps identified and STILL OPEN (must be closed before submission)

| # | Gap | Required action |
|---|---|---|
| ~~1~~ | ✅ **CLOSED 2026-09-16** — `analysis/scripts/step5b_ddg_panel.sh` created, with endpoint, structure md5, sign convention, all five job IDs and the DDMut failure recorded. ~~No DynaMut2 script or raw response saved.~~ The five ddG values were obtained by ad-hoc `curl` and exist only in this Markdown. | Create `analysis/scripts/step5b_ddg_panel.sh` recording the exact submit/poll `curl` calls, and save raw JSON to `analysis/data/ddg_dynamut2_*.json`. Job IDs, for the record: N1002K `178949565796`, L1012P `178949566104`, I909T `178949566347`, Q921H `178949566629`, L844F `178949566886`. |
| ~~2~~ | ✅ **CLOSED 2026-09-16** — `analysis/scripts/step1_database_queries.sh` created, covering every endpoint used, saving raw responses to `analysis/data/queries/`, with known failures listed. | Create `analysis/scripts/step1_database_queries.sh` with every exact URL, and save raw responses to `analysis/data/`. |
| 3 | **Full-length AlphaFold model not committed** (691 KB). | Either commit it or rely on the documented MD5 `943e5596717db0424b1a020ae429e174` + retrieval command (currently the latter; acceptable). |
| ~~4~~ | ✅ **CLOSED 2026-09-16** — `README.md` rewritten with a status banner, verified-findings table and Track 1 Provenance Erratum. ~~factually stale~~ Its "Key Findings" table still asserts the chr15:40,425,440 / chr15:40,488,950 frameshift pair as BUB1B compound-het — contradicted by R3.1. | Rewrite `README.md`. Remove the compound-het claim; state the build issue and the unresolved provenance. |
| ~~5~~ | ✅ **ADDRESSED 2026-09-16** — CSVs left byte-for-byte unmodified by design (altering a scored submission destroys provenance); originals archived; correction documented in `analysis/TRACK1_SUBMISSION_ERRATUM.md`. ~~assert "compound heterozygous" with `epcr=0.95`** while §27.3 of the methods document states phase was never established. | Reword the `notes` field to the R3.2.7 approved wording. Reconsider whether `epcr=0.95` is defensible with provenance and phase both unresolved. |
| ~~6~~ | ✅ **CLOSED 2026-09-16** — §30 "Genome-Build / Provenance Erratum" appended; historical record left intact; HISTORICAL RECORD vs CORRECTED INTERPRETATION used throughout. | Add an erratum section; do not silently edit the historical record. |
| ~~7~~ | ✅ **CLOSED 2026-09-16** — `analysis/README.md` created with reading order and status banner. | Create one with a reading order and the current status banner. |
| 8 | Raw VCF and FASTQ are gated and not committed (`.gitignore` excludes `*.vcf*`). | Correct as-is; ensure `analysis/data/provenance/` output is committed once generated, since it is small and is the evidence of provenance. |

### Commands to reproduce this round

```bash
# Structure (v4 is retired; v6 is current)
curl -O https://alphafold.ebi.ac.uk/files/AF-O60566-F1-model_v6.pdb
md5 AF-O60566-F1-model_v6.pdb     # expect 943e5596717db0424b1a020ae429e174

python3 analysis/scripts/step4_structure_gate.py      AF-O60566-F1-model_v6.pdb
python3 analysis/scripts/step5_contacts.py            AF-O60566-F1-model_v6.pdb
python3 analysis/scripts/step6_conservation.py        analysis/data/homol.json
python3 analysis/scripts/step9_structural_network.py  AF-O60566-F1-model_v6.pdb analysis/data/homol.json

# BLOCKING - run against the gated proband VCF before trusting anything downstream
python3 analysis/scripts/step0_verify_provenance.py /path/to/WGS_EX2312012_HGWCNDSX7.vcf.gz
```

### Additional query provenance for Round 3

| Query | Endpoint | Result |
|---|---|---|
| BUB1B span GRCh38 | `rest.ensembl.org/lookup/symbol/homo_sapiens/BUB1B` | chr15:40,160,984–40,221,137 |
| BUB1B span GRCh37 | `grch37.rest.ensembl.org/lookup/symbol/homo_sapiens/BUB1B` | chr15:40,453,224–40,513,337 |
| chr15 length GRCh38 | `rest.ensembl.org/info/assembly/homo_sapiens/15` | 101,991,189 |
| chr15 length GRCh37 | `grch37.rest.ensembl.org/info/assembly/homo_sapiens/15` | 102,531,392 |
| Genes at GRCh38 15:40.4–40.5 Mb | `rest.ensembl.org/overlap/region/human/15:40400000-40500000?feature=gene` | IVD, BAHD1, CHST14 + lncRNAs (**no BUB1B**) |
| GRCh37 coords of both variants | NCBI dbSNP esummary, rs759242053 / rs2542593804 | 40,501,902 / 40,512,813 |
| MaveDB BUB1B score-sets | `api.mavedb.org/api/v1/search/score-sets` | `{"detail":"Not Found"}` — no DMS exists |

**Failed / invalid queries (recorded, not reported as results):**
- ClinVar codon searches `BUB1B[gene] AND "p.*NNNN"` returned 0 for all codons **including 1012, where records demonstrably exist** → the syntax is invalid and those zeros are artefacts.
- DDMut result endpoint: `Internal Server Error` on all polls (Round 2) — no values obtained.
- LOVD: IP/network block persists — status **UNKNOWN**, no bypass attempted.

---

## R3.11 — PROVENANCE RESOLVED (executed 2026-09-16)

`analysis/scripts/step0_verify_provenance.py` was run against the gated proband
VCF. **This supersedes the "BLOCKING / UNVERIFIED" status asserted in §R3.1 for
the two Track 2 variants.**

### Source file

| Item | Value |
|---|---|
| File | `WGS_EX2312012_HGWCNDSX7.vcf.gz` (gated dataset; local path not recorded. Two local copies were present and had identical md5.) |
| md5 | `a04ea354141cfb032872d67a11c8d2d8` |
| Size | 315,153,971 bytes |
| Sample | `WGS_EX2312012` |
| Caller | GATK 4.2.4.0 `VariantFiltration` (filters: QD2, MQ40, RPRS-8, FS60, MQRankSum-12.5) |
| bcftools | 1.24 |

### Build — GRCh38, confirmed by two independent header lines

- `##reference=file://refGenome/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta`
- `##contig=<ID=15,length=101991189>` → **GRCh38** (GRCh37 chr15 = 102,531,392)
- Contig naming: **no `chr` prefix**

### Both variants ARE present in the proband

| Variant | POS | REF>ALT | FILTER | GT | DP | GQ | AD | VAF | PGT | PID |
|---|---|---|---|---|---|---|---|---|---|---|
| c.2210T>G p.Leu737\* | 15:40,209,701 | T>G ✓ | PASS | 0/1 | 46 | 99 | 21,25 | 0.543 | `.` | `.` |
| c.3006T>G p.Asn1002Lys | 15:40,220,612 | T>G ✓ | PASS | 0/1 | 28 | 99 | 15,13 | 0.464 | `.` | `.` |

REF/ALT match expectation exactly; both `PASS`; GQ 99; adequate depth; clean
heterozygous allele balance. **Normalization is not at issue** — both are SNVs
(the indels elsewhere in the locus do not affect these records).

**→ Both variants are legitimately attributable to the proband. ESTABLISHED (Tier 1).**

### Phase — still UNKNOWN

Declared FORMAT tags: `AD, DP, GQ, GT, PGT, PID, PL`. **`PS` is not declared** —
GATK uses `PGT`/`PID` for physical phasing. Both variants have `PGT=.` and
`PID=.`, i.e. **no phasing group**, and both genotypes are `/`-delimited.

GATK physical phasing links only variants within a single read/fragment. The two
sites are **10,911 bp** apart, far beyond short-read reach (~350–550 bp). **Phase
remains UNDETERMINED**, exactly as analysed in §R3.2. Trio genotyping or long-read
sequencing is required.

### The Track 1 build error is confirmed real

Re-running the documented window on the actual VCF returns **36 variants** —
matching the methods document exactly — confirming the pipeline ran as written.
All three original candidates are present and `PASS`:

| Candidate | VCF record | GRCh38 gene | GRCh37 gene |
|---|---|---|---|
| 15:40,425,440 | `C>CTATA` PASS 0/1 DP 25 GQ 99 | **IVD** | *no gene* |
| 15:40,488,950 | `C>CA` PASS 0/1 DP 26 GQ 99 | lncRNA ENSG00000259536 | *BUB1B* |
| 15:40,447,560 | `GAATAAATA>G,GAATA` PASS 1/2 DP 41 GQ 99 | **BAHD1** | *no gene* |

**They are real proband variants in the wrong genes.** The original *BUB1B*
compound-heterozygous frameshift conclusion is **NOT SUPPORTED** — superseded by
`analysis/TRACK1_SUBMISSION_ERRATUM.md`.

### Correction to the verification script (recorded, not hidden)

The first revision of `step0_verify_provenance.py` queried `FORMAT/PS`
unconditionally. Because `PS` is undeclared in this VCF, `bcftools query` exited
255 (`Error: no such tag defined in the VCF header: FORMAT/PS`) with empty stdout,
and the script's helper returned `''`, which was misread as **"variant not
present"**. The first run therefore reported **both variants absent — a false
negative.** Diagnosed by re-querying without `%PS`.

**Fix:** the script now (i) parses `##FORMAT` IDs from the header and queries only
declared tags, (ii) surfaces `bcftools` stderr and exits loudly on non-zero return
instead of swallowing it, and (iii) records the input md5 and bcftools version.
All results above come from the corrected script.

### Artefacts written

```
analysis/data/provenance/
├── header_provenance.txt                  ##reference/##contig/GATK cmdline/sample
├── bub1b_region_GRCh38.vcf.gz (+ .tbi)    15 variants, correct GRCh38 BUB1B locus
├── bub1b_locus_variants.tsv               POS/REF/ALT/FILTER/GT/DP/GQ/AD
├── track1_window_GRCh38.tsv               the 36 variants from the erroneous window
├── README_original_pre-erratum.md         README.md as it stood before correction
├── kavya5cloud_bub1b-compound-het-frameshift_original.csv
└── kavya5cloud_submission3_bub1b_compoundhet_original.csv
```

### Effect on the scientific conclusions

| Conclusion | Change |
|---|---|
| Both variants attributable to the proband | **UNKNOWN → ESTABLISHED** |
| Phase | **UNKNOWN — unchanged** |
| Leu737\* pathogenicity | unchanged (ClinVar 2-star P/LP) |
| N1002K mechanism | **C — UNKNOWN — unchanged** |
| N1002K destabilisation | **NOT SUPPORTED — unchanged** |
| Direct PP2A-B56 disruption | **NOT SUPPORTED — unchanged** |
| Helix-cap / allosteric model | **HYPOTHESIS ONLY — unchanged** |
| Therapeutic gate | **CLOSED — unchanged** |

Provenance moving from UNKNOWN to ESTABLISHED **removes a blocker but adds no
mechanistic evidence.** The priority chain advances one step:
**PROVENANCE ✅ → PHASE ❌ → MECHANISM ❌ → TARGET ❌ → DRUG ❌.**

---

# Round 4 — Going WIDE: independent re-establishment of the candidate gene (2026-09-16)

Prompted by a PI audit flagging the project YELLOW: BUB1B mechanism work had gone
deep *before* the gene was independently re-established following the Track 1
genome-build error. This round tests the gene choice itself, **without using the
Track 1 extraction as evidence for anything**.

**Outcome: BUB1B survives. Decision matrix = CASE B (plausible but unresolved).**
See `analysis/data/DECISION_MATRIX.md`.

## R4.1 Phenotype — AVAILABLE (extracted, not invented)

8 HPO terms recorded in `MVA_Hackathon_2026_Track1_METHODS.md` §2.1, extracted
verbatim to `analysis/data/phenotype/PHENOTYPE.md`: Rhabdomyosarcoma HP:0002859,
Nephrocalcinosis HP:0000121, Short stature HP:0004322, Failure to thrive
HP:0001508, Skeletal muscle atrophy HP:0003202, Premature birth HP:0001622,
Small for gestational age HP:0001518, Recurrent spontaneous abortion HP:0200067.

**A `PHENOTYPE_MISSING.md` was therefore NOT created** — the brief specified that
file only if phenotype data were absent.

**Recorded honestly:** the HPO set contains **no term for mosaic aneuploidy,
variegated aneuploidy, PCS, or microcephaly**. The MVA diagnosis is *asserted* in
our Track 1 document, not *evidenced* by the HPO list available to us.

## R4.2 Gene panel — PanelApp, phenotype-derived (no invented genes)

| Source | Version | Retrieved | GREEN genes used |
|---|---|---|---|
| GE PanelApp **panel 290 "Familial rhabdomyosarcoma"** | v1.6 (2025-11-23) | 2026-09-16 | 11 |
| GE PanelApp **panel 259 "Childhood solid tumours cancer susceptibility"** | v1.30 (2025-10-13) | 2026-09-16 | 72 |
| MVA/mitotic set specified in the brief | — | — | 10 |
| | | **UNION** | **80** |

Panel 290 was chosen **because** the proband's HPO includes Rhabdomyosarcoma —
this is what makes the gene selection phenotype-driven rather than assumption-driven.
**BUB1B is GREEN (confidence 3), BIALLELIC on panel 290.**
PanelApp has no dedicated MVA panel (searched 2026-09-16); the MVA gene set is
labelled as brief-derived, not PanelApp-derived. `CCDC84` resolved to approved
symbol **CENATAC**. Script: `analysis/scripts/build_gene_panel.py`.

## R4.3 Genome-wide inventory

| Category | Count |
|---|---|
| PASS 0/1 | 2,847,564 |
| PASS 1/1 | 1,826,977 |
| PASS 1/2 (multiallelic) | 66,249 |
| non-PASS 0/1 | 199,513 |
| non-PASS 1/1 | 71,290 |
| non-PASS 1/2 | 611 |
| **Total** | **~5,012,204** |

Annotation: **snpEff 5.4c**, database **GRCh38.mane.1.2.refseq**, `-canon`,
GRCh38, contig naming `1..22,X,Y` (matches VCF). NM_001211.6 retained for BUB1B.
→ 11,320 PASS HIGH/MODERATE variants → **203 genes with an AR model**.

## R4.4 The decisive step — population frequency

**Critical methodological point.** The VCF's `INFO/AF` is GATK's per-sample allele
fraction (0.5 for a het), **not** a population frequency, and was never used as
one. Population AF came from Ensembl VEP REST (gnomAD), retrieved 2026-09-16.

**Of 43 qualifying panel variants, 40 were COMMON POLYMORPHISMS.** Sanity check:
TP53 p.Pro72Arg AF 0.748 (rs1042522), ERCC2 p.Asp312Asn AF 0.513, XPC p.Gln939Lys
AF 0.729 — all correctly classified common. Survivors:

| Gene | Variant | Zyg | Impact | gnomAD popmax AF | Class |
|---|---|---|---|---|---|
| **BUB1B** | 15:40209701 T>G `p.Leu737*` | HET | HIGH/pLoF | 9.98e-05 (rs759242053) | RARE |
| **BUB1B** | 15:40220612 T>G `p.Asn1002Lys` | HET | MODERATE | not returned by VEP | see note |
| ATM | 11:108271261 T>C `p.Ser978Pro` | HET | MODERATE | 4.95e-03 (rs139552233) | RARE, **no second allele** |

*Note on N1002K:* VEP's colocated frequencies returned none, so this pipeline
classed it `ABSENT_from_gnomAD`. The **direct gnomAD v4.1.1 lookup in Round 1
remains authoritative**: AC=1, AN=1,614,226, **AF 6.195e-7**, 0 homozygotes. The
discrepancy reflects VEP not surfacing an AC=1 singleton, not a conflict.

### A bug found and fixed in this round
The first version of `annotate_candidates_af.py` used the VEP **batch POST**
endpoint, which returned 500/503. Its fallback logic mapped *any* missing
frequency to `ABSENT_from_gnomAD` — so **all 43 candidates were falsely reported
as absent from gnomAD**, including TP53 p.Pro72Arg. Caught because that variant
is one of the commonest human polymorphisms. The script now uses per-variant GET,
and reports `QUERY_FAILED` as a distinct class that is **never** treated as
evidence of rarity. *(Second instance this project of "API failure silently
became a scientific claim" — the first was the `FORMAT/PS` false negative in
§R3.11. Both are now guarded.)*

## R4.5 No stronger competitor genome-wide

99 genes carried HOM_pLoF or TWO_pLoF (stronger AR models than BUB1B's). They are
dominated by families with known common LoF or alignment difficulty: **olfactory
receptors, HLA, MUC, KRTAP, PSG, NPIPB, LILRB, ZNF, GOLGA6L, DEFB**. Every
disease-relevant HOM_pLoF gene frequency-checked was **COMMON** (AF 0.36–1.00):
WNK1, LRRK1, CEP89, TDRD12, MRPS34, DZANK1, TLR8, DIAPH2, GPR33, CCDC198,
SERPINB11, VSIG10L, USP29, NUDT11.

Three retained rare pLoF — all with the same **clustered-indel artifact signature**:

| Gene | Rare pLoF | Span | Phenotype match |
|---|---|---|---|
| SERPINA1 | 4 frameshifts | **61 bp** | No (liver/lung; A1AT is caused by common Z/S missense) |
| POU6F2 | 2 frameshifts | **2 bp** | No (weak Wilms candidate; not chromosomal instability) |
| ADAMTS1 | 2 frameshifts | **8 bp** | No established Mendelian disease |

Four heterozygous frameshifts within 61 bp in one genome is not plausible true
biallelic LoF. **Stated as an assessment from the variant pattern, not a
read-level demonstration** — alignments are unavailable, so none is formally
excluded. BUB1B's two variants are a stop_gained and a missense **10,911 bp
apart** — not this pattern.

**Of the MVA/mitotic gene set (BUB1B, CEP57, TRIP13, BUB1, CENATAC, KNL1, BUB3,
MAD2L1, TTK, CENPE): only BUB1B has any AR model at all.** For the other nine:
*no qualifying variant identified under the documented filters* — **not** "gene
excluded".

## R4.6 Full BUB1B locus scan — no third hit

Window chr15:40,110,984–40,271,137 (gene body ±50 kb — a **chosen** screening
window, not a claim of complete regulatory coverage). All classes, PASS **and**
non-PASS retained. Script: `analysis/scripts/scan_bub1b_locus.py`.

172 non-reference variants; 17 annotated to BUB1B; 14 in the gene body.
By class: intergenic 79, intronic 68, upstream 20, 5′UTR 2, **pLoF 1**,
**missense 1**, downstream 1. By FILTER: PASS 164, MQ40 6, LowQual;QD2 2.

**Only two consequential BUB1B variants exist: `p.Leu737*` and `p.Asn1002Lys`.**
No canonical splice, no splice-region, no coding indel, no additional missense —
including among non-PASS calls. The two 5′UTR variants lie in the flank
(40,239,625 and 40,253,237, both beyond the BUB1B 3′ end at 40,221,137) and
belong to a neighbouring transcript.

**Limitation:** 68 intronic variants were catalogued but **no splice-prediction
tool (SpliceAI/Pangolin) was available**, so a deep-intronic cryptic-splice second
hit is **not excluded**.

## R4.7 SV/CNV — NOT POSSIBLE

No `##ALT` declarations, no symbolic alleles, no `NON_REF`/gVCF, no depth track,
no BAM/CRAM, no FASTQ, no pre-computed calls. **No SV/CNV analysis was performed
and none is reported.** A depth-based workaround from `FORMAT/DP` was considered
and rejected as uninterpretable (ascertainment-biased, no control cohort, single
sample). Full assessment: `analysis/data/SV_CNV_AVAILABILITY.md`.

**A CNV second hit in BUB1B cannot be excluded** and is a leading explanation if
phase turns out to be *cis*.

## R4.8 N1002K φ/ψ check — **VERDICT B, and it weakens our own model**

Script: `analysis/scripts/step11_phi_psi.py`. AF-O60566-F1-model_v6, pLDDT 91.1.

```
 1001  L   phi=-77.8   psi=-17.1    helical
 1002  N   phi=-126.6  psi=+37.3    <== N1002
 1003  A   phi=-60.6   psi=-27.8    helical
 1004  N   phi=+49.0   psi=-140.9   POSITIVE PHI (alphaL)
```

**N1002 has normal negative φ (−126.6°).** φ/ψ = (−126.6, +37.3) places it in the
**bridge region** — allowed, sparsely populated, consistent with pydssp calling it
loop rather than helix — but **not** positive-φ.

**Consequence, reported against our own hypothesis:** the argument that *only*
Asn/Gly tolerate this backbone conformation **does not apply**. Any steric case
against Lys must rest on side-chain hydrogen bonding and packing (§Step 5) alone,
not on backbone geometry. **The helix C-cap model loses one of its supports.**
Interestingly the positive-φ residue nearby is **N1004**, a different residue.

**Orthologue tolerance:** 6/6 orthologues (chimp, mouse, rat, dog, chicken,
*Xenopus*) carry **Asn** at position 1002. **No basic residue (Lys/Arg) is seen at
this position in any orthologue examined.**

**Experimental structure check — verified, not assumed.** PDBe lists 6tlj (3.8 Å)
and 5khu (4.8 Å) as mapping UniProt 1–1050, but direct parsing of the deposited
coordinates shows the BUBR1 chains model only **residues 19–345 (6tlj, chain S)**
and **18–308 (5khu, chain Q)**. **Residue 1002 is not present in any experimental
structure.** The AlphaFold model remains the only structural source — now a
verified limitation rather than an assumed one.

## R4.9 Phase — confirmed unresolvable from this data

Distance = 40,220,612 − 40,209,701 = **10,911 bp**. Library is Illumina NovaSeq
(flowcell `HGWCNDSX7`); typical PCR-free insert ~350–550 bp. No `FORMAT/PS`
declared; GATK's `PGT`/`PID` are declared but **both variants carry `PGT=.`,
`PID=.`** — no phasing group. GATK physical phasing operates only within a
read/fragment and cannot span 10.9 kb.

Population/statistical phasing (SHAPEIT5/Beagle) would be **weak and indirect** for
two variants at AF 6e-7 and 1e-4 that are absent from reference panels, and is
**never** converted into patient phase. Resolution requires **trio genotyping** or
**long-read sequencing**.

## R4.10 Reproducibility additions

New scripts, all executed (no placeholders):
`build_gene_panel.py`, `screen_panel_ar.py`, `annotate_candidates_af.py`,
`screen_genomewide_ar.py`, `check_strong_ar_genes.py`, `scan_bub1b_locus.py`,
`step11_phi_psi.py`. `rank_genomewide_ar.py` was written but **superseded** by
`check_strong_ar_genes.py` after VEP rate-limiting made the exhaustive version
impractical; it is retained and labelled rather than deleted.

Tools: snpEff **5.4c** (build 2026-02-23), db **GRCh38.mane.1.2.refseq**;
bcftools **1.24**; Python **3.12.7**; Biopython **1.88**; Ensembl VEP REST
(gnomAD frequencies), PanelApp API, PDBe API — all retrieved **2026-09-16**.

Patient genotype-level outputs under `analysis/data/genomewide/`,
`analysis/data/panel/` and `analysis/data/bub1b_locus/` are **gitignored** on the
same data-governance basis as `analysis/data/provenance/` (see §R3.11).

---

# Round 5 — Splice screen: closing the cryptic-splice second-hit gap (2026-09-24)

**Outcome: NO hidden BUB1B splice second hit. CASE B is unchanged.**
Full method/versions: `analysis/data/splicing/README.md`.
Scripts: `step12_splice_screen.py`, `step12b_finalize_splice.py`, `step12c_merge_splice.py`.

## R5.1 Correction to the Round 4 record

§R4.6 said *"68 intronic BUB1B variants"*. **Only 12 of the 68 are annotated to
BUB1B**; the other **56 are PAK6** — the adjacent gene, which overlaps BUB1B at
the 3′ end (BUB1B-PAK6 readthrough, ENSG00000259288). All 68 were screened, but
the BUB1B conclusion rests on **12 intronic + 2 coding controls = 14 records**.

## R5.2 Tools actually executed

| | SpliceAI | Pangolin |
|---|---|---|
| Version | **1.3.1** | GitHub `tkzeng/Pangolin` (2026-09-24) |
| Backend | TensorFlow 2.21.0 / Keras 3.15.1 | PyTorch 2.9.1 (CPU) |
| Annotation | bundled `grch38.txt` | **GENCODE v44** chr15 → gffutils DB |
| Parameters | `-A grch38 -D 500 -M 0` | `-d 500` |
| Input | `locus_normalized.vcf` | same variants as CSV (identical CHROM/POS/REF/ALT) |

Reference: Ensembl release-112 chr15 FASTA; REF bases verified against the VCF.
Normalization: `bcftools norm -f chr15.fa -m -any` → 172 in / **175** out
(3 multiallelic split, 2 realigned, **0 mismatch-removed, 0 skipped**).

*Pangolin's VCF path crashed (`Info.__new__() missing 'type_code'` — it targets
unmaintained PyVCF; only PyVCF3 installs on Python 3.12). Its documented CSV path
was used instead, fed from the same normalized VCF. Tool-compatibility workaround,
not a change of data.*

## R5.3 Result — all 14 BUB1B records NO SIGNAL, 14/14 concordant

| Variant | Intronic position | SpliceAI max ΔS | Pangolin max \|Δ\| | Predicted effect | Population evidence | Status |
|---|---|---|---|---|---|---|
| 15:40209701 T>G | *coding control* `p.Leu737*` | 0.03 | 0.03 | acceptor_gain@−34nt | rs759242053, AF 9.98e-5 | NO SIGNAL |
| 15:40168264 G>A | c.180−1798 | 0.02 | 0.02 | acceptor_gain@−213nt | rs28570325, AF 0.0306 | NO SIGNAL |
| 15:40187404 A>G | c.1058+1762 | 0.02 | 0.03 | donor_gain@−1nt | rs8036410, AF 1.00 | NO SIGNAL |
| 15:40220612 T>G | *coding control* `p.Asn1002Lys` | 0.02 | 0.01 | acceptor_gain@−48nt | not returned by VEP¹ | NO SIGNAL |
| 15:40198239 G>GT | c.1289−1362 | 0.01 | 0.00 | acceptor_gain@+21nt | rs35740616, AF 0.683 | NO SIGNAL |
| 15:40180642 CT>C | c.582−3047 | 0.00 | 0.00 | none | rs71132149, AF 0.356 | NO SIGNAL |
| 15:40181093 AT>A | c.582−2604 | 0.00 | 0.00 | none | rs372589327, AF 0.843 | NO SIGNAL |
| 15:40182809 A>C | c.582−905 | 0.00 | 0.00 | none | rs28620590, AF 0.0384 | NO SIGNAL |
| 15:40186692 G>A | c.1058+1050 | 0.00 | 0.00 | none | rs4924431, AF 0.998 | NO SIGNAL |
| 15:40192892 C>T | c.1059−3653 | 0.00 | 0.00 | none | rs185599777, AF 0.00745 | NO SIGNAL |
| 15:40193435 T>C | c.1059−3110 | 0.00 | 0.00 | none | rs483238, AF 1.00 | NO SIGNAL |
| 15:40216470 A>G | c.2679−1026 | 0.00 | 0.00 | none | **not in gnomAD** | NO SIGNAL |
| 15:40216568 TA>T | c.2679−927 | 0.00 | 0.00 | none | rs57676380, AF 0.468 | NO SIGNAL |
| 15:40216570 TA>T | c.2679−925 | 0.00 | 0.00 | none | rs200074915, AF 0.444 | NO SIGNAL |

¹ VEP did not return a frequency; the **authoritative Round 1 gnomAD v4.1.1 lookup
stands: AC=1, AF 6.195e-7**.

**Highest score anywhere in BUB1B: 0.03** — an order of magnitude below SpliceAI's
most permissive (high-recall) reference point of 0.2. **Zero variants reached
LOW PRIORITY, REVIEW, or HIGH-PRIORITY.**

Across all 176 records (both genes): 97 NO SIGNAL · 77 UNSUPPORTED_VARIANT
(upstream of both transcripts; **both tools declined them independently, for the
same reason**) · 2 LOW PRIORITY (**both PAK6**, 0.05–0.06) · **0 TOOL_FAILURE**.

## R5.4 Canonical splice-region variants — none exist

The BUB1B locus scan found **zero** variants annotated `splice_acceptor`,
`splice_donor` or `splice_region`, at any FILTER level. All 12 intronic variants
are **deep intronic** — nearest to a splice junction is c.2679−925.

## R5.5 Two more silent-failure bugs, found and fixed

1. **Case-sensitivity.** The parser matched `SPLICEAI=`; the tool writes
   `SpliceAI=`. The first parse returned **175/175 PREDICTION_UNAVAILABLE** —
   indistinguishable from "no splice data" while the model had run perfectly.
   Fixed case-insensitively, plus a guard that trips loudly when 0 records carry a
   usable score.
2. **Destructive rewrite.** `step12b` opened the parsed table with `"w"` and raised
   mid-write, truncating it; the next run silently saw 0 records. Rewrites are now
   atomic (temp + `os.replace`). The raw `spliceai_output.vcf` was untouched.

**Third and fourth instances in this project of a silent failure nearly becoming a
scientific claim** (cf. §R3.11 `FORMAT/PS`, §R4.4 VEP `QUERY_FAILED`). Every such
path now fails loudly.

## R5.6 Effect on conclusions

| Item | Before | After |
|---|---|---|
| Cryptic-splice second hit in BUB1B | not excluded | **screened; no candidate found** |
| CNV/SV second hit | not excluded | **still not excluded** (no data) |
| Phase | UNKNOWN | **UNKNOWN** |
| Decision matrix | CASE B | **CASE B** |
| N1002K | prioritised VUS | **prioritised VUS** — additionally, it does **not** act via splicing (ΔS 0.02/0.01) |
| Mechanism | C — UNKNOWN | **C — UNKNOWN** |
| Therapeutic gate | CLOSED | **CLOSED** |

This **narrows** the hidden-second-hit space without resolving CASE B. A
prediction-level negative is not proof of absence: SpliceAI/Pangolin have limited
sensitivity for deep-intronic elements, branchpoints, and pseudoexon activation,
and neither sees structural variation.

---

# Round 6 — Phase audit and CNV/SV evidence audit (2026-09-24)

**Outcome: phase = UNPHASED; CNV/SV = unresolved from available data. CASE B confirmed.**
Scripts: `step13_phase_audit.py`, `step14_cnv_sv_audit.py`.
Reports: `analysis/data/phase/PHASE_REPORT.md` (gitignored — contains genotypes),
`analysis/data/cnv_sv/CNV_SV_REPORT.md`.
Decision tree: `analysis/data/DECISION_MATRIX_UPDATED.md`.
Stop/go rule: `analysis/data/NEXT_EXPERIMENT.md`.

## R6.1 Phase audit — **UNPHASED**

Every phase-capable field was enumerated from the VCF header before querying, so
an undeclared tag could not crash the query and be misread as an absent variant
(the §R3.11 failure mode).

| Field | Status in this VCF |
|---|---|
| `PGT`, `PID` | **declared** (GATK physical phasing) |
| `PS` | **not declared** (WhatsHap/HapCUT2 convention) |
| `HP`, `PQ`, `PW`, `PHASE`, `PSET`, `HAP`, `BX`, `MI` | **declared nowhere** |

| Variant | GT | DP | GQ | AD | PGT | PID |
|---|---|---|---|---|---|---|
| `p.Leu737*` 15:40209701 T>G | **0/1** | 46 | 99 | 21,25 | `.` | `.` |
| `p.Asn1002Lys` 15:40220612 T>G | **0/1** | 28 | 99 | 15,13 | `.` | `.` |

REF/ALT matched expectation at both sites; both `PASS`. Distance **10,911 bp**.
**Shared phase set: NONE** — both PGT and PID are empty at both variants.

**Classification: `UNPHASED`.** Both genotypes use the unphased `/` separator and
no phase-set identifier links them. **Phase was not inferred from allele balance,
GQ, DP, or physical proximity**, and a missing field was never read as *cis* or
*trans*.

Resolution requires trio genotyping, long-read sequencing, Hi-C/Pore-C, or
allele-specific long-range PCR. Statistical/population phasing and short-read
physical phasing are explicitly rejected (both variants are ultra-rare and absent
from reference panels; fragments of ~350–550 bp cannot span 10.9 kb).

## R6.2 CNV/SV audit — **unresolved from available data**

Ten evidence classes were searched. **All negative:**

| # | Evidence class | Result |
|---|---|---|
| 1 | `##ALT` symbolic allele declarations | **NONE** |
| 2 | Symbolic ALT records (`<DEL>`/`<DUP>`/`<CNV>`/`<INV>`/`<INS>`) | **0** |
| 3 | Breakend (BND) records | **0** |
| 4 | SV/CNV INFO or FORMAT keys (SVTYPE, SVLEN, END, CIPOS, CIEND, IMPRECISE, CN, CNQ, …) | **all ABSENT** |
| 5 | gVCF reference blocks (`<NON_REF>`) | **0** — site-level VCF, not a gVCF |
| 6 | Usable read-depth/dosage track | **NONE** |
| 7 | Split-read / discordant-pair fields (SR, PE, PR, RP, RR) | **NONE** |
| 8 | BAM / CRAM / FASTQ on disk | **NONE** |
| 9 | Pre-computed CNV/SV call sets (Manta, DELLY, LUMPY, gCNV, CNVnator, `.seg`/`.cns`/`.cnr`) | **NONE** |
| 10 | BUB1B gene-body records | 14, **0 symbolic** — SNV/indel only |

**`FORMAT/DP` was not used as CNV evidence.** The script records its presence and
then explicitly refuses to derive dosage from it: called-site depth is
ascertainment-biased, has no matched control cohort, and this is a single sample.

**A CNV or SV second hit in *BUB1B* — e.g. a single-exon deletion on the allele
not carrying `p.Leu737*` — CANNOT BE EXCLUDED.**

**Minimum practical assay (NOT performed):** MLPA first-line for exon-level
dosage across all 23 exons; qPCR/ddPCR for targeted exons; long-read WGS resolves
dosage **and** phase in one experiment. Caveat recorded: dosage assays miss
balanced inversions and translocations entirely.

## R6.3 Effect on conclusions

| Item | Before Round 6 | After Round 6 |
|---|---|---|
| Phase | UNKNOWN | **UNPHASED (formally audited and classified)** |
| CNV/SV | not assessable | **audited across 10 evidence classes; unresolved — no data of any type** |
| Decision tree | CASE B | **CASE B confirmed** |
| `p.Leu737*` | strong pathogenic evidence | unchanged |
| `p.Asn1002Lys` | prioritised VUS | **unchanged — prioritised VUS** |
| Mechanism | C — UNKNOWN | **unchanged** |
| Therapeutic gate | CLOSED | **unchanged — CLOSED** |

**No scientific conclusion changed.** Round 6 converted two informal statements
("phase unknown", "CNV not assessable") into formally audited, reproducible
findings with explicit classifications, and produced the decision tree and
stop/go rule that direct the next experiment.
