import os 
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from config.paths_config import RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, CONFIG_PATH,RAW_DIR
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml


logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]
        os.makedirs(RAW_DIR, exist_ok=True)
        
        logger.info("DataIngestion initialized with config: %s", self.config)
    
    
    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info("CSV file downloaded to {RAW_FILE_PATH}")
            
        except Exception as e:
            logger.error("Error downloading CSV from GCP: %s", e)
            raise CustomException(str(e)) from e
        
        
    def split_data(self):
        try:
            logger.info("Starting the spliting")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data,  random_state=42,test_size=1-self.train_test_ratio)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            
            logger.info("Data split into train and test sets")
        except Exception as e:
            logger.error("Error splitting data: %s", e)
            raise CustomException(str(e)) from e
        
    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion process completed successfully")
        except CustomException as ce:
            logger.error("CustomException occurred: %s", ce)
            raise
        except Exception as e:
            logger.error("An unexpected error occurred: %s", e)
            raise CustomException(str(e)) from e
        finally:
            logger.info("Data ingestion process finished")
            
            
if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
    
            
            
        