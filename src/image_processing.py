from pathlib import Path
import cv2
import numpy as np 

def load_and_preprocess_image(
    image_path: Path,
    size:tuple[int,int] = (256,256)
) -> np.ndarray:

    """
    Carrega a imagem do disco e aplicar as etapas de pré-processamento:
    - Converte a imagem para escala de cinza
    - Redimensiona a imagem para um valor fixo (256x256)
    - Normalizar os valores dos pixels

    Args:
        image_path (Path): Caminho onde está a imagem.
        size (tuple): Tamanho desejado (largura, altura).

    Returns:
        np.ndarray: Imagem pré-processada como uma matriz NumPy 2D.
    """
    #Confere se a imagem existe
    if not image_path.exits():
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
    
    #Lê a imagem usando OpenCV
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Falha ao carregar a imagem: {image_path}")

    #Converte a imagem para a escala de preto e branco (grayscale)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Redimensiona a imagem para o tamanho desejado 
    resized_image = cv2.resize(gray_image. size)

    #Normaliza os valores dos pixels em um intervalo de [0,1]
    normalized_image = resized_image.astype(np.float32)/ 255.0

    return normalized_image
    

