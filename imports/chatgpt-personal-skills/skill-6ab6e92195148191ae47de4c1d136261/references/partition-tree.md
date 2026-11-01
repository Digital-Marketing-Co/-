# 1-2 digit partition tree

Locked reading: 10=J, 11=K, 22=V, 26=Z. Zero is skipped. Values outside 1..26 cannot occupy one cell.

Example 112263 valid full strings

AABBFC, AABZC, AAVFC, ALBFC, ALZC, KBBFC, KBZC, KVFC

Invalid cells include 63.

Reduction of those strings by ordinal sum plus a second 1-2 parse of the sum yields the leaf bag DB, BD, CC, X, AE, O. The same leaf bag appears on 221163 because the two dates are digit permutations of the same compact November-22 pattern.

Connected node means the leaf is reachable from more than one branch. It does not mean a hidden author.
