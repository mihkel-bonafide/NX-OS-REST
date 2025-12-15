import requests
from hostfile import host, username, pword
from urllib3.exceptions import InsecureRequestWarning  # this is used below to disable an insecure HTTPS warning

""" 
This module gets an authentication token from the NX-OS device. -MPG
"""

def get_token():   
    # Suppress HTTPS warnings
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    endpoint = "/api/aaaLogin.json"
    url = host + endpoint

# IMPORTANT: When using this as the payload of the request, use json=streetcred, NOT 
# data=streetcred, or you're gonna have a bad time.
    streetcred = {
        "aaaUser": {
            "attributes": {
                "name": username,
                "pwd": pword
            }
        }
    }
    headers = {
        "Content-Type" : "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, headers=headers, json=streetcred, verify=False).json()  
    token = response["imdata"][0]["aaaLogin"]["attributes"]["token"]
    return token

def main():
    token = get_token()
    print(token)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass     
