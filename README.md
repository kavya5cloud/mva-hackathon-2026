# Rare Disease, Real Kid — MVA Hackathon 2026

**Team:** kavya5cloud · **Tracks:** 1 (Variant Prediction) + 2 (Drug Repurposing)
**Proband:** `WGS_EX2312012`, GRCh38, single-sample WGS, ~5.02 M variants
**Evidence frozen:** 2026-09-26

> ### The result, in one paragraph
>
> A child with Mosaic Variegated Aneuploidy features carries two heterozygous
> *BUB1B* variants. **One is solidly pathogenic** (`p.Leu737*`, ClinVar 2-star).
> **The other is a VUS whose mechanism we could not establish** (`p.Asn1002Lys`) —
> and our own calibrated modelling argues *against* the mechanism we set out to
> prove. The two variants are **10,911 bp apart and unphased**, so no second
> pathogenic allele is established. *BUB1B* is therefore a **leading genetic
> hypothesis, not a confirmed molecular diagnosis**, the mechanism is **UNKNOWN**,
> and we report **no drug candidate — deliberately, as the evidence requires.**

---

## Why this repository is worth your time

Most negative results are quiet. This one is documented, reproducible, and
adversarial toward its own authors. Three things here cut against our own position,
and **every one of them is independently checkable in this repo**:

| | What we did | Where to verify |
|---|---|---|
| **1** | **We falsified our own hypothesis.** We set out to show N1002K destabilises BUBR1. A ΔΔG predictor we calibrated *before* interpreting it — correct on **4/4** known-outcome *BUB1B* variants — puts N1002K at **−0.01 kcal/mol**, clustering with the experimentally WT-like control. | [Report §6](analysis/kavya5cloud_track2_report.md) |
| **2** | **We found and published an error in our own scored Track 1 submission** — a genome-build mistake that invalidated its headline conclusion — then re-derived the candidate gene from scratch rather than assuming it. | [Erratum](analysis/TRACK1_SUBMISSION_ERRATUM.md) · [below](#the-error-we-found-in-our-own-submission) |
| **3** | **We weakened our own replacement model.** A φ/ψ check removed a key support of our helix-cap hypothesis. We report it instead of omitting it. | [Report §5](analysis/kavya5cloud_track2_report.md) |

And **six silent-failure bugs in our own tooling were caught and fixed** — each one
a case where an API error or a parsing slip would have silently become a scientific
claim. A `FORMAT/PS` query that reported real variants as absent. A VEP failure that
made TP53 p.Pro72Arg (**AF 0.748**) look absent from gnomAD. An INFO-key casing
mismatch that turned 175/175 splice predictions into silent nulls. A non-atomic
rewrite that truncated a results file. A claim-scan that reported zero hits because
zsh does not word-split unquoted variables. A classifier that excused its own
findings. **Every one of those paths now fails loudly rather than returning a
comfortable answer.**

> The scientific contribution here is not a drug. It is a **defensible
> negative**, with the evidence that makes it defensible attached.

---

## Verified findings

Both variants confirmed **directly in the proband VCF** (md5 `a04ea354141cfb032872d67a11c8d2d8`)
via [`step0_verify_provenance.py`](analysis/scripts/step0_verify_provenance.py):

| Variant | GRCh38 | FILTER | GT | DP | GQ | VAF | ClinVar (exact allele) | Status |
|---|---|---|---|---|---|---|---|---|
| `c.2210T>G` **p.Leu737\*** | chr15:40,209,701 T>G | PASS | 0/1 | 46 | 99 | 0.543 | **VCV000533901 — Pathogenic/LP, 2-star**, multiple submitters, no conflicts | **strong pathogenic evidence** |
| `c.3006T>G` **p.Asn1002Lys** | chr15:40,220,612 T>G | PASS | 0/1 | 28 | 99 | 0.464 | **no record**; gnomAD **AF 6.195e-7** (AC 1 / AN 1,614,226) | **prioritised VUS** |

### Three traps we did not fall into

- **`c.3006T>A`** also encodes p.Asn1002Lys and *does* carry a ClinVar VUS record. **It is not the patient's allele.** No evidence transfers from it.
- **Human L1012 ≡ mouse L1002.** The published mouse `L1002P` allele is a *different residue* from this patient's `N1002K`.
- **Human BUBR1 is a pseudokinase** — no phosphotransfer activity. UniProt's "active site 882" is by-similarity only. No claim here depends on BUBR1 kinase activity.

---

## How *BUB1B* was re-established without assuming it

After the Track 1 error, we refused to inherit the answer. The gene was re-derived
from the phenotype and from an unbiased genome-wide screen:

```
8 HPO terms (verbatim, incl. Rhabdomyosarcoma HP:0002859)
   └─> PanelApp panel 290 v1.6 + 259 v1.30 + brief's MVA set ──> 80 genes
5,012,204 variants ──snpEff──> 11,320 PASS HIGH/MODERATE ──> 203 genes with an AR model
```

| Finding | Number |
|---|---|
| Qualifying panel variants that were **common polymorphisms** | **40 of 43** (TP53 p.Pro72Arg AF 0.748 · ERCC2 p.Asp312Asn AF 0.513 · XPC p.Gln939Lys AF 0.729) |
| Panel genes retaining a rare qualifying variant after frequency filtering | **2** — *BUB1B* (rare pLoF **+** a second rare allele) and *ATM* (single allele, no second) |
| Of the 10 core MVA/SAC genes, how many had **any** AR model | **1** — *BUB1B* |
| Consequential variants in the entire *BUB1B* locus ±50 kb, all classes, PASS **and** non-PASS | **exactly 2** — the two above |
| Deep-intronic *BUB1B* variants screened for cryptic splicing | **14/14 NO SIGNAL**, two independent tools concordant, max ΔS **0.03** vs SpliceAI's most permissive reference point of 0.2 |

The 99 genes with *stronger* AR models were all common polymorphisms or carried a
clustered-indel artifact signature (e.g. **4 frameshifts within 61 bp** in *SERPINA1*).

---

## Why no drug is proposed

The therapeutic gate was defined **before** any drug search, and **no drug search was
ever run** — not a single compound was named, ranked or scored.

| Gate condition | Observed |
|---|---|
| Reduced BUBR1 abundance | **never measured** |
| Shortened half-life · proteasome-dependent loss · rescue by stabilisation | **no data** |
| *or* a precise defective signalling node identified | **no data** — residue 1002 was never tested |

Independently sufficient reasons the gate stays shut: mechanism is **UNRESOLVED**;
**no E3 ligase for misfolded BUBR1 has ever been identified**, so even the favoured
hypothesis has no target; phase is **UNPHASED**, so N1002K is not established as a
pathogenic allele in this child; and the one plausible node is **not druggable in the
required direction** — inhibitors would *reduce* KARD phosphorylation and worsen the
predicted defect.

**Every obvious repurposing class is actively contraindicated here.** HSP90 inhibitors,
proteasome inhibitors, MPS1/TTK, Aurora and KIF11 inhibitors, classical antimitotics
and APC/C activators would each be expected to **worsen missegregation in a child who
already has MVA.** Naming one would have scored better and been wrong.

**To reopen the gate:** demonstrate reduced abundance + shortened half-life +
proteasome-dependent loss, **and** establish *trans*.

---

## Limitations we state before you find them

1. **Phase is unobtainable** from this data — ~350–550 bp fragments cannot span 10,911 bp. A physical limit, not a tooling choice.
2. **CNV/SV is unresolved, not excluded.** Audited across **10 evidence classes**, all negative: no symbolic ALTs, 0 BND records, no SV/CNV keys, not a gVCF, no usable depth track, no BAM/CRAM/FASTQ. `FORMAT/DP` was **deliberately not** used as a dosage proxy.
3. **Zero experimental assays** were performed. Every mechanistic statement is computational or extrapolated from *other* variants.
4. **AlphaMissense (0.9229), DynaMut2, SpliceAI/Pangolin and AlphaFold are all Tier 3 and correlated — their agreement is not replication.** AlphaMissense in fact *fails* our abundance calibration: it cannot separate stable Q921H from destabilised I909T, and calls destabilised L844F "likely benign".
5. Residue 1002 is **in no experimental structure**; no molecular dynamics was run; only **one** ΔΔG predictor returned values (DDMut's API failed, FoldX unlicensed).
6. NMD for `p.Leu737*` is **predicted, not measured**. Conservation is established to *Xenopus*, **not** teleosts.
7. **The MVA diagnosis itself is asserted, not evidenced** in available records — no karyotype, no chromosome counts, no premature-chromatid-separation assay.
8. The screen is coding-focused, SNV/indel only, no *de novo* model without parents. **"No qualifying variant identified" is not "gene excluded."** LOVD was inaccessible — status UNKNOWN, not negative.

### Language this project does not use

These phrasings are **prohibited** in every current document, and
[`step15_claim_scan.py`](analysis/scripts/step15_claim_scan.py) enforces it:

- ❌ never used — compound heterozygous · biallelic · *in trans* · *in cis*
- ❌ never used — "*BUB1B* confirmed" · "molecular diagnosis established"
- ❌ never used — "N1002K is pathogenic" · "N1002K destabilises BUBR1"
- ❌ never used — "disrupts PP2A-B56 binding" (PP2A-B56 binds the KARD, **51–85 Å away**) · "BUBR1 kinase activity"
- ❌ never used — CNV/SV or splicing described as *excluded* (both are **unresolved**)
- ❌ never used — "conserved, therefore pathogenic" · "rare, therefore pathogenic"
- ❌ never used — any named drug, or any claim that a treatment exists

---

## The error we found in our own submission

The Track 1 methods correctly state **GRCh38** — and the VCF *is* GRCh38 (chr15
contig length 101,991,189). But the recorded extraction interval is the ***BUB1B*
locus in GRCh37***:

```bash
bcftools view -r 15:40400000-40500000 WGS_EX2312012_HGWCNDSX7.vcf.gz   # GRCh37 coordinates
```

| Build | *BUB1B* span | Overlap with that window |
|---|---|---|
| **GRCh38** — the VCF's actual build | chr15:40,160,984–40,221,137 | **0 bp** |
| GRCh37 | chr15:40,453,224–40,513,337 | 46,770 bp |

The window returns **36 variants**, matching the methods document exactly — the
pipeline ran precisely as described. But in GRCh38 those variants lie in ***IVD*,
*BAHD1* and *CHST14***. The three prioritised candidates are **real, PASS-quality
proband variants in the wrong genes**, so the original "compound-heterozygous
frameshift pair in *BUB1B*" conclusion **is not supported**.

**How we handled it:** the scored submission CSVs are preserved **byte-for-byte**,
verified by `diff`. Nothing was silently rewritten. The historical claim stands in
place under an explicit erratum banner, and the corrected extraction
(`15:40158984-40223137` → **15 variants**) recovers both variants above.

---

## Repository layout

**Read in this order:**

| # | Path | What it is |
|---|---|---|
| 1 | [`analysis/kavya5cloud_track2_report.md`](analysis/kavya5cloud_track2_report.md) | **The Track 2 deliverable** — 16 sections, every claim tiered |
| 2 | [`analysis/PITCH_FACTS.md`](analysis/PITCH_FACTS.md) | Every verified number in one place; nothing unverified |
| 3 | [`analysis/README.md`](analysis/README.md) | Reviewer's guide + full reproduction commands |
| 4 | [`analysis/FINAL_AUDIT.md`](analysis/FINAL_AUDIT.md) | Self-audit: findings, corrections, frozen state |
| 5 | [`analysis/round2_variant_characterisation.md`](analysis/round2_variant_characterisation.md) | Complete evidence record, Rounds 1–6, failures included |
| 6 | [`analysis/TRACK1_SUBMISSION_ERRATUM.md`](analysis/TRACK1_SUBMISSION_ERRATUM.md) | Formal erratum for the Track 1 CSVs |
| — | [`analysis/scripts/`](analysis/scripts/) | 21 scripts (19 Python, 2 shell), all syntax-validated |
| — | [`analysis/data/`](analysis/data/) | Evidence artifacts — **no genotype-level patient data** |
| — | [`analysis/environment.txt`](analysis/environment.txt) | Versions **and documented absences** (mkdssp, FoldX, MD engine) |
| — | [`MVA_Hackathon_2026_Track1_METHODS.md`](MVA_Hackathon_2026_Track1_METHODS.md) | Historical Track 1 methods + §30 build erratum |

## Reproducibility

Thresholds were **pre-registered before results were inspected and not altered
afterwards**: RSA <0.20 / >0.40 · pLDDT ≥70 · an ASN-at-1002 hard gate · gnomAD
popmax >0.001 and ClinVar B/LB ≥2-star stop criteria. Failed queries and access
limitations are **recorded, not omitted**.

```bash
# Verify both variants in the proband VCF (build inferred from contig length, not assumed)
python3 analysis/scripts/step0_verify_provenance.py /path/to/WGS_EX2312012_HGWCNDSX7.vcf.gz

# Formal phase classification -> exactly one of PHASED_IN_TRANS / PHASED_IN_CIS / UNPHASED / INSUFFICIENT_DATA
python3 analysis/scripts/step13_phase_audit.py

# CNV/SV evidence audit across 10 classes
python3 analysis/scripts/step14_cnv_sv_audit.py

# Scan every document for overclaims; aborts loudly if the scan itself is broken
python3 analysis/scripts/step15_claim_scan.py
```

Structure `AF-O60566-F1-model_v6.pdb`, md5 `943e5596717db0424b1a020ae429e174`.
Tooling: bcftools 1.24 · snpEff 5.4c (`GRCh38.mane.1.2.refseq`) · SpliceAI 1.3.1 ·
Pangolin (GENCODE v44) · Python 3.12.7 · Biopython 1.88 · NumPy 1.26.4.

## The next experiment is genetic, not mechanistic

No amount of further modelling can substitute for **resolving phase**: proband
long-read sequencing (preferred), or trio genotyping where parents are available and
informative, plus *BUB1B* exon-dosage testing for the structural second hit we cannot
exclude. Spec: [`analysis/data/phase/`](analysis/data/) ·
decision tree: [`analysis/data/NEXT_STEP_TREE.md`](analysis/data/NEXT_STEP_TREE.md).

## Data governance

The dataset is gated — request access at
<https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data>. **No raw
VCF/BAM/FASTQ and no genotype-level output is committed**; exclusions are explicit
in [`.gitignore`](.gitignore) and were verified before every push.

**AI-assisted analysis disclosure:** Anthropic Claude Opus 5 and Claude Opus 5.5 were
used via the Claude API with a Pro plan. Data sharing for model training was disabled.
AI-assisted outputs were independently checked against the project's source data and
evidence record. Full statement: [Track 2 report §15](analysis/kavya5cloud_track2_report.md) ·
[Track 1 methods §30](MVA_Hackathon_2026_Track1_METHODS.md).

## Final scientific state (frozen)

```
p.Leu737*      = strong pathogenic evidence
p.Asn1002Lys   = prioritised VUS
Phase          = UNPHASED
CNV/SV         = unresolved from available data
BUB1B          = leading genetic hypothesis, NOT a confirmed molecular diagnosis
Mechanism      = UNKNOWN
Therapeutic gate = CLOSED
Drug candidate = NONE PROPOSED
```

## License

CC BY 4.0, per hackathon rules.
