
import pandas as pd 
from ShippingCost.logger import logging
from ShippingCost.exception import ShippingException
from ShippingCost.config import mongo_client
import os,sys
import yaml
import numpy as np
import dill


def get_collection_as_dataFrame(database_name : str , collection_name: str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """

    try:
        logging.info(f"Reading data from database :{database_name} and collection {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping _id column")
            df= df.drop("_id" , axis =1)
        logging.info(f"Rows and columns in df are {df.shape}")
        return df
    except Exception as e:
        raise ShippingException(e, sys)
    
    
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise ShippingException(e, sys) from e
        
        
def load_numpy_array_data(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"File {file_path} does not exist")
        logging.info(f'file path{file_path}')
        with open(file_path , 'rb') as file_obj:
            return np.load(file_obj)
        
    except Exception as e:
        raise ShippingException(e, sys) from e
            
def save_object(file_path: str, obj:object):
    try:
        logging.info(f'Making directory {file_path} to save object')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj , file_obj)
        
        
    except Exception as e:
        raise ShippingException(e, sys)
    
def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise Exception(f'File path {file_path} does not exists')
        
        logging.info(f'loading object from file path {file_path}')
        with open(file_path) as file_obj:
            return dill.load(file_obj)
        
        
    except Exception as e:
        raise ShippingException(e, sys)
