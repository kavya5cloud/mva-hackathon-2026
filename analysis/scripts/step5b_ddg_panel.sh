#!/usr/bin/env bash
# step5b_ddg_panel.sh -- reproduce the DynaMut2 ddG calibration panel.
#
# Endpoint : https://biosig.lab.uq.edu.au/dynamut2/api/prediction_single
# Structure: analysis/data/BUBR1_kinase_766_1050.pdb  (pseudokinase domain 766-1050
#            excised from AlphaFold AF-O60566-F1-model_v6.pdb,
#            source md5 943e5596717db0424b1a020ae429e174)
# Chain    : A       Sign convention: negative ddG = destabilising
# Retrieved: 2026-09-15
#
# Results obtained on 2026-09-15 (job IDs recorded for re-fetch):
#   N1002K  job 178949565796  ddG = -0.01   <- variant of interest
#   L1012P  job 178949566104  ddG = -1.80   (experimentally destabilised)
#   I909T   job 178949566347  ddG = -3.48   (experimentally destabilised)
#   Q921H   job 178949566629  ddG = -0.154  (experimentally stable / WT-like)
#   L844F   job 178949566886  ddG = -1.697  (experimentally reduced abundance)
#
# DDMut (independent predictor) was also attempted on the same structure; its
# RESULT endpoint returned {"message": "Internal Server Error"} on every poll for
# all five jobs. NO DDMut VALUES WERE OBTAINED and none are reported anywhere.
# FoldX is not licensed in this environment. Predictors are never averaged.

set -euo pipefail
PDB="${1:-analysis/data/BUBR1_kinase_766_1050.pdb}"
OUT="analysis/data/ddg"
API="https://biosig.lab.uq.edu.au/dynamut2/api/prediction_single"
mkdir -p "$OUT"

echo "structure: $PDB"
echo "md5:       $(md5 -q "$PDB" 2>/dev/null || md5sum "$PDB" | cut -d' ' -f1)"
echo "date:      $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

for M in N1002K L1012P I909T Q921H L844F; do
  JOB=$(curl -s -X POST "$API" -F "pdb_file=@${PDB}" -F "mutation=${M}" -F "chain=A" -m 120 \
        | python3 -c 'import json,sys; print(json.load(sys.stdin).get("job_id",""))')
  echo "${M}: submitted job ${JOB}"
  echo "${M} ${JOB}" >> "$OUT/job_ids.txt"
done

echo; echo "waiting 120s for jobs to complete..."; sleep 120

echo; echo "mutation  ddG(kcal/mol)"
while read -r M JOB; do
  R=$(curl -s "${API}?job_id=${JOB}" -m 60)
  echo "$R" > "$OUT/dynamut2_${M}.json"
  printf "%-9s %s\n" "$M" "$(echo "$R" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("prediction","PENDING/ERROR"))')"
done < "$OUT/job_ids.txt"

echo; echo "raw JSON saved to $OUT/"
