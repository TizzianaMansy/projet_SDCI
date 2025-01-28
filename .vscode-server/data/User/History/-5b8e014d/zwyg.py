import requests
import json
from flask import Flask, jsonify

app = Flask(__name__)

controller_url = "http://localhost:8080/stats/flowentry/add"

# Define the flow entries
flow_entries = [
    {
        "dpid": 2,
        "cookie": 1,
        "cookie_mask": 1,
        "table_id": 0,
        "priority": 50000,
        "match": {
            "in_port": 3,
            "eth_type": 2048,
            "ipv4_src": "10.0.0.30"  # ip de gf1
        },
        "actions": [
            {
                "type": "SET_FIELD",
                "field": "eth_dst",
                "value": "12:c7:51:10:90:e7"
            },
            {
                "type": "SET_FIELD",
                "field": "ipv4_dst",
                "value": "10.0.0.200"
            },
            {
                "type": "OUTPUT",
                "port": 1
            }
        ]
    },
    {
        "dpid": 2,
        "cookie": 1,
        "cookie_mask": 1,
        "table_id": 0,
        "priority": 50000,
        "match": {
            "in_port": 3,
            "eth_type": 2048,
            "ipv4_src": "10.0.0.40"  # ip de gf2
        },
        "actions": [
            {
                "type": "SET_FIELD",
                "field": "eth_dst",
                "value": "12:c7:51:10:90:e7"
            },
            {
                "type": "SET_FIELD",
                "field": "ipv4_dst",
                "value": "10.0.0.200"
            },
            {
                "type": "OUTPUT",
                "port": 1
            }
        ]
    },
    {
        "dpid": 2,
        "cookie": 1,
        "cookie_mask": 1,
        "table_id": 0,
        "priority": 50000,
        "match": {
            "in_port": 3,
            "eth_type": 2048,
            "ipv4_src": "10.0.0.50"  # ip de gf3
        },
        "actions": [
            {
                "type": "SET_FIELD",
                "field": "eth_dst",
                "value": "12:c7:51:10:90:e7"
            },
            {
                "type": "SET_FIELD",
                "field": "ipv4_dst",
                "value": "10.0.0.200"
            },
            {
                "type": "OUTPUT",
                "port": 1
            }
        ]
    }
]

# Function to send flow entries to the controller
def add_flow_rules():
    results = []
    for i, flow_entry in enumerate(flow_entries, start=1):
        response = requests.post(controller_url, json=flow_entry)
        if response.status_code == 200:
            results.append({"flow_entry": i, "status": "success"})
        else:
            results.append({"flow_entry": i, "status": "failure", "error": response.text})
    return results

# Flask endpoint to trigger rule creation
@app.route('/add_rules', methods=['POST'])
def add_rules_endpoint():
    results = add_flow_rules()
    return jsonify(results)

# Main entry point to run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
