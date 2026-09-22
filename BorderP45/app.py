import os
from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__, static_folder="public")

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

@app.route("/")
def index():
    return send_from_directory(PUBLIC_DIR, "index.html")

@app.route("/sw.js")
def service_worker():
    response = send_from_directory(PUBLIC_DIR, "sw.js")
    response.headers["Content-Type"] = "application/javascript"
    response.headers["Service-Worker-Allowed"] = "/"
    return response

@app.route("/manifest.json")
def manifest():
    response = send_from_directory(PUBLIC_DIR, "manifest.json")
    response.headers["Content-Type"] = "application/manifest+json"
    return response

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(PUBLIC_DIR, filename)

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "app": "BorderP45"}), 200

@app.route("/api/transfer/ton", methods=["POST"])
def transfer_ton():
    data = request.get_json(silent=True) or {}
    recipient = data.get("recipient")
    amount = data.get("amount")
    comment = data.get("comment", "")

    if not recipient or not amount:
        return jsonify({"success": False, "error": "Recipient and amount are required"}), 400

    return jsonify({
        "success": True,
        "message": "TON transfer simulated successfully",
        "tx_hash": "ton_sim_tx_" + os.urandom(8).hex(),
        "recipient": recipient,
        "amount": amount,
        "comment": comment
    }), 200

@app.route("/api/transfer/jetton", methods=["POST"])
def transfer_jetton():
    data = request.get_json(silent=True) or {}
    jetton_master = data.get("jetton_master")
    recipient = data.get("recipient")
    amount = data.get("amount")
    comment = data.get("comment", "")

    if not recipient or not amount or not jetton_master:
        return jsonify({"success": False, "error": "Jetton master, recipient, and amount are required"}), 400

    return jsonify({
        "success": True,
        "message": "Jetton transfer simulated successfully",
        "tx_hash": "jetton_sim_tx_" + os.urandom(8).hex(),
        "jetton_master": jetton_master,
        "recipient": recipient,
        "amount": amount,
        "comment": comment
    }), 200

@app.route("/api/tonconnect/parse", methods=["GET", "POST"])
def tonconnect_parse():
    import json
    from urllib.parse import unquote, parse_qs, urlparse

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        raw_url = data.get("url") or ""
    else:
        raw_url = request.args.get("url") or ""

    version = request.args.get("v") or ""
    connect_id = request.args.get("id") or ""
    request_payload_raw = request.args.get("r") or ""
    return_url = request.args.get("ret") or ""

    if raw_url and not (version or connect_id or request_payload_raw or return_url):
        parsed = urlparse(raw_url)
        params = parse_qs(parsed.query)
        version = params.get("v", [""])[0]
        connect_id = params.get("id", [""])[0]
        request_payload_raw = params.get("r", [""])[0]
        return_url = params.get("ret", [""])[0]

    request_payload = {}
    if request_payload_raw:
        try:
            request_payload = json.loads(request_payload_raw)
        except Exception:
            try:
                request_payload = json.loads(unquote(request_payload_raw))
            except Exception:
                request_payload = {"raw": request_payload_raw}

    manifest_url = request_payload.get("manifestUrl", "")
    items = request_payload.get("items", [])

    return jsonify({
        "success": True,
        "v": version,
        "id": connect_id,
        "ret": return_url,
        "request": request_payload,
        "manifestUrl": manifest_url,
        "items": items
    }), 200

@app.route("/api/tonconnect/connect", methods=["POST"])
def tonconnect_connect():
    data = request.get_json(silent=True) or {}
    connect_id = data.get("id", "")
    address = data.get("address", "EQD_simulated_wallet_address_1234567890")
    return_url = data.get("ret", "")

    proof_signature = os.urandom(32).hex()

    response_event = {
        "event": "connect",
        "id": connect_id,
        "payload": {
            "items": [
                {
                    "name": "ton_addr",
                    "address": address,
                    "network": "-239",
                    "publicKey": os.urandom(32).hex(),
                    "walletStateInit": "te6ccgEBAQEAAgAAAA=="
                },
                {
                    "name": "ton_proof",
                    "proof": {
                        "timestamp": 1700000000,
                        "domain": {
                            "lengthBytes": 12,
                            "value": "tonviewer.com"
                        },
                        "signature": proof_signature,
                        "payload": data.get("proof_payload", "")
                    }
                }
            ],
            "device": {
                "platform": "chrome",
                "appName": "BorderP45",
                "appVersion": "1.0.0",
                "maxProtocolVersion": 2
            }
        }
    }

    return jsonify({
        "success": True,
        "message": "TonConnect connection approved",
        "response": response_event,
        "return_url": return_url
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
