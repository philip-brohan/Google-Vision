#!/usr/bin/env python

# Run all the months in the OCR-weatherrescue benchmark

import subprocess
import os.path
import time

for year in range(1898,1905):
    for month in range(1,13):
        if year==1904 and month>9: continue
        if os.path.isfile("%04d-%02d.png" % (year,month)): continue
        print("%04d-%02d" % (year,month))
        proc = subprocess.Popen("./scripts/make_comparison.py " +
                                "--year=%d "  % year  +
                                "--month=%d " % month +
                                "--opimg=%04d-%02d.png " % (year,month) +
                                "--opstats=%04d-%02d.pkl " % (year,month) +
                                "--colour=1.0 "       +
                                "--contrast=0.1 "     +
                                "--brightness=1.0 "   +
                                "--sharpness=0.0 ",
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        time.sleep(1)
                    
