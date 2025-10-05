import pandas as pd
from pathlib import Path

def parse_blast_results(blast_file, output_csv):
    columns = [
        "qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore"
    ]
    df = pd.read_csv(blast_file, sep="\t", header=None, names=columns)
    top_hits = df.groupby("qseqid").first().reset_index()
    top_hits.to_csv(output_csv, index=False, sep=";")
    print(f"Resultados analisados do BLAST salvo em {output_csv}")
    return top_hits

if __name__ == "__main__":
    blast_file = Path("output/blast_results.txt")
    output_csv = Path("output/blast_summary.csv")
    parse_blast_results(blast_file, output_csv)