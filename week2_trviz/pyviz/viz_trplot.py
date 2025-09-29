import sys
from trviz.visualizer import TandemRepeatVisualizer

def plot_from_txt():
    # allow filenames from CLI args
    txt_path = sys.argv[1] if len(sys.argv) > 1 else "outputs/aligned.txt"
    motif_map_path = sys.argv[2] if len(sys.argv) > 2 else "outputs/motif_map.txt"
    out = "outputs/plot.png"

    rows, ids = [], []
    with open(txt_path) as f:
        for line in f:
            parts = line.strip().split("\t")
            ids.append(parts[0])
            rows.append(parts[1])

    # load motif map
    symbol_to_motif = {}
    with open(motif_map_path) as f:
        for line in f:
            motif, sym, count = line.strip().split("\t")
            symbol_to_motif[sym] = motif

    viz = TandemRepeatVisualizer()
    viz.trplot(
        rows,
        sample_ids=ids,
        symbol_to_motif=symbol_to_motif,
        output_name=out
    )
    print(f"Plot saved to {out}")

if __name__ == "__main__":
    plot_from_txt()
