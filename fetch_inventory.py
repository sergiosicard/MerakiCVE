# -----------------------------------------------------------------------------
# Script: fetch_inventory.py
#
# Description:
#     This script connects to the Meraki Dashboard API to fetch a complete
#     list of devices for a specified organization. It is designed to be
#     user-friendly by automatically discovering the organization ID(s)
#     associated with the provided API key.
#
# Key Features:
#     - Dynamically fetches all accessible organizations.
#     - If only one organization is found, it is selected automatically.
#     - If multiple organizations are found, it prompts the user to select one.
#     - Saves the final device list as 'device_inventory.json' in the same
#       directory, making it ready for use by correlation scripts.
#
# Prerequisites:
#     - Python 3
#     - Required libraries: 'requests', 'python-dotenv'
#       (Install with: pip install requests python-dotenv)
#     - A '.env' file in the same directory as this script.
#
# .env File Configuration:
#     The .env file must contain the following key:
#     MERAKI_API_KEY="your_meraki_api_key_here"
#
# Usage:
#     Run the script from the command line:
#     python fetch_inventory.py
#
# Output:
#     A JSON file named 'device_inventory.json' containing the raw device
#     data from the Meraki API.
#
# Author: Sergio Sicard - Charter Communications Account Team - Cisco Systems Inc.
# Version: 1.0
# Date: July 30 2025
# -----------------------------------------------------------------------------



import os
import json
import requests
from dotenv import load_dotenv

# --- Configuration ---
MERAKI_BASE_URL = "https://api.meraki.com/api/v1"
INVENTORY_FILE = "device_inventory.json"

def get_organization_id(api_key):
    """
    Fetches all organizations for an API key and prompts the user to select one
    if there are multiple.
    """
    print("-> Step 1: Fetching available organizations...")
    url = f"{MERAKI_BASE_URL}/organizations"
    headers = {"X-Cisco-Meraki-API-Key": api_key, "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        organizations = response.json()

        if not organizations:
            print("[!] Error: No organizations found for this API key.")
            return None
        
        if len(organizations) == 1:
            org = organizations[0]
            print(f"   -> Automatically selected the only available organization: '{org['name']}'")
            return org['id']
        
        # If multiple organizations, prompt the user to choose
        print("\nMultiple organizations found. Please choose one to scan:")
        for i, org in enumerate(organizations):
            print(f"  {i + 1}: {org['name']} (ID: {org['id']})")
        
        while True:
            try:
                choice = int(input("\nEnter the number of the organization: "))
                if 1 <= choice <= len(organizations):
                    return organizations[choice - 1]['id']
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("\n[!] HTTP 401 Unauthorized: The Meraki API key is invalid or has been revoked.")
        else:
            print(f"\n[!] An HTTP error occurred while fetching organizations: {e}")
        return None
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        return None

def fetch_devices_and_save(api_key, org_id):
    """
    Fetches all devices for a given organization ID and saves them to a file.
    """
    print(f"\n-> Step 2: Fetching devices for Organization ID: ...{org_id[-4:]}")
    url = f"{MERAKI_BASE_URL}/organizations/{org_id}/devices"
    headers = {"X-Cisco-Meraki-API-Key": api_key, "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        devices = response.json()

        with open(INVENTORY_FILE, 'w') as f:
            json.dump(devices, f, indent=4)
        
        print(f"\n[✓] Success! Found {len(devices)} devices.")
        print(f"    Inventory has been saved to '{INVENTORY_FILE}'")

    except requests.exceptions.HTTPError as e:
        print(f"\n[!] An HTTP error occurred while fetching devices: {e}")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

def main():
    """
    Main function to orchestrate fetching the inventory.
    """
    print("--- Starting Meraki Device Inventory Fetch ---")
    load_dotenv()
    meraki_api_key = os.getenv("MERAKI_API_KEY")

    if not meraki_api_key:
        print("\n[!] Error: MERAKI_API_KEY not found in your .env file.")
        return

    # Get the Organization ID dynamically
    organization_id = get_organization_id(meraki_api_key)

    # If we successfully got an org ID, fetch the devices
    if organization_id:
        fetch_devices_and_save(meraki_api_key, organization_id)

# --- Main Execution ---
if __name__ == "__main__":
    main()
