# Week 4 – Sequence Alignment Report

For this assignment I implemented four alignment algorithms: global (Needleman–Wunsch), local (Smith–Waterman), semi-global/fitting, and affine-gap global. I first wrote everything in Python to make sure the logic was correct, then ported it to Codon. Both versions use +3 for match, −3 for mismatch, and −2 for gaps (with affine using −5 open and −1 extend). I tested everything on the given pairs (q1–t1 through q5–t5) and the long MT-human vs MT-orang sequences.

At first, the Codon version gave type errors like `List[type[int]]` and couldn’t find `argparse`, so I replaced it with manual argument parsing. The affine-gap alignment also needed debugging because my initial initialization over-penalized the first gaps. Once fixed, both Python and Codon versions produced the same scores. Codon ran long for the shorters sequences but way faster for long sequences like human and orang

I built an `evaluate.sh` that automatically runs both implementations, measures runtime in milliseconds, and prints results in a clean table.

