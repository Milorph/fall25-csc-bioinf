
from typing import List, Tuple

def read_fasta(path: str, name: str) -> List[str]:
    data: List[str] = []
    if path.endswith("/"):
        full: str = path + name
    else:
        full: str = path + "/" + name

    with open(full, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] != ">":
                data.append(line)

    first_len: int = len(data[0]) if len(data) > 0 else 0
    print(name, len(data), first_len)
    return data

def read_data(path: str) -> Tuple[List[str], List[str], List[str]]:
    short1: List[str] = read_fasta(path, "short_1.fasta")
    short2: List[str] = read_fasta(path, "short_2.fasta")
    long1:  List[str] = read_fasta(path, "long.fasta")
    return (short1, short2, long1)
