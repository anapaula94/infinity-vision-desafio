-- Criação da Tabela
CREATE TABLE IF NOT EXISTS resultados_comparacao (
    id SERIAL PRIMARY KEY,
    img_1_origem TEXT,        
    img_2_origem TEXT,       
    img_final_resultado TEXT, 
    distancia_calculada FLOAT, 
    foi_aprovado BOOLEAN,     
    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);