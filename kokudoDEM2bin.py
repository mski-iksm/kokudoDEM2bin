#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import kokudolibs as kl

parser = argparse.ArgumentParser(
    description='Download and convert Japanese DEM to binary files.')
parser.add_argument("-l", "--llur",
                    help='Locate the target region by lon/lat coordinate.\
                     Input the Lower Left corner and Upper Right corner cordinate.\
                     Order must be [LL(lon) UR(lon) LL(lat) UR(lat)]',
                    nargs=4, type=float, required=True)
parser.add_argument("-nd", "--nodownload",
                    help='Set for skip downloading.',
                    action='store_true')
parser.add_argument("-ncon", "--noconnect",
                    help='Set for skip connecting json files.',
                    action='store_true')
parser.add_argument("-nc", "--noconvert",
                    help='Set for skip converting connected json file to binary.',
                    action='store_true')
parser.add_argument("-res", "--resolution",
                    help='Set resolution of output binary data.\
                    Unit is in `pixels/degree`.\
                    Default is 21600, which is equivalent to 1/6 arc second degree per pixel (i.e. ~5m).',
                    type=int, default=21600)

parser.add_argument("-nf", "--nofig",
                    help='Set for skip illustrating figure.',
                    action='store_true')
parser.add_argument("-sf", "--showfig",
                    help='Set for show figure instead of saveing as png file.',
                    action='store_true')
parser.add_argument("-min", "--vmin",
                    help='vmin value of DEM illustration. Default is None.',
                    type=float, default=None)
parser.add_argument("-max", "--vmax",
                    help='vmax value of DEM illustration. Default is None.',
                    type=float, default=None)


args = parser.parse_args()

lon_min = args.llur[0]
lon_max = args.llur[1]
lat_min = args.llur[2]
lat_max = args.llur[3]

# get coordinate tile number
ll_x, ll_y, ur_x, ur_y = kl.get_tile(lon_min, lon_max, lat_min, lat_max)

# download json files into json DIR
if args.nodownload is False:
    kl.download_json(ll_x, ll_y, ur_x, ur_y)

# connect json files
if args.noconnect is False:
    kl.connect_jsons(ll_x, ll_y, ur_x, ur_y, lat_min, lon_min)


# interpolate and convert connected json file into binary
# pixel reslution is 1/6 arc second
if args.noconvert is False:
    kl.convert_json(lat_min, lon_min, lat_max, lon_max, args.resolution)

# output fig
if args.nofig is False:
    kl.make_fig(lat_min, lon_min, lat_max, lon_max,
                args.showfig, args.vmin, args.vmax, args.resolution)
