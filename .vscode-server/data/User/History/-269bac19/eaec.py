import requests
import time
import logging


logging.basicConfig(level=logging.INFO)


GI_URL = "http://10.0.0.20:8080/ping"
SATURATION_THRESHOLD = None
def calculate_threshold():
    response_times = []
    for i in range(3):
        try : 
            start_time = time.time()
            response = requests.get(GI_URL)
            if response.status_code == 200:
                data = response.json()
                pong_ts = data.get("pong")
                if pong_ts : 
                    response_time = (pong_ts/1000.0) - start_time
                    logging.info(f"Response time : {response_time}")
                    response_times.append(response_time)
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed with error {e}")
    if response_times: 
        average_response_time = sum(response_times) / len(response_times) 
        return average_response_time 
    else: 
        logging.warning("No valid response times received") 
        return None


""" def monitor_gi():
    if SATURATION_THRESHOLD is None:
        print("Threshold for saturation not set")
        return
    
    while True:
        try:
            start_time = time.time()
            response = requests.get(GI_URL)
            if response.status_code == 200:
                data = response.json()
                pong_ts = data.get("pong")
                if pong_ts : 
                    response_time = (pong_ts/1000.0) - start_time
                    if response_time > SATURATION_THRESHOLD:
                        print(f"Gi is saturated : {response_time} s.")
                    else:
                        print(f"No saturation {response_time} s")
                else :
                    print("no pong timestamp")
            else:
                print(f"status code : {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed with error {e}")
        time.sleep(5) """


if __name__ == "__main__":
    SATURATION_THRESHOLD = calculate_threshold()
    logging.info(f"Initial Saturation Threshold set to: {SATURATION_THRESHOLD} seconds")