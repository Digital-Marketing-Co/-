#!/usr/bin/env python3
from pathlib import Path
import json,re,html,csv,hashlib,sys
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,Flowable,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(sys.argv[1]) if len(sys.argv)>1 else Path.cwd()
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
st=getSampleStyleSheet();st.add(ParagraphStyle(name='Main',fontName='Body',fontSize=10.5,leading=15.3,textColor=HexColor('#172b3b'),spaceAfter=10));st.add(ParagraphStyle(name='TitleS',fontName='Bold',fontSize=20,leading=25,textColor=HexColor('#102b48'),spaceAfter=16));st.add(ParagraphStyle(name='Cell',parent=st['Main'],fontSize=9.1,leading=12.4,spaceAfter=0));st.add(ParagraphStyle(name='SmallS',parent=st['Main'],fontSize=8.3,leading=11.5,spaceAfter=6));st.add(ParagraphStyle(name='CaptionS',parent=st['SmallS'],textColor=HexColor('#41657b'),fontSize=8));st.add(ParagraphStyle(name='Cover',fontName='Bold',fontSize=38,leading=44,textColor=white,spaceAfter=16))
W,H=612,792;content=504
src={s['source_id']:s for s in json.loads((R/'source_registry.json').read_text())};sections=json.loads((R/'manuscript.json').read_text());plans=json.loads((R/'curriculum.json').read_text());inv=json.loads((R/'image_inventory.json').read_text());imgs={i['id']:i for i in inv};notes=[];seen=set();placements=[]
def image_path(iid):
 p=Path(imgs[iid]['path']);return str(p if p.is_absolute() else R/p)
def esc(t):return html.escape(str(t))
def authors(s,biblio=False):
 a=s['authors']
 if not a:return '[author not verified]'
 a=a[:7]+(['et al.'] if len(a)>10 else a[7:])
 if biblio and a and ' ' in a[0] and len(a[0])<60 and a[0] not in ['American Veterinary Society of Animal Behavior','Cornell University College of Veterinary Medicine','ManyDogs Project']:
  parts=a[0].rsplit(' ',1);a[0]=parts[1]+', '+parts[0]
 return ', '.join(a)
def cite(sid):
 s=src[sid];n=len(notes)+1;first=sid not in seen;seen.add(sid)
 locator='; '.join(l['location'] for l in s['locators'] if l['verified']) or ('abstract' if 'abstract' in s['access_level'] else 'relevant web section; no PDF page claim')
 if first:
  t=f'{authors(s)}, “{s["title"]},” <i>{esc(s["venue"])}</i> ({s["date"] or "n.d."}), {esc(locator)}. '
  t=esc(authors(s))+', “'+esc(s['title'])+',” <i>'+esc(s['venue'])+'</i> ('+esc(s['date'] or 'n.d.')+'), '+esc(locator)+'. '
 else:t=esc('AVSAB' if s['source_id']=='S02' else s['authors'][0] if s['source_id'] in ['S10','S22'] else s['authors'][0].split()[-1])+', “'+esc(s['title'])+',” '+esc(locator)+'. '
 url=('https://doi.org/'+s['doi']) if s.get('doi') else s['stable_url']
 t+=f'<link href="{esc(url)}" color="#087594">Publication</link>.'
 notes.append({'note':n,'source_id':sid,'text':t})
 return f'<super><link href="#note{n}" color="#087594">{n}</link></super>'
def para(t,style='Main'):
 t=esc(t)
 t=re.sub(r'\[\[(S\d+)\]\]',lambda m:cite(m.group(1)),t)
 return Paragraph(t,st[style])
class Banner(Flowable):
 def __init__(self,id):Flowable.__init__(self);self.id=id;self.width=content;self.height=326
 def draw(self):
  self.canv.drawImage(image_path(self.id),-60,35.75,width=612,height=612*9/16,mask='auto')
  placements.append({'id':self.id,'page':self.canv.getPageNumber(),'type':'banner','left':0,'right':612,'top':792,'height':344.25})
class Concept(Image):
 def __init__(self,id):self.id=id;super().__init__(image_path(id),width=content,height=content*9/16)
 def draw(self):super().draw();placements.append({'id':self.id,'page':self.canv.getPageNumber(),'type':'inline'})
