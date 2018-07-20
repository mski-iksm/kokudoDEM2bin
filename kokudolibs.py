#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import urllib.request
import urllib.error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
import numpy as np
import matplotlib.pyplot as plt
import _tkinter
import itertools
from multiprocessing import Pool, Process, cpu_count
import json
import shutil
from mpl_toolkits.axes_grid1 import make_axes_locatable


def get_tile(lon_min, lon_max, lat_min, lat_max):
    # input lats/lons should be 0.01
    ll_x = int(lon2x(lon_min))  # small x
    ur_x = int(lon2x(lon_max))  # large x
    ll_y = int(lat2y(lat_min))  # large y
    ur_y = int(lat2y(lat_max))  # small y
    print("ll_x, ll_y, ur_x, ur_y:", ll_x, ll_y, ur_x, ur_y)
    print("comming in {} tiles".format((ur_x - ll_x + 1) * (ll_y - ur_y + 1)))
    return ll_x, ll_y, ur_x, ur_y


def lon2x(lon):
    x = (lon + 180) * 2**18 / 360
    return x


def x2lon(x):
    lon = x * 360 / (2**18) - 180
    return lon


def lat2y(lat):
    l = math.atanh(math.sin(math.radians(85.0511)))
    y = (1 - (math.atanh(math.sin(math.radians(lat))) / l)) * (2**17)
    return y


def y2lat(y):
    l = math.atanh(math.sin(math.radians(85.0511)))
    phi = math.asin(math.tanh((1 - y * 2**(-17)) * l))
    return math.degrees(phi)


def download_json(ll_x, ll_y, ur_x, ur_y):
    # download 1 tile outside target area
    xylist = list(itertools.product(
        range(ll_x - 1, ur_x + 2), range(ur_y - 1, ll_y + 2)))
    list(map(downoad_iter, xylist))


def downoad_iter(arg):
    x = arg[0]
    y = arg[1]

    savename = "json/{}_{}.geojson".format(x, y)

    if os.path.exists(savename) is False:
        for filetype in ["5a", "10b"]:
            filename = "https://cyberjapandata.gsi.go.jp/xyz/experimental_dem{}/18/{}/{}.geojson".format(
                filetype, x, y)

            try:
                urllib.request.urlretrieve(filename, savename)
                print("{} file found at {}".format(filetype, filename))
                break
            except urllib.error.HTTPError as e:
                print("no {} file found at {}".format(filetype, filename))
                if filetype == "10b":
                    shutil.copy2("./json/default_json.geojson", savename)

    else:
        print("json file for {} {} arleady exists".format(x, y))


def connect_jsons(ll_x, ll_y, ur_x, ur_y, lat_min, lon_min):
    # connect target json files
    # use python native json instead of gdal commands
    connected_json_features = []
    for x in range(ll_x - 1, ur_x + 2):
        for y in range(ur_y - 1, ll_y + 2):
            jsonfilename = "json/{}_{}.geojson".format(x, y)
            print("connecting {}".format(jsonfilename))
            file = open(jsonfilename, "r")
            jsondata = json.loads(file.read())["features"]
            connected_json_features = connected_json_features + jsondata
            file.close()

    new_json_dic = {'type': 'FeatureCollection',
                    'features': connected_json_features}
    str_lat_min = str(lat_min).replace('.', '_')
    str_lon_min = str(lon_min).replace('.', '_')
    new_json_name = "connected_json/{}_{}.geojson".format(lat_min, lon_min)
    new_json_file = open(new_json_name, "w")
    json.dump(new_json_dic, new_json_file, indent=4)
    new_json_file.close()


def convert_json(lat_min, lon_min, lat_max, lon_max, resolution):
    # connected_json -> bin
    xsize = int(resolution * (lon_max - lon_min))
    ysize = int(resolution * (lat_max - lat_min))
    jsonname = "connected_json/{}_{}.geojson".format(lat_min, lon_min)
    binname = "bin/{}_{}.bin".format(lat_min, lon_min)
    script = "gdal_grid -ot Float32 -of ENVI -l OGRGeoJSON -zfield alti -a nearest -txe {} {} -tye {} {} -outsize {} {} {} {}".format(
        lon_min, lon_max, lat_min, lat_max, xsize, ysize, jsonname, binname)
    print(script)
    os.system(script)


def make_fig(lat_min, lon_min, lat_max, lon_max, showfig, vmin, vmax, resolution):
    binname = "bin/{}_{}.bin".format(lat_min, lon_min)
    if os.path.exists(binname):
        print("illustraing {}".format(binname))
        xsize = int(resolution * (lon_max - lon_min))
        ysize = int(resolution * (lat_max - lat_min))
        bindata = np.fromfile(
            binname, dtype="float32").reshape([ysize, xsize])

        plt.close()
        fig, ax = plt.subplots()
        image = ax.imshow(np.flipud(bindata), vmin=vmin, vmax=vmax)
        ax.axis("image")

        divider = make_axes_locatable(ax)
        ax_cb = divider.new_horizontal(size="3%", pad=0.05)
        fig.add_axes(ax_cb)
        plt.colorbar(image, cax=ax_cb)

        #plt.imshow(np.flipud(bindata), vmin=vmin, vmax=vmax)
        # plt.colorbar()
        figname = "fig/{}_{}.png".format(lat_min, lon_min)

        if showfig:
            plt.show()
        else:
            plt.savefig(figname)
