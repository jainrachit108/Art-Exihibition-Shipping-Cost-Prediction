# Art Shipping Cost Predictor App
This is an end-to-end Art Shipping Cost Predictor app that uses an XGBoost model to predict the shipping cost of art pieces. The app includes a complete training pipeline and prediction pipeline. The data ingestion, data validation, data transformation, and model training components are all included. The app also includes config and artifact entities.

Click on the link and predict the cost of Shipment for your Art Piece.
https://jainrachit108-art-exihibition-shipping-cost-predicti-app-gho446.streamlit.app/


## Features
### Training Pipeline
The training pipeline ingests data from a MongoDB server, performs data validation, and transforms the data before training an XGBoost model. The model is then saved as an artifact.

### Prediction Pipeline
The prediction pipeline loads the saved model artifact and uses it to predict the shipping cost of art pieces.

### Data Dumping into MongoDB
The app also provides the feature to dump the dataset into MongoDB. This allows the user to easily update the dataset with new data.

## Streamlit App
The model is integrated into a Streamlit app, which allows the user to easily upload art piece details and get a shipping cost prediction.

How to Run the App

1. Clone the repository: git clone https://github.com/jainrachit108/Art-Exihibition-Shipping-Cost-Prediction.git
2. Install the required packages: pip install requirements.txt
3. Set up the MongoDB server and ensure it's running.
4. Run the training pipeline: python main.py 

This will download the dataset from the MongoDB server, perform data validation, transform the data, train an XGBoost model, and save the model artifact.
5. Run the Streamlit app: streamlit run app.py
This will start the Streamlit app, where you can upload a new art piece details and get a shipping cost prediction.

## Credits
This app was created by Rachit Jain.


