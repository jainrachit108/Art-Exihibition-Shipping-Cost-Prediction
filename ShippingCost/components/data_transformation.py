from ShippingCost.logger import logging
from ShippingCost.exception import ShippingException
from ShippingCost.entity import config_entity
from ShippingCost.entity import artifact_entity
import sys, os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from ShippingCost.utils import save_numpy_array_data



class DataTransformation:
    def __init__(self, 
                 data_validation_artifact: artifact_entity.DataValidationArtifact,
                 data_transformation_config: config_entity.DataTransformationConfig) -> None:
        
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        
        except Exception as e:
            ShippingException(e, sys)
            
            
            
            
    def random_imputation(self,df, col):
        try:
            imputed_col_values = np.random.choice(df[~df[col].isna()][col].values, size = df[col].isna().sum())
            col_null_indices = df[df[col].isna()].index
            df.loc[col_null_indices, col] = imputed_col_values
            return df

        except Exception as e:
            ShippingException(e, sys)
    
    def remove_outliers_iqr(self,dataframe, column):
        """
        Remove outliers from a pandas DataFrame using the IQR method.
        
        Parameters:
        dataframe (pandas.DataFrame): Input DataFrame.
        column (str): Name of column to remove outliers from.
        
        Returns:
        pandas.DataFrame: DataFrame with outliers removed.
        """
        data = dataframe[column]
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        cleaned_dataframe = dataframe[(data > lower_bound) & (data < upper_bound)]
        return cleaned_dataframe
            
    def initiate_data_transformation(self):
        try:
            logging.info(f"{'<<'*20} Data Transformation {'>>' * 20}")
            logging.info('Loading validated dataset')
            df = pd.read_csv(self.data_validation_artifact.validated_dataset_path)
            
            #Randomly imputing missing values of Height, Width and Artist Reputation
            logging.info('Randomly Imputing missing values of Height')
            df = self.random_imputation(df , 'Height')
            logging.info('Randomly Imputing missing values of Width')
            df = self.random_imputation(df, 'Width')
            logging.info('Randomly imputing the missing values of Artist Reputation')
            df = self.random_imputation(df, 'Artist Reputation')
            
            #One-hot Encoding 
            logging.info('One-hot Encoding the Categorical Columns')
            logging.info('Creating one-hot Encoder object')
            encoder = OneHotEncoder(sparse = False, handle_unknown = 'ignore')
            logging.info('One hot encoding "Material, International, Express Shipment, Installation Included, Transport, Fragile, Customer Information, Remote Location')
            df_encoded = encoder.fit_transform(df[['Material','International','Express Shipment', 'Installation Included','Transport','Fragile', 'Customer Information', 'Remote Location']])
            df_encoded = pd.DataFrame(df_encoded,  columns = encoder.get_feature_names_out(['Material','International','Express Shipment','Installation Included','Transport','Fragile', 'Customer Information', 'Remote Location']))
            
            df_encoded.drop(['Transport_nan', 'Remote Location_nan','Material_nan'], axis = 1, inplace = True)
            logging.info('OneHotEncoding completed Successfully')
            
            
            numerical_cols = ['Artist Reputation','Height','Width'	,'Weight','Price Of Sculpture','Base Shipping Price']
            X = pd.concat([df[numerical_cols] , df_encoded], axis= 1)
            
            #Performing KNN Imputation on dataset to impute values of weight column
            imputer = KNNImputer(n_neighbors=5)
            imputed_df = imputer.fit_transform(X)
            X = pd.DataFrame(imputed_df, columns=X.columns)
            df_new = pd.concat([X , df['Cost']], axis =1)


            #Removing outliers
            
            logging.info('Removing Outliers from Height')
            df_new = self.remove_outliers_iqr(df_new, 'Height')
            
            logging.info('Removing Outliers from width')
            df_new = self.remove_outliers_iqr(df_new, 'Width')

            logging.info('Removing Outliers from Weight')
            df_new = self.remove_outliers_iqr(df_new, 'Weight')

            logging.info('Removing Outliers from Price Of Sculpture')
            df_new = self.remove_outliers_iqr(df_new, 'Price Of Sculpture')
            
            X = df_new.drop('Cost', axis = 1)
            y = df_new['Cost']
            
            #Splitting training and testing data
            logging.info('Splitting training and testing data')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3, random_state = 42)
            
            #Performing Feature Scaling
            logging.info('Feature Scaling')
            scaler = RobustScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
            logging.info('Creating transformation path directory')
            transformation_file_dir = os.path.dirname(self.data_transformation_config.data_transformation_dir)
            os.makedirs(transformation_file_dir, exist_ok= True)
            logging.info('Saving X_train, X_test, y_train, y_test in data transformation path')
            save_numpy_array_data(file_path=self.data_transformation_config.Xtrain_dataset, array=X_train)
            save_numpy_array_data(file_path=self.data_transformation_config.Ytrain_dataset, array=y_train)
            save_numpy_array_data(file_path=self.data_transformation_config.Xtest_dataset, array=X_test)
            save_numpy_array_data(file_path=self.data_transformation_config.Ytest_dataset, array=y_test)
            
            
            #Creating Data Transformation Artifact
            logging.info('Creating data transformation Artifact')
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(X_train_array_path=self.data_transformation_config.Xtrain_dataset,
                                                                                      X_test_array_path= self.data_transformation_config.Xtest_dataset,
                                                                                      y_train_array_path=self.data_transformation_config.Ytrain_dataset,
                                                                                      y_test_array_path=self.data_transformation_config.Ytest_dataset)
            
            
        except Exception as e:
            ShippingException(e, sys)
            