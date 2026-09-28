# BUB1B splice screen — SpliceAI + Pangolin

**Executed 2026-09-24.** Purpose: test for a hidden cryptic-splice second hit in
*BUB1B*, one of the two remaining hidden-variant classes under CASE B (the other,
CNV/SV, remains unaddressable from this VCF — see `../SV_CNV_AVAILABILITY.md`).

**Result: NO hidden splice second hit. All 14 BUB1B records score NO SIGNAL under
both tools, with 14/14 concordance.**

---

## Correction to the Round 4 record

Round 4 described *"68 intronic BUB1B variants"*. Re-checking the snpEff gene
assignment shows **only 12 of those 68 are annotated to BUB1B**; the other **56
are PAK6**, the adjacent gene (BUB1B and PAK6 overlap at the 3′ end and form the
BUB1B-PAK6 readthrough locus, ENSG00000259288).

All 68 were screened regardless. The BUB1B conclusion rests on **12 intronic
variants + 2 coding controls** (`p.Leu737*`, `p.Asn1002Lys`) = **14 records**.

---

## Input

| Item | Value |
|---|---|
| Source VCF | `WGS_EX2312012_HGWCNDSX7.vcf.gz` (gated), md5 `a04ea354141cfb032872d67a11c8d2d8` |
| Build | **GRCh38**, contig naming `15` (no `chr` prefix) |
| Locus extracted | `15:40110984-40271137` (BUB1B gene body ±50 kb) |
| Variants extracted | 172 |
| After normalization | **175** (3 multiallelic sites split, 2 realigned, 0 mismatch-removed, 0 skipped) |
| Reference FASTA | Ensembl release-112 `Homo_sapiens.GRCh38.dna.chromosome.15.fa.gz` → `chr15.fa` (103,691,101 bytes). REF bases verified to match at 15:40209701(T), 15:40220612(T), 15:40168264(G). |

```bash
bcftools view -r 15:40110984-40271137 $VCF -Ov -o locus_raw.vcf
bcftools norm -f chr15.fa -m -any locus_raw.vcf -Ov -o locus_normalized.vcf
#   Lines total/split/joined/realigned/mismatch_removed/dup_removed/skipped: 172/3/0/2/0/0/0
```

## SpliceAI

| Item | Value |
|---|---|
| Version | **SpliceAI 1.3.1** (`pip install spliceai`) |
| Backend | TensorFlow **2.21.0**, Keras **3.15.1**, pyfaidx 0.9.0.4, Python 3.12.7 |
| Annotation | bundled `grch38.txt` (BUB1B: 23 exons, 40161025–40221136; PAK6: 40217448–40276396) |
| Parameters | `-A grch38 -D 500 -M 0` |
| Date | 2026-09-24 |

```bash
python3 -m spliceai -I locus_normalized.vcf -O spliceai_output.vcf \
    -R chr15.fa -A grch38 -D 500 -M 0
```

INFO format: `SpliceAI=ALLELE|SYMBOL|DS_AG|DS_AL|DS_DG|DS_DL|DP_AG|DP_AL|DP_DG|DP_DL`

## Pangolin

