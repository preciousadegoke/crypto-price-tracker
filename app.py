from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_price")
def get_price():
    coin = request.args.get("coin", "bitcoin")
    currency = request.args.get("currency", "usd")

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            price = data[coin][currency]
            return jsonify({"price": price})
        except KeyError:
            return jsonify({"error": "Invalid coin or currency"}), 400
    else:
        return jsonify({"error": "API request failed"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
