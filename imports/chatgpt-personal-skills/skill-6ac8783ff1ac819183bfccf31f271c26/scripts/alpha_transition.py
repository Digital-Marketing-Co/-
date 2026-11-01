#!/usr/bin/env python3
"""Apply the user's requested deterministic RGBA logarithmic alpha transition."""
import argparse,math
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');p.add_argument('--start',type=float,default=.65);a=p.parse_args()
assert 0<=a.start<1
im=Image.open(a.input).convert('RGBA');w,h=im.size
assert abs(w/h-16/9)<.01,'Require native 16:9 source; do not distort or crop to fake compliance'
px=im.load()
for y in range(h):
 t=max(0,min(1,(y/(h-1)-a.start)/(1-a.start)));base=1-math.log1p(9*t)/math.log(10)
 for x in range(w):
  # A tiny smooth spatial voxel pattern, with zero modulation at endpoints.
  modulation=1-.035*t*(1-t)*((x//12+y//12)%3)/2
  r,g,b,old=px[x,y];px[x,y]=(r,g,b,round(old*base*modulation))
im.save(a.output)
print({'dimensions':im.size,'alpha_extrema':im.getchannel('A').getextrema(),'bottom_alpha':max(im.getchannel('A').crop((0,h-1,w,h)).getdata())})
