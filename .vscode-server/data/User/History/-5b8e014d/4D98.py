import requests
import json

controller_url = "http://localhost:8080/stats/flowentry/add"

# règles de flux pour rediriger le trafic de gf1, gf2 et gf3 vers la VNF

flow_entry_1 = {
     "dpid": 2,
     "cookie": 1,
     "cookie_mask": 1,
     "table_id": 0,
     "priority": 50000,
     "match": {
         "in_port": 3,
         "eth_type": 2048,
         "ipv4_src": "10.0.0.30" #ip de gf1
     },
     "actions": [
         {
             "type": "SET_FIELD",
             "field": "eth_dst",
             "value": "12:c7:51:10:90:e7"
         },
         {
             "type": "SET_FIELD",
             "field": "ipv4_dst",
             "value": "10.0.0.200"
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
         "ipv4_src": "10.0.0.40" #ip de gf2
     },
     "actions": [
         {
             "type": "SET_FIELD",
             "field": "eth_dst",
             "value": "12:c7:51:10:90:e7"
         },
         {
             "type": "SET_FIELD",
             "field": "ipv4_dst",
             "value": "10.0.0.200"
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
         "ipv4_src": "10.0.0.50" #ip de gf3
     },
     "actions": [
         {
             "type": "SET_FIELD",
             "field": "eth_dst",
             "value": "12:c7:51:10:90:e7"
         },
         {
             "type": "SET_FIELD",
             "field": "ipv4_dst",
             "value": "10.0.0.200"
         },
         {
             "type": "OUTPUT",
             "port": 1
         }
     ]
 }

response_1 = requests.post(controller_url, json=flow_entry_1)
response_2 = requests.post(controller_url, json=flow_entry_2)
response_3 = requests.post(controller_url, json=flow_entry_3)

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
