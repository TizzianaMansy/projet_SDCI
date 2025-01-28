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
import subprocess
import os


def analyze():
    print("Analyze")
    time.sleep(1)

# Execute class
class Execute(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def createVNF(self): #creation de la VNF d'ordonnancement
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "image": "vnf_ordo:latest",
            "network": "(id=eth2-vnf,ip=10.0.0.200/24)"
        }

        url = "http://127.0.0.1:5001/restapi/compute/dc1/vnf_ordo"

        try:
            response = requests.put(url, headers=headers, json=payload)
            if response.status_code == 200:
                print("VNF created successfully:", response.json())
            else:
                print("Failed to create VNF:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def start_ryu_script(self): # lancement du script ryu avec les règles OpenFlow
        try:
            script_path = "./ryu.py"  
            
            process = subprocess.Popen(
                ["ryu-manager", script_path], 
                stdout=subprocess.PIPE,       
                stderr=subprocess.PIPE,      
                universal_newlines=True 
            )
            
            print(f"Ryu script '{script_path}' lancé avec succès.")
            return process 

        except Exception as e:
            print(f"Erreur lors du lancement de Ryu : {e}")
        
    def start_ordo(self): # lancement de l'ordonnanceur
        try:
            response = requests.post("http://172.17.0.8:5000/start_ordo")  # cette adresse est l'IP du docker de la VNF d'ordonnancement
            if response.status_code == 200:
                print("Ordonnaceur started successfully")
            else:
                print("Failed to start ordo:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def stop_ordo(self): # arrêt de l'ordonnanceur
        try:
            response = requests.post("http://172.17.0.8:5000/stop_ordo")
            if response.status_code == 200:
                print("Ordonnanceur stopped successfully")
            else:
                print("Failed to stop ordo:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)
    
    def run(self):
        self.start_ryu_script()
        time.sleep(5)
        self.start_ordo()
        time.sleep(5)
        while self.running:
            time.sleep(1)

    def stop(self): 
        self.running = False


    

def plan():
    print("Plan")
    time.sleep(1)   


# the Monitor class
class Monitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.alerts = 0
        self.running = True
        self.threshold = None  

    def createVNF(self): # creation de la VNF de monitoring
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

    
    def start_monitoring(self): # démarrage du monitoring
        try:
            response = requests.post("http://172.17.0.7:5000/start") # adresse IP du docker de la VNF de monitoring
            if response.status_code == 200:
                print("Monitoring started")
            else:
                print("Failed to start monitoring:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def stop_monitoring(self): # arrêt du monitoring
        try:
            response = requests.post("http://172.17.0.7:5000/stop")
            if response.status_code == 200:
                print("Monitoring stopped")
            else:
                print("Failed to stop monitoring:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def calculate_threshold(self): # calcul du seuil de saturation
        try:
            response = requests.get("http://172.17.0.7:5000/data")
            if response.status_code == 200:
                data = response.json()
                response_times = data.get("last_5_response_times")
                if response_times:
                    self.threshold = max(response_times) * 1.25 # threshold = temps de réponse le plus élevé + 25%
                    print("Threshold calculated:", self.threshold)
                else:
                    print("No response times available")
            else:
                print("Failed to get data:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def getdata(self): # récupération des données de monitoring
        try:
            response = requests.get("http://172.17.0.7:5000/data")
            if response.status_code == 200:
                data = response.json()
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
            if self.threshold: # si on a bien un seuil de saturation
                data = self.getdata()
                if data:
                    response_times = data.get("last_5_response_times")
                    avg_reponse = data.get("average_response_time")
                    if response_times:
                        if avg_reponse > self.threshold: # on compare le temps de réponse moyen avec le seuil
                            self.alerts += 1 # déclenchement d'une alerte
                            print("Alert:", self.alerts)
                        else:
                            print(f"No saturation, response time : {avg_reponse}")
            else:
                print("No threshold")

            time.sleep(5)
           

    def stop(self):
        self.running = False

# the main program
def main():
    monitor = Monitor()
    execute = Execute()
    monitor.createVNF() # on commence par créer les VNFs
    time.sleep(5)
    execute.createVNF()
    time.sleep(5)
    time.sleep(5)
    execute.start()
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
    execute.stop()
    execute.join()

if __name__ == "__main__":
    main()

