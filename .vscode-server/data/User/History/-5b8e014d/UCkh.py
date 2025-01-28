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
             "type": "SET_FIELD",
             "field": "eth_dst",
             "value": "7e:9a:8e:c4:03:43"
         },
         {
             "type": "SET_FIELD",
             "field": "ipv4_dst",
             "value": "10.0.0.12"
         },
         {
             "type": "OUTPUT",
             "port": 1
         }
     ]
 }


flow_entry_2 = {
     "dpid": 2,
     "cookie": 1,
     "cookie_mask": 1,
     "table_id": 0,
     "priority": 50000,
     "match": {
         "in_port": 3,
         "eth_type": 2048,
         "ipv4_src": "10.0.0.40"
     },
     "actions": [
         {
             "type": "SET_FIELD",
             "field": "eth_dst",
             "value": "7e:9a:8e:c4:03:43"
         },
         {
             "type": "SET_FIELD",
             "field": "ipv4_dst",
             "value": "10.0.0.12"
         },
         {
             "type": "OUTPUT",
             "port": 1
         }
     ]
 }


flow_entry_3 = {
     "dpid": 2,
     "cookie": 1,
     "cookie_mask": 1,
     "table_id": 0,
     "priority": 50000,
     "match": {
         "in_port": 3,
         "eth_type": 2048,
         "ipv4_src": "10.0.0.50"
     },
     "actions": [
         {
             "type": "SET_FIELD",
             "field": "eth_dst",
             "value": "7e:9a:8e:c4:03:43"
         },
         {
             "type": "SET_FIELD",
             "field": "ipv4_dst",
             "value": "10.0.0.12"
         },
         {
             "type": "OUTPUT",
             "port": 1
         }
     ]
 }


# Define the flow entry data for the VNF to GI redirection
flow_entry_4 = {
    "dpid": 2, 
    "cookie": 2,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 50000,
    "match": {
        "in_port": 1,  
        "eth_type": 2048,  
        "ipv4_src": "10.0.0.12"  
    },
    "actions":[
         {
             "type": "SET_FIELD",
             "field": "eth_src",
             "value": "00:00:00:00:00:30"
         },
         {
             "type": "SET_FIELD",
             "field": "eth_dst",
             "value": "00:00:00:00:00:20"
         },
         {
             "type": "SET_FIELD",
             "field": "ipv4_src",
             "value": "10.0.0.30"
         },
         {
             "type": "SET_FIELD",
             "field": "ipv4_dst",
             "value": "10.0.0.20"
         },
         {
             "type": "OUTPUT",
             "port": 1
         }
     ]
} 
 
# Send the POST request for the first flow entry (gf1 -> VNF)
response_1 = requests.post(controller_url, json=flow_entry_1)
response_2 = requests.post(controller_url, json=flow_entry_2)
response_3 = requests.post(controller_url, json=flow_entry_3)

# Send the POST request for the second flow entry (VNF -> GI)
response_4 = requests.post(controller_url, json=flow_entry_4)

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

if response_4.status_code == 200:
    print("Flow entry 2 (VNF -> GI) successfully added.")
else:
    print(f"Failed to add flow entry 4. Status code: {response_4.status_code}")
    print("Response:", response_4.text)
