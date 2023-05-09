from flask import Flask, render_template, request
from ShippingCost.pipeline.prediction_pipeline import ShippingData


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')
    
    else:
        
        artist_reputation = float(request.form['artist_reputation'])
        height = float(request.form.get('height'))
        width = float(request.form.get('width'))
        weight = float(request.form.get('weight'))
        material = request.form['material']
        price = float(request.form.get('price'))
        base_price = float(request.form.get('base_price'))
        international = request.form['international']
        express_shipment = request.form['express_shipment']
        installation_included = request.form['installation_included']
        transportation = request.form['transportation']
        fragile = request.form['fragile']
        customer_info = request.form['customer_info']
        remote_location = request.form['remote_location']
        
        data = ShippingData(artist_reputation=artist_reputation, height=height, width=width,weight=weight,material=material,base_price=base_price,price=price, 
                     international=international,express_shipment=express_shipment,customer_info=customer_info,fragile=fragile,installation_included=installation_included,remote_location=remote_location,transportation=transportation)
        
        cost = data.predict()
        return render_template('index.html', prediction_text = cost[0])




if __name__ == '__main__':
    app.run(debug=True)
