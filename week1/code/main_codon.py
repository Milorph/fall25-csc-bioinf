
from typing import List, Optional
from utils_codon import read_data
from dbg_codon import DBG
import sys

def main() -> None:
    argv: List[str] = sys.argv
    if len(argv) < 2:
        print("Usage: main_codon.py <data_dir>")
        return

    data_dir: str = "./" + argv[1]
    short1, short2, long1 = read_data(data_dir)

    k: int = 25
    dbg: DBG = DBG(k=k, data_list=[short1, short2, long1])

    out_path: str = data_dir + "/contig.fasta"
    with open(out_path, "w") as f:
        for i in range(20):
            c: Optional[str] = dbg.get_longest_contig()
            if c is None:
                break
            print(i, len(c))
            f.write(f">contig_{i}\n")
            f.write(c + "\n")


if __name__ == "__main__":
    main()
