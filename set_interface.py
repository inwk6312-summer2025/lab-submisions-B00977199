import yaml
import requests
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# RESTCONF headers and auth
HEADERS = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json"
        }
AUTH = ("admin", "admin")  # Change if needed

def load_config(file_path):
 with open(file_path) as f:
  return yaml.safe_load(f)

def set_interface_ip(router_ip, interface_name, ip_address, netmask):
 #url = f"http://{router_ip}/restconf/data/ietf-interfaces:interfaces/interface={interface_name}"
 url = f"https://129.173.143.7:20003/restconf/data/ietf-interfaces:interfaces/interface={encoded_if_name}"

            # Prepare payload according to RESTCONF yang model
 data = {
   "ietf-interfaces:interface": {
   "name": interface_name,
   "description": "Configured via RESTCONF",
   "type": "iana-if-type:ethernetCsmacd",
   "enabled": True,
   "ietf-ip:ipv4": {
    "address": [{
      "ip": ip_address,
      "netmask": netmask
       }]
      }
     }
    }  
 try:
     response = requests.put(url, auth=AUTH, headers=HEADERS, data=json.dumps(data))
     if response.status_code in [200, 201, 204]:
      logger.info(f"Successfully set {interface_name} on {router_ip}")
     else:
      logger.error(f"Failed to set {interface_name} on {router_ip}, Status Code: {response.status_code}, Response: {response.text}")
 except requests.exceptions.RequestException as e:
    logger.error(f"Request failed for {router_ip}: {e}")
def main():
 config = load_config("routers.yml")
 for router in config.get('routers', []):
     router_ip = router['management_ip']
     for interface in router.get('interfaces', []):
      set_interface_ip(router_ip, interface['name'], interface['ip_address'], interface['netmask'])

if __name__ == "__main__":
 main()

