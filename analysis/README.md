# MVA Hackathon 2026 — Track 2 analysis

**Team:** kavya5cloud · **Analysis frozen:** 2026-09-26

> ## FINAL SCIENTIFIC STATE
>
> ```
> Leu737* = strong pathogenic evidence.
> N1002K = prioritised VUS.
> Phase = UNPHASED.
> CNV/SV = unresolved from available data.
> BUB1B = leading genetic hypothesis, not confirmed molecular diagnosis.
> Mechanism = UNKNOWN.
> Therapeutic gate = CLOSED.
> No drug candidate proposed.
> ```
>
> **This repository does not establish clinical causality.** It documents a
> candidate genotype, the reasoning that narrowed it, and the specific evidence
> that is still missing.

---

## WHAT WAS ANALYZED

A single-sample whole-genome VCF from one proband with Mosaic Variegated
Aneuploidy features (`WGS_EX2312012_HGWCNDSX7.vcf.gz`, GRCh38, GATK 4.2.4.0,
~5.02 M variants; md5 `a04ea354141cfb032872d67a11c8d2d8`). The dataset is gated
and is **not** committed here.

Two *BUB1B* variants were the focus, both **verified present in the proband**:

| Variant | GRCh38 | GT | DP | GQ | Status |
|---|---|---|---|---|---|
| `NM_001211.6:c.2210T>G` (p.Leu737\*) | chr15:40,209,701 T>G | 0/1 | 46 | 99 | **strong pathogenic evidence** |
| `NM_001211.6:c.3006T>G` (p.Asn1002Lys) | chr15:40,220,612 T>G | 0/1 | 28 | 99 | **prioritised VUS** |

Alongside them: an 80-gene phenotype-driven panel, an unbiased genome-wide
recessive screen, the full *BUB1B* locus ±50 kb across all variant classes, and
the AlphaFold model of BUBR1.

## WHY IT WAS ANALYZED

Track 2 asked whether a drug-repurposing hypothesis could be built on a *BUB1B*
mechanism. Two things redirected the work:

1. **Our original mechanistic hypothesis failed.** We set out to show that
   `p.Asn1002Lys` destabilises BUBR1. A ΔΔG predictor calibrated against four
   *BUB1B* variants with published abundance phenotypes — correct on all four —
   scored it as neutral.
2. **We found a genome-build error in our own Track 1 pipeline.** The recorded
   extraction used the **GRCh37** *BUB1B* interval against a **GRCh38** VCF. That
   invalidated the original Track 1 conclusion and meant the candidate gene had to
   be **re-derived from scratch** rather than assumed.

## WHAT WAS FOUND

- **`p.Leu737*` is a well-supported pathogenic null allele** — ClinVar 2-star Pathogenic/Likely pathogenic for MVA syndrome 1; codon `TTA`→`TGA` verified from the CDS; exon 17/23.
- ***BUB1B* was independently re-established** as the only candidate surviving an unbiased, phenotype-driven, frequency-filtered genome-wide screen. Of ten MVA/mitotic-checkpoint genes, only *BUB1B* carried any qualifying recessive genotype. 40 of 43 panel candidates turned out to be **common polymorphisms**.
- **`p.Asn1002Lys` is ultra-rare and highly conserved** (gnomAD AF 6.195e-7; invariant human→*Xenopus*; phyloP 4.80). These are **supporting observations, not pathogenicity evidence**.
- **A genome-build erratum, fully documented**, with the original scored submissions preserved byte-for-byte.

## WHAT WAS NOT FOUND

- **No second pathogenic *BUB1B* allele.** The full locus scan found only the two variants above — no third coding, splice-region, or canonical splice variant, at any filter level.
- **No hidden splice second hit.** SpliceAI 1.3.1 and Pangolin, run independently, scored all 14 *BUB1B* records **NO SIGNAL** (max ΔS 0.03, 14/14 concordant).
- **No better-supported alternative gene** in the analysed data.
- **No functional evidence for `p.Asn1002Lys`** — no publication, no assay, and no deep mutational scan of *BUB1B* in MaveDB.
- **No validated targetable mechanism**, and **no E3 ligase for misfolded BUBR1 has ever been identified**.
- **No drug candidate.** This is a deliberate conclusion, not a missing section.

## WHAT REMAINS UNRESOLVED

1. **Phase (UNPHASED).** Both genotypes unphased, no shared phase set, 10,911 bp apart — beyond short-read reach. The genotype is compatible with *trans*, *cis*, or an incidental variant, and **these cannot be distinguished**.
2. **CNV/SV (unresolved from available data).** An audit across ten evidence classes found nothing: no symbolic alleles, no gVCF, no depth track, no BAM/CRAM/FASTQ, no pre-computed calls. A structural second hit **cannot be excluded**.
3. **Mechanism (UNKNOWN).** Destabilisation falsified; direct PP2A-B56 disruption unsupported; the helix-cap model is computational only and was weakened by a backbone φ/ψ check.
4. **The MVA diagnosis itself is asserted, not evidenced** in available records — no karyotype, no chromosome counts, no PCS assay.

Full list: [`FINAL_AUDIT.md`](FINAL_AUDIT.md) §7.

## Scientific interpretation

`p.Leu737*` is a securely classified pathogenic null allele. `p.Asn1002Lys` is a
**prioritised variant of uncertain significance**: rare, conserved, and
structurally interesting, but with no functional evidence and with our own
calibrated modelling arguing against the destabilisation mechanism we first
proposed. Because phase is unresolved and CNV/SV cannot be assessed from these
data, **no second pathogenic *BUB1B* allele has been established.**

*BUB1B* therefore remains a **leading genetic hypothesis rather than a confirmed
molecular diagnosis.** The proband's genotype is best described as **two
heterozygous variants of interest in a recessive-model candidate gene**. It is
not described as compound heterozygous, biallelic, *in cis*, or *in trans*,
because none of those has been demonstrated.

The mechanism is unresolved and no therapeutic candidate is proposed. The
highest-value next experiment is **genetic, not mechanistic**: resolve phase
(proband long-read sequencing preferred; trio genotyping where parents are
available) and/or *BUB1B* exon dosage. Functional work on `p.Asn1002Lys` should
follow only once the allele architecture is constrained — a *cis* result would
make that work unjustifiable.

---

## Read in this order

| # | File | What it is |
|---|---|---|
| 1 | [`kavya5cloud_track2_report.md`](kavya5cloud_track2_report.md) | **Start here.** The 16-section scientific report. |
| 2 | [`PITCH_FACTS.md`](PITCH_FACTS.md) | **Verified facts only** — every number, conclusion and limitation safe to state in the pitch. |
| 3 | [`data/FINAL_STOP_GO.md`](data/FINAL_STOP_GO.md) | Nine plain questions and their current answers. |
| 4 | [`data/FINAL_EVIDENCE_TABLE.md`](data/FINAL_EVIDENCE_TABLE.md) | Every claim with its evidence, strength, limitation and consequence. |
| 5 | [`FINAL_AUDIT.md`](FINAL_AUDIT.md) | Final consistency/provenance audit; preserved historical material; limitations. |
| 6 | [`data/NEXT_EXPERIMENT.md`](data/NEXT_EXPERIMENT.md) · [`data/NEXT_STEP_TREE.md`](data/NEXT_STEP_TREE.md) | What to do next, and the branch tree after each phase result. |
| 7 | [`data/DECISION_MATRIX_UPDATED.md`](data/DECISION_MATRIX_UPDATED.md) | Current allele-architecture decision tree (CASE A–E). |
| 8 | [`data/phase/PHASE_EXPERIMENT_SPEC.md`](data/phase/PHASE_EXPERIMENT_SPEC.md) · [`data/phase/MINIMUM_DECISIVE_TEST.md`](data/phase/MINIMUM_DECISIVE_TEST.md) | Phase route comparison and pre-registered acceptance criteria. |
| 9 | [`data/cnv_sv/CNV_SV_REPORT.md`](data/cnv_sv/CNV_SV_REPORT.md) | CNV/SV audit + the minimum practical dosage assay. |
| 10 | [`data/splicing/README.md`](data/splicing/README.md) | Splice screen method, versions and result. |
| 11 | [`TRACK1_SUBMISSION_ERRATUM.md`](TRACK1_SUBMISSION_ERRATUM.md) | Formal erratum for the Track 1 submissions and the genome-build error. |
| 12 | [`data/phenotype/PHENOTYPE.md`](data/phenotype/PHENOTYPE.md) | Proband HPO terms, verbatim, plus missing clinical fields. |
| 13 | [`round2_variant_characterisation.md`](round2_variant_characterisation.md) | **Full evidence record, Rounds 1–6** — every query, result, failed query and access limitation. |
| 14 | [`environment.txt`](environment.txt) | Software versions **and documented absences**. |

## Rounds

| Round | Work | Outcome |
|---|---|---|
| 1 | ClinVar / gnomAD triage | Both variants characterised; T>G kept distinct from T>A |
| 2 | Domain boundaries, structural gate, H-bonds, ΔΔG calibration, conservation, PP2A-B56, degradation literature | **Destabilisation hypothesis falsified** as primary mechanism |
| 3 | Provenance/build audit, phase analysis, structural network, hypothesis matrix, therapeutic gate | Helix C-cap model proposed (**hypothesis only**); gate **closed** |
| 4 | Phenotype-driven PanelApp panel, genome-wide AR screen, full locus scan, SV/CNV availability, φ/ψ check | ***BUB1B* independently re-established**; CASE B. **φ/ψ weakened our own model** |
| 5 | SpliceAI + Pangolin over the locus | **No cryptic-splice second hit**; CASE B unchanged |
| 6 | Phase audit, CNV/SV audit | **UNPHASED**; CNV/SV unresolved; phase is the next experiment |
| Final | Consistency, provenance and reproducibility audit | **No scientific conclusion changed** |

