#a simple python program to implement the MAPE loop  using one thread for just the Monitor phase
# no other threads are used for Analyze, Plan, Execute phases
# the Monitor phase is implemented in a separate thread
# the monitor raises alerts towards the main program
# when receving an alert, the main program executes in sequence the Analyze, Plan, Execute phases
# the main program always waits for alerts from the monitor
# the monitor runs continuously in the background
# the main program runs in a loop
# the monitor is implemented as a separate class

import time
import threading
import random
import sys
import requests
import json

# the analyze, plan, execute phases are implemented in separate functions
def analyze():
    print("Analyze")
    time.sleep(1)

def plan():
    print("Plan")
    time.sleep(1)

def execute():
    print("Execute")
    time.sleep(1)   


# the Monitor class
class Monitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.alerts = 0
        self.running = True
        self.threshold = None  

    def createVNF(self):
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "image": "vnf_monitor:latest",
            "network": "(id=eth-vnf,ip=10.0.0.100/24)"
        }

        url = "http://127.0.0.1:5001/restapi/compute/dc1/vnf_monitor"

        try:
            response = requests.put(url, headers=headers, json=payload)
            if response.status_code == 200:
                print("VNF created successfully:", response.json())
            else:
                print("Failed to create VNF:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    
    def start_monitoring(self):
        try:
            response = requests.post("http://172.17.0.7:5000/start")
            if response.status_code == 200:
                print("Monitoring started")
            else:
                print("Failed to start monitoring:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def stop_monitoring(self):
        try:
            response = requests.post("http://172.17.0.7:5000/stop")
            if response.status_code == 200:
                print("Monitoring stopped")
            else:
                print("Failed to stop monitoring:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def calculate_threshold(self):
        try:
            response = requests.get("http://172.17.0.7:5000/data")
            if response.status_code == 200:
                data = response.json()
                response_times = data.get("last_5_response_times")
                if response_times:
                    self.threshold = max(response_times) * 1.25
                    print("Threshold calculated:", self.threshold)
                else:
                    print("No response times available")
            else:
                print("Failed to get data:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def getdata(self):
        try:
            response = requests.get("http://172.17.0.7:5000/data")
            if response.status_code == 200:
                data = response.json()
                print("Data:", data)
                return data
            else:
                return None
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None


    def run(self):
         
        self.start_monitoring()
        time.sleep(6)
        self.calculate_threshold() 
        while self.running:
            if self.threshold:
                data = self.getdata()
                if data:
                    response_times = data.get("last_5_response_times")
                    avg_reponse = data.get("average_response_time")
                    if response_times:
                        if avg_reponse > self.threshold:
                            self.alerts += 1
                            print("Alert:", self.alerts)
            else:
                print("No threshold")
            time.sleep(5)
           

    def stop(self):
        self.running = False

# the main program
def main():
    monitor = Monitor()
    monitor.createVNF()
    time.sleep(5)
    monitor.start()
    
    while True:
        while monitor.alerts == 0:
            time.sleep(1)
        print("Analyze")
        time.sleep(1)
        print("Plan")
        time.sleep(1)
        print("Execute")
        time.sleep(1)

    monitor.stop()
    monitor.join()

if __name__ == "__main__":
    main()

