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
    if not image_path.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
    
    #Lê a imagem usando OpenCV
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Falha ao carregar a imagem: {image_path}")

    #Converte a imagem para a escala de preto e branco (grayscale)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica Gaussian Blur para reduzir ruído e pequenas variações
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

    _, mask = cv2.threshold(
    blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    largest_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(largest_contour)
    product_crop = gray_image[y:y+h, x:x+w]

    # Redimensiona para tamanho fixo
    product_resized = cv2.resize(product_crop, (256, 256))    


    #Normaliza os valores dos pixels em um intervalo de [0,1]
    normalized_image = product_resized.astype("float32") / 255.0

    return normalized_image
    

