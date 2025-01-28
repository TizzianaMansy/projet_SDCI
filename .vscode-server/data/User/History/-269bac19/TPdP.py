import requests
import time
import logging



GI_URL = "http://127.0.0.1:8080/ping"

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
                    response_times.append(response_time)
        except requests.exceptions.RequestException as e:
            print(f"Failed with error {e}")
    average_response_time = sum(response_times)/ len(response_times)
    return average_response_time


if __name__ == "__main__"