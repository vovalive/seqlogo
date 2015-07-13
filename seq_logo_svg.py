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

from math import *

sequence='atagtattaggaaaataccataataatatttctacagaatactaagttaatactatgtgtagaataataaataatcagattaaaaaaattttatttatctgaaacatatttaatcaattgaactgattattttcagcagtaataattacatatgtacatagtacatatgtaaaatatcattaatttctgttatatataatagtatctattttagagagtattaattattactataattaagcatttatgcttaattataagctttttatgaacaaaattatagacattttagttcttataataaataatagatattaaagaaaataaaaaaatagaaataaatatcataacccttgataacccagaaattaatacttaatcaaaaatgaaaatattaattaataaaagtgaattgaataaaattttgaaaaaaatgaataacgttattatttccaataacaaaataaaaccacatcattcatattttttaatagaggcaaaagaaaaagaaataaacttttatgctaacaatgaatacttttctgtcaaatgtaatttaaataaaaatattgatattcttgaacaaggct'

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
coef=1.001

oh = ShapeBuilder()

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
	x=x1
	y=y1
	return a

def eggs(se):
	global distance,z
	for nuc in sequence:
		print x,y,angle,nuc 
		svg_document.addElement(add_nucleotide(nuc))
		print x,y,angle,nuc 
		print '==================='
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

print(svg_document.getXML())
print x,y
print xses
print yses
print min(xses),max(xses)
print min(yses),max(yses)

x=(max(xses)-min(xses))*2
y=(max(yses)-min(yses))*2
eggs(sequence)
svg_document.save("temp.svg")

f.close()

