from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_price")
def get_price():
    coin = request.args.get("coin", "").lower()
    currency = request.args.get("currency", "usd").lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"

    try:
        response = requests.get(url)
        data = response.json()
        if coin in data and currency in data[coin]:
            return jsonify({
                "coin": coin,
                "currency": currency,
                "price": data[coin][currency]
            })
        else:
            return jsonify({"error": "Coin or currency not found"}), 404
    except Exception as e:
        return jsonify({"error": "Error fetching price"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
