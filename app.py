from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_price')
def get_price():
    coin = request.args.get('coin')
    if not coin:
        return jsonify({'error': 'Missing coin parameter'})

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        if coin in data:
            price = data[coin]['usd']
            return jsonify({'price': price})
        else:
            return jsonify({'error': f"Coin '{coin}' not found."})
    except Exception as e:
        return jsonify({'error': 'Error fetching price'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
