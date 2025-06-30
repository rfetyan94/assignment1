import requests
import json
import os

def pin_to_ipfs(data):
    assert isinstance(data, dict), f"Error pin_to_ipfs expects a dictionary"
    
    # Load JWT token securely from a local file
    with open(".pinata_jwt", "r") as f:
        JWT = f.read().strip()

    headers = {
        "Authorization": f"Bearer {JWT}",
        "Content-Type": "application/json"
    }

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    response = requests.post(url, headers=headers, data=json.dumps(data))

    assert response.status_code == 200, f"Failed to pin to IPFS: {response.text}"
    
    cid = response.json()["IpfsHash"]
    return cid

def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"

    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    response = requests.get(url)

    assert response.status_code == 200, f"Failed to retrieve from IPFS: {response.text}"

    if content_type == "json":
        data = response.json()
    else:
        data = response.content

    assert isinstance(data, dict), f"get_from_ipfs should return a dict"
    return data
