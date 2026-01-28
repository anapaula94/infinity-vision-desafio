import cv2
import numpy as np
from pathlib import Path
from database import DatabaseManager

from config_loader import load_config
from image_processing import load_and_preprocess_image
from similarity import calculate_euclidean_distance, is_same_product

def main(config_path: str) -> None:
    """
    Main da aplicação.

    Args:
        config_path (str): Caminho para o arquivo de configuração.
    """
    #Carrega a configuração 
    config = load_config(config_path)

    #Carrega e processa a imagem fornecida
    image_test_path = config["image_test"]
    image_test = load_and_preprocess_image(image_test_path)

    #Conecta ao banco para buscar referências
    if "database" not in config:
        print("Erro: Configurações de banco de dados não encontradas.")
        return
    
    try:
        db = DatabaseManager(config["database"])
        # Busca todos os produtos cadastrados no banco
        produtos_referencia = db.list_all_products() 

        if not produtos_referencia:
            print("Aviso: Nenhum produto de referência encontrado no banco de dados.")
            return

        print(f"Iniciando comparação de {image_test_path.name} contra {len(produtos_referencia)} produtos...")

        match_encontrado = False

        for produto in produtos_referencia:
            nome_ref = produto['nome_produto']
            caminho_ref = Path(produto['caminho_imagem_referencia'])
        
            #Carrega e processa a imagem de referência do banco
            image_ref = load_and_preprocess_image(caminho_ref)
            #Calcula a distancia Euclidiana
            distance = calculate_euclidean_distance(image_test, image_ref)
            #Verifica se as imagens representam o mesmo produto
            same_product = is_same_product(distance, config["threshold"])

            if same_product:
                    match_encontrado = True
                    print(f"\n[MATCH] Produto identificado: {nome_ref}")
                    print(f"Distância: {distance:.4f}")

                    # 6. Salva a imagem concatenada do match
                    img_test_save = (image_test * 255).astype(np.uint8)
                    img_ref_save = (image_ref * 255).astype(np.uint8)
                    combined_image = np.hstack((img_test_save, img_ref_save))
                    
                    output_path = config["output_dir"] / f"match_{nome_ref.replace(' ', '_')}.jpg"
                    cv2.imwrite(str(output_path), combined_image)

                    # 7. Registra o resultado na tabela de logs
                    db.save_result(
                        img1=image_test_path,
                        img2=caminho_ref,
                        img_res=output_path,
                        dist=distance,
                        is_same=True
                    )
                    # Se encontrar o primeiro match, podemos parar (opcional)
                    break 

        if not match_encontrado:
            print("\nResultado: Nenhum produto correspondente encontrado com o threshold atual.")

        db.close()

    except Exception as e:
        print(f"Erro durante a execução: {e}")

        """#Mostra os resultados
        print("Resultados da Comparação:")
        print(f"Imagem 1: {config['image_1'].name}")
        print(f"Imagem 2: {config['image_2'].name}")
        print(f"Distância Euclidiana: {distance: .4f}")

        if same_product:
            print("Resultado: MESMO PRODUTO")
        else:
            print("Resultado: PRODUTOS DIFERENTES")

        #Salva as alterações
        # Converte de float [0,1] de volta para uint8 [0,255] para salvar a imagem
        img1_save = (image_1 * 255).astype(np.uint8)
        img2_save = (image_2 * 255).astype(np.uint8)

        # Concatena as imagens transformadas lado a lado
        combined_image = np.hstack((img1_save, img2_save))
        # Define o caminho de saída vindo do config e salva [cite: 4, 11]
        output_path = config["output_dir"] / "resultado_comparacao.jpg"
        cv2.imwrite(str(output_path), combined_image)
        print(f"Imagem transformada salva em: {output_path}")

        #salva em bando de dados
        if "database" in config:
            try:
                db = DatabaseManager(config["database"])
                db.save_result(
                    img1=config["image_1"],
                    img2=config["image_2"],
                    img_res=output_path,
                    dist=distance,
                    is_same=same_product
                )
                print("Dados salvos no banco de dados com sucesso.")
                db.close()
            except Exception as e:
                print(f"Aviso: Não foi possível salvar no banco.Erro: {e}")"""


if __name__ == "__main__":
    #configuração do caminho(path)
    config_file_path = Path("config/config.yaml")
    main(str(config_file_path))