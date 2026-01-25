from pathlib import Path
import yaml


def load_config(config_path: str) -> dict:
    """
    Carrega e valida o arquivo de configuração.

    Args:
        config_path (str): Caminho para o arquivo de configurãção YAML.

    Returns:
        dict: Parâmetros de configuração.
    """
    config_file = Path(config_path)

    if not config_file.exists(config_path):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")

    with config_file.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    required_keys = ["image_1", "image_2", "output_dir", "threshold"]
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Chave de configurção ausente: {key}")

    #Converte paths to Path 
    config["image_1"] = Path(config["image_1"])
    config["image_2"] = Path(config["image_2"])
    config["output_dir"] = Path(config["output_dir"])

    #Cria o repositório output caso não exista
    config["output_dir"].mkdir(parents=True, exist_ok=True)

    return config
