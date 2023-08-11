#!/bin/bash



# cat monuments-south.txt | ./compute-monuments.sh

# Given a list of scan IDs provided in the input as one per line, 
# this will output dirurnal correction data for a monument scan

# 150916_180221-msa_pitch_params.p
# 150916_180221-msa_roll_params.p
# 150916_180221.rxp
# 150916_180221.rxp-incl.txt

S3_PATH="s3://grid-glacierscans/flat/original-scans/ATLAS-South"

test -t 0 && exec < <(printf '%s\n' "$@")
while IFS= read -r line; do
    MONUMENT_ID="$line"
    S3_LOCATION="$S3_PATH/$MONUMENT_ID.rxp.gz"
    echo "fetching $S3_LOCATION"
    FILENAME=$(basename "$S3_LOCATION")
    aws s3 cp $S3_LOCATION .
    gunzip -f $FILENAME
    FILENAME=$(basename $FILENAME .gz)
    MSA="$(basename $FILENAME .rxp)-msa.rxp"
    rimtatls -m histvar --compressed "$FILENAME" "$MSA"
    ri-inclination  $MSA > $MSA-incl.txt
    extract-diurnal-adjustment $MSA "$MSA-incl.txt"
    mv msa_pitch_params.p "$MONUMENT_ID-msa_pitch_params.p"
    mv msa_roll_params.p "$MONUMENT_ID-msa_roll_params.p"

done
