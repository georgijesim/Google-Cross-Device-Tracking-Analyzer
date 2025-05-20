# Google Cross-Device Tracking Analyzer

A desktop application that analyzes and visualizes data from Google Takeout CSV exports, helping you understand how Google tracks your activities and devices. Load your Google Takeout activity or device log CSVs to get:

- **File Preview**: View the first few lines of the uploaded CSV.
- **Parsed Table**: Displays timestamp, IP address, device type, location, and app used.
- **Summary Stats**: Breakdown of unique devices, IP addresses (for activity logs), locations, total records, tracking period, and app or device type counts.
- **Visualizations**: Bar, pie, and line charts for activity logs (not available for device logs).
- **Privacy Shortcuts**: Quick links to Google’s Web & App Activity, Location History, and Ad Settings dashboards.
- **Export**: Save a timestamped `.txt` report with the summary and detailed table.

---

## Features

- **Flexible CSV Parsing**: Handles activity and device log CSVs, skips malformed rows, and manages missing columns.
- **Device-Type Extraction**: Automatically extracts device types from user-agent strings (activity logs) or device data (device logs).
- **Visualizations for Activity Logs**: Includes bar chart (activities by app), pie chart (activities by device type), and line chart (activities over time, with daily, weekly, or monthly breakdowns).
- **One-Click Export**: Exports analysis to a timestamped `.txt` file.
- **Privacy Shortcuts**: Direct links to manage Google privacy settings - healping you navigate Google's forest of links for privacy controls.
- **Supported Data**: Processes Google Takeout "Access Log Activity" and device log CSVs. Future support planned for location and YouTube logs.

---

## Obtaining Google Takeout Data

To use this app, you need Google Takeout data for "Access Log Activity" or device logs. Follow these steps:

1. **Access Google Takeout**:
   - In the app, click the "Manage Web & App Activity" button to open Google’s privacy dashboard, or visit [takeout.google.com](https://takeout.google.com).
   - Sign in to your Google account.

2. **Request Data**:
   - Select "Access Log Activity" (for activity logs) and/or "Devices" (for device logs) in the list of Google services.
   - Choose your export format (CSV is required) and delivery method (e.g., email link).
   - Click "Create Export" to request the data.

3. **Wait for Export**:
   - Google will process your request, which may take a few hours to a couple of days.
   - You’ll receive an email with a download link to your Takeout archive.
   - A common error we noticed is the export commonly fails with no explaination, unfortunately at this point all we can recommend is to keep trying.

4. **Download and Extract**:
   - Download the archive and extract the CSV files (e.g., `AccessLogActivity.csv` for activity logs or device-related CSVs).
   - Note the file paths, as you’ll upload them individually in the app.

---

## Installation & Requirements

### Prerequisites
- **Python 3.7+**: Ensure Python is installed (`python --version` or `python3 --version`).
- A system with a graphical interface (Windows, macOS, or Linux with a desktop environment) for the `tkinter` GUI.

### Dependencies
- `tkinter`: For the GUI (usually included with Python; install `python3-tk` on Linux if missing).
- `pandas`: For CSV parsing and data manipulation.
- `matplotlib`: For generating visualizations.

### Setup
1. **Clone or Download**:
   - Clone this repository or download and extract the ZIP file.
   - Navigate to the project folder:
     ```bash
     cd path/to/google-cross-device-tracking-analyzer
     ```

2. **Install Dependencies**:
   - Run the following command to install required packages:
     ```bash
     pip install pandas matplotlib
     ```
   - On Linux, if `tkinter` is missing, install it:
     ```bash
     sudo apt-get install python3-tk  # Debian/Ubuntu
     sudo dnf install python3-tkinter  # Fedora
     ```

3. **Verify Folder Structure**:
   - Ensure the following files and folders are present:
     - `main.py`: The main application script.
     - `utils/visualizations.py`: Functions for generating bar, pie, and line charts.
     - `parsers/activity_parser.py`: Parser for activity log CSVs.
     - `parsers/device_parser.py`: Parser for device log CSVs.

---

## Running the App

1. **Start the App**:
   - Run the main script:
     ```bash
     python main.py
     ```
   - A window titled "Google Cross Device Tracking Analyzer" will open.

2. **Workflow**:
   - **Select CSV Type**: Choose "Activity Logs" or "Device Logs" from the dropdown.
   - **Select File**: Click "Select CSV File" to browse and upload a Google Takeout CSV.
   - **View Preview**: The "File Preview" section shows the first 10 lines of the CSV.
   - **Parse Data**: Click "Parse Data" to process the CSV.
   - **Check for Errors**: The "Output" section displays success or error messages (e.g., missing columns or parsing issues).
   - **View Table**: The "Device Access History" table shows parsed data (timestamp, IP address, device type, location, app used).
   - **View Summary**: The "Tracking Summary" shows a breakdown (e.g., unique devices, tracking period, app or device counts).
   - **Scroll for Visualizations** (Activity Logs only): Scroll down to see bar, pie, and line charts. Use the timeframe dropdown to adjust the line chart (Daily, Weekly, Monthly).
   - **Export or Manage Privacy**:
     - Click "Export Analysis" to save a `.txt` report.
     - Use privacy buttons to visit Google’s dashboards.
     - Click "Exit" to close the app.

---

## File Descriptions

- **`main.py`**:
  - The main application script, launching a `tkinter` GUI.
  - Features a two-column layout: left for file upload and preview, right for table and summary.
  - Handles CSV selection, parsing, table display, summary, visualizations (for activity logs), and export.

- **`utils/visualizations.py`**:
  - Contains functions to generate visualizations for activity logs:
    - `create_bar_chart`: Bar chart of activities by app.
    - `create_pie_chart`: Pie chart of activities by device type.
    - `create_line_chart`: Line chart of activities over time (daily, weekly, or monthly).
  - Suppresses Pandas timezone warnings for clean output.

- **`parsers/activity_parser.py`**:
  - Parses Google Takeout "Access Log Activity" CSVs.
  - Extracts timestamp, IP address, device type (from user-agent), location, and app used.
  - Generates a breakdown (unique devices, IPs, activities, tracking period, app counts).

- **`parsers/device_parser.py`**:
  - Parses Google Takeout device log CSVs.
  - Extracts timestamp and location from `Device Last Location`, device type, and sets IP address and app used to `N/A`.
  - Generates a breakdown (unique device types, locations, records, tracking period, device type counts).
  - Handles complex fields and malformed rows with robust error checking.

- **`Takeout/...`**
- Contains 2 sample Google Takeout CSV's for testing the app

---

## Notes

- **Activity vs. Device Logs**:
  - Activity logs include detailed app usage and IP data, with visualizations.
  - Device logs focus on device types and locations, without visualizations.
- **Error Handling**: The app displays errors for missing files, invalid CSVs, or parsing issues in the "Output" section.
- **Future Enhancements**: Planned support for location logs, YouTube logs, and integration with Google’s My Ads Center. We also plan to create a wholistic privacy profile where users can keep track of all of their Google Takeout information easily - with constant updates and automated export requests to Google Takeout.
- **Data Privacy**: Use the privacy shortcuts to review and manage your Google data. The app processes data locally and does not upload it.

---

## Troubleshooting

- **Missing `tkinter`**: Install `python3-tk` on Linux or ensure Python includes `tkinter` (standard on Windows/macOS).
- **CSV Parsing Errors**: Verify the CSV is a valid Google Takeout export. Check the "Output" section for specific error messages.
- **Visualizations Not Showing**: Ensure you selected "Activity Logs" (device logs don’t show visualizations).
- **Dependencies Issues**: Run `pip install pandas matplotlib` again, or use a virtual environment to avoid conflicts.

For bugs or feature requests, open an issue on the repository or contact the developers (listed in the repo).