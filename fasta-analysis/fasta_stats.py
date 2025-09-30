#!/usr/bin/env python3

"""
fasta_stats.py
Leitura de FASTA e geração de estatísticas por sequência:
 - id, descrição, length, counts (A,C,G,T,N), GC%, ambiguous_bases
Uso: python fasta_stats.py -i examples/test.fasta -o output.csv
"""

import argparse
from pathlib import Path
from collections import Counter
from Bio import SeqIO
from Bio.Seq import Seq
import csv
import json
import sys

def compute_counts_and_gc(seq_str):
    """Retorna (length, gc_percent, counts_dict, ambiguous_cout)."""
    s = seq_str.upper()
    counts = Counter(s)
    length = len(s)
    #GC% cuidado com length 0
    gc = 0.0
    if length:
        gc = (counts.get("G", 0) + counts.get("C", 0)) / length * 100
    #bases canônicas
    canonical = counts.get("A", 0) + counts.get("C", 0) + counts.get("G", 0) + counts.get("T", 0)
    ambiguous = length - canonical
    return length, round(gc, 3), dict(counts), ambiguous

def record_to_dict(record, do_revcomp=False):
    """Transforma um SeqRecord em um dicionário plano com estatísticas."""
    seq_str = str(record.seq)
    length, gc, counts, ambiguous = compute_counts_and_gc(seq_str)
    out = {
        "id": record.id,
        "description": record.description,
        "length": len(record.seq),
        "gc_percent": gc,
        "count_A": counts.get("A",0),
        "count_C": counts.get("C",0),
        "count_G": counts.get("G",0),
        "count_T": counts.get("T",0),
        "count_N": counts.get("N",0),
        "ambiguous_bases": ambiguous
    }
    if do_revcomp:
        #usar Biopython para reverse complement seguro
        out["revcomp"] = str(Seq(seq_str).reverse_complement())
    return out

def parse_args():
    p = argparse.ArgumentParser(description="FASTA per-sequence statistics")
    p.add_argument("-i", "--input", required=True, help="Arquivo FASTA de entrada")
    p.add_argument("-o", "--output", default=None, help="Arquivo CSV de saída (se omitido, imprime no stdout)")
    p.add_argument("--json", action="store_true", help="Salvar também em JSON (mesmo nome do CSV com .json)")
    p.add_argument("--revcomp", action="store_true", help="Incluir reverse-complement no output (pode ser pesado)")
    p.add_argument("--min-length", type=int, default=0, help="Filtrar sequências com comprimento < valor")
    return p.parse_args()

def main():
    args = parse_args()
    in_path = Path(args.input)
    if not in_path.exists():
        print(f"Erro: arquivo {in_path} não encontrado.", file=sys.stderr)
        sys.exit(1)

    records = []
    for rec in SeqIO.parse(str(in_path), "fasta"):
        if len(rec.seq) < args.min_length:
            continue
        rec_dict = record_to_dict(rec, do_revcomp=args.revcomp)
        records.append(rec_dict)

    if not records:
        print("Nenhuma sequência processada.", file=sys.stderr)
        sys.exit(1)

    #Campos/colunas ordenadas
    fieldnames = ["id", "description", "length", "gc_percent", "count_A", "count_C", "count_G", "count_T", "count_N", "ambiguous_bases"]
    if args.revcomp:
        fieldnames.append("revcomp")

    #Output CSV
    if args.output:
        with open(args.output, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow(r)
            print(f"CSV salvo em: {args.output}")
    else:
            #Imprimir tabela simples no stdout
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow(r)

    #JSON opcional
    if args.json:
        json_path = Path(args.output) if args.output else Path("fasta_stats.json")
        #se CSV fornecido, trocar extensão
        if json_path.suffix ==".csv":
            json_path = json_path.with_suffix(".json")
        with open(json_path, "w") as fh:
            json.dump(records, fh, indent=2)
            print(f"JSON salvo em: {json_path}")

if __name__ == "__main__":
    main()
        