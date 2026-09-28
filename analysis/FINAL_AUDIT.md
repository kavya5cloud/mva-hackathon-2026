# Final audit — MVA Hackathon 2026 Track 2

**Date: 2026-09-26.** Scientific analysis frozen. No new biological analyses,
drug searches, structural predictions, or reinterpretations were performed in this
pass.

---

## 1. Audit scope

A consistency, provenance, reproducibility and terminology audit of the complete
Track 2 analysis directory, plus the repository-root files it depends on. The
audit checked for:

broken paths · stale filenames · references to deleted files · references to the
superseded *BUB1B* interval · claims that phase is *cis*/*trans* · claims that
`p.Asn1002Lys` is pathogenic · claims of compound heterozygosity or biallelic
status · claims that CNV/SV has been excluded · claims that splice mechanisms are
completely excluded · drug candidates presented as recommendations · stale
"68 BUB1B intronic variants" wording · terminology drift between reports.

**Explicitly out of scope:** rewriting historical Track 1 material to make it
look cleaner. Historical provenance and errata are preserved (§5).

---

## 2. Files inspected

**19 Python scripts, 2 shell scripts** — all in `analysis/scripts/`:
`step0_verify_provenance` · `step1_database_queries.sh` · `step4_structure_gate` ·
`step5_contacts` · `step5b_ddg_panel.sh` · `step6_conservation` ·
`step9_structural_network` · `step11_phi_psi` · `step12_splice_screen` ·
`step12b_finalize_splice` · `step12c_merge_splice` · `step13_phase_audit` ·
`step14_cnv_sv_audit` · `step15_claim_scan` · `build_gene_panel` ·
`screen_panel_ar` · `annotate_candidates_af` · `screen_genomewide_ar` ·
`check_strong_ar_genes` · `scan_bub1b_locus` · `rank_genomewide_ar` *(superseded, retained)*

**18 committed Markdown documents**, including `kavya5cloud_track2_report.md`,
`round2_variant_characterisation.md` (the full Rounds 1–6 evidence record),
`TRACK1_SUBMISSION_ERRATUM.md`, the decision matrices, the phase and CNV/SV
reports, `PHENOTYPE.md`, `splicing/README.md`, and both repository READMEs.

**Data and provenance artefacts:** `environment.txt`, `data/README.md`,
`data/provenance/` (archived originals + redacted VCF header), `data/panel/`
(PanelApp responses, gene panel, BED), `data/step4_results.json`,
`data/homol.json`, `data/BUBR1_kinase_766_1050.pdb`.

**Genotype-level outputs** under `data/genomewide/`, `data/panel/`,
`data/bub1b_locus/`, `data/splicing/`, `data/phase/PHASE_REPORT.md` and
`data/provenance/*.tsv` — all verified **gitignored**.

---

## 3. Stale / inconsistent claims found

| # | Finding | Location | Severity |
|---|---|---|---|
| 1 | **Executive summary predated Rounds 4–6.** It described only the Round 1–3 work and did not mention the independent genome-wide re-establishment of *BUB1B*, the splice screen, or the phase/CNV audits. It also presented the helix C-cap model as reconciling the evidence **without the φ/ψ caveat that weakened it** | `kavya5cloud_track2_report.md` §1 | **Material — internal inconsistency** |
| 2 | **§16 Final Conclusion likewise predated Rounds 4–6** and asserted the helix-cap model without the φ/ψ qualification | `kavya5cloud_track2_report.md` §16 | **Material — internal inconsistency** |
| 3 | **The φ/ψ result was recorded in the evidence record but never carried into the report's structural section**, so §5 presented the helix-cap model unqualified | `kavya5cloud_track2_report.md` §5 | **Material — omission** |
| 4 | **§6 stated the helix-cap model "explains why these are compatible"** — too strong for a computational model whose support had been weakened | `kavya5cloud_track2_report.md` §6 | Moderate — overstatement |
| 5 | **The archived pre-erratum README carried no historical banner.** A reader opening it directly would see an unqualified "compound heterozygous frameshift pair in *BUB1B*" claim with nothing marking it superseded | `data/provenance/README_original_pre-erratum.md` | **Material — could be misread as current** |
| 6 | **A trio-outcome table read as assertive.** A row stated "**in trans — compound heterozygous CONFIRMED**"; although the surrounding prose was conditional, the row could be extracted as a claim. No trio data exist | `round2_variant_characterisation.md` §R3.2.3 | Moderate — extractable misstatement |
| 7 | **The claim-scan itself produced a false all-clear.** A shell version reported 0 hits for all 16 terms — including "drug candidate", which demonstrably appears — because **zsh does not word-split unquoted variables**, leaving the file list empty | QA tooling | **Material — QA integrity** |

**Not found (verified absent):** broken paths or links (all resolve); references
to deleted files; stale "68 BUB1B intronic" wording presented as current (the only
occurrences are the corrections themselves); any current claim that phase is
*cis*/*trans*; any claim that `p.Asn1002Lys` is pathogenic or likely pathogenic;
any claim that CNV/SV or splicing has been *excluded*; any drug candidate
presented as a recommendation.

