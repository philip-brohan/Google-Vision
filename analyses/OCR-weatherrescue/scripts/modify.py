#!/usr/bin/env python

# Run one of the samples through an image modification

from PIL import Image, ImageEnhance
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--source", help="Image file name",
                    type=str,required=True)
parser.add_argument("--colour", help="Colour scale factor",
                    type=float,default=1.0)
parser.add_argument("--contrast", help="Contrast scale factor",
                    type=float,default=1.0)
parser.add_argument("--brightness", help="Brightness scale factor",
                    type=float,default=1.0)
parser.add_argument("--sharpness", help="Sharpness scale factor",
                    type=float,default=1.0)
parser.add_argument("--opfile", help="Output file name",
                    default="modified.jpg",
                    type=str,required=False)
args = parser.parse_args()

im = Image.open(args.source)

if args.colour != 1.0:
   enhancer = ImageEnhance.Color(im)
   im = enhancer.enhance(args.colour)

if args.contrast != 1.0:
   enhancer = ImageEnhance.Contrast(im)
   im = enhancer.enhance(args.contrast)

if args.brightness != 1.0:
   enhancer = ImageEnhance.Brightness(im)
   im = enhancer.enhance(args.brightness)

if args.sharpness != 1.0:
   enhancer = ImageEnhance.Sharpness(im)
   im = enhancer.enhance(args.sharpness)

im.save(args.opfile)

