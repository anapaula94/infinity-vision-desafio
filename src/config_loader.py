import yaml
import os


def load_config(config_path: str) -> dict:
    """
    Carrega e valida o arquivo de configuração.

    Args:
        config_path (str): Caminho para o arquivo de configurãção YAML.

    Returns:
        dict: Parâmetros de configuração.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    required_keys = ["image_1", "image_2", "output_dir", "threshold"]

    for key in required_keys:
        if key not in config:
            raise KeyError(f"Chave de configurção ausente: {key}")

    return config