---

## 4. Corrections made

| # | Correction | Method |
|---|---|---|
| 1 | **Executive summary rewritten.** Now covers both variants, the strong/VUS asymmetry, the independent genome-wide re-derivation, the splice screen, unresolved phase and CNV/SV, *BUB1B* as leading hypothesis rather than confirmed diagnosis, unresolved mechanism, no therapeutic candidate, and the genetic next experiment | Replaced §1 |
| 2 | **§16 Final Conclusion rewritten** to reflect Rounds 4–6 and to state the φ/ψ weakening explicitly | Replaced §16 |
| 3 | **φ/ψ caveat added to §5**, including the verified fact that residue 1002 is **not modelled in any experimental structure** (6tlj/5khu resolve only ~19–345) | Inserted into §5 |
| 4 | **§6 wording softened** from "explains why these are compatible" to "offers a way these could be compatible — though that model is computational only, and the φ/ψ result in §5 weakens it" | In-place edit |
| 5 | **Historical banner prepended** to the archived pre-erratum README, marking it SUPERSEDED and pointing to the erratum and current README. **The archived content below the banner is byte-for-byte unchanged** | Prepend only |
| 6 | **Trio table made explicitly hypothetical** — headed "*(Hypothetical outcomes. No trio data exist for this proband; nothing in this table has been observed.)*", column renamed "Inference **if** observed", and "CONFIRMED"/"FALSIFIED" replaced with "would be established" | In-place edit |
| 7 | **Claim scan rewritten in Python** (`step15_claim_scan.py`) with a hard guard that aborts on an empty file list, a control-term check, a context window for multi-line prohibitions, and file-level detection of historical banners. It now classifies hits as GENUINE / FALSE POSITIVE / HISTORICAL | New script |

**No scientific conclusion was changed.** Every correction was an
internal-consistency or presentation fix.

---

## 5. Intentionally preserved historical material

Preserved deliberately, **not** cleaned up:

| Artefact | Why preserved | How labelled |
|---|---|---|
| `MVA_Hackathon_2026_Track1_METHODS.md` | The Track 1 methods record as submitted. Rewriting it would destroy provenance | Top banner ("HISTORICAL DOCUMENT — READ THE ERRATUM FIRST") + §30 Genome-Build / Provenance Erratum. **19 historical compound-heterozygous references retained** |
| `kavya5cloud_bub1b-compound-het-frameshift.csv` | Scored submission artefact | **Byte-for-byte unchanged** (verified by `diff` and git). Correction documented in `TRACK1_SUBMISSION_ERRATUM.md` |
| `kavya5cloud_submission3_bub1b_compoundhet.csv` | Scored submission artefact | **Byte-for-byte unchanged** (verified). Coordinates confirmed correct; only the "compound-heterozygous" interpretation is corrected, in the erratum |
| `data/provenance/README_original_pre-erratum.md` | `README.md` before the 2026-09-16 correction | Historical banner added above; **content unchanged** |
| `data/provenance/gitignore_original.txt` | `.gitignore` before the scope fix | Archived |
| `data/DECISION_MATRIX.md` | Round 4 decision matrix | Retained and labelled superseded by `DECISION_MATRIX_UPDATED.md` |
| `scripts/rank_genomewide_ar.py` | Superseded by `check_strong_ar_genes.py` after VEP rate-limiting | Retained with an in-file note, **not deleted** |
| Verbatim CSV quotes inside `TRACK1_SUBMISSION_ERRATUM.md` | The erratum's purpose is to record what was claimed | Quoted as original records |

---

## 6. Final scientific state

```
Leu737* = strong pathogenic evidence.
N1002K = prioritised VUS.
Phase = UNPHASED.
CNV/SV = unresolved from available data.
BUB1B = leading genetic hypothesis, not confirmed molecular diagnosis.
Mechanism = UNKNOWN.
Therapeutic gate = CLOSED.
No drug candidate proposed.
```

**No contradiction with this state was found anywhere in the existing evidence.**

---

## 7. Unresolved limitations

