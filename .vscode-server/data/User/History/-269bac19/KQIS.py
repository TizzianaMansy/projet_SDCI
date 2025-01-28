import requests
import time
import logging



GI_URL = "http://10.0.0.20:8080/ping"




def monitor_gi():
   
    
    while True:
        try:
            start_time = time.time()
            response = requests.get(GI_URL)
            if response.status_code == 200:
                data = response.json()
                pong_ts = data.get("pong")
                if pong_ts : 
                    response_time = (pong_ts/1000.0) - start_time
                    
                else :
                    print("no pong timestamp")
            else:
                print(f"status code : {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed with error {e}")
        time.sleep(5)


if __name__ == "__main__":
    monitor_gi()