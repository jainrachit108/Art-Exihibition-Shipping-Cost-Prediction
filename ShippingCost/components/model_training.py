from ShippingCost.logger import logging
from ShippingCost.exception import ShippingException
from ShippingCost.entity import config_entity
from ShippingCost.entity import artifact_entity
import sys, os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error
from ShippingCost.utils import load_numpy_array_data, save_object





class ModelTrainer:
    def __init__(self, data_transformation_artifact = artifact_entity.DataTransformationArtifact,
                 model_training_config = config_entity.ModelTrainingConfig) -> None:
        try:
            logging.info(f"{'>>'*20}Model Trainer {'<<'*20} ")
            self.model_trainer_config = model_training_config
            self.data_transformation_artifact = data_transformation_artifact          
            
        except Exception as e:
            raise ShippingException(e ,sys)
            
    def initiate_model_training(self):
        try:
            
            logging.info('Loading X_train, y_train, X_test, y_test array from data transform artifact')
            
            X_train = load_numpy_array_data(file_path=self.data_transformation_artifact.Xtrain_dataset_path)
            X_test = load_numpy_array_data(file_path=self.data_transformation_artifact.Xtest_dataset_path)
            y_train = load_numpy_array_data(file_path=self.data_transformation_artifact.Ytrain_dataset_path)
            y_test = load_numpy_array_data(file_path= self.data_transformation_artifact.Ytest_dataset_path)
            logging.info('Successfully loaded X_train, X_test, y_train, y_test')
            
            logging.info('Creating Model Regressor object')
            xgb  = XGBRegressor()



            param_grid = {
                    'n_estimators': [100],
                    'learning_rate': [0.1],
                    'min_child_weight': [1],
                    'subsample': [0.6],
                    'colsample_bytree': [0.6, 0.8],
                    'max_depth': [5]
                    }
            
            grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')
            grid_search.fit(X_train, y_train)

            logging.info(f'Best parameters:{grid_search.best_params_}')
            
            xgb_reg_best = XGBRegressor(**grid_search.best_params_)

            xgb_reg_best.fit(X_train, y_train)

            # Make predictions on test data
            y_pred = xgb_reg_best.predict(X_test)


            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)            
            logging.info(f'RMSE:{rmse}')
            logging.info(f'R-squared:{r2}')  
            
            #Saving Model 
            logging.info('Creating model trainer directory')
            model_trainer_dir = os.path.dirname(self.model_trainer_config.model_trainer_dir)
            os.makedirs(model_trainer_dir, exist_ok=True)
            logging.info('Saving model.pkl file in model trainer directory')
            save_object(self.model_trainer_config.model_obj_path, xgb_reg_best)
            
            #Creating Artifact
            logging.info('Creating artifact folder')
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_obj_path=self.model_trainer_config.model_obj_path) 
            logging.info('Successfully loaded the data in the model trainer artifact')
            return model_trainer_artifact
            
            
        except Exception as e:
            raise ShippingException(e ,sys)
            