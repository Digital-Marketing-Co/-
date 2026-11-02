#!/usr/bin/env python3
"""Render every PDF page to evidence PNG and report geometry flags.
PNG rendering is evidence generation, NOT automated visual perception/approval.
"""
import argparse, hashlib, json
from pathlib import Path
import fitz
from pdf_layout_audit import inspect

def render(pdf, destination, dpi=120):
    if not 72 <= dpi <= 220:
        raise ValueError("DPI must be in [72, 220]")
    source=Path(pdf).resolve()
    out=Path(destination).resolve()
    if out == source.parent or out == source or source in out.parents:
        # A per-document sibling subfolder is permitted, but never overwrite source.
        if out == source or out == source.parent:
            raise ValueError("Separate output directory required")
    out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):
        raise ValueError("Evidence directory must be empty to prevent stale frames")
    doc=fitz.open(str(source))
    try:
        if doc.is_encrypted:
            raise ValueError("Encrypted PDF unsupported")
        pages=[]
        scale=dpi/72
        for i,page in enumerate(doc,1):
            frame=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False)
            p=out/f"page-{i:04d}.png"
            frame.save(str(p))
            pages.append({"page":i,"file":p.name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"width":frame.width,"height":frame.height})
    finally:
        doc.close()
    geometry=inspect(str(source))
    report={"source_file":source.name,"source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"page_count":len(pages),"rendered_pages":pages,"geometry":geometry,"visual_inspection":"NOT TESTED","limitations":["Rendered page images require actual inspection at reading and zoom scales.","Geometry flags do not establish math or accessibility correctness."]}
    (out/"report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("pdf");p.add_argument("evidence_directory");p.add_argument("--dpi",type=int,default=120)
    a=p.parse_args()
    print(json.dumps(render(a.pdf,a.evidence_directory,a.dpi),indent=2))
