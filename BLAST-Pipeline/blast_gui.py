import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import logging
from blast_pipeline import check_blast_installed, create_blast_db, run_blastn  # Importe funções do seu pipeline
from parse_blast import parse_blast_results  # Importe o parser

def select_query_file():
    file_path = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta *.fas")])
    if file_path:
        entry_query.delete(0, tk.END)
        entry_query.insert(0, file_path)

def select_ref_file():
    file_path = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta *.fas")])
    if file_path:
        entry_ref.delete(0, tk.END)
        entry_ref.insert(0, file_path)

def run_blast_analysis():
    query_file = entry_query.get()
    ref_file = entry_ref.get()
    evalue = entry_evalue.get() or "1e-5"  # Valor padrão se vazio

    if not query_file or not ref_file:
        messagebox.showerror("Erro", "Selecione arquivos de consulta e referência!")
        return

    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    output_dir = Path(base_dir) / "output"
    output_dir.mkdir(exist_ok=True)

    try:
        # Configura logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        # Verifica instalação do BLAST
        check_blast_installed()

        # Cria banco de dados
        db_name = "ref_db"
        create_blast_db(Path(ref_file), db_name, output_dir)

        # Executa BLAST
        blast_output = output_dir / "blast_results.txt"
        run_blastn(Path(query_file), output_dir / db_name, blast_output, float(evalue))

        # Analisa resultados
        summary_csv = output_dir / "blast_summary.csv"
        top_hits = parse_blast_results(blast_output, summary_csv)

        # Exibe resultados na GUI
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Resultados do BLAST:\n\n")
        for index, row in top_hits.iterrows():
            result_text.insert(tk.END, f"Consulta: {row['qseqid']}\n")
            result_text.insert(tk.END, f"Alvo: {row['sseqid']}\n")
            result_text.insert(tk.END, f"% Identidade: {row['pident']:.2f}%\n")
            result_text.insert(tk.END, f"Comprimento: {row['length']}\n")
            result_text.insert(tk.END, f"E-value: {row['evalue']}\n\n")

        messagebox.showinfo("Sucesso", f"Análise BLAST concluída! Resultados salvos em {output_dir}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um problema: {str(e)}")

def export_to_json():
    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    output_dir = Path(base_dir) / "output"
    csv_path = output_dir / "blast_summary.csv"
    if csv_path.exists():
        import pandas as pd
        df = pd.read_csv(csv_path, sep=';')
        json_path = output_dir / "blast_summary.json"
        df.to_json(json_path, orient='records', indent=2)
        messagebox.showinfo("Sucesso", f"Resultados exportados para {json_path}")
    else:
        messagebox.showerror("Erro", "Nenhum resultado CSV encontrado para exportar!")

# Configuração da janela
try:
    root = tk.Tk()
    root.title("BLAST Pipeline GUI")
    root.geometry("600x600")
    root.configure(bg='#f0f0f0')

    # Rótulos e campos
    tk.Label(root, text="Selecione arquivo de consulta (Query FASTA):", bg='#f0f0f0', font=('Arial', 10, 'bold')).pack(pady=5)
    entry_query = tk.Entry(root, width=50, bg='white', font=('Arial', 10))
    entry_query.pack(pady=5)
    btn_select_query = tk.Button(root, text="Escolher Query", command=select_query_file, bg='#4CAF50', fg='white', font=('Arial', 10))
    btn_select_query.pack(pady=5)

    tk.Label(root, text="Selecione arquivo de referência (Reference FASTA):", bg='#f0f0f0', font=('Arial', 10, 'bold')).pack(pady=5)
    entry_ref = tk.Entry(root, width=50, bg='white', font=('Arial', 10))
    entry_ref.pack(pady=5)
    btn_select_ref = tk.Button(root, text="Escolher Reference", command=select_ref_file, bg='#4CAF50', fg='white', font=('Arial', 10))
    btn_select_ref.pack(pady=5)

    tk.Label(root, text="E-value (padrão: 1e-5):", bg='#f0f0f0', font=('Arial', 10)).pack(pady=5)
    entry_evalue = tk.Entry(root, width=20, bg='white', font=('Arial', 10))
    entry_evalue.insert(0, "1e-5")
    entry_evalue.pack(pady=5)

    # Botões
    btn_run = tk.Button(root, text="Executar BLAST", command=run_blast_analysis, bg='#2196F3', fg='white', font=('Arial', 10))
    btn_run.pack(pady=10)

    btn_json = tk.Button(root, text="Exportar em JSON", command=export_to_json, bg='#9C27B0', fg='white', font=('Arial', 10))
    btn_json.pack(pady=5)

    # Área de resultados
    result_text = tk.Text(root, height=20, width=60, bg='white', font=('Courier', 10))
    result_text.pack(pady=10)

    root.mainloop()
except Exception as e:
    print(f"Erro fatal: {str(e)}")
    input("Pressione Enter para sair...")