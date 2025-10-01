import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta *.fas")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def export_to_json():
    if os.path.exists("output/results.csv"):
        df = pd.read_csv("output/results.csv")
        json_path = os.path.join("output", "results.json")
        df.to_json(json_path, orient='records')
        messagebox.showinfo("Sucesso", f"Resultados exportados para {json_path}")
    else:
        messagebox.showerror("Erro", "Nenhum resultado CSV encontrado para exportar!")

def run_analysis():
    input_file = entry.get()
    if not input_file:
        messagebox.showerror("Erro", "Selecione um arquivo FASTA!")
        return
    output_dir = "output"
    output_file = os.path.join(output_dir, "results.csv")
    # Cria o diretório output se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        data = []
        for record in SeqIO.parse(input_file, "fasta"):
            seq = str(record.seq).upper()  # Converte para maiúsculas
            length = len(seq)
            gc = (seq.count('G') + seq.count('C')) / length * 100 if length > 0 else 0
            counts = {
                'A': seq.count('A'),
                'C': seq.count('C'),
                'G': seq.count('G'),
                'T': seq.count('T'),
                'N': seq.count('N')
            }
            ambig = sum(1 for base in seq if base not in 'ATCGN')
            data.append([record.id, str(record.description), length, gc, counts['A'], counts['C'],
                         counts['G'], counts['T'], counts['N'], ambig])  # Corrigido: T em vez de N duplicado
        df = pd.DataFrame(data, columns=['id', 'description', 'length', 'gc_percent', 'count_A', 'count_C',
                                        'count_G', 'count_T', 'count_N', 'ambiguous_bases'])
        df.to_csv(output_file, index=False)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Resultados da Análise:\n\n")
        for index, row in df.iterrows():
            result_text.insert(tk.END, f"Sequência: {row['id']}\n")
            result_text.insert(tk.END, f"Comprimento: {row['length']}\n")  # Removido espaço extra
            result_text.insert(tk.END, f"GC%: {row['gc_percent']:.2f}%\n")  # Removido espaço extra
            result_text.insert(tk.END, f"Contagens: A={row['count_A']}, C={row['count_C']}, G={row['count_G']}, T={row['count_T']}\n")  # Removido espaço extra
            result_text.insert(tk.END, f"Ambíguas: {row['ambiguous_bases']}\n\n")  # Removido espaço extra
        try:
            bins = int(bins_entry.get()) if bins_entry.get() else 20
        except ValueError:
            bins = 20
        messagebox.showinfo("Sucesso", f"Análise concluída! Resultados salvos em output/results.csv e histogram.png (bins={bins})")
        df['length'].hist(bins=bins, color='teal', edgecolor='black')  # Usa bins dinâmico
        plt.title('Histograma dos Comprimentos')
        plt.xlabel('Comprimento')
        plt.ylabel('Frequência')
        histogram_path = os.path.join(output_dir, "histogram.png")  # Corrigido: histogram_path
        plt.savefig(histogram_path)
        plt.show()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um problema: {str(e)}")

# Configuração da janela
root = tk.Tk()
root.title("FASTA Analysis GUI")
root.geometry("500x500")

# Usa ttk para um tema mais moderno
try:
    from tkinter import ttk
    style = ttk.Style()
    style.theme_use('clam')
except:
    pass

# Define uma cor de fundo clara
root.configure(bg='#f0f0f0')

# Adiciona um rótulo
tk.Label(root, text="Selecione um arquivo FASTA:", bg='#f0f0f0', font=('Arial', 10, 'bold')).pack(pady=10)

# Adiciona um campo de entrada
entry = tk.Entry(root, width=50, bg='white', font=('Arial', 10))
entry.pack(pady=5)

# Adiciona um rótulo e campo para número de bins
tk.Label(root, text="Número de bins do histograma:", bg='#f0f0f0', font=('Arial', 10)).pack(pady=5)
bins_entry = tk.Entry(root, width=10, bg='white', font=('Arial', 10))
bins_entry.insert(0, "20")
bins_entry.pack(pady=10)

# Adiciona um botão para selecionar arquivo
btn_select = tk.Button(root, text="Escolher Arquivo", command=select_file, bg='#4CAF50', fg='white', font=('Arial', 10))
btn_select.pack(pady=5)

# Adiciona um botão para executar a análise
btn_run = tk.Button(root, text="Executar Análise", command=run_analysis, bg='#2196F3', fg='white', font=('Arial', 10))
btn_run.pack(pady=10)

# Adiciona um botão para exportar em JSON
btn_json = tk.Button(root, text="Exportar em JSON", command=export_to_json, bg='#9C27B0', fg='white', font=('Arial', 10))
btn_json.pack(pady=5)

# Adiciona uma área de texto para resultados
result_text = tk.Text(root, height=15, width=50, bg='white', font=('Courier', 10))  # Ajustado height para 15
result_text.pack(pady=10)

# Manter a janela aberta
root.mainloop()