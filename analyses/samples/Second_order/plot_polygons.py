#!/usr/bin/env python

# Plot a comparison of original image and transcription results.

import pickle
import argparse
from PIL import Image

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches
import numpy

from google.cloud import vision
from google.cloud.vision import types

# We're going to need the original image
im = Image.open("../../../samples/Margate_1891_02.jpg")
imwidth, imheight = im.size

fig=Figure(figsize=((im.size[0]/100)*1.04,
                    (im.size[1]/100)*1.04),
       dpi=100,
       facecolor=(0.88,0.88,0.88,1),
       edgecolor=None,
       linewidth=0.0,
       frameon=False,
       subplotpars=None,
       tight_layout=None)
ax_original=fig.add_axes([0.02,0.02,0.96,0.96],label='original')
ax_result=fig.add_axes([0.02,0.02,0.96,0.96],label='result')
# Matplotlib magic
canvas=FigureCanvas(fig)
# Turn off the axis tics
ax_original.set_axis_off()
ax_result.set_axis_off()

# Put the original image in its half of the figure
ax_original.imshow(im)

# Load the JSON from Textract for this image
document=pickle.load( open( "detection.pkl", "rb" ) )

# Convert box vertex list to numpy array for matplotlib
def bb2p(bb):
    result=numpy.zeros((len(bb.vertices),2))
    for idx in range(len(bb.vertices)):
        result[idx,0]=bb.vertices[idx].x/imwidth
        result[idx,1]=1.0-bb.vertices[idx].y/imheight
    return result
    
# Draw all the blocks
zorder=10
for page in document.pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            for word in paragraph.words:
                bp=matplotlib.patches.Polygon(bb2p(word.bounding_box),
                                  closed=True,
                                  edgecolor=(0,0,1,1),
                                  facecolor=(0,0,1,0.2),
                                  fill=True,
                                  linewidth=0.2,
                                  alpha=0.2,
                                  zorder=zorder)
                ax_result.add_patch(bp)

# Draw the image
fig.savefig('Second_order.png')
