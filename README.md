# Google Cross-Device Tracking Analyzer

A desktop app that helps you explore and summarize the data Google collects about your activities across devices. Load in your Google Takeout CSV export and get:

- **File preview** of the first few lines  
- **Parsed table** of timestamp, IP address, device type, location & app used  
- **Summary stats** (unique devices, IPs, total events, tracking period, apps used)  
- **Quick links** to Google privacy dashboards  
- **Export** a full text report with both the summary and the detailed table  

---

## Features

- **Flexible CSV parsing**: skips bad lines, handles missing columns  
- **Automatic device-type extraction** from your user-agent string  
- **Simple GUI** built with PySimpleGUI  
- **One-click export** of analysis to a timestamped `.txt` file  
- **Privacy shortcuts** open your Web & App Activity, Location History, and Ad Settings pages
- **Currently supports** processing Google Tackout Access Log Activity CSV's. Will add functionality for location and Youtube logs and integration with Google My Ads Center

---

## Installation & Requirements

1. **Clone or download** this repo and `cd` into its folder.
2. Make sure you’re running **Python 3.7+**.
3. Install dependencies:
   `pip install PySimpleGUI pandas`
