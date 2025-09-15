# Bonus Point Report: Genome Identification (data1–data4)

We identified the genomes for datasets **data1–data4** by taking the longest contig from each assembly and running BLASTn (megablast) against the NCBI `nt` database. Results are summarized below.

---

## Data1
**Top BLAST hits:**
- *Porphyromonas gingivalis* strain W83 (CP025932.1) – 99.825% identity, 8,582 bp alignment  
- *Porphyromonas gingivalis* strain W50 (CP092048.1) – 99.825% identity, 8,582 bp alignment  
- Other *P. gingivalis* strains with identical scores  

**Conclusion:**  
The genome is ***Porphyromonas gingivalis***. The contig aligns equally well to W83 and W50 (and derivatives), so the exact strain is ambiguous.  

---

## Data2
**Top BLAST hits:**
- *Porphyromonas gingivalis* strain W83 (CP025932.1) – 99.615% identity, 8,580 bp alignment  
- *Porphyromonas gingivalis* strain W50 (CP092048.1) – 99.615% identity, 8,580 bp alignment  
- Other *P. gingivalis* strains with identical scores  

**Conclusion:**  
The genome is also ***Porphyromonas gingivalis***. Similar to data1, multiple strains score identically, so strain-level identification is not possible from this contig alone.  

---

## Data3
**Top BLAST hits:**
- *Paracidovorax citrulli* strain KACC 18784 (CP127360.1) – 99.969% identity, 9,824 bp alignment  
- *Paracidovorax citrulli* strain KACC 17005 (CP127363.1) – 99.969% identity, 9,824 bp alignment  
- Other *P. citrulli* strains with identical scores  

**Conclusion:**  
The genome is ***Paracidovorax citrulli***. All top hits point consistently to *P. citrulli* strains with nearly perfect identity (>99.9%). Strain-level resolution is again ambiguous because multiple strains align equally well.  

---

## Data4
**Top BLAST hits:**
- *Butyrivibrio proteoclasticus* B316 (CP001810.1) – 98.956% identity, 91,836 bp alignment  
- [Clostridium] saccharolyticum WM1 (CP002109.1) – 98.540% identity, 67,726 bp alignment  
- *Lacrimispora saccharolytica* FDAARGOS_1340 (CP070235.1) – 98.528% identity, 67,741 bp alignment  

**Conclusion:**  
The genome is most consistent with ***Butyrivibrio proteoclasticus***, specifically strain **B316**, supported by a long (≈92 kb) alignment at ~99% identity. Other close clostridial relatives also align well, but with shorter coverage.  

---

# Final Summary
- **Data1:** *Porphyromonas gingivalis* (strain W83/W50 ambiguous)  
- **Data2:** *Porphyromonas gingivalis* (strain W83/W50 ambiguous)  
- **Data3:** *Paracidovorax citrulli* (strain ambiguous)  
- **Data4:** *Butyrivibrio proteoclasticus* (closest to strain B316)  

