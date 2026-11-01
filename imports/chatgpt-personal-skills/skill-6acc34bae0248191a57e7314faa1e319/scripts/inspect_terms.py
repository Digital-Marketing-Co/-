#!/usr/bin/env python3
import json
import sys
from schemata import Vocabulary
v=Vocabulary()
for term in sys.argv[1:]:
    print(json.dumps({'term':term,'definition':v.terms.get(term),'ancestors':sorted(v.ancestors(term))},indent=2,ensure_ascii=False))
