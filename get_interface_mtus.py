import requests
from hostfile import host, username, pword
from urllib3.exceptions import InsecureRequestWarning  # this is used below to disable an insecure HTTPS warning

""" 
This module gets an authentication token from the NX-OS device. -MPG
"""

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
HEADERS = {
        "Content-Type" : "application/json",
        "Accept": "application/json"
    }

def get_token():   
    endpoint = "/api/aaaLogin.json"
    url = host + endpoint
    credentials = {
        "aaaUser": {
            "attributes": {
                "name": username,
                "pwd": pword
            }
        }
    }

    response = requests.post(url, headers=HEADERS, json=credentials, verify=False).json()  
    token = response["imdata"][0]["aaaLogin"]["attributes"]["token"]
    return token

def get_interface_mtus():
    endpoint = "/api/node/mo/sys/intf.json?query-target=children"
    url = host + endpoint

    token = ""
    token = get_token()
    cookies = {}
    cookies = {"APIC-cookie" : token}

    response = requests.get(url, headers=HEADERS, cookies=cookies, verify=False).json() 
    # print(response)
    # This is a short-cut - how this should work is to loop through all interfaces and pull the MTUs from UP/UPs 
    mtu = response["imdata"][0]["l1PhysIf"]["attributes"]["mtu"]  
    print(f"MTU for interface eth1/1 is: {mtu}")

def main():
    get_interface_mtus()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass  