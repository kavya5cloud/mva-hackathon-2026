# Pitch facts — MVA Hackathon 2026 Track 2

**Purpose.** Every number, fact, conclusion and limitation below is verified and
traceable in this repository. **Nothing here is new interpretation.** If a claim
is not in this file, do not make it in the pitch.

**Evidence frozen:** 2026-09-26. **Source of record:**
[`kavya5cloud_track2_report.md`](kavya5cloud_track2_report.md) ·
[`round2_variant_characterisation.md`](round2_variant_characterisation.md) ·
[`FINAL_AUDIT.md`](FINAL_AUDIT.md)

---

## The one-line version

> A child with MVA features carries two heterozygous *BUB1B* variants. One is
> solidly pathogenic. The other is a VUS whose mechanism we could not establish —
> and our own modelling argues against the mechanism we set out to prove. Phase is
> unresolved, so **no second pathogenic allele is established**. We therefore
> report **no drug candidate**, deliberately.

---

## Verified variant facts

| | Variant 1 | Variant 2 |
|---|---|---|
| HGVS | `NM_001211.6:c.2210T>G` | `NM_001211.6:c.3006T>G` |
| Protein | **p.Leu737\*** | **p.Asn1002Lys** |
| GRCh38 | chr15:40,209,701 T>G | chr15:40,220,612 T>G |
| dbSNP | rs759242053 | rs2542593804 |
| In proband VCF | PASS, GT 0/1, DP 46, GQ 99, VAF 0.543 | PASS, GT 0/1, DP 28, GQ 99, VAF 0.464 |
| ClinVar (exact allele) | **VCV000533901 — Pathogenic/Likely pathogenic, 2-star** | **no record** |
| gnomAD | exomes 7.87e-5 | **AF 6.195e-7**, AC 1 / AN 1,614,226, 0 homozygotes |
| **Status** | **strong pathogenic evidence** | **prioritised VUS** |

- Distance between the two variants: **10,911 bp**.
- `p.Leu737*`: codon 737 `TTA` → `TGA`, verified from the Ensembl CDS; **exon 17 of 23**; PTC **746 nt** upstream of the final exon–exon junction → NMD **predicted**, *not measured*.
- **A different allele, `c.3006T>A`, also gives p.Asn1002Lys** and has a 1-star VUS ClinVar record (VCV004600147). It is **not** the patient allele and no evidence transfers from it.
- Human **L1012** ≡ mouse **L1002**. The patient variant is **human N1002K** — a different residue from the mouse L1002P / human L1012P literature allele.

## Verified provenance facts

- Proband VCF `WGS_EX2312012_HGWCNDSX7.vcf.gz`, md5 `a04ea354141cfb032872d67a11c8d2d8`, **GRCh38**, GATK 4.2.4.0, single sample, ~5.02 M variants.
- **Both variants verified present in the proband** — REF/ALT match, both PASS, both GQ 99.
- **A genome-build error was found in our own Track 1 pipeline.** The recorded extraction used `-r 15:40400000-40500000` — the **GRCh37** *BUB1B* interval — against a **GRCh38** VCF. That window has **0 bp overlap** with *BUB1B* in GRCh38 and instead contains *IVD*, *BAHD1* and *CHST14*.
- Consequence: the original Track 1 "compound heterozygous frameshift pair in *BUB1B*" is **not supported** — those variants lie in *IVD* and a lncRNA. Documented in `TRACK1_SUBMISSION_ERRATUM.md`; both scored submission CSVs preserved **byte-for-byte**.
- Correct GRCh38 *BUB1B* extraction (`15:40158984-40223137`) returns **15** variants, including both variants above.

## Verified screening facts

- Phenotype: **8 HPO terms**, extracted verbatim, including **Rhabdomyosarcoma HP:0002859**.
- Gene panel selected **objectively from that phenotype**: Genomics England PanelApp panel **290 "Familial rhabdomyosarcoma" v1.6**, where ***BUB1B* is GREEN (confidence 3), BIALLELIC***, plus panel **259 v1.30** and the brief's MVA gene set → **80 genes**.
- Genome-wide screen: **5,012,204** variants → snpEff → **11,320** PASS HIGH/MODERATE → **203 genes** with an autosomal-recessive model.
- **40 of 43** qualifying panel variants were **common polymorphisms**. Sanity check: TP53 p.Pro72Arg AF 0.748; ERCC2 p.Asp312Asn AF 0.513; XPC p.Gln939Lys AF 0.729.
- After frequency filtering, only **two** panel genes retained a rare qualifying variant: ***BUB1B*** (rare pLoF **+** a second rare allele) and **ATM** (single rare missense, **no second allele**).
- Of BUB1B, CEP57, TRIP13, BUB1, CENATAC, KNL1, BUB3, MAD2L1, TTK, CENPE — **only *BUB1B*** had any AR model.
- 99 genes carried stronger AR models; all were common polymorphisms or showed a clustered-indel artifact signature (e.g. 4 frameshifts within **61 bp** in *SERPINA1*).
- Full *BUB1B* locus scan (gene body **±50 kb**, all variant classes, PASS **and** non-PASS): **only two consequential variants exist** — the two above. No third coding, splice-region or canonical splice variant.

