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

