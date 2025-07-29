import os
import pandas as pd

from src.logger import get_logger
from src.custom_exception import CustomException
import yaml


logger = get_logger(__name__)

def read_yaml(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path,'r') as f:
            config = yaml.safe_load(f)
            logger.info("Successfully read the YAML file.")
            return config
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise CustomException(e)
    


def load_data(path):
    try:
        logger.info(f"Loading data from {path}")
        return pd.read_csv(path)
    
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        raise CustomException(e)
    
    