inline_order=['I01','I02','I04','I06','I08','I13','I07','I12','I11','I10','I09','I05','I03','I14'];inline_idx=0;words=0;last=0
purposes={'I01':'Systematic observation','I02':'Facial observation without emotion labels','I03':'Tail morphology and whole-body posture','I04':'Context and orientation near a gate','I05':'Scent investigation','I06':'Proximity and resting choices','I07':'Human gesture context','I08':'Managed multispecies spacing','I09':'Accessible senior rest environment','I14':'Protected recall practice','I12':'Puppy rest and safe outlets','I11':'Loose-leash practice','I10':'Voluntary muzzle approach','I13':'Safe enrichment'}
story=[]
def addbody(t):
 global words,last,inline_idx
 story.append(para(t));words+=len(re.findall(r'\b\w+\b',re.sub(r'\[\[.*?\]\]','',t)))
 if words-last>=470 and inline_idx<len(inline_order):add_inline()
def add_inline():
 global last,inline_idx
 iid=inline_order[inline_idx];imgs[iid]['word_position']=words;imgs[iid]['purpose']=purposes[iid];story.append(Concept(iid));story.append(Paragraph(f'{iid} | {purposes[iid]}. AI-generated conceptual representation; not empirical evidence.',st['CaptionS']));story.append(Spacer(1,8));last=words;inline_idx+=1

def furniture(c,d):
 c.saveState()
 if c.getPageNumber()==1:
  c.setFillColor(HexColor('#102437'));c.rect(0,0,W,H,fill=1,stroke=0)
 else:
  c.setStrokeColor(HexColor('#b0d5df'));c.line(54,47,558,47);c.setFont('Body',8);c.setFillColor(HexColor('#466177'));c.drawString(54,31,'SKI / CANINE COMMUNICATION / RESEARCH EDITION 01');c.drawRightString(558,31,str(c.getPageNumber()))
 c.restoreState()
story += [Spacer(1,110),Paragraph('SKI',st['Cover']),Paragraph('Canine Communication<br/>and Humane Training',ParagraphStyle(name='C2',parent=st['Cover'],fontSize=27,leading=35)),Spacer(1,24),Paragraph('A bounded scholarly synthesis and a 28-competency curriculum',ParagraphStyle(name='C3',parent=st['Cover'],fontName='Body',fontSize=13,leading=20)),Spacer(1,40),Paragraph('Research edition<br/>9 October 2026<br/><br/>27 source records · 33 logged queries<br/>Source access and methodological limits disclosed',ParagraphStyle(name='C4',parent=st['C3'] if 'C3' in st else st['Cover'],fontName='Body',fontSize=11,leading=18,textColor=HexColor('#a2d4df'))),PageBreak()]
story.append(Paragraph('Reading this edition',st['TitleS']))
for t in ['The five substantive chapters form a single research-to-practice argument. The final chapter contains curriculum records in a continuous table sequence; individual records are not separate literature-review subsections. Notes and the alphabetized bibliography follow the training templates.','This edition is a selected-record narrative synthesis with explicit limits. It is not a formal systematic review and does not claim saturation. Its practical plans are adjustable curriculum designs under professional guidance; they are not substitutes for individual veterinary assessment.','The companion JSON preserves the research protocol, source registry, evidence schema, quality rubric, curriculum and writable templates. The evidence matrix and search log provide separate machine-readable audit trails. Null values mark details not extracted; they are never estimates.','All behavioral images are generated conceptual representations. Scientific conclusions rest on cited research, not visual resemblance. Native approximately 16:9 source dimensions are preserved within pixel rounding, with a true RGBA logarithmic fade and full-bleed chapter banners.']:
 story.append(para(t))
