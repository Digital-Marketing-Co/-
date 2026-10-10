#!/usr/bin/env python3
"""Propose mnemonic keywords; create only with an explicit flag and token."""
import argparse
import json
import os
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


def destination(value):
    value = value if '://' in value else 'https://' + value
    parsed = urlsplit(value)
    if parsed.scheme not in ('https','http') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Require an HTTP(S) destination without embedded credentials')
    if any(ord(c)<32 for c in value):
        raise ValueError('Destination contains control characters')
    return value


def candidates(value, keyword=None):
    parsed=urlsplit(destination(value))
    host=(parsed.hostname or '').removeprefix('www.').split('.')[0]
    words=[re.sub('[^a-z0-9-]','',x.lower()) for x in parsed.path.strip('/').split('/')]
    guesses=[keyword] if keyword else [*words[-2:],host,host+'-'+(words[-1] if words else '')]
    result=sorted({x for x in guesses if x and re.fullmatch('[a-zA-Z0-9][a-zA-Z0-9-]{0,63}',x)},key=lambda x:(len(x),x))
    if keyword and not result:raise ValueError('Keyword must be 1–64 letters, digits, or hyphens')
    return [{'keyword':x,'link':'https://bit.ly/'+x,'status':'UNVERIFIED'} for x in result]


def create(value, keyword, token, group):
    if not token or not group:
        raise ValueError('Creation requires BITLY_ACCESS_TOKEN and BITLY_GROUP_GUID')
    body={'long_url':destination(value),'domain':'bit.ly','keyword':keyword,'group_guid':group}
    request=Request('https://api-ssl.bitly.com/v4/bitlinks',data=json.dumps(body).encode(),
                    headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'},method='POST')
    with urlopen(request,timeout=20) as response:
        data=json.load(response)
    if data.get('long_url') != body['long_url']:
        raise ValueError('Returned destination differs from the requested destination')
    expected='https://bit.ly/'+keyword
    custom=data.get('custom_bitlinks',[])
    returned=[data.get('link'),*['https://'+x.removeprefix('https://') for x in custom]]
    if expected not in returned:
        raise ValueError('API did not confirm the requested keyword; inspect account state before retrying')
    return {'link':expected,'destination':body['long_url'],'status':'CREATED','redirect_status':'NOT TESTED'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url');parser.add_argument('--keyword');parser.add_argument('--create',action='store_true')
    args=parser.parse_args()
    try:
        value=destination(args.url); choices=candidates(value,args.keyword)
        if args.create:
            if not args.keyword:raise ValueError('Creation requires an explicit --keyword')
            result=create(value,choices[0]['keyword'],os.environ.get('BITLY_ACCESS_TOKEN'),os.environ.get('BITLY_GROUP_GUID'))
        else:result={'destination':value,'candidates':choices,'status':'PROPOSED','availability':'UNVERIFIED'}
        print(json.dumps(result,indent=2));return 0
    except Exception as exc:
        # Never log request headers, tokens, or provider response bodies.
        print(json.dumps({'status':'FAILED','error_type':type(exc).__name__,'message':str(exc) if isinstance(exc,ValueError) else 'Provider request failed; inspect account status before retrying'}));return 1


if __name__=='__main__':raise SystemExit(main())
