#!/usr/bin/env python

# Make a documentation page for one month's GCV results from the 
#  OCR-weatherrescue benchmark.

import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year to compare",
                    type=int,required=True)
parser.add_argument("--month", help="Month to compare",
                    type=int,required=True)
args = parser.parse_args()

opfile="../../docs/OCR-weatherrescue/auto_generated/%04d-%02d.rst" % (
               args.year,args.month)

stats=pickle.load(open("%04d-%02d.pkl" % (args.year,args.month), "rb" ) )

with open(opfile,"w") as f:
    f.write(":orphan:\n\n")
    f.write("Google Vision results for the OCR-weatherrescue benchmark %04d-%02d\n" % (
              args.year,args.month))
    f.write("===================================================================\n\n")
    f.write(".. figure:: ../../../analyses/OCR-weatherrescue/%04d-%02d.png\n" % (
                    args.year,args.month) +
            "   :width: 95%\n" +
            "   :align: center\n" +
            "   :figwidth: 95%\n\n" +
            "   Google Vision results for `this month in the benchmark "+
            " <http://brohan.org/OCR-weatherrescue/individual_months/1903-11.html>`_. "+
            "Green blocks are entries sucessfully read. " +
            "Filled red blocks are entries inacurately read, "+
            "and hatched red blocks are entries missed altogether.\n\n")
    f.write("Of %d entries:\n " % stats['Total'])
    f.write("* %d (%d%%) were read successfully,\n " % 
             (stats['Good'],int(round(100*stats['Good']/stats['Total']))))
    f.write("* %d (%d%%) were read inaccurately,\n " % 
             (stats['Bad'],int(round(100*stats['Bad']/stats['Total']))))
    f.write("* %d (%d%%) were missed altogether.\n\n " % 
             (stats['Missing'],int(round(100*stats['Missing']/stats['Total']))))
    f.write("\n|\n\n")
    f.write(".. toctree::    \n" +
            "   :maxdepth: 1 \n" +
            "   :titlesonly: \n" +
            "\n"                 +
            "   ../scripts/make_comparison \n" +
            "   ../scripts/run_textract \n" +
            "   ../scripts/oplot_cluster \n\n")



