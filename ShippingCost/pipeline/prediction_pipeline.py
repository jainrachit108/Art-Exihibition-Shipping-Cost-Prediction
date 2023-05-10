import sys, os
import pandas as pd
from ShippingCost.utils import load_object
from ShippingCost.logger import logging
from ShippingCost.exception import ShippingException
   
ohe_obj_path = 'artifact\data_transformation\ohe object\ohe_obj.pkl'
scaler_obj_path = 'artifact\data_transformation\scaler_object\scaler.pkl'
model_obj_path = 'artifact\Model trainer\model_object\model.pkl'

        
        
    
    
class ShippingData:
    def __init__(self,
                 artist_reputation: float,
                 height:float,
                 width: float,
                 weight:float,
                 material:str,
                 price: float,
                 base_price: float,
                 international:str,
                 express_shipment : str,
                 installation_included: str,
                 transportation: str,
                 fragile : str,
                 customer_info: str,
                 remote_location : str
                 ) -> None:
        
        self.artist_reputation = artist_reputation
        self.height = height
        self.width = width
        self.weight = weight
        self.material = material
        self.price = price
        self.base_price = base_price
        self.international = international
        self.express_shipment = express_shipment
        self.installation_included = installation_included
        self.transportation = transportation
        self.fragile = fragile
        self.customer_info = customer_info
        self.remote_location = remote_location
        
    def get_data_as_dataframe(self):
        try:
            input_data = {
                'Artist Reputation': [self.artist_reputation],
                'Height' : [self.height],
                'Width' : [self.width],
                'Weight' : [self.weight],
                'Material' : [self.material],
                'Price Of Sculpture': [self.price],
                'Base Shipping Price': [self.base_price],
                'International' : [self.international],
                'Express Shipment' : [self.express_shipment],
                'Installation Included': [self.installation_included],
                'Transport': [self.transportation],
                'Fragile' : [self.fragile],
                'Customer Information': [self.customer_info],
                'Remote Location' : [self.remote_location]
                }
            
            return pd.DataFrame(input_data)
                        
        except Exception as e:
            raise ShippingException(e, sys)
        
    def predict(self):
            try:
                df = self.get_data_as_dataframe()
                logging.info('Load-ming Encoder Object')
                ohe_encoder = load_object(file_path=ohe_obj_path)
                logging.info('Performating One Hot Encoding ')
                
                df_encoded = ohe_encoder.transform(df[['Material','International','Express Shipment', 'Installation Included','Transport','Fragile', 'Customer Information', 'Remote Location']])
                df_encoded = pd.DataFrame(df_encoded,  columns = ohe_encoder.get_feature_names_out(['Material','International','Express Shipment','Installation Included','Transport','Fragile', 'Customer Information', 'Remote Location']))
                numerical_cols = ['Artist Reputation','Height','Width'	,'Weight','Price Of Sculpture','Base Shipping Price']
                df_predict = pd.concat([df[numerical_cols],df_encoded], axis =1)
                scaler = load_object(file_path=scaler_obj_path)
                df_predict = scaler.transform(df_predict)
                xgb = load_object(file_path = model_obj_path)
                cost = xgb.predict(df_predict)        
                return cost
            except Exception as e:
                raise ShippingException(e, sys)
