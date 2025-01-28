from scapy.all import *
import time
import threading
import queue

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

# Define the VNF interface (e.g., interface connected to the switch)
vnf_interface = "eth2-vnf"  # Update with actual interface name


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
    while True:
        # First, send the highest priority packets (gf1)
        if not priority_queues["gf1"].empty():
            pkt = priority_queues["gf1"].get()
            if IP in pkt:
                pkt[IP].dst = "10.0.0.300"
                del pkt[IP].chksum
            sendp(pkt, iface=vnf_interface)  # Send back to s2 (via VNF interface)
            print(f"Sent packet from {pkt[IP].src} to {pkt[IP].dst}")
        # Then send packets from gf2
        elif not priority_queues["gf2"].empty():
            pkt = priority_queues["gf2"].get()
            sendp(pkt, iface=vnf_interface)  # Send back to s2
            print(f"Sent packet from {pkt[IP].src} to s2")
        # Finally, send packets from gf3
        elif not priority_queues["gf3"].empty():
            pkt = priority_queues["gf3"].get()
            sendp(pkt, iface=vnf_interface)  # Send back to s2
            print(f"Sent packet from {pkt[IP].src} to s2")
        time.sleep(0.1)  # Add some delay to simulate processing time

# Function to capture packets from the network and pass to the processing function
def capture_packets():
    sniff(iface=vnf_interface, prn=process_packet, store=0)  # Sniff packets on the VNF interface

# Start the packet capturing and processing in separate threads
capture_thread = threading.Thread(target=capture_packets)
send_thread = threading.Thread(target=send_to_s2)

capture_thread.start()
send_thread.start()

# Wait for the threads to finish (this will run indefinitely)
capture_thread.join()
send_thread.join()


