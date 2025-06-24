from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def interface():
    return render_template('index.html')

@app.route('/price', methods=['POST'])
def get_price():
    coin = request.form.get('coin')
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd'
    try:
        response = requests.get(url)
        data = response.json()
        if coin in data:
            price = data[coin]['usd']
            return jsonify({'price': price})
        else:
            return jsonify({'error': 'Invalid coin name'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Use Render-compatible host and port
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
