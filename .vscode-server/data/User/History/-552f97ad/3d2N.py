from scapy.all import *
import time
import threading
import queue
from flask import Flask, jsonify

app = Flask(__name__)

# file d'attente
priority_queues = {
    "gf1": queue.Queue(),
    "gf2": queue.Queue(),
    "gf3": queue.Queue(),
}

gf1_ip = "10.0.0.30"
gf2_ip = "10.0.0.40"
gf3_ip = "10.0.0.50"

vnf_interface = "eth2-vnf"  

# flags pour contrôler les threads
capture_running = False
send_running = False

# Threads
capture_thread = None
send_thread = None

# Pour process les paquets, on les ajoute à la file d'attente
def process_packet(pkt):
    if pkt.haslayer(IP):
        if pkt[IP].src == gf1_ip:
            priority_queues["gf1"].put(pkt)
        elif pkt[IP].src == gf2_ip:
            priority_queues["gf2"].put(pkt)
        elif pkt[IP].src == gf3_ip:
            priority_queues["gf3"].put(pkt)
        else:
            print(f"Unknown source IP: {pkt[IP].src}")


# Pour envoyer les paquets de la file d'attente à S2
def send_to_s2():
    global send_running
    while send_running:
        if not priority_queues["gf1"].empty(): 
            pkt = priority_queues["gf1"].get()
            print(pkt)
            pkt[IP].dst = "10.0.0.20" # adresse IP de la GI
            pkt[Ether].dst = "00:00:00:00:00:20" # adresse MAC de la GI
            if Raw in pkt: # on imprime le payload
                print(f"Payload before sending: {pkt[Raw].load}")  
            else:
                print("No payload in this packet before sending.")
            print(pkt.summary())  
            sendp(pkt, iface=vnf_interface) 
            print(f"Sent packet from {pkt[IP].src} to {pkt[IP].dst} with MAC {pkt[Ether].dst}")
     
        elif not priority_queues["gf2"].empty():
            pkt = priority_queues["gf2"].get()
            pkt[IP].dst = "10.0.0.20"
            pkt[Ether].dst = "00:00:00:00:00:20"
            if Raw in pkt:
                print(f"Payload before sending: {pkt[Raw].load}")  
            else:
                print("No payload in this packet before sending.")
            print(pkt.summary()) 
            sendp(pkt, iface=vnf_interface)  
            print(f"Sent packet from {pkt[IP].src} to {pkt[IP].dst} with MAC {pkt[Ether].dst}")
       
        elif not priority_queues["gf3"].empty():
            pkt = priority_queues["gf3"].get()
            pkt[IP].dst = "10.0.0.20"
            pkt[Ether].dst = "00:00:00:00:00:20"
            if Raw in pkt:
                print(f"Payload before sending: {pkt[Raw].load}")  
            else:
                print("No payload in this packet before sending.")
            print(pkt.summary()) 
            sendp(pkt, iface=vnf_interface)  
            print(f"Sent packet from {pkt[IP].src} to {pkt[IP].dst} with MAC {pkt[Ether].dst}")
        else:
            time.sleep(0.1)


# Pour capturer les paquets
def capture_packets():
    global capture_running
    sniff(iface=vnf_interface, prn=process_packet, store=0, stop_filter=lambda x: not capture_running)  # Sniff packets on the VNF interface


# début des threads
@app.route('/start_ordo', methods=['POST'])
def start_threads():
    global capture_thread, send_thread, capture_running, send_running
   
    if not (capture_running or send_running): 
        capture_running = True
        send_running = True

        capture_thread = threading.Thread(target=capture_packets, daemon=True)
        send_thread = threading.Thread(target=send_to_s2, daemon=True)

        capture_thread.start()
        send_thread.start()

        return jsonify({"message": "Threads started"}), 200
    else:
        return jsonify({"message": "Threads are already running"}), 400


@app.route('/stop_ordo', methods=['POST'])
def stop_threads():
    global capture_running, send_running


    if capture_running or send_running:
        capture_running = False
        send_running = False


        return jsonify({"message": "Threads stopping..."}), 200
    else:
        return jsonify({"message": "Threads are not running"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)





