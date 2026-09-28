# /Q maps (v1.1)

## A1Z26

A=1 ... Z=26. Digit concatenation of a word W uses the raw ordinals (S=19, C=3, D=4 → 1934, or zero-padded 190304).

## Plus and times windows

For ordinals \(v_1,\ldots,v_n\) and for every split of the concatenated decimal string \(s\) into \(s[:k]\) and \(s[k:]\):

\[
\sigma_k = \mathrm{int}(s[:k]) + \mathrm{int}(s[k:]),\qquad
\pi_k = \mathrm{int}(s[:k]) \cdot \mathrm{int}(s[k:])
\]

Also adjacent \(v_i+v_{i+1}\) and \(v_i\cdot v_{i+1}\), plus the full sum and full product.

Read an integer back through A1Z26 bundles: 17=Q, 26=Z and BF, 57=EG, 108=JH / AH / J8.

## Pairs

K ↔ AA, V ↔ BB, FC ↔ SFC. Applied after letterization, not before arithmetic unless the source already contains those letters.

## Base 22

Digits 0-9A-L. A0 reads 0→A … 21→V. A1 reads 0→O, 1→A … 21→U.

## Date integers in the house battery

112263, 11221963, 221163, 22111963 (November 22 compact forms). These are labels, not findings.

## Furthermore chain (v1.2)

After the first adjacent + or * pair on a length-3 window \(v_1,v_2,v_3\):

\[
a=v_1+v_2,\quad b=v_2+v_3,\quad a+b \;\text{and}\; a\cdot b
\]

Letterize each result with A1Z26 when it lies in 1..26. Concatenate those two letters.

Locked demonstration

ABC = 1,2,3 → a=3, b=5 → 8=H, 15=O → HO ≈ HOE.

The product window 2 and 6 furthermore-sums to 8=H and furthermore-products to 12=L → HL.

Approx is only HO → HOE. No other fuzzy stems.
