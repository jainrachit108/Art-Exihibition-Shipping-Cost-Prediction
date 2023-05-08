from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        return render_template('index.html', prediction_text = 'Your estimated Shipping Cost will be ')

    if request.method == 'GET':
        ...


if __name__ == '__main__':
    app.run(debug=True)
