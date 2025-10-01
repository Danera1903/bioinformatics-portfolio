# Como Usar o FASTA Analysis

Este guia explica como utilizar os scripts de análise de arquivos FASTA disponíveis no diretório `fasta-analysis`. O principal script, `fasta_stats.py`, calcula estatísticas de sequências (comprimento, porcentagem de GC, contagem de nucleotídeos) e gera visualizações como histogramas.

## Pré-requisitos
- **Python 3.x** instalado.
- Bibliotecas necessárias: `biopython`, `pandas`, `matplotlib`, `seaborn`.
- Instale as dependências com:
  ```bash
  pip install biopython pandas matplotlib seaborn

## Passo a Passo

## 1 Clone o Repositório:
git clone https://github.com/Danera1903/bioinformatics-portfolio.git
cd bioinformatics-portfolio/projects/fasta-analysis

## 2 Prepare um Arquivo FASTA:
Coloque seu arquivo FASTA (ex.: meu_arquivo.fasta) na pasta examples/ ou use o exemplo fornecido (test.fasta).

## 3 Execute o Script:
Rode o script fasta_stats.py com os argumentos necessários:
python fasta_stats.py -i examples/test.fasta -o output/results.csv

## Opções:

-i: Caminho do arquivo FASTA de entrada.
-o: Caminho do arquivo CSV de saída com as estatísticas.

## 4 Visualize os Resultados:
Abra o arquivo output/results.csv para ver as estatísticas (ex.: comprimento, GC%, contagem de bases).
Gere um histograma (opcional) com:

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("output/results.csv")
df['length'].hist(bins=20, color='teal', edgecolor='black')
plt.title('Histograma dos Comprimentos')
plt.show()

Para salvar a imagem:
plt.savefig('output/histogram.png')

Exemplo de Saída
O arquivo output/results.csv conterá algo como:

id,description,length,gc_percent,count_A,count_C,count_G,count_T,count_N,ambiguous_bases
seq1,seq1 Homo_sapiens_example,28,39.286,6,5,6,6,5,5
seq2,seq2 Unknown_organism,27,55.556,6,7,8,6,0,0

## Notas
Certifique-se de que o ambiente virtual (se usado) esteja ativado: venv\Scripts\activate (Windows) ou source venv/bin/activate (Linux/Mac).
Para mais detalhes, consulte o código em fasta_stats.py.

Sinta-se à vontade para sugerir melhorias ou relatar problemas! 🚀.