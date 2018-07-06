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


def get_tile(lon_min, lon_max, lat_min, lat_max):
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
    L = math.atanh(math.sin(math.radians(85.0511)))
    y = (1 - (math.atanh(math.sin(math.radians(lat))) / L)) * (2**17)
    return y


def y2lat(y):
    L = math.atanh(math.sin(math.radians(85.0511)))
    phi = math.asin(math.tanh((1 - y * 2**(-17)) * L))
    return math.degrees(phi)


def download_json(ll_x, ll_y, ur_x, ur_y):
    xylist = list(itertools.product(
        range(ll_x, ur_x + 1), range(ur_y, ll_y + 1)))
    n = cpu_count()
    p = Pool(n * 2)
    p.map(downoad_iter, xylist)
    p.close()
    p.terminate()


def downoad_iter(arg):
    x = arg[0]
    y = arg[1]

    fname5a = "json/{}_{}_{}.geojson".format(x, y, "5a")
    fname10b = "json/{}_{}_{}.geojson".format(x, y, "10b")

    if (os.path.exists(fname5a) is False) and (os.path.exists(fname10b) is False):
        for filetype in ["5a", "10b"]:
            filename = "https://cyberjapandata.gsi.go.jp/xyz/experimental_dem{}/18/{}/{}.geojson".format(
                filetype, x, y)
            savename = "json/{}_{}_{}.geojson".format(x, y, filetype)

            try:
                print("{} file found at {}".format(filetype, filename))
                urllib.request.urlretrieve(filename, savename)
                break
            except urllib.error.HTTPError as e:
                print("no {} file found at {}".format(filetype, filename))

    else:
        print("json file for {} {} arleady exists".format(x, y))


def connectbins(ll_x, ll_y, ur_x, ur_y, maxsize):
    for box_x in range(ll_x, ur_x + 1, maxsize):
        for box_y in range(ur_y, ll_y + 1, maxsize):
            outname = "connected_bin/{}_{}.bin".format(box_x, box_y)
            if os.path.exists(outname):
                os.remove(outname)

            box_x_max = min(box_x + maxsize, ur_x + 1)
            box_y_max = min(box_y + maxsize, ll_y + 1)
            outdata = np.ones((box_x_max - box_x) * (box_y_max - box_y) * 30 * 30
                              ).reshape(((box_y_max - box_y) * 30, (box_x_max - box_x) * 30)) * (-1e20)
            for ix, x in enumerate(range(box_x, box_x_max)):
                for iy, y in enumerate(range(box_y, box_y_max)):
                    for filetype in ["5a", "10b"]:
                        binname = "bin/{}_{}_{}.bin".format(x, y, filetype)
                        if os.path.exists(binname):
                            print("connecting {}".format(binname))
                            bindata = np.fromfile(
                                binname, dtype="float32").reshape((30, 30))
                            outdata[iy * 30:iy * 30 + 30,
                                    ix * 30:ix * 30 + 30] = bindata[::-1, :]
                            break
                        else:
                            print("{} not found".format(binname))

            outdata = outdata.astype("float32")
            outdata.tofile(outname)


def convertjson(ll_x, ll_y, ur_x, ur_y):
    xylist = list(itertools.product(
        range(ll_x, ur_x + 1), range(ur_y, ll_y + 1)))
    n = cpu_count()
    p = Pool(n)
    p.map(json2raster, xylist)
    p.close()
    p.terminate()


def json2raster(arg):
    x = arg[0]
    y = arg[1]

    fname5a = "bin/{}_{}_{}.bin".format(x, y, "5a")
    fname10b = "bin/{}_{}_{}.bin".format(x, y, "10b")

    if (os.path.exists(fname5a) is False) and (os.path.exists(fname10b) is False):
        for filetype in ["5a", "10b"]:
            jsonname = "json/{}_{}_{}.geojson".format(x, y, filetype)
            binname = "bin/{}_{}_{}.bin".format(x, y, filetype)
            if os.path.exists(jsonname):
                print("conveting {}".format(jsonname))
                lon_min = x2lon(x)
                lon_max = x2lon(x + 1)
                lat_min = y2lat(y + 1)
                lat_max = y2lat(y)

                xsize = 30
                ysize = 30

                script = "gdal_grid -ot Float32 -of ENVI -zfield alti -a nearest -txe {} {} -tye {} {} -outsize {} {} {} {}".format(
                    lon_min, lon_max, lat_min, lat_max, xsize, ysize, jsonname, binname)
                print(script)
                os.system(script)
                break
            else:
                print("{} not found".format(jsonname))

    else:
        print("converted binary file for {} {} arleady exists".format(x, y))


def make_fig(ll_x, ur_x, ll_y, ur_y, maxsize, vmin, vmax):
    for box_x in range(ll_x, ur_x + 1, maxsize):
        for box_y in range(ur_y, ll_y + 1, maxsize):

            box_x_max = min(box_x + maxsize, ur_x + 1)
            box_y_max = min(box_y + maxsize, ll_y + 1)
            binname = "connected_bin/{}_{}.bin".format(box_x, box_y)
            if os.path.exists(binname):
                print("illustraing {}".format(binname))
                bindata = np.fromfile(
                    binname, dtype="float32").reshape(
                    [(box_y_max - box_y) * 30, (box_x_max - box_x) * 30])

                plt.close()
                plt.imshow(bindata, vmin=vmin, vmax=vmax)
                plt.colorbar()
                figname = "fig/{}_{}.png".format(box_x, box_y)
                # plt.show()
                plt.savefig(figname)
