#!/usr/bin/env python3
import argparse,numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');p.add_argument('--start',type=float,default=.65);p.add_argument('--opaque-background',default=None);a=p.parse_args()
assert 0<=a.start<1
im=Image.open(a.input).convert('RGBA');w,h=im.size
assert abs(w/h-16/9)<.01,'Native 16:9 source required'
if a.opaque_background:
 bg=Image.new('RGBA',im.size,a.opaque_background);bg.alpha_composite(im);im=bg
arr=np.asarray(im).copy();t=np.clip((np.arange(h)/(h-1)-a.start)/(1-a.start),0,1);base=1-np.log1p(9*t)/np.log(10)
mod=1-.035*t[:,None]*(1-t[:,None])*((np.arange(w)[None,:]//12+np.arange(h)[:,None]//12)%3)/2
arr[:,:,3]=np.round(arr[:,:,3]*base[:,None]*mod).astype('uint8');out=Image.fromarray(arr);out.save(a.output)
print({'dimensions':out.size,'alpha':out.getchannel('A').getextrema(),'top_min':int(arr[0,:,3].min()),'bottom_max':int(arr[-1,:,3].max())})
