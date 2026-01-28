import psycopg2
from pathlib import Path
#import sys
#import os

#sys.path.append(os.getcwd())
from config_loader import load_config

def populate_products(db_config: dict):
    #Cadastra as imagens de referência na tabela produtos.
    try:
        #Conecta com o banco
        conn = psycopg2.connect(**db_config["database"])
        cur = conn.cursor()

        #Caminho das imagens de referência
        path_ref = Path("data/input")
        #Busca todas as imagens .jpg ou .png na pasta
        image_files = list(path_ref.glob("*.jpg")) + list(path_ref.glob("*.png"))

        if not image_files:
            print(f"Nenhuma imagem encontrada em {path_ref}")
            return

        for img_path in image_files:
            nome_produto = img_path.stem.replace("_"," ").title()
            caminho_str = str(img_path.absolute())

            #Insere no banco de dados
            query = """
                INSERT INTO produtos (nome_produto, caminho_imagem_referencia)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """
            cur.execute(query,(nome_produto, caminho_str))

        conn.commit()
        print(f"Sucesso: {len(image_files)} produtos sincronizados com o banco.")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao popular o banco: {e}")

if __name__ == "__main__":
    
    #Carrega as configurações
    config_data = load_config("config/config.yaml")
    populate_products(config_data)