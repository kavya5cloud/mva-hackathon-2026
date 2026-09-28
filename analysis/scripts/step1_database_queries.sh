#!/usr/bin/env bash
# step1_database_queries.sh -- reproduce every external database query used in
# Rounds 1-3, saving raw responses to analysis/data/queries/.
# All queries below were originally run 2026-09-15 / 2026-09-16.
# No API keys are required; no credentials are stored in this repository.

set -euo pipefail
OUT="analysis/data/queries"
mkdir -p "$OUT"
say() { echo; echo "### $*"; }
get() { echo "  GET $2"; curl -s "$2" -o "$OUT/$1" -w "      HTTP %{http_code}  %{size_download} bytes\n"; }

say "UniProt O60566 (domains, sites)"
get uniprot_O60566.json "https://rest.uniprot.org/uniprotkb/O60566.json"

say "AlphaFold DB entry metadata (gives current model version + URLs)"
get alphafold_O60566.json "https://alphafold.ebi.ac.uk/api/prediction/O60566"

say "Ensembl VEP - both patient variants"
get vep_c3006TG.json "https://rest.ensembl.org/vep/human/hgvs/NM_001211.6%3Ac.3006T%3EG?content-type=application/json&canonical=1&hgvs=1&numbers=1"
get vep_c2210TG.json "https://rest.ensembl.org/vep/human/hgvs/NM_001211.6%3Ac.2210T%3EG?content-type=application/json&canonical=1&hgvs=1&numbers=1"

say "Ensembl VEP + AlphaMissense - calibration panel"
for h in c.3006T\>G c.3035T\>C c.2726T\>C c.2763G\>C c.2530C\>T; do
  q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote('NM_001211.6:'+sys.argv[1],safe=''))" "$h")
  get "vep_am_${h//[^A-Za-z0-9]/_}.json" "https://rest.ensembl.org/vep/human/hgvs/${q}?content-type=application/json;AlphaMissense=1;canonical=1"
done

say "Ensembl transcript structure + CDS (ENST00000287598)"
get ensembl_tx.json  "https://rest.ensembl.org/lookup/id/ENST00000287598?expand=1;content-type=application/json"
get ensembl_cds.json "https://rest.ensembl.org/sequence/id/ENST00000287598?type=cds;content-type=application/json"

say "Ensembl Compara orthologues (aligned protein)"
get homol.json "https://rest.ensembl.org/homology/symbol/human/BUB1B?content-type=application/json;type=orthologues;sequence=protein;aligned=1;target_species=pan_troglodytes;target_species=mus_musculus;target_species=rattus_norvegicus;target_species=canis_lupus_familiaris;target_species=gallus_gallus;target_species=xenopus_tropicalis;target_species=danio_rerio"

say "BUB1B gene span - BOTH builds (the genome-build erratum)"
get bub1b_grch38.json "https://rest.ensembl.org/lookup/symbol/homo_sapiens/BUB1B?content-type=application/json"
get bub1b_grch37.json "https://grch37.rest.ensembl.org/lookup/symbol/homo_sapiens/BUB1B?content-type=application/json"
get chr15_grch38.json "https://rest.ensembl.org/info/assembly/homo_sapiens/15?content-type=application/json"
get chr15_grch37.json "https://grch37.rest.ensembl.org/info/assembly/homo_sapiens/15?content-type=application/json"
get genes_in_track1_window_grch38.json "https://rest.ensembl.org/overlap/region/human/15:40400000-40500000?feature=gene;content-type=application/json"

say "ClinVar (NCBI E-utilities)"
get clinvar_search_c3006TG.json  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BUB1B%5Bgene%5D+AND+c.3006T%3EG&retmode=json"
get clinvar_search_N1002K.json   "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BUB1B%5Bgene%5D+AND+Asn1002Lys&retmode=json"
get clinvar_summaries.json       "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=533901,4600147,3221415&retmode=json"

say "dbSNP (NCBI E-utilities) - both variants"
get dbsnp_rs759242053.json  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id=759242053&retmode=json"
get dbsnp_rs2542593804.json "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id=2542593804&retmode=json"

say "UCSC conservation at chr15:40,220,612 (hg38)"
get ucsc_phyloP100way.json    "https://api.genome.ucsc.edu/getData/track?genome=hg38;track=phyloP100way;chrom=chr15;start=40220611;end=40220612"
get ucsc_phastCons100way.json "https://api.genome.ucsc.edu/getData/track?genome=hg38;track=phastCons100way;chrom=chr15;start=40220611;end=40220612"

echo
echo "### KNOWN FAILURES (documented, not retried into fabrication)"
echo "  DDMut result endpoint     -> Internal Server Error on all polls; NO values obtained"
echo "  MaveDB BUB1B score-sets   -> {\"detail\":\"Not Found\"}; no deep mutational scan exists"
echo "  LOVD                      -> IP/network block; status UNKNOWN, not negative"
echo "  AlphaFold model_v4        -> HTTP 404 (retired); v6 used instead"
echo "  ClinVar 'p.*NNNN' syntax  -> invalid; returns 0 even for codons with known records"
echo
echo "raw responses in $OUT/"
