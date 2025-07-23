
from flask import Flask, request, jsonify
from kiteconnect import KiteConnect
import logging

app = Flask(__name__)

# Disable Flask default logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Zerodha API credentials
api_key = "azq8hwwztgwoyti6"
api_secret = "qn1ljjtxzpblzisgldlpsmovtrk82lqk"
access_token = "1O6OYj7kiVkgQL6TN2x7TNGG9aiMkOHA"

# Create Kite instance
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    action = data.get("action", "").upper()
    symbol = data.get("symbol", "GOLDPETAL1!")
    quantity = int(data.get("qty", 1))

    if action not in ["BUY", "SELL"]:
        return jsonify({"status": "error", "message": "Invalid action"}), 400

    try:
        kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_MCX,
            tradingsymbol=symbol,
            transaction_type=kite.TRANSACTION_TYPE_BUY if action == "BUY" else kite.TRANSACTION_TYPE_SELL,
            quantity=quantity,
            product=kite.PRODUCT_NRML,
            order_type=kite.ORDER_TYPE_MARKET,
            validity=kite.VALIDITY_DAY
        )
        return jsonify({"status": "success", "message": f"{action} order placed for {symbol}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "✅ Zerodha Webhook Server is Running!"

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)


