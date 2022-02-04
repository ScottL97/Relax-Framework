#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : download.py
@Author: Scott
@Date  : 2022/2/2 18:41
@Desc  : 
"""
import requests
import os


def download_file_by_http(download_dir, url):
    res = requests.get(url, verify=False)
    if res.status_code != 200:
        return 1
    filename = os.path.join(download_dir, url.split('/')[-1].split('&')[0])
    with open(filename, 'wb') as f:
        f.write(res.content)

    return 0
