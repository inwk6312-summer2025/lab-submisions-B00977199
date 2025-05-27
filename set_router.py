import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# Load the YAML configuration
with open('routers.yml', 'r') as file:
    router_data = yaml.safe_load(file)

    # RESTCONF Configuration
USER = 'student'
PASS = 'Meilab123'
BASE_URL = 'http://{0}/restconf/api/running/'.format

def set_interface_ip(router_ip, interface_name, ip_address, netmask):
        """Function to set the interface IP address using RESTCONF."""
        url = BASE_URL(router_ip) + "interfaces/interface/" + interface_name
        auth = HTTPBasicAuth(USER, PASS)
        headers = {
                'Accept': 'application/vnd.yang.data+json',
                'Content-Type': 'application/vnd.yang.data+json'
                }
        data = {
                "ietf-interfaces:interface": {
                    "name": interface_name,
                    "description": f"Configured via RESTCONF",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": True,
                    "ietf-ip:ipv4": {
                        "address": [
                            {
                                "ip": ip_address,
                                 "netmask": netmask
                                 }
                            ]
                        }
                    }
                }
        logging.info(f"Setting {interface_name} IP to {ip_address} on {router_ip}")
        response = requests.put(url, auth=auth, headers=headers, data=json.dumps(data))
        if response.status_code == 204:
            logging.info(f"Successfully set {interface_name} IP on {router_ip}, Status Code: {response.status_code}")
        else:
            logging.error(f"Failed to set {interface_name} IP on {router_ip}, Status Code: {response.status_code}, Response: {response.text}")
def update_router_interfaces():
    """Iterates through the router data and updates the interfaces using RESTCONF."""
    for router in router_data['routers']:
        management_ip = router['management_ip']
        for interface in router['interfaces']:
            set_interface_ip(management_ip, interface['name'], interface['ip_address'], interface['netmask'])

if __name__ == "__main__":
     update_router_interfaces()
