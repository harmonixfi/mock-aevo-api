from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)


def load_test_case_data(test_case, key):
    try:
        # Adjust the path if your JSON files are in a different directory
        file_path = os.path.join(os.getcwd(), f"{test_case}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        return data.get(key, {})
    except FileNotFoundError:
        return {}


@app.route("/orderbook", methods=["GET"])
def orderbook():
    symbol = request.args.get("symbol", "")
    test_case = request.args.get(
        "testcase", "testcase1"
    )  # Default to testcase1.json if not specified
    data = load_test_case_data(test_case, "orderbook").get(symbol.upper())
    if not data:
        return jsonify({"error": "Invalid symbol"}), 400
    return jsonify(data)


@app.route("/getaccount", methods=["GET"])
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


if __name__ == "__main__":
    app.run(debug=True, port="5000")