---

## HOW TO REPRODUCE THE COMPUTATIONAL ANALYSIS

**Tooling:** bcftools 1.24 · snpEff 5.4c (db `GRCh38.mane.1.2.refseq`) ·
SpliceAI 1.3.1 (TensorFlow 2.21.0) · Pangolin (PyTorch 2.9.1, GENCODE v44) ·
Python 3.12.7 · Biopython 1.88 · NumPy 1.26.4. APIs (Ensembl REST/VEP, PanelApp,
NCBI E-utilities, UCSC, PDBe, AlphaFold DB, MaveDB) queried 2026-09-15 → 2026-09-24.
`NM_001211.6` is the reference *BUB1B* transcript throughout. Documented
**absences** (mkdssp, FoldX, MD engine) are in [`environment.txt`](environment.txt).

### Structural analyses (no patient data needed)

```bash
curl -O https://alphafold.ebi.ac.uk/files/AF-O60566-F1-model_v6.pdb   # md5 943e5596717db0424b1a020ae429e174
python3 analysis/scripts/step4_structure_gate.py      AF-O60566-F1-model_v6.pdb
python3 analysis/scripts/step5_contacts.py            AF-O60566-F1-model_v6.pdb
python3 analysis/scripts/step6_conservation.py        analysis/data/homol.json
python3 analysis/scripts/step9_structural_network.py  AF-O60566-F1-model_v6.pdb analysis/data/homol.json
python3 analysis/scripts/step11_phi_psi.py            AF-O60566-F1-model_v6.pdb
bash    analysis/scripts/step1_database_queries.sh    # all external DB queries
bash    analysis/scripts/step5b_ddg_panel.sh          # DynaMut2 ddG panel
```

### Genomic analyses (require the gated proband VCF)

```bash
V=/path/to/WGS_EX2312012_HGWCNDSX7.vcf.gz

# BLOCKING — run first: infers build, verifies both variants are the proband's
python3 analysis/scripts/step0_verify_provenance.py "$V"

# Gene panel + recessive screens
python3 analysis/scripts/build_gene_panel.py
bcftools view -R analysis/data/panel/panel_regions.sorted.bed "$V" -Oz -o analysis/data/panel/panel_raw.vcf.gz
bcftools index -f -t analysis/data/panel/panel_raw.vcf.gz
java -Xmx4g -jar /opt/anaconda3/share/snpeff-5.4.0c-0/snpEff.jar ann \
  -noStats -canon GRCh38.mane.1.2.refseq analysis/data/panel/panel_raw.vcf.gz \
  | bgzip -c > analysis/data/panel/panel_annotated.vcf.gz
python3 analysis/scripts/screen_panel_ar.py
python3 analysis/scripts/annotate_candidates_af.py     # gnomAD AF — the decisive filter
python3 analysis/scripts/screen_genomewide_ar.py
python3 analysis/scripts/check_strong_ar_genes.py
python3 analysis/scripts/scan_bub1b_locus.py "$V"

# Splice screen (needs a chr15 GRCh38 FASTA)
curl -O https://ftp.ensembl.org/pub/release-112/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.15.fa.gz
gunzip -k Homo_sapiens.GRCh38.dna.chromosome.15.fa.gz && mv Homo_sapiens.GRCh38.dna.chromosome.15.fa chr15.fa
python3 analysis/scripts/step12_splice_screen.py "$V" chr15.fa
python3 analysis/scripts/step12b_finalize_splice.py
python3 analysis/scripts/step12c_merge_splice.py

# Phase and CNV/SV audits
python3 analysis/scripts/step13_phase_audit.py "$V"
python3 analysis/scripts/step14_cnv_sv_audit.py "$V"

# QA
python3 analysis/scripts/step15_claim_scan.py
```

Pangolin is run via its CSV path (its VCF path is incompatible with PyVCF3 on
Python 3.12) — exact commands in [`data/splicing/README.md`](data/splicing/README.md).

### Data governance

Genotype-level outputs under `data/genomewide/`, `data/panel/`,
`data/bub1b_locus/`, `data/splicing/`, `data/provenance/*.tsv` and
`data/phase/PHASE_REPORT.md` are **gitignored** — they derive from the gated VCF
and are fully regenerable with the commands above. Summaries live in the Markdown
record. **No raw VCF, BAM or FASTQ is committed.**

### Known inconsistencies elsewhere, handled deliberately

1. ✅ [`../README.md`](../README.md) — rewritten 2026-09-16 with a Track 1 erratum.
2. ✅ [`../MVA_Hackathon_2026_Track1_METHODS.md`](../MVA_Hackathon_2026_Track1_METHODS.md) — top banner + §30 erratum; **historical body preserved intact**.
3. ⚠️ **Both submission CSVs left byte-for-byte unmodified by design** — altering a scored submission would itself destroy provenance. Originals archived under `data/provenance/`; corrections in [`TRACK1_SUBMISSION_ERRATUM.md`](TRACK1_SUBMISSION_ERRATUM.md).
