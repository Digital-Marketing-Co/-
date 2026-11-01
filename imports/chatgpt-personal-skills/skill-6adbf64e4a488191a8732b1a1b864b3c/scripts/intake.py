#!/usr/bin/env python3
"""Parse only the leading invocation and optional unquoted no flag."""
import argparse,json,re
def parse(text):
    m=re.match(r'^\s*[/\$](book|textbook)\b\s*',text,re.I)
    if not m:raise ValueError('Expected leading /book or /textbook')
    brief=text[m.end():]
    flag=re.match(r'^(?:no|-no|--no|--no-interactive)(?=\s|$)\s*',brief,re.I)
    if flag:brief=brief[flag.end():]
    return {'source':text,'mode':m.group(1).lower(),'interactive':not bool(flag),'brief':brief,'missing_subject':not brief.strip()}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('invocation');a=p.parse_args()
    try:print(json.dumps(parse(a.invocation),ensure_ascii=False))
    except ValueError as e:p.exit(1,str(e)+'\n')
