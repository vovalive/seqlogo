import pysvg
import sys

from pysvg.animate import *
from pysvg.attributes import *
from pysvg.builders import *
from pysvg.core import *
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.parser import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.util import *

import pysvg.structure
import pysvg.builders
import pysvg.text

from math import *

#sequence='atggcatctctgagccagctgagtggccacctgaactacacctgtggggcagagaactccacaggtgccagccaggcccgcccacatgcctactatgccctctcctactgcgcgctcatcctggccatcgtcttcggcaatggcctggtgtgcatggctgtgctgaaggagcgggccctgcagactaccaccaactacttagtagtgagcctggctgtggcagacttgctggtggccaccttggtgatgccctgggtggtatacctggaggtgacaggtggagtctggaatttcagccgcatttgctgtgatgtttttgtcaccctggatgtc'
seqmax=2000000

sequence=sys.argv[1]
sequence=sequence.lower()

if len(sequence) > seqmax:
	sequence=sequence[0:seqmax]

outputname="/html/seqlogo/img/logo.svg"

## From file
#print "First 1000 bases only"
#seqfile=sys.argv[1]
#print seqfile
#f=open(seqfile,"r")
#sequence=f.read()
#sequence=sequence[0:1000]
#f.close()
###

###
f=open("plot3d.txt","w")
###

svg_document = pysvg.structure.svg()
shape_builder = pysvg.builders.ShapeBuilder()

colors={'a':'red','t':'black','g':'green','c':'blue'}
x=0
y=0

z=0
xses=[]
yses=[]
linewidth=10
angle=0
degree=30
distance=20
coef=1.0

oh = ShapeBuilder()

style=StyleBuilder()
#style.setStrokeOpacity("1")
#style.setStrokeLineCap("round")

def add_nucleotide(nucleotide):
	global x
	global y
	global angle
	if nucleotide in ['a','t']:
		angle=angle+degree
	elif nucleotide in ['g','c']:
		angle=angle-degree
	x1=x+distance*cos(radians(angle))
	y1=y+distance*sin(radians(angle))
	a=oh.createLine(x,y,x1,y1,strokewidth = linewidth,stroke = colors[nucleotide])
#	a.set_style(style.getStyle())
	x=x1
	y=y1
	return a

def eggs(se):
	global distance,z
	for nuc in sequence:
		print(x,y,angle,nuc) 
		svg_document.addElement(add_nucleotide(nuc))
		print(x,y,angle,nuc) 
		print('===================')
		distance=distance*coef
		z=z+1
		f.write("%d,%d,%d\n"%(x,y,z))

def eggs2(se):
	global distance,xses,yses
	for nuc in sequence: 
		add_nucleotide(nuc)
		distance=distance*coef
		xses+=[x]
		yses+=[y]

eggs2(sequence)

x=-min(-1,min(xses))+distance
y=-min(-1,min(yses))+distance

print(x,y)

svg_document.addElement(oh.createCircle(x,y,10,strokewidth=5, stroke='yellow'))

angle=0
distance=20
eggs(sequence)
svg_document.save(outputname)

#####
# Read in the file
with open(outputname, 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('line', 'line stroke-linecap="round"')

# Write the file out again
with open(outputname, 'w') as file:
  file.write(filedata)
####


f.close()


