-- Criação da Tabela Resultados
CREATE TABLE IF NOT EXISTS resultados_comparacao (
    id SERIAL PRIMARY KEY,
    img_1_origem TEXT,        
    img_2_origem TEXT,       
    img_final_resultado TEXT, 
    distancia_calculada FLOAT, 
    foi_aprovado BOOLEAN,     
    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Criação tabela Produtos
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome_produto TEXT NOT NULL,
    caminho_imagem_referencia TEXT NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);