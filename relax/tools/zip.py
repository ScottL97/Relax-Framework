#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : zip.py
@Author: Scott
@Date  : 2022/2/2 18:41
@Desc  : 
"""
import zipfile
import os


def unzip_file(zipfile_path, unzip_dir):
    if not zipfile_path.endswith('.zip'):
        return 1
    zip_file = zipfile.ZipFile(zipfile_path, 'r')
    for filename in zip_file.namelist():
        with open(os.path.join(unzip_dir, filename), 'w+b') as f:
            f.write(zip_file.read(filename))

    return 0
