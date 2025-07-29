import os 


###############Define paths for data ingestion and model training###############


RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")


CONFIG_PATH = "config/config.yaml"



######data Processing paths######
PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_FILE_PATH = os.path.join(PROCESSED_DIR, "train_processed.csv")
PROCESSED_TEST_FILE_PATH = os.path.join(PROCESSED_DIR, "test_processed.csv")




######Model TRAINING######
MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"

