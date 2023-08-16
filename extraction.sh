# Run MTA and extract all of the monument scans

set -e 

S3PATH="$1"
SCANNAME=$(basename "$S3PATH" ".rxp.gz" )
BNAME=""
download()
{
	aws s3 cp "$1" .
	gunzip -f $(basename "$1")
	BNAME=$(basename "$1" ".rxp.gz" )
	BNAME=$(basename "$BNAME" ".rxp" )
	echo "Saved $BNAME"
}

mta()
{
	
	echo "Extracting MTAs for $BNAME"
	rimtatls -m histvar --compressed "$BNAME.rxp" "$BNAME-mta.rxp"
}

inclination()
{

	ri-inclination "$BNAME-mta.rxp" > "$BNAME-mta-inclination.txt"
}

extract()
{

	extract-diurnal-adjustment "$BNAME-mta.rxp" "$BNAME-mta-inclination.txt"
}

cache()
{
	mkdir -p monuments
	cp "$BNAME-mta-inclination.txt"  monuments
	cp "$BNAME-mta.rxp" monuments
	cp msa_pitch_params.p "monuments/$BNAME-msa_pitch_params.pickle"
	cp msa_roll_params.p "monuments/$BNAME-msa_roll_params.pickle"

}
download "$S3PATH"
mta 
inclination
extract
cache
