# Meraki Vulnerability Correlation Tool

This project provides a set of Python scripts designed to bridge a critical gap in network security management. It automates the process of correlating official Cisco PSIRT (Product Security Incident Response Team) security advisories with a live inventory of devices from a Meraki organization.

The tool fetches threat intelligence directly from the Cisco API, pulls the current device list from the Meraki Dashboard API, and performs an intelligent, version-aware analysis to produce a clear, actionable report of vulnerable devices.

## Key Features

-   **Automated Data Integration**: Programmatically pulls data from two distinct sources: the Cisco Security API and the Meraki Dashboard API.
-   **Live Inventory Fetch**: Retrieves a real-time list of all devices in your Meraki organization, ensuring analysis is always based on current data.
-   **Intelligent Correlation**: Implements precise, version-aware comparison logic to accurately match advisories to specific device models and firmware versions, eliminating false positives.
-   **Actionable Reporting**: Generates a clear, device-centric report that lists which devices are vulnerable and the exact remediation steps required.

## Prerequisites

-   Python 3.6+
-   `pip` for installing Python packages

## Configuration

Follow these steps to set up the tool for your environment.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone [URL_to_your_GitHub_repository]
cd [repository_folder_name]
```


### 2. Install Dependencies
 
This project uses a few external Python libraries. It's recommended to create a requirements.txt file with the following content:
 
requirements.txt
```
requests
python-dotenv
packaging
```

Then, install these dependencies using pip:
```
pip install -r requirements.txt
```
### 3. Create the .env Configuration File
 
For security, API keys are stored in a .env file, which should not be committed to source control. Create a file named .env in the root of the project directory.
 
### 4. Obtain API Keys
 
You will need two separate API keys to use this tool.
 
#### A. Meraki Dashboard API Key
 
This key allows the script to access your Meraki organization and retrieve the device inventory.
 
Log in to your Meraki Dashboard.
In the top-right corner, click on your account name/email and navigate to My Profile.
Scroll down to the API access section.
If you don't have a key, click Generate API key. Copy the key and store it securely.
 
#### B. Cisco Security Advisories (PSIRT) API Key
 
This key allows the script to fetch security advisories from Cisco.
 
Log in to the Cisco API Console: https://apiconsole.cisco.com/
Navigate to My Apps in the top-right menu.
Click Create a new App.
Give your application a Name (e.g., "Meraki Security Checker") and a Description.
Under APIs, find and check the box for the Security Advisories API. This is the most critical step to avoid 403 Forbidden errors.
Click Register.
On your application's details page, you will see a section to generate a Bearer Token. Generate a new token (you can set its expiry time) and copy it.
 
### 5. Populate Your .env File
 
Open the .env file you created and add the keys you just obtained. The file should look exactly like this:
```
# Cisco Security Advisory API Token
CISCO_API_TOKEN="your_cisco_api_token_here"

# Meraki API Credentials
MERAKI_API_KEY="your_meraki_api_key_here"
```
## Usage Workflow
 
The process is a simple two-step command-line workflow.
 
### Step 1: Fetch Your Live Device Inventory
 
First, run the fetch_inventory.py script. This will connect to the Meraki API and create a device_inventory.json file containing all your devices.
```
python fetch_inventory.py
```
If your API key has access to multiple organizations, the script will prompt you to choose which one to scan.
 
### Step 2: Run the Vulnerability Analysis
 
Once your inventory file is created, run the main analysis script. This will download all Meraki advisories from Cisco and correlate them against your new inventory file.
```
python run_vulnerability_check.py
```
Understanding the Output
 
The script will produce a detailed report in your console, grouped by each affected device.
 
### Example Output:
```
--- Analysis Complete: Found vulnerabilities on 1 device(s) ---

==============================================================================
DEVICE: MX-Managed-Firewall (Model: MX68CW-WW, Serial: Q2NY-VLYV-A3LY)
  Current Firmware: MX 18.211 (Vulnerable)
------------------------------------------------------------------------------
  Affected by:
    - Advisory: cisco-sa-meraki-mx-vpn-dos-vNRpDvfb.json
      Title: Cisco Meraki MX and Z Series AnyConnect VPN Denial of Service Vulnerability
      Recommendation: Upgrade to 18.211.4 or later.

==============================================================================
```

Additionally, a folder named csaf_advisories will be created, containing the raw JSON data for every downloaded advisory for your own records or further analysis.
