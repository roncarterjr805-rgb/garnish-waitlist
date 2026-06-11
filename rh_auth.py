#!/usr/bin/env python3
"""
Robinhood OAuth2 token fetcher.
Run this script, enter your credentials at the prompts, and it will
print a bearer token you can use with the MCP trading server.
"""
import getpass
import json
import sys
import uuid

try:
    import requests
except ImportError:
    sys.exit("Install requests first:  pip install requests")

CLIENT_ID = "c82SH0WZOsabOXGP2sxqcj34FFK0aYRm"  # Robinhood's public OAuth client ID
TOKEN_URL = "https://api.robinhood.com/oauth2/token/"

def get_token():
    username = input("Robinhood username (email): ").strip()
    password = getpass.getpass("Password: ")
    device_token = str(uuid.uuid4())

    payload = {
        "client_id": CLIENT_ID,
        "expires_in": 86400,
        "grant_type": "password",
        "password": password,
        "scope": "internal",
        "username": username,
        "device_token": device_token,
        "token_request_path": "/api/marketdata/",
    }

    resp = requests.post(TOKEN_URL, json=payload, timeout=15)

    # MFA challenge
    if resp.status_code == 200 and resp.json().get("mfa_required"):
        mfa_code = input("MFA code: ").strip()
        payload["mfa_code"] = mfa_code
        resp = requests.post(TOKEN_URL, json=payload, timeout=15)

    data = resp.json()

    if "access_token" in data:
        print("\n--- BEARER TOKEN (copy everything below) ---")
        print(data["access_token"])
        print("--- END ---")
        print(f"\nExpires in: {data.get('expires_in', '?')} seconds")
        print(f"Refresh token: {data.get('refresh_token', 'n/a')}")
    else:
        print("\nAuth failed:")
        print(json.dumps(data, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    get_token()
