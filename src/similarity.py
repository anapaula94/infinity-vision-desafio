import numpy as np 


def calculate_euclidean_distance(
    image_1: np.ndarray,
    image_2: np.ndarray
) -> float:
    """
    Calcula a distância euclidiana entre duas imagens.

    Args:
        image_1 (np.ndarray): Primeira imagem pré-processada.
        image_2 (np.ndarray): Segunda imagem pré-processada

    Returns:
        float: Distância euclidiana entre as duas imagens.
    """
    #Confere se ambas imagens tem as mesmas dimensões
    if image_1.shape != image_2.shape:
        raise ValueError("As Imagens devem ter as mesmas dimensões para calcular a distância")

    #Transforma as imagens 2D em vetores 1D
    vector_1 = image_1.flatten()
    vector_2 = image_2.flatten()

    #Calcula a distância Euclidiana entre os vetores

    distance = np.linalg.norm(vector_1 - vector_2)

    return float(distance)


def is_same_product(distance: float, threshold: float) -> bool:
    """
    Determina se as duas imagens representam o mesmo produto.

    Args:
        distance (float): Distância Euclidiana entre as imagens.
        threshold (float): Valor limite para comparação.

    Returns:
        bool: True se o produto for o mesmo , False caso o não sejam o mesmo produto.
    """
    return distance < threshold