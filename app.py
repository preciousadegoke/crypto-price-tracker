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

    # ✅ Debugging line to check the requested URL
    print(f"Fetching: {url}")  

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if coin in data:
            return jsonify({"price": data[coin][currency]})
        else:
            return jsonify({"error": "Invalid coin name"}), 400
    except Exception as e:
        return jsonify({"error": "API request failed"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
