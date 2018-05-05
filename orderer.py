#!/usr/bin/python3
# Catalog photos to subfolders YYYY/YYMMDD
# Vitaly Chekryzhev <13hakta@gmail.com>, 2015

import os, datetime, sys
from os.path import isfile, isdir, join
from PIL import Image
from PIL.ExifTags import TAGS

# Usage: orderer.py [src] [dst]

if len(sys.argv) > 1:
    img_folder = sys.argv[1]
    print("Folder:", img_folder)
else:
    print("Use current folder")
    img_folder = "."

if len(sys.argv) > 2:
    dst_dir = sys.argv[2]
    print("Destination:", dst_dir)
else:
    dst_dir = img_folder

if not isdir(img_folder):
    print("Folder '" + img_folder + "' not accessible")
    exit()

if not isdir(dst_dir):
    print("Folder '" + dst_dir + "' not accessible")
    exit()

filelist = [ f for f in os.listdir(img_folder) if isfile(join(img_folder, f)) ]

img_exts = ['jpg', 'jpeg', 'mp4']

for fname in filelist:
    ext = fname.split(".")[-1].lower()
    if ext in img_exts:
        # Try to extract EXIF info

        (day, mon, year) = ['', '', '']
        tags = None
        try:
            tags = Image.open(img_folder + '/' + fname)._getexif()
        except:
            pass

        if tags and 'DateTimeDigitized' in tags:
            dateshot = str(tags['DateTimeDigitized'])
            day = dateshot[8:10]
            mon = dateshot[5:7]
            year = dateshot[2:4]
        else:
            # Get date info from OS
            t = os.path.getmtime(img_folder + '/' + fname)
            dateshot = datetime.datetime.fromtimestamp(t)
            day = str(dateshot.day)
            mon = str(dateshot.month)
            year = str(dateshot.year - 2000)

        folder = '20' + year + '/' + year + mon.zfill(2) + day.zfill(2)
        fullpath = dst_dir + '/' + folder

        os.makedirs(fullpath, exist_ok=True)
        os.rename(img_folder + '/' + fname,  fullpath + '/' + fname)
        print(fname + ' >' + fullpath)
