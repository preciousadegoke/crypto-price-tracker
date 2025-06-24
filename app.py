from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Now shows HTML by default

@app.route("/price")
def get_price():
    coin = request.args.get('coin', default='bitcoin', type=str).lower()
    currency = request.args.get('currency', default='usd', type=str).lower()

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': coin,
        'vs_currencies': currency
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from API"}), 500

    data = response.json()
    if coin not in data:
        return jsonify({"error": f"Coin '{coin}' not found"}), 404

    return jsonify({
        "coin": coin,
        "currency": currency,
        "price": data[coin][currency]
    })

if __name__ == "__main__":
    app.run(debug=True)
