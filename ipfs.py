import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data, dict), f"Error pin_to_ipfs expects a dictionary"

	PINATA_JWT = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIwYjFiZGQ0MC05ZTg4LTRmZTUtYTE5OC0xY2NmZDM1NzM0MjMiLCJlbWFpbCI6InJmZXR5YW5Ac2Vhcy51cGVubi5lZHUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJGUkExIn0seyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJOWUMxIn1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiNDJkMzhjZTVmNThkZWRmOGJlYTciLCJzY29wZWRLZXlTZWNyZXQiOiJiZTVhMTE0NWY1ZDIzMTM0OTA1NmJhYjllNjc3ZTMwYTdhZjE4MWQ2MzJlYjYzN2YzODdlMzgxOGE1ZTc4ZDYwIiwiZXhwIjoxNzgyNzg3NzY4fQ.o7CDP5gXcq2bmCqp1V1XOIrUNehLrJwJNkFQyCGAoqQ"

	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
	headers = {
		"Authorization": PINATA_JWT,
		"Content-Type": "application/json"
	}

	response = requests.post(url, headers=headers, data=json.dumps(data))

	if response.status_code == 200:
		cid = response.json()["IpfsHash"]
	else:
		raise Exception(f"Pinata upload failed: {response.text}")

	return cid

def get_from_ipfs(cid, content_type="json"):
	assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"

	url = f"https://gateway.pinata.cloud/ipfs/{cid}"
	response = requests.get(url)

	if response.status_code == 200:
		if content_type == "json":
			data = json.loads(response.content)
		else:
			raise ValueError("Unsupported content_type: must be 'json'")
	else:
		raise Exception(f"IPFS retrieval failed: {response.text}")

	assert isinstance(data, dict), f"get_from_ipfs should return a dict"
	return data
