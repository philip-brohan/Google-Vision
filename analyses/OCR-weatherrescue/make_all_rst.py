#!/usr/bin/env python

# make docs for all the months in the OCR-weatherrescue benchmark

import subprocess
import os.path

for year in range(1898,1905):
    for month in range(1,13):
        if year==1904 and month>9: continue
        proc = subprocess.Popen("./scripts/make_rst.py " +
                                "--year=%d "  % year  +
                                "--month=%d " % month,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
                    
