#!/usr/bin/env python3
"""Create a compact zero-margin text print edition from sitemap HTML."""
import argparse, concurrent.futures, json, re, time, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Archive", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Archive-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

SIZE=(595.276,841.89)
ASSET=re.compile(r'\.(?:png|jpe?g|webp|avif|svg|gif|pdf|xml|xsl|txt|json|ico|woff2?|css|js|mp4|webm|zip)$',re.I)
SESSION=requests.Session(); SESSION.headers['User-Agent']='Mozilla/5.0 (compatible; SitePrintArchive/1.0)'
def get(u):
 for n in range(3):
  try:
   r=SESSION.get(u,timeout=35)
   if r.status_code in (429,500,502,503,504):time.sleep(2*(n+1));continue
   return r
  except requests.RequestException:time.sleep(n+1)
 raise RuntimeError('fetch failed')
def inventory(start):
 host=urllib.parse.urlsplit(start).netloc.lower(); queue=[urllib.parse.urljoin(start,'/sitemap.xml')]; seen=set(); found=[]
 while queue:
  u=queue.pop(0)
  if u in seen:continue
  seen.add(u)
  try:root=ET.fromstring(get(u).content)
  except Exception:continue
  for loc in root.findall('.//{*}loc'):
   v=(loc.text or '').strip();p=urllib.parse.urlsplit(v)
   if p.netloc.lower()!=host:continue
   if p.path.lower().endswith('.xml') and ('sitemap' in p.path or root.tag.endswith('sitemapindex')):queue.append(v)
   elif not ASSET.search(p.path):found.append(urllib.parse.urlunsplit((p.scheme,p.netloc,p.path.rstrip('/') or '/','','')))
 found=list(dict.fromkeys(found)); homepage=start.rstrip('/')
 return sorted(found,key=lambda x:0 if x.rstrip('/')==homepage else 1)
def fetch(item):
 i,u=item
 try:
  r=get(u);ct=r.headers.get('content-type','')
  if r.status_code!=200 or 'html' not in ct:return i,u,None,f'{r.status_code} {ct}'
  soup=BeautifulSoup(r.content,'html.parser');title=soup.title.get_text(' ',strip=True) if soup.title else u
  for s in soup(['script','style','noscript','svg','nav','footer','form']):s.decompose()
  main=soup.find('main') or soup.find('article') or soup.body or soup
  blocks=[]
  for tag in main.find_all(['h1','h2','h3','h4','p','li','blockquote','pre','td']):
   if tag.find_parent(['p','li','blockquote','pre','td']):continue
   val=tag.get_text(' ',strip=True)
   if val and (not blocks or val!=blocks[-1][1]):blocks.append((tag.name,val))
  if not blocks:blocks=[('p',main.get_text(' ',strip=True))]
  return i,u,(title,blocks),None
 except Exception as e:return i,u,None,str(e)
def line(c,s,y,font,size):
 c.setFont(font,size);c.drawString(0,y,s)
def write_block(c,s,y,font,size):
 width,height=SIZE;leading=size*1.3; current=''
 for word in s.split():
  candidate=(current+' '+word).strip()
  if stringWidth(candidate,font,size)>width and current:
   if y-leading<0:c.showPage();y=height
   y-=leading;line(c,current,y,font,size);current=word
  else:current=candidate
 if current:
  if y-leading<0:c.showPage();y=height
  y-=leading;line(c,current,y,font,size)
 return y

def main():
 p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--output',required=True);p.add_argument('--manifest',required=True);p.add_argument('--workers',type=int,default=5);p.add_argument('--limit',type=int,default=0);a=p.parse_args()
 urls=inventory(a.url)
 if a.limit:urls=urls[:a.limit]
 if not urls:raise SystemExit('No sitemap HTML URLs found')
 Path(a.output).parent.mkdir(parents=True,exist_ok=True);results={};failures=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
  for i,u,data,error in pool.map(fetch,enumerate(urls)):
   if error:failures.append({'url':u,'error':error})
   else:results[i]=(u,data)
   if (i+1)%100==0:print(f'{i+1}/{len(urls)} fetched',flush=True)
 c=canvas.Canvas(a.output,pagesize=SIZE,pageCompression=1,invariant=1);c.setTitle('Website archive: '+a.url);first=True
 for i,(u,(title,blocks)) in sorted(results.items()):
  if not first:c.showPage()
  first=False;y=SIZE[1]
  y=write_block(c,title,y,'Archive-Bold',14)-9
  y=write_block(c,u,y,'Archive',7)-13
  for kind,value in blocks:
   size=11 if kind=='h1' else 9 if kind.startswith('h') else 8
   y=write_block(c,value,y,'Archive-Bold' if kind.startswith('h') else 'Archive',size)-5
 c.save()
 manifest={'start_url':a.url,'sitemap_html_urls':len(urls),'successful_html':len(results),'failed':failures,'output':a.output,'print_mode':'reconstructed HTML text, zero margins','pdf_bytes':Path(a.output).stat().st_size}
 Path(a.manifest).write_text(json.dumps(manifest,indent=2));print(json.dumps({k:v for k,v in manifest.items() if k!='failed'}),flush=True)
if __name__=='__main__':main()
