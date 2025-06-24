from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# ✅ Add this route to serve the HTML interface
@app.route('/interface')
def interface():
    return render_template('index.html')

@app.route('/')
def home():
    return "Welcome to the Crypto Price Tracker API!"

@app.route('/price')
def get_price():
    coin = request.args.get('coin', default='bitcoin', type=str).lower()
    currency = request.args.get('currency', default='usd', type=str).lower()

    params = {
        'ids': coin,
        'vs_currencies': currency
    }

    response = requests.get(COINGECKO_API_URL, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from CoinGecko'}), 500

    data = response.json()

    if coin not in data:
        return jsonify({'error': f'Coin \"{coin}\" not found.'}), 404

    return jsonify({
        'coin': coin,
        'currency': currency,
        'price': data[coin][currency]
    })

if __name__ == '__main__':
    app.run(debug=True)
