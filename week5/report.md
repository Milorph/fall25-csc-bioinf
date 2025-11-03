This week’s deliverable focused on running a full variant-calling and phasing pipeline using Illumina and PacBio FASTQ samples on the CYP2C gene family. I downloaded the provided .fq.bz2 reads, extracted them, and aligned them to chromosome 10 of GRCh38 using minimap2. Variant calling was performed with bcftools mpileup and bcftools call, followed by phasing using whatshap. Finally, I compared the phased VCFs for shared and unique variants, and inspected discordant sites visually in IGV.

Gotchas:

The PacBio file was tricky — WhatsHap failed at first because the BAM lacked alignments overlapping the target region. Re-running with the correct chromosome subset fixed it.

.fq.bz2 compression initially broke the workflow, so I switched to uploading extracted FASTQs instead.

In GitHub Actions, nbconvert had issues finding python3 and saving to week5/week5/week5_output.ipynb; fixing the notebook path and kernel resolved it.

Running in Colab was much slower than local or CI, especially for minimap2 alignment.