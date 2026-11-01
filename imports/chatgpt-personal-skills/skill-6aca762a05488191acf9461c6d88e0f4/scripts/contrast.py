"""Evaluate foreground candidates against actual RGB background samples."""
import argparse
import json


def rgb(value):
    value = value.removeprefix('#')
    if len(value) != 6:
        raise ValueError('Require six hexadecimal RGB digits')
    return tuple(int(value[i:i+2], 16) / 255 for i in (0, 2, 4))


def luminance(color):
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in color]
    return sum(v * w for v, w in zip(linear, (.2126, .7152, .0722)))


def ratio(a, b):
    x, y = sorted((luminance(a), luminance(b)))
    return (y + .05) / (x + .05)


def evaluate(backgrounds, candidates, target, alpha=1):
    if not backgrounds or not candidates or not 0 <= alpha <= 1 or target < 1:
        raise ValueError('Require samples, candidates, alpha in [0,1], and target >= 1')
    scores = {}
    for candidate in candidates:
        fg = rgb(candidate)
        scores[candidate] = min(ratio(tuple(alpha*f+(1-alpha)*b for f,b in zip(fg, rgb(bg))), rgb(bg)) for bg in backgrounds)
    selected = max(scores, key=scores.get)
    return {'candidate': selected, 'worst_ratio': scores[selected], 'target': target,
            'pass': scores[selected] >= target, 'scores': scores,
            'scope': 'Supplied RGB samples only; sample final rendered backgrounds separately'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--backgrounds', nargs='+', required=True)
    parser.add_argument('--candidates', nargs='+', default=['#FFFFFF', '#000000'])
    parser.add_argument('--target', type=float, default=7)
    parser.add_argument('--alpha', type=float, default=1)
    args = parser.parse_args()
    result = evaluate(args.backgrounds, args.candidates, args.target, args.alpha)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['pass'] else 1)
