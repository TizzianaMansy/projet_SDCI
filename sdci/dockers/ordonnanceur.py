from scapy.all import *
import time
import threading
import queue
from flask import Flask, jsonify


# Flask app
app = Flask(__name__)


# Packet queue for different priorities
priority_queues = {
    "gf1": queue.Queue(),
    "gf2": queue.Queue(),
    "gf3": queue.Queue(),
}


# IP addresses for different hosts
gf1_ip = "10.0.0.30"
gf2_ip = "10.0.0.40"
gf3_ip = "10.0.0.50"


# Define the VNF interface 
vnf_interface = "eth2-vnf"  


# Flags to control threads
capture_running = False
send_running = False


# Threads
capture_thread = None
send_thread = None


# Function to process packets and prioritize based on source IP
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


# Function to send packets back to switch s2
def send_to_s2():
    global send_running
    while send_running:
        if not priority_queues["gf1"].empty():
            pkt = priority_queues["gf1"].get()
            print(pkt)
            pkt[IP].dst = "10.0.0.20"
            pkt[Ether].dst = "00:00:00:00:00:20"
            if Raw in pkt:
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


# Function to capture packets from the network and pass to the processing function
def capture_packets():
    global capture_running
    sniff(iface=vnf_interface, prn=process_packet, store=0, stop_filter=lambda x: not capture_running)  # Sniff packets on the VNF interface


# API endpoint to start threads
@app.route('/start_ordo', methods=['POST'])
def start_threads():
    global capture_thread, send_thread, capture_running, send_running
   
    if not (capture_running or send_running):  # Only start if not already running
        capture_running = True
        send_running = True


        # Start threads
        capture_thread = threading.Thread(target=capture_packets, daemon=True)
        send_thread = threading.Thread(target=send_to_s2, daemon=True)


        capture_thread.start()
        send_thread.start()


        return jsonify({"message": "Threads started"}), 200
    else:
        return jsonify({"message": "Threads are already running"}), 400


# API endpoint to stop threads
@app.route('/stop_ordo', methods=['POST'])
def stop_threads():
    global capture_running, send_running


    if capture_running or send_running:
        capture_running = False
        send_running = False


        return jsonify({"message": "Threads stopping..."}), 200
    else:
        return jsonify({"message": "Threads are not running"}), 400


# API endpoint to check thread status
@app.route('/status', methods=['GET'])
def check_status():
    return jsonify({
        "capture_running": capture_running,
        "send_running": send_running
    }), 200


# Run Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)





