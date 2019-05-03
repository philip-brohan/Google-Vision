#!/usr/bin/env python

# Run Google OCR on the Second Order Station sample image

import pickle

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf import json_format

# Load the jpeg
with open("../../../samples/Margate_1891_02.jpg",'rb') as jf:
    ie=jf.read()

# Analyze the document
image = types.Image(content=ie)
client = vision.ImageAnnotatorClient()
response = client.document_text_detection(image=image)
document = response.full_text_annotation

# Save the resulting JSON
pickle.dump(document, open( "detection.pkl", "wb" ) )
with open('detection.txt', 'w') as file:
     file.write(json_format.MessageToJson(document))