## Verified mechanism facts

- **DynaMut2 ΔΔG (computational, Tier 3), calibrated before interpretation:** I909T **−3.48**, L1012P **−1.80**, L844F **−1.70** (all experimentally destabilised); Q921H **−0.15** (experimentally WT-like) — **correct on 4/4**. **N1002K = −0.01**, clustering with the stable Q921H.
- → **The destabilisation hypothesis is DISFAVOURED as the primary mechanism.** This was the hypothesis we set out to prove.
- **AlphaMissense 0.9229** (likely_pathogenic) — highest in the panel, **but it fails the abundance calibration**: it cannot separate stable Q921H (0.49) from destabilised I909T (0.45), and calls destabilised L844F "likely benign".
- Conservation (measured): **N1002 invariant human → *Xenopus*** (6/6 alignable species); **phyloP100way 4.7967**; **phastCons100way 1.000**. Conserved where Q921 has diverged (Q→Y). *Zebrafish is gapped — conservation is not established to teleosts.*
- Structure (AlphaFold AF-O60566-F1-model_v6, pLDDT **91.06**): residue RSA **0.162**; **ND2 SASA 0.00 Å²**; **three hydrogen bonds, all to main chain** (W978 N 2.83 Å, V998 O 2.83 Å, W978 O 2.95 Å).
- **PP2A-B56 does not bind the pseudokinase domain** — it binds the KARD (S670/S676), **51–85 Å** away (PMID 33207204). So "N1002K disrupts PP2A-B56 binding" is **not supported**.
- N1002 is **28.6 Å** from K795 (ATP site) and **18.4 Å** from D882 — the **furthest of all seven MVA positions** from the degenerate nucleotide pocket.
- **Human BUBR1 is a pseudokinase** with no phosphotransfer activity.
- Backbone φ/ψ at N1002: **φ = −126.6°** (normal negative) — **this weakened our own helix-cap model**, since the "only Asn/Gly tolerate this backbone" argument does not apply.
- **Residue 1002 is not modelled in any experimental structure** (6tlj and 5khu resolve only ~19–345). AlphaFold is the only structural source.
- **No E3 ligase for misfolded BUBR1 has ever been identified.**

## Verified splice facts

- SpliceAI **1.3.1** and Pangolin run **independently** on the same normalised variants, locus **±50 kb**.
- *BUB1B* set = **12 deep-intronic variants + 2 coding controls = 14 records**. **All 14 NO SIGNAL.**
- **Max SpliceAI ΔS = 0.03**; **max Pangolin |Δ| = 0.03**; **14/14 concordant**; **0 REVIEW, 0 HIGH-PRIORITY**.
- Context: SpliceAI's most permissive (high-recall) reference point is **0.2** — an order of magnitude above anything observed.
- **Correction:** of the 68 variants originally counted as "intronic *BUB1B*", only **12 are *BUB1B***; the other **56 are *PAK6***, the adjacent gene.
- **No canonical `splice_acceptor`, `splice_donor` or `splice_region` variant exists in the analysed interval.**

## Verified phase and CNV/SV facts

- **Phase = UNPHASED** (formal classification). Both GT `0/1`; GATK `PGT`/`PID` declared but **both empty** at both variants; **no `PS` field**; **no shared phase set**.
- Short-read fragments (~350–550 bp) **cannot span 10,911 bp** — this is a physical limit, not a tooling choice.
- **CNV/SV = unresolved from available data.** Audit across **10 evidence classes**, all negative: no symbolic ALT alleles, 0 BND records, all SV/CNV INFO/FORMAT keys absent, not a gVCF, no usable depth track, no split-read/discordant-pair fields, **no BAM/CRAM/FASTQ**, no pre-computed CNV/SV calls.
- **`FORMAT/DP` was not used as a dosage proxy** — called-site depth is ascertainment-biased, single-sample, with no control cohort.

