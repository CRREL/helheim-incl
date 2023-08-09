
import os
from helheim_incl.incl import *


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Extract STAC catalog for USGS 3DEP EPT PDS")
    parser.add_argument("msa_roll_params", type=str, help="Python pickle output from extract_adjustment for roll parameters")
    parser.add_argument("msa_pitch_params", type=str, help="Python pickle output from extract_adjustment for pitch parameters")
    parser.add_argument("data_dir", type=str, help="output data directory")
    parser.add_argument("sop_file", type=str, help="SOP file")
    parser.add_argument("pop_file", type=str, help="POP file")
    parser.add_argument("--save_unadjusted", type=bool, default=False, help="")
    parser.add_argument("laz_file", type=str, help="Points to apply adjustment to")
    parser.add_argument("incl_file", type=str, help="-incl.txt file extracted by ri-inclination from original RXP data")

    args = parser.parse_args()

    with open(args.msa_roll_params, 'rb') as f:
        msa_roll_params = pickle.load(f)
    with open(args.msa_pitch_params, 'rb') as f:
        msa_pitch_params = pickle.load(f)

    # LAZ and inclination filenames
    basename, _ = os.path.splitext(os.path.basename(args.laz_file))


    print("Processing {}".format(args.laz_file))

    # Read in point and inclination data
    array = get_pnts(args.laz_file)
    it, roll, pitch = get_incl(args.incl_file)

    # Optionally convert unadjusted points to UTM, save
    if args.save_unadjusted:
        no_adj(np.copy(array), args.sop_file, args.pop_file, args.data_dir, basename)

    # Adjust points, convert to UTM, save
    tr_warp_adj(array, it, roll, pitch,
                msa_roll_params, msa_pitch_params,
                args.sop_file, args.pop_file, args.data_dir, basename)

if __name__=='__main__':

    main()








