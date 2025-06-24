@app.route("/get_price")
def get_price():
    coin = request.args.get("coin", "bitcoin").lower()
    currency = request.args.get("currency", "usd").lower()

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            if coin in data and currency in data[coin]:
                return jsonify({"price": data[coin][currency]})
            else:
                return jsonify({"error": f"No data found for {coin} in {currency}"}), 404
        except Exception as e:
            return jsonify({"error": "Error parsing API response"}), 500
    else:
        return jsonify({"error": "API request failed"}), 500