## Conclusions that are safe to state

1. **`p.Leu737*` has strong pathogenic evidence** (ClinVar 2-star, multiple submitters, no conflicts).
2. **`p.Asn1002Lys` is a prioritised VUS.** No functional evidence of any kind exists for it.
3. **Phase is UNPHASED.** The genotype must **not** be called compound heterozygous, biallelic, *in cis*, or *in trans*.
4. **CNV/SV status is unresolved from available data** — not excluded.
5. **No hidden splice second hit was detected**, within the limits of computational prediction.
6. ***BUB1B* was independently re-established** as the only candidate surviving an unbiased, phenotype-driven, frequency-filtered genome-wide screen.
7. **No second pathogenic *BUB1B* allele has been established**, so ***BUB1B* is a leading genetic hypothesis, not a confirmed molecular diagnosis***.
8. **Mechanism = UNKNOWN.**
9. **Therapeutic gate = CLOSED. No drug candidate is proposed** — a deliberate conclusion, not an omission.
10. **The highest-value next experiment is genetic, not mechanistic:** resolve phase (proband long-read sequencing preferred; trio genotyping where parents are available and informative) and/or *BUB1B* exon-dosage testing.

## Limitations that must be stated if the topic comes up

1. Phase is unobtainable from the available short-read data.
2. CNV/SV cannot be assessed at all from these inputs; a structural second hit **cannot be excluded**.
3. **Zero experimental assays** were performed in this project. Every mechanistic statement is computational or extrapolated from *other* *BUB1B* variants.
4. All structural work rests on a **predicted** model; residue 1002 is in no experimental structure; no molecular dynamics was run.
5. **Only one ΔΔG predictor returned values** — DDMut's API failed (no values obtained, none reported) and FoldX is unlicensed.
6. AlphaMissense, SpliceAI/Pangolin, DynaMut2 and the AlphaFold work are **all Tier 3 and correlated** — their agreement is **not** replication.
7. NMD for `p.Leu737*` is **predicted, not measured**.
8. **The MVA diagnosis itself is asserted, not evidenced** in available records — no karyotype, no chromosome counts, no premature-chromatid-separation assay; the HPO set contains no aneuploidy or PCS term.
9. Conservation is established to *Xenopus*, **not** teleosts.
10. The genome-wide screen is bounded by its filters — coding-focused, SNV/indel only, no CNV/SV, no *de novo* model without parents. **"No qualifying variant identified" is not "gene excluded."**
11. The splice screen covered ±50 kb; **distal regulatory elements were not examined**.
12. **LOVD was inaccessible** — status UNKNOWN, not negative.

## Things that must NOT be said

- ❌ "compound heterozygous" · "biallelic" · "in trans" · "in cis"
- ❌ "*BUB1B* confirmed" / "molecular diagnosis established"
- ❌ "N1002K is pathogenic" or "likely pathogenic"
- ❌ "N1002K destabilises BUBR1" · "reduces BUBR1 abundance"
- ❌ "N1002K disrupts PP2A-B56 binding"
- ❌ "N1002K is an ATP-binding or catalytic residue" · "BUBR1 kinase activity"
- ❌ "CNV/SV excluded" · "splicing excluded" · "no splice mechanism exists"
- ❌ "conserved, therefore pathogenic" · "rare, therefore pathogenic"
- ❌ "conserved to zebrafish"
- ❌ "the T>A ClinVar VUS supports our variant"
- ❌ "mouse L1002P supports human N1002K"
- ❌ any named drug, or any claim that a treatment exists

## Honest framing of the negative result

Three things we did that a reviewer can check, all of which cut **against** our
own starting position:

1. **We falsified our own mechanism.** We set out to show N1002K destabilises BUBR1; a predictor we validated on 4/4 known-outcome variants says it does not.
2. **We found and published an error in our own Track 1 submission** — a genome-build mistake that invalidated the original conclusion — and then re-derived the candidate gene from scratch rather than assuming it.
3. **We weakened our own replacement model.** The φ/ψ check removed one of the helix-cap hypothesis's supports, and we report that rather than omitting it.

**Six silent-failure bugs in our own tooling were caught and fixed** — each one a
case where an API error or parsing slip would have become a scientific claim
(`FORMAT/PS` false negative; VEP query-failure misread as "absent from gnomAD";
SpliceAI INFO-key casing; a non-atomic file rewrite; a claim-scan that reported
zero hits because zsh does not word-split unquoted variables; and a classifier
that excused its own findings). Every such path now fails loudly.