1. **Phase is UNPHASED** and unobtainable from the available short-read data — the variants are 10,911 bp apart. Requires trio genotyping or long-read sequencing.
2. **CNV/SV is unresolved from available data.** No dosage or structural evidence of any type exists. A structural second hit in *BUB1B* cannot be excluded.
3. **No functional evidence for `p.Asn1002Lys` exists** — no publication, no assay, and no deep mutational scan of *BUB1B* in MaveDB.
4. **The splice screen is a computational negative.** It does not exclude branchpoint or pseudoexon mechanisms, detects no structural variation, and did not examine regulatory elements beyond ±50 kb.
5. **All structural work rests on a predicted model.** Residue 1002 is not present in any experimental structure. No molecular dynamics was run.
6. **Only one ΔΔG predictor returned values** — DDMut's API failed and FoldX is unlicensed. A single well-calibrated predictor is weaker than a consensus.
7. **NMD for `p.Leu737*` is predicted, not measured.** Patient RNA would be required.
8. **The MVA diagnosis is asserted, not evidenced** in available records: no karyotype, no chromosome-count data, and no premature-chromatid-separation assay. The HPO set contains no aneuploidy or PCS term.
9. **The genome-wide screen is bounded by its filters** — coding-focused, SNV/indel only, no CNV/SV, and no *de novo* model possible without parental samples. "No qualifying variant identified" is not "gene excluded".
10. **Conservation is established to *Xenopus*, not teleosts** — the zebrafish orthologue is gapped across the region.
11. **LOVD remains inaccessible** (network block). Status UNKNOWN, not negative.
12. **Environment side-effect:** installing TensorFlow for the splice screen upgraded `protobuf` in the base anaconda environment, which pip reports as incompatible with pre-existing `mediapipe` and `streamlit`. Unrelated to this project but recorded in `environment.txt`.

---

## 8. Final claim-scan result

`analysis/scripts/step15_claim_scan.py`, run 2026-09-26 over all **18 committed
Markdown files**, searching 16 dangerous/stale terms.

```
TOTAL hits: 128   GENUINE: 8   FALSE POSITIVE: 99   HISTORICAL: 21
```

**All 8 "genuine" hits were individually reviewed and are correct in context:**

| Location | Term | Why it is correct |
|---|---|---|
| `FINAL_AUDIT.md`:70 | drug candidate | This document's own audit-scope list ("any drug candidate presented as a recommendation") |
| `kavya5cloud_track2_report.md`:108 | biallelic | Gene-level fact: "*BUB1B* … whose **biallelic** loss causes MVA syndrome 1". A statement about the gene–disease relationship, **not** about this proband |
| `TRACK1_SUBMISSION_ERRATUM.md`:57, 91 | compound heterozygous | **Verbatim quotes of the original CSV records**, reproduced because documenting them is the erratum's purpose |
| `NEXT_STEP_TREE.md`:13 | in trans | Branch label `+-- IN TRANS` in the decision tree — a hypothetical outcome, in the structure specified for that document |
| `splicing/README.md`:14 · `round2…md`:1588 | 68 intronic BUB1B | **The corrections themselves**, quoting the stale Round 4 wording in order to correct it to 12 |
| `round2…md`:1061 | biallelic | Gene-level fact: "Biallelic *BUB1B* LoF causes **MVA syndrome 1** (MIM 257300)" |

**Zero genuine problematic claims remain.** No current document asserts
compound heterozygosity, biallelic status, *cis*/*trans* phase, `p.Asn1002Lys`
pathogenicity, exclusion of CNV/SV or splicing, or any drug candidate.

**21 historical hits** sit in two files that carry explicit self-declaring
SUPERSEDED banners (`MVA_Hackathon_2026_Track1_METHODS.md`,
`data/provenance/README_original_pre-erratum.md`) and are **preserved
deliberately, not rewritten**.

### Two QA-tooling bugs found and fixed during this pass

1. **False all-clear.** A shell version of the scan reported 0 hits for all 16 terms — including "drug candidate", which demonstrably appears — because **zsh does not word-split unquoted variables**, so the file list was empty. Rewritten in Python with a hard guard that aborts on an empty list plus a control-term check that must be found.
2. **Historical misclassification.** The first classifier treated any file mentioning "historical" in its opening lines as a historical artifact, which wrongly excused this audit document's own 13 hits. The banner test now requires a **self-declaring** marker in a heading, blockquote or HTML comment, with an additional guard for files that declare themselves current.

*(These are the fifth and sixth silent-failure modes caught in this project —
cf. `FORMAT/PS` in §R3.11, VEP `QUERY_FAILED` in §R4.4, and the SpliceAI INFO-key
casing and non-atomic rewrite in `data/splicing/README.md`. Every such path now
fails loudly.)*
