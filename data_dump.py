import pymongo
import pandas as pd
import json
from ShippingCost.config import mongo_client
from ShippingCost.logger import logging
# Provide the mongodb localhost url to connect python to mongodb.

DATABASE_NAME = 'Art_Exibition_Shipping_cost'
COLLECTION_NAME = 'Shipping_Cost_dataset'

DATA_PATH = "ShippingCostPrediction.csv"

if __name__ == '__main__':
    df =pd.read_csv(DATA_PATH)
    print(f'Rows and columns are {df.shape}')
    df.reset_index(drop = True, inplace = True)
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    logging.info('Loading Data to mongoDB')
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
    logging.info('Successfully loaded data to mongoDB')