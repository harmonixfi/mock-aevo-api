import random
from flask import Flask, request, jsonify
import json
import os

from web3 import Web3

import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

CAMELOT_SWAP_ADDRESS = os.getenv("CAMELOT_SWAP_ADDRESS")
WEB3_PROVIDER = "http://127.0.0.1:8545/"

# Initialize the web3 instance
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))


def get_price_of(web3: Web3, token1: str, token2: str, decimals1: int, decimals2: int):
    with open("./abis/camelot_swap.json", "r") as file:
        camelot_swap_abi = json.load(file)

    # Initialize the contract instance
    camelot_swap_contract = web3.eth.contract(
        address=CAMELOT_SWAP_ADDRESS, abi=camelot_swap_abi
    )

    price = camelot_swap_contract.functions.getPriceOf(
        token1, token2, decimals1, decimals2
    ).call()

    return price


def load_test_case_data(test_case, key):
    try:
        # Adjust the path if your JSON files are in a different directory
        file_path = os.path.join(os.getcwd(), f"./data/{test_case}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        return data.get(key, {})
    except FileNotFoundError:
        return {}


@app.route("/orderbook", methods=["GET"])
def orderbook():
    symbol = request.args.get("instrument_name", "")
    test_case = request.args.get(
        "testcase", "testcase1"
    )  # Default to testcase1.json if not specified
    data = load_test_case_data(test_case, "orderbook")

    # Get the price of ETH
    eth_price = get_price_of(web3, "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", 18, 6)
    eth_price = eth_price / 10**6
    data['asks'][0][0] = eth_price - eth_price * (random.uniform(0.2, 0.3)/100)
    data['bids'][0][0] = eth_price + eth_price * (random.uniform(0.1, 0.3)/100)
    return jsonify(data)


@app.route("/orders", methods=["POST"])
def create_order():
    # Return the response
    return jsonify({"success": True})


@app.route("/account", methods=["GET"])
def getaccount():
    test_case = request.args.get("testcase", "testcase1")
    data = load_test_case_data(test_case, "getaccount")
    return jsonify(data)


@app.route("/withdraw", methods=["POST"])
def withdraw():
    # For demonstration, simply return success. Adapt as necessary.
    return jsonify({"success": True})


@app.route("/transaction-history", methods=["GET"])
def transaction_history():
    test_case = request.args.get("testcase", "testcase1")
    data = load_test_case_data(test_case, "transaction_history")
    return jsonify(data)


@app.route("/klines", methods=["GET"])
def klines():
    data = load_test_case_data("candles", "klines")
    # Get the price of ETH
    # eth_price = get_price_of(web3, "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", 18, 6)
    # eth_price = eth_price / 10**6

    # # Update the latest candle data with a random spread around the ETH price
    # candle = data[-1]
    # # Modify the close price with 80% probability
    # close_price_options = [
    #     eth_price - random.uniform(0.1, 0.3),  # 80% probability
    #     eth_price + random.uniform(0, 0.1)   # 20% probability
    # ]
    # weights = [0.8, 0.2]
    # candle[3] = random.choices(close_price_options, weights=weights, k=1)[0]

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port="5000", host="0.0.0.0")
