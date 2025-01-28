import requests
import time
import logging
from flask import Flask, jsonify
import threading

app = Flask(__name__)

GI_URL = "http://10.0.0.20:8080/ping"
response_times = [] 
monitor_thread = None
monitoring = False  
lock = threading.Lock() 


def monitor_gi():
    global response_times, monitoring
    while monitoring:
        try:
            start_time = time.time()
            response = requests.get(GI_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                pong_ts = data.get("pong")
                if pong_ts:
                    response_time = (pong_ts / 1000.0) - start_time
                    
                    with lock:
                        response_times.append(response_time)
                        if len(response_times) > 5:  
                            response_times.pop(0)
                else:
                    logging.warning("No pong timestamp in response")
            else:
                logging.warning(f"Unexpected status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed with error {e}")
        time.sleep(5) 


@app.route('/start', methods=['POST'])
def start_monitoring():
    global monitor_thread, monitoring
    if not monitoring:
        monitoring = True
        monitor_thread = threading.Thread(target=monitor_gi, daemon=True)
        monitor_thread.start()
        return jsonify({"status": "Monitoring started"}), 200
    else:
        return jsonify({"error": "Monitoring is already running"}), 400

# Endpoint to stop monitoring
@app.route('/stop', methods=['POST'])
def stop_monitoring():
    global monitoring
    if monitoring:
        monitoring = False
        return jsonify({"status": "Monitoring stopped"}), 200
    else:
        return jsonify({"error": "Monitoring is not running"}), 400

# Endpoint to get the last 5 response times and their average
@app.route('/data', methods=['GET'])
def get_data():
    global response_times
    with lock:
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            return jsonify({
                "last_5_response_times": response_times,
                "average_response_time": avg_response_time
            }), 200
        else:
            return jsonify({"error": "No data available"}), 400

# Main entry point
if __name__ == "__main__":
    logging.basicConfig(
        filename='/app/logfile.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    app.run(host='0.0.0.0', port=5000)