| Item | Value |
|---|---|
| Version | **Pangolin** (GitHub `tkzeng/Pangolin`, installed 2026-09-24) |
| Backend | PyTorch **2.9.1** (CPU), pyfastx 2.3.1, gffutils, PyVCF3 |
| Annotation | **GENCODE v44** chr15 subset → gffutils DB (`gencode_v44_chr15.db`); `chr15` renamed to `15` to match the VCF/FASTA |
| Parameters | `-d 500` (matched to SpliceAI's window) |
| Date | 2026-09-24 |

```bash
python3 -m pangolin.pangolin pangolin_input.csv chr15.fa gencode_v44_chr15.db pangolin_out -d 500
```

**Note — why the CSV path was used.** Pangolin's VCF path crashed with
`TypeError: Info.__new__() missing 1 required positional argument: 'type_code'`:
Pangolin targets the unmaintained PyVCF, whose `_Info` signature differs in
PyVCF3 (the only version installable on Python 3.12). Pangolin's documented CSV
input path bypasses that code entirely. **The CSV was generated from the same
normalized VCF, preserving exact CHROM/POS/REF/ALT**, so both tools saw identical
input. This is a tool-compatibility workaround, not a change of data.

Output format per gene: `<ENSG>|<pos>:<largest_increase>|<pos>:<largest_decrease>|Warnings:`
Gene IDs at this locus: `ENSG00000156970`=BUB1B, `ENSG00000137843`=PAK6,
`ENSG00000259288`=BUB1B-PAK6 readthrough. Only the **BUB1B** context is used.

## Status codes (failures are never scored as zero)

| Code | Meaning |
|---|---|
| `NO SIGNAL` / `LOW PRIORITY` / `REVIEW` / `HIGH-PRIORITY SPLICE CANDIDATE` | successful prediction, triage bucket by score |
| `UNSUPPORTED_VARIANT` | variant outside every annotated transcript — the tool legitimately declines to score it |
| `PREDICTION_UNAVAILABLE` | inside a transcript but unscored — would require investigation |
| `TOOL_FAILURE` | non-zero exit / crash |

**Prioritisation thresholds** (triage buckets, **not** pathogenicity classifications;
final category uses the higher of the two tools, i.e. conservative):
`<0.05` NO SIGNAL · `0.05–0.20` LOW PRIORITY · `0.20–0.50` REVIEW · `≥0.50` HIGH-PRIORITY.
SpliceAI authors' reference points: 0.2 high recall, 0.5 recommended, 0.8 high precision.

## Overall counts (all 176 annotation records, both genes)

| Status | n |
|---|---|
| NO SIGNAL | 97 |
| UNSUPPORTED_VARIANT (outside every annotated transcript) | 77 |
| LOW PRIORITY | 2 (both **PAK6**: 15:40240313 T>C donor_loss 0.06; 15:40264484 A>G donor_gain 0.05) |
| REVIEW / HIGH-PRIORITY | **0** |
| TOOL_FAILURE | 0 |

The 77 unsupported variants all lie at 40,111,456–40,158,208 — entirely upstream
of the BUB1B transcript start (40,161,025) and outside PAK6. Both tools declined
them for the same reason, independently.

## Canonical splice-region variants (inspected separately, per the brief)

**None exist.** The BUB1B locus scan found **zero** variants annotated
`splice_acceptor`, `splice_donor`, or `splice_region` — at any FILTER level. All
12 BUB1B intronic variants are **deep intronic** (nearest is c.2679−925; range
c.180−1798 to c.1058+1762).

## Files

| File | Contents |
|---|---|
| `locus_raw.vcf` / `locus_normalized.vcf` | input before/after `bcftools norm` |
| `spliceai_output.vcf` | raw SpliceAI output (98 annotated records) |
| `spliceai_run.log` | stdout + stderr of the SpliceAI run |
| `spliceai_parsed.tsv` / `.json` | parsed, all 176 records, refined status codes |
| `pangolin_input.csv` / `pangolin_out.csv` | Pangolin input and raw output |
| `bub1b_splice_final.tsv` | SpliceAI + population AF, BUB1B only |
| `bub1b_splice_merged.tsv` | **final table** — SpliceAI + Pangolin + concordance |

Genotype-level files here are gitignored (gated-data governance); all are
regenerable with the commands above.

## Bugs found and fixed during this run (recorded, not hidden)

1. **Case-sensitivity parsing bug.** The parser matched `SPLICEAI=` but SpliceAI
   writes `SpliceAI=`. The first parse reported **175/175 PREDICTION_UNAVAILABLE**
   — i.e. it would have looked like "no splice data" when the model had in fact
   run correctly. Now matched case-insensitively, with a guard that loudly trips
   if 0 records carry a usable score.
2. **Destructive rewrite.** `step12b` opened `spliceai_parsed.tsv` with `"w"` and
   then raised mid-write, leaving the file **truncated**; the next run silently saw
   0 BUB1B records. Rewrites are now atomic (temp file + `os.replace`). The raw
   `spliceai_output.vcf` was untouched, so nothing was lost.

*(This is the third and fourth instance in this project of a silent failure
nearly becoming a scientific claim — cf. the `FORMAT/PS` false negative in §R3.11
and the VEP `QUERY_FAILED`/absent conflation in §R4.4.)*
