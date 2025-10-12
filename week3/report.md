week 3 report

this week i worked on reimplementing biotite’s tree and treenode classes in codon. i started with the biotite source and rewrote it to be fully compatible with codon’s static typing but first chaing it to Pure python from CPython. that meant removing numpy and changing all the type hints to things like list, optional, and tuple. i also replaced treeerror with valueerror since codon didn’t like custom exceptions being mixed with builtin ones.

after the code built locally, i made test_phylo.codon and test_phylo.py to compare codon vs python runtime. both versions parse a newick string and compute distances between leaves. then i made evaluate.sh in the week3 folder to build the codon binary, run both versions, and show the runtimes in a small table.

overall, it compiled and ran cleanly. locally codon runs in about 0-1 ms and python takes around 4-6 ms. the struggles were codon’s strict typing.

gotchas:
- codon is strict about optional typing, you can’t just use labels=None, it must be declared optional[list[str]].

