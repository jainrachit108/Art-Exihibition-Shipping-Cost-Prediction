
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
    