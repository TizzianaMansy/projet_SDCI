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
        except :

    average_response_time = (response_times[0]+response_times[1]+response_times[2])/3