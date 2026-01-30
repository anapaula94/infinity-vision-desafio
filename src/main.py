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


if __name__ == "__main__":
    #configuração do caminho(path)
    config_file_path = Path("config/config.yaml")
    main(str(config_file_path))