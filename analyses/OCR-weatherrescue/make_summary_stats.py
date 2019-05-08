#!/usr/bin/env python

# make summary statistics for all the months in the OCR-weatherrescue benchmark

import pickle

tots={'Total':   0,
      'Good':    0,
      'Bad':     0,
      'Missing': 0}

for year in range(1898,1905):
    for month in range(1,13):
        if year==1904 and month>9: continue
        with open("%04d-%02d.pkl" % (year,month), "rb" ) as pkf:
            stats=pickle.load(pkf)
        for var in tots:
            tots[var] += stats[var]
                    
print(tots)
