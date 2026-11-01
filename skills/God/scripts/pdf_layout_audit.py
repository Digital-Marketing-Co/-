"""Conservative PDF text geometry checks; reports suspects, not visual proof."""
import json
import sys
import fitz

def inspect(path):
    doc = fitz.open(path)
    issues = []
    for index, page in enumerate(doc, 1):
        bounds = page.rect
        blocks = page.get_text('dict').get('blocks', [])
        for b in blocks:
            for line in b.get('lines', []):
                for span in line.get('spans', []):
                    if not span.get('text', '').strip():
                        continue
                    rect = fitz.Rect(span['bbox'])
                    if not rect.intersects(bounds) or rect.x0 < bounds.x0 - 1 or rect.y0 < bounds.y0 - 1 or rect.x1 > bounds.x1 + 1 or rect.y1 > bounds.y1 + 1:
                        issues.append({'page': index, 'type': 'TEXT_OUTSIDE_PAGE', 'text': span['text'][:60]})
                    if span.get('size', 100) < 6:
                        issues.append({'page': index, 'type': 'VERY_SMALL_TEXT', 'text': span['text'][:60]})
        if not page.get_text().strip():
            issues.append({'page': index, 'type': 'NO_EXTRACTABLE_TEXT'})
    return {'pages_checked':len(doc),'status':'REVIEW' if issues else 'NO_GEOMETRY_FLAGS', 'issues':issues,'limitations':['Does not establish visual correctness, figure fidelity, mathematical validity or PDF accessibility.']}
if __name__ == '__main__':
    print(json.dumps(inspect(sys.argv[1]), indent=2))
