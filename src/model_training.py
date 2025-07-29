import  os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from config.model_params import LIGHTGBM_PARAMS, RANDOM_SEARCH_PARAMS
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import  load_data,read_yaml
from scipy.stats import randint, uniform
import mlflow
import mlflow.sklearn 


logger = get_logger(__name__)


class ModelTrainer:
    def __init__(self,train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        
        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS
        
    
    
    
    def load_split_data(self):
        try:
            logger.info("Loading training and testing data")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            
            
            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']
            
            
            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']
            
            logger.info("Data loaded successfully")
            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error in loading data: {e}")
            raise CustomException(f"Error in loading data: {e}")
        
    
    
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Starting LightGBM model training")
            model = lgb.LGBMClassifier(**self.params_dist)
            logger.info("Starting our Hyperparameter tuning ")
            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
            )
            
            random_search.fit(X_train, y_train)
            logger.info("Model training completed successfully")
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_
            logger.info(f"Best parameters found: {best_params}")
            
            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error in training model: {e}")
            raise CustomException(f"Error in training model: {e}")
        
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating the model")
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            logger.info("Accuracy: {:.2f}".format(accuracy))
            logger.info("Precision: {:.2f}".format(precision))
            logger.info("Recall: {:.2f}".format(recall))
            logger.info("F1 Score: {:.2f}".format(f1))
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1
            }
        except Exception as e:
            logger.error(f"Error in evaluating model: {e}")
            raise CustomException(f"Error in evaluating model: {e}")
        
        
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            
            logger.info(f"Saving the model to {self.model_output_path}")
            joblib.dump(model, self.model_output_path)
            
            
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error in saving model: {e}")
            raise CustomException(f"Error in saving model: {e}")
        
    
    
    def run(self):
        try:
            with mlflow.start_run():
                # mlflow.set_experiment("Hotel  Booking Model Training")
                # mlflow.log_params(self.params_dist)
                # mlflow.log_params(self.random_search_params)
                logger.info("Starting model training process")
                
                logger.info("Starting our MLFLOW experimentation")
                
                logger.info("Logging the training and testing dataset to MLFLOW")
                
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")
                
                X_train, y_train, X_test, y_test = self.load_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                evaluation_metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)
                logger.info("Model training process completed successfully")
                
                logger.info("Logging the model to MLFLOW")
                
                mlflow.log_artifact(self.model_output_path)
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(evaluation_metrics)
                
        
        except Exception as e:
            logger.error(f"Error in model training process: {e}")
            raise CustomException(f"Error in model training process: {e}")
        
if __name__ == "__main__":
    trainer = ModelTrainer(
        train_path=PROCESSED_TRAIN_FILE_PATH,
        test_path=PROCESSED_TEST_FILE_PATH,
        model_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()
    
            