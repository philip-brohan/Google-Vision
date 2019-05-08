#!/usr/bin/env python

# Make a comparison figure showing GCV performance against a month's
#  data from the weatherrescue OCR benchmark.

import argparse
import sys
import subprocess
from calendar import monthrange

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year to compare",
                    type=int,required=True)
parser.add_argument("--month", help="Month to compare",
                    type=int,required=True)
parser.add_argument("--colour", help="Colour scale factor",
                    type=float,default=1.0)
parser.add_argument("--contrast", help="Contrast scale factor",
                    type=float,default=1.0)
parser.add_argument("--brightness", help="Brightness scale factor",
                    type=float,default=1.0)
parser.add_argument("--sharpness", help="Sharpness scale factor",
                    type=float,default=1.0)
parser.add_argument("--opimg", help="Image output file name",
                    default="oplot.png",
                    type=str,required=False)
parser.add_argument("--opstats", help="Statistics output file name",
                    default="stats.pkl",
                    type=str,required=False)
args = parser.parse_args()

source="../../../OCR-weatherrescue/images/%04d-%02d.jpg" % (
                      args.year,args.month)

benchmark="../../../OCR-weatherrescue/data/%04d-%02d.csv" % (
                      args.year,args.month)

# Make the modified image
#proc = subprocess.Popen("./scripts/modify.py " +
#                        "--source=%s "     % source +
#                        "--colour=%f "     % args.colour +
#                        "--contrast=%f "   % args.contrast +
#                        "--brightness=%f " % args.brightness +
#                        "--sharpness=%f "  % args.sharpness,
#                    stdout=subprocess.PIPE, 
#                    stderr=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
#if len(err)>0: sys.exit(0)

# Run Textract
proc = subprocess.Popen("./scripts/run_gcv.py " +                    
                        "--source=%s "     % source,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
#if len(err)>0: 
#    print(err)
#    print(out)
#    sys.exit(0)
    
# Make the validation plot
ndays=monthrange(args.year,args.month)[1]
proc = subprocess.Popen("./scripts/oplot_cluster.py " +
                        "--source=%s "     % source +
                        "--benchmark=%s "  % benchmark +
                        "--opimg=%s "      % args.opimg +
                        "--opstats=%s "    % args.opstats +
                        "--ndays=%d "      % ndays,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print(err)
print(out)
