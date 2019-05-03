#!/usr/bin/env python

# Plot a comparison of original image and transcription results.

import pickle
from PIL import Image

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches
import numpy

# We're going to need the original image
im = Image.open("../../../samples/24-118-jeannette-vol003_199.jpg")
imwidth, imheight = im.size

fig=Figure(figsize=((1*im.size[0]/100)*1.04,
                    (2*im.size[1]/100)*1.06),
       dpi=100,
       facecolor=(0.88,0.88,0.88,1),
       edgecolor=None,
       linewidth=0.0,
       frameon=False,
       subplotpars=None,
       tight_layout=None)
ax_original=fig.add_axes([0.02,0.51,0.96,0.47])
ax_result=fig.add_axes([0.02,0.02,0.96,0.47])
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

# Get bounding box centroid for text
def b2t(bb):
    vertices=bb2p(bb)
    result=[0,0]
    result[0]=numpy.mean(vertices[:,0])
    result[1]=numpy.mean(vertices[:,1])
    return result
    
bp=matplotlib.patches.Polygon(numpy.array([[0,0],[1,0],[1,1],[0,1]]),
                  closed=True,
                  edgecolor=(0,0,0,1),
                  facecolor=(0,0,0,0.2),
                  fill=True,
                  linewidth=0.2,
                  alpha=0.05,
                  zorder=0)
ax_result.add_patch(bp)
for page in document.pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            for word in paragraph.words:
                bp=matplotlib.patches.Polygon(bb2p(word.bounding_box),
                                  closed=True,
                                  edgecolor=(0,0,0,1),
                                  facecolor=(0,0,0,0.2),
                                  fill=True,
                                  linewidth=0.2,
                                  alpha=0.2,
                                  zorder=10)
                ax_result.add_patch(bp)
                for symbol in word.symbols:
                    bp=matplotlib.patches.Polygon(bb2p(symbol.bounding_box),
                                  closed=True,
                                  edgecolor=(0,0,1,0.01),
                                  facecolor=(0,0,1,0.2),
                                  fill=True,
                                  linewidth=0.2,
                                  alpha=0.2,
                                  zorder=100)
                    ax_result.add_patch(bp)
                # Text
                    txt_centroid=b2t(symbol.bounding_box)
                    angle=0
                    #if (block['Geometry']['BoundingBox']['Height'] >
                    #    block['Geometry']['BoundingBox']['Width']*2):
                    #    angle=90
                    ax_result.text(txt_centroid[0],txt_centroid[1],
                                   symbol.text,
                                   fontsize=20,
                                   verticalalignment='center',
                                   horizontalalignment='center',
                                   rotation=angle)    

# Draw the image
fig.savefig('Jeannette_text.png')
