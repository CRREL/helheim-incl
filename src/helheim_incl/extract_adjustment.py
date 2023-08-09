
import os
from helheim_incl.incl import *
import pickle



def main():
    import argparse

    parser = argparse.ArgumentParser(description="Extract STAC catalog for USGS 3DEP EPT PDS")
    parser.add_argument("msa_pnts_file", type=str, help="LAS file to apply corrections to")
    parser.add_argument("msa_incl_file", type=str, help="Text file produced from ri-inclination from MTAd LAZ file")

    args = parser.parse_args()

    # Only need to compute the SOP MSA modeled inclination once
    msa_it, msa_roll, msa_pitch = get_incl(args.msa_incl_file)
    msa_array = get_pnts(args.msa_pnts_file)
    msa_phi = get_phi(msa_it, msa_array["GpsTime"], msa_array["X"], msa_array["Y"])
    msa_roll_params = fit_model(msa_phi, msa_roll)
    msa_pitch_params = fit_model(msa_phi, msa_pitch)

    pickle.dump( msa_roll_params, open( "msa_roll_params.p", "wb" ) )
    pickle.dump( msa_pitch_params, open( "msa_pitch_params.p", "wb" ) )


if __name__=='__main__':

    main()



