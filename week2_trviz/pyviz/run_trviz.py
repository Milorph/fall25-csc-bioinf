# pyviz/run_trviz.py
import argparse, os
from pathlib import Path
import warnings
from Bio import BiopythonDeprecationWarning

# Silence the deprecation warning if you like (optional)
warnings.simplefilter("ignore", BiopythonDeprecationWarning)

from trviz.main import TandemRepeatVizWorker
from trviz.utils import get_sample_and_sequence_from_fasta

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fasta", "-f", type=str,
                   help="Path to FASTA with TR sequences (headers are sample IDs).")
    p.add_argument("--motif", "-m", action="append", required=False,
                   help="Motif(s) to guide decomposition. Repeat flag for multiple.")
    p.add_argument("--out", "-o", type=str, default=None,
                   help="Output PNG path (default: outputs/trviz_plot.png)")
    p.add_argument("--tr_id", type=str, default="TEST_TR")
    args = p.parse_args()

    # Resolve defaults relative to THIS file
    here = Path(__file__).resolve().parent
    proj = here.parent  # project root
    fasta_path = Path(args.fasta) if args.fasta else (proj / "data" / "demo.fa")
    output_dir = proj / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_png = Path(args.out) if args.out else (output_dir / "trviz_plot.png")

    if not fasta_path.exists():
        raise FileNotFoundError(
            f"FASTA not found: {fasta_path}\n"
            f"Tip: if you run from pyviz/, pass --fasta ../data/demo.fa"
        )

    # Load sequences
    sample_ids, tr_sequences = get_sample_and_sequence_from_fasta(str(fasta_path))
    print(f"Loaded {len(tr_sequences)} sequences from {fasta_path}")

    if len(tr_sequences) == 0:
        raise ValueError(
            "No sequences parsed from FASTA. Check that:\n"
            "  - headers start with '>'\n"
            "  - sequences are below their header lines\n"
            "  - file encoding/line breaks are normal (UTF-8, LF)\n"
        )

    # Choose motifs (from CLI or a reasonable default)
    motifs = args.motif if args.motif else ["ACCTTG", "ACCTTC"]

    viz = TandemRepeatVizWorker()
    viz.generate_trplot(
        tr_id=args.tr_id,
        sample_ids=sample_ids,
        tr_sequences=tr_sequences,
        motifs=motifs,
        output_dir=str(output_dir),
        output_name=str(out_png),
        verbose=True
    )
    print(f"Done. Wrote {out_png}")

if __name__ == "__main__":
    main()
