#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import logging
from pathlib import Path
from Bio import SeqIO

def check_blast_installed():
    try:
        subprocess.run(["makeblastdb", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["blastn", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        logging.error("Ferramentas BLAST+ (makeblastdb ou blastn) não encontradas. Instale o NCBI BLAST+.")
        sys.exit(1)

def create_blast_db(ref_fasta, db_name, output_dir):
    cmd = ["makeblastdb", "-in", str(ref_fasta), "-dbtype", "nucl", "-out", str(output_dir / db_name)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Banco de dados BLAST criado: {db_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao criar banco de dados BLAST: {e}")
        sys.exit(1)

def run_blastn(query_fasta, db_path, output_file, evalue):
    cmd = [
        "blastn", "-query", str(query_fasta), "-db", str(db_path), "-out", str(output_file), "-outfmt", "6", "-evalue", str(evalue),
        "-task", "blastn-short"
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Resultados do BLAST salvos em {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar blastn {e}")
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description="Automatiza criação de banco de dados BLAST e alinhamento")
    parser.add_argument("-q", "--query", required=True, help="Arquivo FASTA de consulta")
    parser.add_argument("-r", "--reference", required=True, help="Arquivo FASTA de referência")
    parser.add_argument("-o", "--output", default="output", help="Diretório de saída")
    parser.add_argument("-e", "--evalue", type=float, default=1e-5, help="Limiar de e-value")
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    args = parse_args()

    # Valida arquivos de entrada
    query_path = Path(args.query)
    ref_path = Path(args.reference)
    if not query_path.exists() or not ref_path.exists():
        logging.error("Arquivo FASTA de consulta ou referência não encontrado.")
        sys.exit(1)

    # Cria diretório de saída
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    # Verifica instalação do BLAST
    check_blast_installed()

    # Cria banco de dados BLAST
    db_name = "ref_db"
    create_blast_db(ref_path, db_name, output_dir)

    # Executa blastn
    blast_output = output_dir / "blast_results.txt"
    run_blastn(query_path, output_dir / db_name, blast_output, args.evalue)

    logging.info("Pipeline BLAST concluído com sucesso!")

    if __name__ == "__main__":
        main()