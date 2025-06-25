from flask import Flask, request, jsonify
import os
import threading
import time
from causal_clock import CausalClock

app = Flask(__name__)

# Get node config from environment
CURRENT_NODE = os.environ.get("NODE_NAME")
NODE_LIST = os.environ.get("NODE_LIST", "X,Y,Z").split(',')

# ✅ Always run Flask on port 6000 inside Docker (host will map it)
APP_PORT = 6000

# Initialize causal clock and local key-value store
clock = CausalClock(CURRENT_NODE, NODE_LIST)
local_store = {}  # Format: {'key': ('value', clock)}
pending_updates = []  # Buffer for delayed writes

@app.route("/store", methods=["POST"])
def handle_write():
    msg = request.json

    # ✅ Input validation
    if not all(k in msg for k in ["key", "value", "clock", "origin"]):
        return jsonify({"error": "Missing required fields"}), 400

    key = msg["key"]
    value = msg["value"]
    incoming_clock = msg["clock"]
    origin = msg["origin"]

    # ✅ Check causality condition
    if clock.is_valid_event(incoming_clock, origin):
        clock.merge(incoming_clock)
        local_store[key] = (value, incoming_clock)
        return jsonify({
            "status": "saved",
            "node": CURRENT_NODE,
            "key": key,
            "value": value,
            "clock": clock.clock
        })
    else:
        pending_updates.append(msg)
        return jsonify({
            "status": "delayed",
            "reason": "causality conflict",
            "local_clock": clock.clock,
            "incoming_clock": incoming_clock
        }), 202

@app.route("/retrieve", methods=["GET"])
def handle_read():
    key = request.args.get("key")
    if key not in local_store:
        return jsonify({
            "value": None,
            "message": f"Key '{key}' not found",
            "clock": clock.clock
        })

    value, stored_clock = local_store[key]
    return jsonify({
        "key": key,
        "value": value,
        "stored_clock": stored_clock,
        "local_clock": clock.clock
    })

def process_pending():
    while True:
        for entry in pending_updates[:]:
            if clock.is_valid_event(entry["clock"], entry["origin"]):
                pending_updates.remove(entry)
                clock.merge(entry["clock"])
                local_store[entry["key"]] = (entry["value"], entry["clock"])
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=process_pending, daemon=True).start()
    app.run(host="0.0.0.0", port=APP_PORT)
