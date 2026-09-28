# /decode battery

All logs base 2 unless noted. \(N\) is token count after the regex tokenizer `[A-Za-z]+(?:'[A-Za-z]+)?`. Types are lowercased. \(V\) is the number of distinct types. \(f(w)\) is the count of type \(w\). Rank \(r\) is 1 for the most frequent type.

## Inventory

- \(N\), \(V\), TTR \(V/N\)
- frequency spectrum \(V(f)\) = number of types with count \(f\)
- hapax, dis, tris (\(f=1,2,3\))
- hapax-legomenon rate \(V(1)/V\)

## Information

Unigram entropy

\[
H_1 = -\sum_w \frac{f(w)}{N}\log_2\frac{f(w)}{N}
\]

Maximum entropy on the observed alphabet \(H_{\max}=\log_2 V\). Redundancy \(R=1-H_1/H_{\max}\). Perplexity \(2^{H_1}\).

Bigram conditional entropy

\[
H_2 = -\sum_{u,v}\hat p(u,v)\log_2\hat p(v\mid u)
\]

Mutual information \(I(W_t;W_{t+1})=H_1-H_2\) on the joint of adjacent tokens.

Letter entropy \(H_{\mathrm{let}}\) on a-z after case fold. Compare to Shannon's 4.14 bit first-order English letter entropy (26-letter, 1951).

## Zipf and Heaps

Zipf \(f(r)\approx C r^{-\alpha}\). Zipf-Mandelbrot \(f(r)\approx C(r+\beta)^{-\alpha}\). Fit \(\alpha\) by OLS on \(\log f\) versus \(\log r\) for ranks with \(f\ge 2\) when \(V\) is small. Heaps \(V(n)=Kn^{\beta}\) is reported only as a running curve on prefixes; a single document cannot identify \(K,\beta\) tightly.

## Good-Turing and add-one

Good-Turing \(P_{\mathrm{GT}}(\text{unseen})\approx V(1)/N\). Add-one

\[
P_{+1}(w)=\frac{f(w)+1}{N+V}.
\]

## Next token

MLE trigram if the suffix was seen, else bigram, else unigram, mixed with the interpolation in SKILL.md. Report the top three masses.

## Cipher battery (all are tests of H1, not proofs)

- Index of coincidence on letters, expected English \(\approx 0.0667\), random 26-letter \(\approx 0.0385\)
- Chi-square of letter frequencies against published English percentages
- Missing-letter set
- Acrostic of first letters, first letters of sentences if punctuation exists
- Compression ratio with zlib as a crude Kolmogorov proxy
- Runs test on a binary split (function words vs content, or the two dominant types)
- Change-point by maximising the two-piece unigram log-likelihood over split index \(t\)

## Outliers

A type is an outlier if \(f(w)\) exceeds the Zipf prediction at its rank by a factor of 3 or more, or if it is a hapax that is orthographically longer than mean length plus two sample standard deviations. Report both lists.

## Device caveat

An iPhone 16 Pro Max first bar is a function of the on-device predictor (historically a small transformer UniLM for the three bars, later overlapping Apple Intelligence AFM-class models), the user language model, locale, and contacts. This battery estimates a corpus-internal continuation. It is not a dump of Apple weights.