for s in sections:story.append(Paragraph(esc(s['title']),st['Main']))
story.append(PageBreak())
for sec in sections:
 story.append(Banner(sec['banner']));story.append(Paragraph(esc(sec['title']),st['TitleS']));imgs[sec['banner']]['purpose']=sec['title'];imgs[sec['banner']]['word_position']=words
 story.append(Paragraph('Banner: AI-generated conceptual representation; not empirical evidence.',st['CaptionS']))
 for p in sec['paragraphs']:addbody(p)
 if sec['banner']=='B02':
  rows=[['Observation','Alternatives / context needed','Proportionate response'],['Tail moves side to side','Arousal and different social contexts; body tension, approach and escape matter.','Do not infer friendliness or permit contact from wagging alone.'],['Freezing as hand approaches','Possible concern, pain or learned inhibition; examine timing and movement.','Pause contact, allow space, seek assessment if new or handling-linked.'],['Sclera visible','Eye/head direction and morphology affect visibility; context is essential.','Avoid intrusive approach; read whole cluster.'],['Ears pulled back','Anatomy, attention and affective context vary.','Compare individual baseline rather than decode one ear position.'],['Lip lick / tongue movement','Food, heat/activity and possible concern are alternatives.','Check preceding event and paired changes.'],['Raised hackles','Arousal; cannot independently establish intent to attack.','Increase safe distance if uncertainty or tension is rising.'],['Rolls onto back','Possible rest, play or interaction response.','Do not assume an invitation to touch.'],['Growls','Play, guarding or threatening contexts differ.','Pause intrusive pressure; protect warnings and evaluate risk.'],['Persistent barking','Trigger-specific patterns, learned access or distress may contribute.','Observe sequence; manage trigger before training alternatives.'],['Sniffs or marks','Investigation, history and deposit context matter.','Provide safe sniffing; avoid unsupported territorial narratives.'],['Play bow followed by chase','Evaluate voluntary return, pauses and pursuit after withdrawal.','Interrupt gently if one participant cannot disengage.'],['Approaches a cat','Investigation, social interaction or pursuit risk remain possible.','Use barriers/escape routes; do not assume mutual play.'],['Quiet during separation','Rest and inhibition are alternatives; video context needed.','Assess overall comfort; absence of noise alone is insufficient.'],['Fails verbal cue','Hearing, competing stimuli, prior learning and motivation.','Lower difficulty and assess sensory/medical possibilities.']]
  tt=Table([[Paragraph(esc(z),st['Cell']) for z in row] for row in rows],colWidths=[106,219,179],repeatRows=1,hAlign='LEFT');tt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#102b48')),('TEXTCOLOR',(0,0),(-1,0),white),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,1),(-1,-1),HexColor('#edf5f7')),('GRID',(0,0),(-1,-1),.3,HexColor('#c5d9df')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
  # Paragraph colors must be white explicitly, not just Table TEXTCOLOR.
  for j,z in enumerate(rows[0]):tt._cellvalues[0][j]=Paragraph('<font color="white">'+esc(z)+'</font>',st['Cell'])
  story.append(tt);story.append(Spacer(1,12));words+=sum(len(re.findall(r'\b\w+\b',' '.join(row))) for row in rows)
 if sec['banner']=='B05':
  for c in plans:
   rows=[['Record',c['id']+' | '+c['name']+' | '+c['category']],['Purpose / prerequisites',c['purpose']+' '+c['prerequisites']],['Observable success',c['success_criteria']],['Setting / equipment / rewards',c['environment']+' '+c['equipment']+' '+c['reinforcement']],['Teaching sequence',' '.join(str(i+1)+'. '+x for i,x in enumerate(c['steps']))],['Progression / regression',c['progression']],['Generalization / maintenance',c['generalization']+' '+c['maintenance']],['Troubleshooting / welfare',c['troubleshooting']+' '+c['welfare']],['Evidence status','Original curriculum design under cited framework. '+ ' '.join('[['+sid+']]' for sid in c['evidence_ids'])]]
   data=[]
   for i,row in enumerate(rows):data.append([Paragraph(('<font color="white">' if i==0 else '<b>')+esc(row[0])+('</font>' if i==0 else '</b>'),st['Cell']),para(row[1],'Cell')])
   data[0][1]=Paragraph('<font color="white">'+esc(rows[0][1])+'</font>',st['Cell'])
   t=Table(data,colWidths=[129,375],hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#102b48')),('BACKGROUND',(0,1),(-1,-1),HexColor('#f1f7f9')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.25,HexColor('#c5d9df')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(KeepTogether([t,Spacer(1,12)]));words+=sum(len(re.findall(r'\b\w+\b',row[1])) for row in rows)
   if words-last>=470 and inline_idx<len(inline_order):add_inline()
  addbody('Individualization: puppies need brief manageable experiences and protected rest; adolescents may need easier criteria under distraction; adults need goals tied to real household needs; seniors need assessment of pain, footing and sensory change; dogs with disabilities need accessible cues and comfortable response forms. These are design adaptations; individual medical and behavioral assessment governs their application. No fixed acquisition timeline is promised.')
  temp=json.loads((R/'training_templates.json').read_text());story.append(Paragraph('<b>Individual plan template</b> | Copy and complete before starting.',st['Main']))
  for group in ['dog_profile','session_record']:
   data=[[Paragraph('<font color="white">'+esc(group.replace('_',' ').title())+'</font>',st['Cell']),Paragraph('<font color="white">Record</font>',st['Cell'])]]+[[Paragraph(esc(k.replace('_',' ')),st['Cell']),Paragraph('____________________________________',st['Cell'])] for k in temp[group]]
   t=Table(data,colWidths=[220,284],repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#102b48')),('GRID',(0,0),(-1,-1),.3,HexColor('#c5d9df')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t);story.append(Spacer(1,15))
  story.append(para('For an individual competency, copy every field from its record and replace general statements with the dog’s baseline, criterion, preferred rewards, exact environment and next smallest step. Record successes out of actual opportunities, observed discomfort and recovery. A single unsuccessful trial is information; it is not proof of stubbornness.'))
 story.append(PageBreak())
# Remaining illustrations appear only if needed at cadence, never as a fake quota gallery.
story.append(Paragraph('Notes',st['TitleS']))
for n in notes:story.append(Paragraph(f'<a name="note{n["note"]}"/>{n["note"]}. '+n['text'],st['SmallS']))
story.append(PageBreak());story.append(Paragraph('Bibliography',st['TitleS']))
for sid,s in sorted(src.items(),key=lambda kv:kv[1]['authors'][0].lower() if kv[0] in ['S02','S10','S22'] else kv[1]['authors'][0].split()[-1].lower()):
 url='https://doi.org/'+s['doi'] if s.get('doi') else s['stable_url']
 meta='';
 if s.get('volume'): meta+=' '+str(s['volume'])
 if s.get('issue'): meta+=' ('+str(s['issue'])+')'
 if s.get('pages'): meta+=': '+str(s['pages'])
 if s.get('article_number') and str(s['article_number'])!=str(s.get('pages')): meta+=': '+str(s['article_number'])
 text=esc(authors(s,True))+'. “'+esc(s['title'])+'.” <i>'+esc(s['venue'])+'</i>'+esc(meta)+'. '+esc(s['date'] or 'n.d.')+'. '+f'<link href="{esc(url)}" color="#087594">{esc(url)}</link>.'
 if s.get('pdf_url'):text+=f' <link href="{esc(s["pdf_url"])}" color="#087594">Authoritative PDF</link> ('+esc(s.get('pdf_retrieval','verified web link; download not claimed'))+').'
 text+=' ['+sid+'; '+esc(s['access_level'])+']'
 story.append(Paragraph(text,st['SmallS']))
doc=SimpleDocTemplate(str(R/'monograph.pdf'),pagesize=(W,H),leftMargin=54,rightMargin=54,topMargin=48,bottomMargin=58,title='SKI: Canine Communication and Humane Training',author='Research edition',allowSplitting=1)
doc.build(story,onFirstPage=furniture,onLaterPages=furniture)
for i in inv:
 pp=[x for x in placements if x['id']==i['id']];i['placement']=pp;i['status']='verified' if pp else 'generated_not_used';i['visual_approval']='Anatomy/context inspected in source overview; final page review pending'
(R/'image_inventory.json').write_text(json.dumps(inv,indent=2));(R/'notes.json').write_text(json.dumps(notes,indent=2));(R/'render_stats.json').write_text(json.dumps({'body_word_count':words,'inline_used':inline_idx,'notes':len(notes),'placements':placements},indent=2));print('Body words',words,'inline',inline_idx,'notes',len(notes))
