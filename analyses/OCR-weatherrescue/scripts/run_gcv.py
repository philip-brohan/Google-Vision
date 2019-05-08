#!/usr/bin/env python

# Run Google Vision on the selected image

import argparse
import pickle

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf import json_format

parser = argparse.ArgumentParser()
parser.add_argument("--source", help="Image file name",
                    type=str,default='modified.jpg')
parser.add_argument("--opfile", help="Output file name",
                    default="detection.pkl",
                    type=str,required=False)
args = parser.parse_args()

# Load the jpeg
with open(args.source,'rb') as jf:
    ie=jf.read()

# Analyze the document
image = types.Image(content=ie)
client = vision.ImageAnnotatorClient()
response = client.document_text_detection(image=image)
document = response.full_text_annotation

# Save the resulting JSON
pickle.dump(document
            , open( args.opfile, "wb" ) )
