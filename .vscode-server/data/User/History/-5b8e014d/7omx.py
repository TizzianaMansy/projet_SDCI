import requests
import json

controller_url = "http://localhost:8080/stats/flowentry/add"

flow_entry_1 = {
    "dpid": 2, 
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 50000,
    "match": {
        "in_port": 3,  
        "eth_type": 2048,  
        "ipv4_src": "10.0.0.30" 
    },
    "actions": [
        {
            "type": "OUTPUT", 
            "port": 1
        }
    ]
}

flow_entry_2 = {
    "dpid": 2,  # Switch DPID (2 for s2 in your case)
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 50000,
    "match": {
        "in_port": 3,  # The input port of s2 (port 3)
        "eth_type": 2048,  # EtherType for IPv4 (0x0800)
        "ipv4_src": "10.0.0.40"  # Source IP (gf1's IP)
    },
    "actions": [
        {
            "type": "OUTPUT",  # Output to port 1 (connected to VNF)
            "port": 1
        }
    ]
}

flow_entry_3 = {
    "dpid": 2,  # Switch DPID (2 for s2 in your case)
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 50000,
    "match": {
        "in_port": 3,  # The input port of s2 (port 3)
        "eth_type": 2048,  # EtherType for IPv4 (0x0800)
        "ipv4_src": "10.0.0.50"  # Source IP (gf1's IP)
    },
    "actions": [
        {
            "type": "OUTPUT",  # Output to port 1 (connected to VNF)
            "port": 1
        }
    ]
}

# Define the flow entry data for the VNF to GI redirection
""" flow_entry_4 = {
    "dpid": 2,  # Switch DPID (2 for s2 in your case)
    "cookie": 2,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 50000,
    "match": {
        "in_port": 1,  # The input port of s2 (port 1, connected to VNF)
        "eth_type": 2048,  # EtherType for IPv4 (0x0800)
        "ipv4_dst": "10.0.0.20"  # Destination IP (GI IP)
    },
    "actions": [
        {
            "type": "OUTPUT",  # Output to port 2 (connected to GI)
            "port": 2
        }
    ]
} 
 """
# Send the POST request for the first flow entry (gf1 -> VNF)
response_1 = requests.post(controller_url, json=flow_entry_1)
response_2 = requests.post(controller_url, json=flow_entry_2)
response_3 = requests.post(controller_url, json=flow_entry_3)

# Send the POST request for the second flow entry (VNF -> GI)
#response_4 = requests.post(controller_url, json=flow_entry_4)

# Check the response from the controller for both flow entries
if response_1.status_code == 200:
    print("Flow entry 1 (gf1 -> VNF) successfully added.")
else:
    print(f"Failed to add flow entry 1. Status code: {response_1.status_code}")
    print("Response:", response_1.text)

if response_2.status_code == 200:
    print("Flow entry 2 (gf2 -> VNF) successfully added.")
else:
    print(f"Failed to add flow entry 2. Status code: {response_2.status_code}")
    print("Response:", response_2.text)

if response_3.status_code == 200:
    print("Flow entry 3 (gf3 -> VNF) successfully added.")
else:
    print(f"Failed to add flow entry 3. Status code: {response_3.status_code}")
    print("Response:", response_3.text)

""" if response_4.status_code == 200:
    print("Flow entry 2 (VNF -> GI) successfully added.")
else:
    print(f"Failed to add flow entry 4. Status code: {response_4.status_code}")
    print("Response:", response_4.text) """
