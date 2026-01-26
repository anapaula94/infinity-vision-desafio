import cv2
import numpy as np
from pathlib import Path

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

    #Carrega e processa as imagens
    image_1 = load_and_preprocess_image(config["image_1"])
    image_2 = load_and_preprocess_image(config["image_2"])

    #Calcula a distancia Euclidiana
    distance = calculate_euclidean_distance(image_1, image_2)    

    #Verifica se as imagens representam o mesmo produto
    same_product = is_same_product(distance, config["threshold"])

    
    #Mostra os resultados
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

if __name__ == "__main__":
    #configuração do caminho(path)
    config_file_path = Path("config/config.yaml")
    main(str(config_file_path))