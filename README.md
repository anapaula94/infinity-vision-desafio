# Desafio Técnico – Infinity Vision

Este repositório contém a solução para o desafio técnico proposto pela Infinity Vision,
que consiste em comparar imagens de produtos de supermercado utilizando técnicas
básicas de Visão Computacional.

## Objetivo
Determinar se duas imagens representam o mesmo produto, a partir da distância
euclidiana entre versões pré-processadas das imagens.

## Funcionalidades Principais
A aplicação utiliza técnicas de processamento digital de imagens para determinar se duas fotos representam o mesmo item com base em um limiar (threshold) configurável.
- Busca Dinâmica 1:N: Compara uma imagem de entrada contra todos os produtos cadastrados no banco de dados.
- Processamento de Imagem: Conversão para escala de cinza e redimensionamento para 256x256.
- Visão Computacional: Extração de contornos para isolar o produto (crop) e cálculo de Distância Euclidiana.
- Análise de Similaridade: Classificação automática entre "Mesmo Produto" ou "Produtos Diferentes".
- Banco de Dados: Armazenamento de resultados e caminhos de arquivos em banco de dados PostgreSQL

## Tecnologias utilizadas
- Python 3.9+: Linguagem base.
- OpenCV: Biblioteca especializada para transformações e visão computacional.
- NumPy: Operações matemáticas em matrizes para cálculo de distância.
- PostgreSQL: Banco de dados relacional para persistência de logs.
- Psycopg2: Driver de conexão com o banco de dados.
- PyYAML: Manipulação do arquivo de configuração.
- Docker & Docker Compose: Orquestração de containers.

## Configuração e Instalação

1. Requisitos Prévios
- nstalar dependências: pip install opencv-python numpy pyyaml psycopg2-binary
- Ter o PostgreSQL instalado e rodando na porta 5432.

2. Banco de Dados 
Execute o script em sql/create_table.sql para criar a tabela resultados_comparacao. Esta tabela armazena:
- Caminhos das imagens originais e da imagem resultado (concatenada).
- A distância numérica calculada e o resultado final da comparação.

## 🚀 Como Executar (Via Docker)

Esta é a forma recomendada, pois o Docker configurará automaticamente o banco de dados PostgreSQL e o ambiente Python.

###  Requisitos Prévios
- Ter o **Docker** e o **Docker Desktop** instalados.

### Iniciar os Containers
Na raiz do projeto, execute:
```bash
docker compose up -d --build
```
### Criar Tabelas

```bash
docker compose exec db psql -U postgres -d infinity_vision_db -c "conteudo do arquivo create_table.sql"
```

### Popular banco com imagens de referência
```bash
docker compose exec app python src/populate_db.py
```
### Rodar a Comparação Principal
```bash
docker compose exec app python src/main.py
```

## Como Executar Localmente

No terminal, a partir da raiz do projeto, execute o Bash:
```bash
python src/populate_db.py
```
```bash
python src/main.py
```

## Saídas do Programa

- Console: Exibição da distância euclidiana e status da comparação.
- Imagem: Uma única imagem concatenando as duas fotos processadas é salva no output_dir.
- Banco de Dados: Registro completo da operação para auditoria futura.

