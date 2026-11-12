#!/usr/bin/env python3
"""Deterministic security checks for skill text. No network or paid inference."""
import argparse, json, pathlib, re, unicodedata
BIDI=set(chr(x) for x in list(range(0x202A,0x202F))+list(range(0x2066,0x206A)))
INVISIBLE={"\u200b","\u200c","\u200d","\ufeff","\u2060"}
SENSITIVE=re.compile(r"(?i)(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-[A-Za-z0-9]{30,})")
def inspect(path, data):
    findings=[]
    for i,line in enumerate(data.splitlines(),1):
        if any(c in BIDI for c in line): findings.append({"line":i,"kind":"bidi-control"})
        if any(c in INVISIBLE for c in line): findings.append({"line":i,"kind":"invisible-character"})
        if SENSITIVE.search(line): findings.append({"line":i,"kind":"possible-secret"})
        if unicodedata.normalize("NFKC",line)!=line: findings.append({"line":i,"kind":"compatibility-normalization-difference"})
    return findings
def run(paths):
    out={}
    for path in paths:
        p=pathlib.Path(path)
        if p.is_file():
            out[str(p)]=inspect(str(p),p.read_text(encoding="utf-8"))
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument("paths",nargs="+");args=ap.parse_args()
    result=run(args.paths);print(json.dumps(result,indent=2,ensure_ascii=False))
    raise SystemExit(1 if any(result.values()) else 0)
if __name__=="__main__": main()
