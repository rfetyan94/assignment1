import requests
import json

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error: pin_to_ipfs expects a dictionary"

    # Pinata endpoint and your JWT
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    with open(".pinata_jwt", "r") as f:
      jwt_token = f.read().strip()

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "pinataContent": data
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise error for bad status

    cid = response.json()["IpfsHash"]
    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"

    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    response = requests.get(url)
    response.raise_for_status()

    if content_type == "json":
        data = response.json()
    else:
        data = response.content

    assert isinstance(data, dict), "get_from_ipfs should return a dict"
    return data
