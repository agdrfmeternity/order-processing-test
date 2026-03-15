from flask import Flask, request, jsonify

app = Flask(__name__)
orders = {}
current_id = 1

@app.route("/login", methods=["GET"])
def login_page():
    return """
    <html>
        <body>
            <h1>Login</h1>
            <input id="login"/>
            <input id="password"/>
            <button id="submit">Login</button>
        </body>
    </html>
    """

@app.route("/create_order", methods=["POST"])
def create_order():
    global current_id
    name = request.json["name"]
    orders[current_id] = {
        "name": name,
        "status": "New"
    }
    order_id = current_id
    current_id += 1
    return jsonify({"order_id": order_id})

@app.route("/order/<int:order_id>")
def get_order(order_id):
    return jsonify(orders[order_id])

@app.route("/prepare/<int:order_id>", methods=["POST"])
def prepare(order_id):
    orders[order_id]["status"] = "Ready"
    return jsonify({"result": "ok"})

def run():
    app.run(port=8080)