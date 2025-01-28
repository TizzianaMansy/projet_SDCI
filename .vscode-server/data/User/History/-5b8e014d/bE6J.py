import requests
import json

# Define the URL of the OpenFlow controller
controller_url = "http://localhost:8080/stats/flowentry/add"

# Define the flow entry data (transparent redirection)
flow_entry = {
    "dpid": 2,  # Switch DPID (2 for s2 in your case)
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 50000,
    "match": {
        "in_port": 3,  # The input port of s2 (port 3)
        "eth_type": 2048,  # EtherType for IPv4 (0x0800)
        "ipv4_src": "10.0.0.30"  # Source IP (gf1's IP)
    },
    "actions": [
        {
            "type": "OUTPUT",  # Output to port 1 (connected to VNF)
            "port": 1
        }
    ]
}

# Send the POST request to the controller
response = requests.post(controller_url, json=flow_entry)

# Check the response from the controller
if response.status_code == 200:
    print("Flow entry successfully added.")
else:
    print(f"Failed to add flow entry. Status code: {response.status_code}")
    print("Response:", response.text)



