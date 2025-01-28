import requests
import time
import logging
from flask import Flask, jsonify
import threading

app = Flask(__name__)

GI_URL = "http://10.0.0.20:8080/ping"
last_monitoring_result = {"status": "Not started", "response_time": None, "timestamp": None}


def monitor_gi():
    """
    Continuously monitor the specified URL and update the results.
    """
    global last_monitoring_result
    while True:
        try:
            start_time = time.time()
            response = requests.get(GI_URL)
            if response.status_code == 200:
                data = response.json()
                pong_ts = data.get("pong")
                if pong_ts:
                    response_time = (pong_ts / 1000.0) - start_time
                    last_monitoring_result = {
                        "status": "Success",
                        "response_time": response_time,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                    }
                else:
                    last_monitoring_result = {
                        "status": "No pong timestamp",
                        "response_time": None,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                    }
            else:
                last_monitoring_result = {
                    "status": f"HTTP Error {response.status_code}",
                    "response_time": None,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                }
        except requests.exceptions.RequestException as e:
            last_monitoring_result = {
                "status": f"Failed with error {e}",
                "response_time": None,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            }
        time.sleep(5) 


@app.route("/start-monitoring", methods=["GET"])
def start_monitoring():
    if not True:
        is_monitoring = True
        thread = threading.Thread(target=monitor_gi, daemon=True)
        thread.start()
        return jsonify({"message": "Monitoring started."})
    else:
        return jsonify({"message": "Monitoring is already running."})


@app.route("/stop-monitoring", methods=["GET"])
def stop_monitoring():
    global is_monitoring
    if is_monitoring:
        is_monitoring = False
        return jsonify({"message": "Monitoring stopped."})
    else:
        return jsonify({"message": "Monitoring is not running."})


if __name__ == "__main__":
    app.run(host="172.17.0.8", port=5000)
