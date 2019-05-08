#!/usr/bin/env python

# Overplot transcription results on the original image.
# Show successful, erronious, and missing results.

import argparse
import pickle
from PIL import Image

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches
from matplotlib.cm import Set2
import numpy
from scipy.stats import gaussian_kde
import pandas

from protobuf_to_dict import protobuf_to_dict

parser = argparse.ArgumentParser()
parser.add_argument("--source", help="Image file name",
                    type=str,default='modified.jpg')
parser.add_argument("--pickle", help="Pickled GCV results file name",
                    type=str,default='detection.pkl')
parser.add_argument("--benchmark", help="Benchmark results file name",
                    type=str,required=True)
parser.add_argument("--ndays", help="How many days in this month",
                    type=int,required=True)
parser.add_argument("--guides", help="Plot the day+hour guidelines",
                    type=bool,default=False)
parser.add_argument("--opimg", help="Image output file name",
                    default="oplot.png",
                    type=str,required=False)
parser.add_argument("--opstats", help="Statistics output file name",
                    default="stats.pkl",
                    type=str,required=False)
args = parser.parse_args()

# We're going to need the original image
im = Image.open(args.source)
imwidth, imheight = im.size

# And the benchmark data
bm = pandas.read_csv(args.benchmark)

fig=Figure(figsize=((1*im.size[0]/100)*1.04,
                    (1*im.size[1]/100)*1.04),
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

# Show the original image
ax_original.imshow(im)

# Load the JSON from GCV for this image
document=pickle.load( open( args.pickle, "rb" ) )

# Convert it to a dict so we can modify it
document=protobuf_to_dict(document)

# GV is bad at deciding which characters form part of the same word
#  patch this up a bit.
def merge_words(w1,w2):
    w1['symbols']=w1['symbols']+w2['symbols']
    w1['bounding_box']['vertices'][0]['x']=min(w1['bounding_box']['vertices'][0]['x'],
                                               w2['bounding_box']['vertices'][0]['x'])
    w1['bounding_box']['vertices'][0]['y']=min(w1['bounding_box']['vertices'][0]['y'],
                                               w2['bounding_box']['vertices'][0]['y'])
    w1['bounding_box']['vertices'][1]['x']=max(w1['bounding_box']['vertices'][1]['x'],
                                               w2['bounding_box']['vertices'][1]['x'])
    w1['bounding_box']['vertices'][1]['y']=min(w1['bounding_box']['vertices'][1]['y'],
                                               w2['bounding_box']['vertices'][1]['y'])
    w1['bounding_box']['vertices'][2]['x']=max(w1['bounding_box']['vertices'][2]['x'],
                                               w2['bounding_box']['vertices'][2]['x'])
    w1['bounding_box']['vertices'][2]['y']=max(w1['bounding_box']['vertices'][2]['y'],
                                               w2['bounding_box']['vertices'][2]['y'])
    w1['bounding_box']['vertices'][3]['x']=min(w1['bounding_box']['vertices'][3]['x'],
                                               w2['bounding_box']['vertices'][3]['x'])
    w1['bounding_box']['vertices'][3]['y']=max(w1['bounding_box']['vertices'][3]['y'],
                                               w2['bounding_box']['vertices'][3]['y'])
    return(w1)

# Most of the numbers we want are split into three words - merge them
def reword(doc):
     for page in document['pages']:
        for block in page['blocks']:
            for paragraph in block['paragraphs']:
                paragraph['newwords']=[]
                last_word=None
                for word in paragraph['words']:
                    if (last_word is not None and
                        len(word['symbols'])==3 and
                        not last_word['symbols'][0]['text'].isdigit()):
                        try:
                            word=merge_words(last_word,word)
                        except KeyError:
                            word=word
                        paragraph['newwords'].append(word)
                        last_word=None
                    else:
                        if last_word is not None:
                            paragraph['newwords'].append(last_word)
                        last_word=word
                if last_word is not None:
                    paragraph['newwords'].append(last_word)
                paragraph['threewords']=[]
                last_word=None
                for word in paragraph['newwords']:
                    if (last_word is not None and
                        len(word['symbols'])==4 and
                        last_word['symbols'][0]['text'].isdigit()):
                        try:
                            word=merge_words(last_word,word)
                        except KeyError:
                            word=word
                        paragraph['threewords'].append(word)
                        last_word=None
                    else:
                        if last_word is not None:
                            paragraph['threewords'].append(last_word)
                        last_word=word
                if last_word is not None:
                    paragraph['threewords'].append(last_word)
     return(document)
 
document=reword(document)

# Convert box vertex list to numpy array for matplotlib
def bb2p(bb):
    result=numpy.zeros((len(bb['vertices']),2))
    for idx in range(len(bb['vertices'])):
        result[idx,0]=bb['vertices'][idx]['x']/imwidth
        result[idx,1]=1.0-bb['vertices'][idx]['y']/imheight
    return result

# Get bounding box centroid for text
def b2t(bb):
    vertices=bb2p(bb)
    result=[0,0]
    result[0]=numpy.mean(vertices[:,0])
    result[1]=numpy.mean(vertices[:,1])
    return result

# Make fake bounding box around point for missing items
def m2p(x,y):
    result=numpy.zeros((4,2))
    result[0,0]=x-0.014
    result[0,1]=y-0.008
    result[1,0]=x-0.014
    result[1,1]=y+0.008
    result[2,0]=x+0.014
    result[2,1]=y+0.008
    result[3,0]=x+0.014
    result[3,1]=y-0.008
    return result

# Get bounding box metrics
def bb_width(bb):
    vertices=bb2p(bb)
    width=numpy.max(vertices[:,0])-numpy.min(vertices[:,0])
    return width

def bb_height(bb):
    vertices=bb2p(bb)
    height=numpy.max(vertices[:,1])-numpy.min(vertices[:,1])
    return height

def bb_left(bb):
    vertices=bb2p(bb)
    left=numpy.min(vertices[:,0])
    return left

def bb_right(bb):
    vertices=bb2p(bb)
    right=numpy.max(vertices[:,0])
    return right

def bb_top(bb):
    vertices=bb2p(bb)
    top=numpy.max(vertices[:,1])
    return top

def bb_bottom(bb):
    vertices=bb2p(bb)
    bottom=numpy.min(vertices[:,1])
    return bottom

# Do a few obvious fix-ups on the GCV output
def fixup(text):
    # Insert the decimal point where it might have been missed
    if len(text)==4:
       text=text[0]+'.'+text[1:]
    # Replace any non-digit with decimal point
    for id in range(len(text)):
        if not text[id].isdigit(): 
            text=text[0:id]+'.'+text[id+1:]
    return text

# Get the characters comprising a word as a single string
def getWordString(word):
    ws=''
    for symbol in word['symbols']:
        ws=ws+symbol['text']
    return ws


def hasNumbers(word):
    return any(char.isdigit() for char in getWordString(word))

# Find the column locations corresponding to hours, 
#  and the row locations corresponding to days
xc=[]
yc=[]
for page in document['pages']:
    for block in page['blocks']:
        for paragraph in block['paragraphs']:
            for word in paragraph['threewords']:
                try:
                    if not hasNumbers(word): continue
                    cent=b2t(word['bounding_box'])
                    xc.append(cent[0])
                    yc.append(cent[1])
                except KeyError:
                    continue

# Find clusters of points in a and y - these are the rows and columns
def get_columns(xc):
    kde = gaussian_kde(xc,bw_method=0.03)
    x_grid=numpy.linspace(0,1,1000)
    dens=kde.evaluate(x_grid)
    col=[]
    for i in range(1,len(x_grid)-1):
        if (dens[i]>1 and 
            dens[i]>dens[i-1] and
            dens[i]>dens[i+1]):
            col.append(x_grid[i])
    return(col)

columns=get_columns(xc)
# If fewer than 26 columns we've lost some in the fold, add it back
while len(columns)<26:
   columns.insert(0,columns[0]-(columns[1]-columns[0])) 
columns=columns[1:(len(columns)-1)]
rows=get_columns(yc)
# Image might or might not have a row of hour numbers
if len(rows)==args.ndays+2:
    rows=rows[1:(len(rows)-1)]
else:
    rows=rows[1:(len(rows))]

# Draw the breaks
if args.guides==True:
    for clm in columns:
        ax_result.add_line(matplotlib.lines.Line2D(
                xdata=(clm,clm),
                ydata=(0,1),
                linestyle='solid',
                linewidth=1,
                color=(1,0,0,1),
                zorder=5))
    for row in rows:
        ax_result.add_line(matplotlib.lines.Line2D(
                xdata=(0,1),
                ydata=(row,row),
                linestyle='solid',
                linewidth=1,
                color=(1,0,0,1),
                zorder=5))

# Keep track of good, bad, and missing data
stats={'Total':   0,
       'Good':    0,
       'Bad':     0,
       'Missing': 0}

# Make 2d array of blocks - for each row/column intersection
data_points=[[None] * len(columns) for i in range(len(rows))]
for page in document['pages']:
    for block in page['blocks']:
        for paragraph in block['paragraphs']:
            for word in paragraph['threewords']:
                try:
                    if (bb_width(word['bounding_box']) > 0.045 or
                        bb_width(word['bounding_box']) < 0.015 or
                        bb_height(word['bounding_box']) > 0.03 or
                        bb_height(word['bounding_box']) < 0.001): continue
                    at_column=None
                    for cmi in range(len(columns)):
                        clm=columns[cmi]
                        if (bb_left(word['bounding_box'])<clm and
                            bb_right(word['bounding_box'])>clm):
                            at_column=cmi
                            break
                    if at_column is None: continue
                    for rwi in range(len(rows)):
                        row=rows[rwi]
                        if (bb_top(word['bounding_box'])>row and
                            bb_bottom(word['bounding_box'])<row):
                            data_points[rwi][at_column]=word
                            break
                except KeyError:
                    continue
# Draw a marker at every hour - either a text block or a missing marker
for rwi in range(len(rows)):
   for cmi in range(len(columns)):
      try:
          stats['Total'] += 1
          if data_points[rwi][cmi] is None:
            # Mark as missing
               stats['Missing'] += 1
               pp=matplotlib.patches.Polygon(m2p(columns[cmi],rows[rwi]),
                                             closed=True,
                                             fill=False, 
                                             hatch='/',
                                             edgecolor=(1,0,0,1),
                                             facecolor=(1,0,0,1),
                                             linewidth=1.0,
                                             alpha=1.0,
                                             zorder=10)
               ax_result.add_patch(pp)
          else:
              word=data_points[rwi][cmi]
              # Compare the GCV value with the benchmark
              try:
                  bmvalue=bm.iloc[len(rows)-rwi-1][cmi+1].replace("'","")
              except:
                  bmvalue=0.0
              if fixup(getWordString(word))==bmvalue:
                  stats['Good'] += 1 
                  bcol=(0.7,1,0.7,1)
              else:
                  stats['Bad'] += 1
                  bcol=(1,0.5,0.5,1)
              pp=matplotlib.patches.Polygon(bb2p(word['bounding_box']),
                                            closed=True,
                                            edgecolor=bcol,
                                            facecolor=bcol,
                                            fill=True,
                                            linewidth=0.2,
                                            alpha=0.85,
                                            zorder=10)
              ax_result.add_patch(pp)
           # Text
              txt_centroid=b2t(word['bounding_box'])
              angle=0
              ax_result.text(txt_centroid[0],txt_centroid[1],
                             fixup(getWordString(word)),
                             fontsize=18,
                             verticalalignment='center',
                             horizontalalignment='center',
                             rotation=angle,
                             zorder=10)
      except KeyError:
          continue

# Draw the image
fig.savefig(args.opimg)

# Output the stats
print(stats)
with open( args.opstats, "wb" ) as pkf:
    pickle.dump(stats, pkf )
