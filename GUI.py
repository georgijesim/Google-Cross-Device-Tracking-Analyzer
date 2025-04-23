import PySimpleGUI as sg
import pandas as pd
import webbrowser
import os
from datetime import datetime

# Modern color scheme (unchanged)
BACKGROUND_COLOR = '#F5F7FA'
BUTTON_COLOR = ('#FFFFFF', '#4A90E2')
TEXT_COLOR = '#2C3E50'
FRAME_COLOR = '#FFFFFF'
TABLE_HEADER_COLOR = '#4A90E2'
TABLE_ALTERNATE_COLOR = '#F8F9FA'
BORDER_COLOR = '#E1E4E8'

def select_file():
    return sg.popup_get_file('Select your Google Takeout CSV file', 
                           file_types=(('CSV Files', '*.csv'),), 
                           background_color=BACKGROUND_COLOR)

def parse_csv_file(file_path):
    try:
        # Read CSV with flexible column handling
        df = pd.read_csv(file_path, sep=',', parse_dates=['Activity Timestamp'], 
                        on_bad_lines='skip', encoding='utf-8')
        
        # Extract device type from User Agent String
        def extract_device_type(ua):
            if pd.isna(ua):
                return 'Unknown'
            # Look for "Device Type :" and extract the next word
            if 'Device Type :' in ua:
                parts = ua.split('Device Type :')[1].split('.')[0].strip()
                return parts
            return 'Unknown'
        
        # Ensure required columns exist, fill missing with 'N/A'
        df['Timestamp'] = df['Activity Timestamp'].fillna(pd.NaT)
        df['IP Address'] = df.get('IP Address', 'N/A')
        df['Device Type'] = df['User Agent String'].apply(extract_device_type)
        df['Location'] = df.get('Activity Country', 'N/A').fillna('N/A')
        df['App Used'] = df.get('Product Name', 'N/A')  # Add app usage
        
        # Select relevant columns
        required_columns = ['Timestamp', 'IP Address', 'Device Type', 'Location', 'App Used']
        return df[required_columns].dropna(subset=['Timestamp'])  # Drop rows with no timestamp
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {str(e)}")

def analyze_tracking_data(df):
    # Enhanced analysis for cross-device tracking
    unique_devices = df['Device Type'].nunique()
    unique_ips = df['IP Address'].nunique()
    login_count = len(df)
    earliest = df['Timestamp'].min()
    latest = df['Timestamp'].max()
    days_tracked = (latest - earliest).days if pd.notna(earliest) and pd.notna(latest) else 0
    apps_used = df['App Used'].value_counts().to_dict()
    
    summary = (
        f"Unique Devices Tracked: {unique_devices}\n"
        f"Unique IP Addresses: {unique_ips}\n"
        f"Total Activities Recorded: {login_count}\n"
        f"Tracking Period: {days_tracked} days (from {earliest} to {latest})\n"
        f"Apps Used: {', '.join([f'{app}: {count}' for app, count in apps_used.items()])}"
    )
    return summary

def export_analysis(df, summary, folder):
    output_file = os.path.join(folder, f"tracking_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(output_file, 'w') as f:
        f.write("Cross-Device Tracking Analysis\n\n")
        f.write(summary)
        f.write("\n\nDetailed Data:\n")
        df.to_string(f)
    return output_file

def main():
    sg.theme('LightBlue')
    sg.set_options(font=('Segoe UI', 10), text_color=TEXT_COLOR, background_color=BACKGROUND_COLOR)

    # Adjusted Left Column Layout
    left_column = [
        [sg.Text('File Upload', font=('Segoe UI', 16, 'bold'), pad=(0, (0, 15)))],
        [sg.Button('Select CSV File', button_color=BUTTON_COLOR, size=(20, 1), pad=(0, (0, 10)))],
        [sg.Frame('', [
            [sg.Multiline(size=(50, 8), key='-OUTPUT-', disabled=True, background_color=FRAME_COLOR)]
        ], background_color=FRAME_COLOR, expand_x=True, expand_y=True)],
        [sg.Button('Parse Data', button_color=BUTTON_COLOR, size=(15, 1), pad=(0, (0, 15)))],
        [sg.Frame('File Preview', [
            [sg.Multiline(size=(50, 15), key='-FILE_PREVIEW-', disabled=True, background_color=FRAME_COLOR)]
        ], background_color=FRAME_COLOR, expand_x=True, expand_y=True)]
    ]

    # Adjusted Right Column Layout
    right_column = [
        [sg.Text('Device Access History', font=('Segoe UI', 16, 'bold'), pad=(0, (0, 15)))],
        [sg.Frame('', [
            [sg.Table(values=[[]], headings=['Timestamp', 'IP Address', 'Device Type', 'Location', 'App Used'],
                     max_col_width=25, auto_size_columns=True, justification='left',
                     num_rows=20, key='-TABLE-', background_color=FRAME_COLOR,
                     alternating_row_color=TABLE_ALTERNATE_COLOR, header_background_color=TABLE_HEADER_COLOR,
                     header_text_color='#FFFFFF', expand_x=True, expand_y=True)]
        ], background_color=FRAME_COLOR, expand_x=True, expand_y=True)],
        [sg.Frame('Tracking Summary', [
            [sg.Multiline(size=(50, 8), key='-SUMMARY-', disabled=True, background_color=FRAME_COLOR)]
        ], background_color=FRAME_COLOR, expand_x=True)],
        [sg.Frame('Privacy Controls', [
            [sg.Text("Google uses this data to link activities across devices.", pad=(10, (10, 5)))],
            [sg.Button('Manage Web & App Activity', key='-WEB_APP-', button_color=BUTTON_COLOR, size=(25, 1))],
            [sg.Button('Manage Location History', key='-LOCATION-', button_color=BUTTON_COLOR, size=(25, 1))],
            [sg.Button('Manage Ad Settings', key='-AD_SETTING-', button_color=BUTTON_COLOR, size=(25, 1))],
            [sg.Button('Export Analysis', key='-EXPORT-', button_color=BUTTON_COLOR, size=(15, 1))],
            [sg.Button('Exit', button_color=BUTTON_COLOR, size=(15, 1))]
        ], background_color=FRAME_COLOR, expand_x=True)]
    ]

    layout = [
        [sg.Text('Google Cross Device Tracking Analyzer', font=('Segoe UI', 20, 'bold'), justification='center', pad=(0, (0, 20)))],
        [sg.Column(left_column, vertical_alignment='top', pad=(20, 0), expand_x=True, expand_y=True),
         sg.VSeperator(),
         sg.Column(right_column, vertical_alignment='top', pad=(20, 0), expand_x=True, expand_y=True)]
    ]

    window = sg.Window('Google Cross Device Tracking Analyzer', layout, size=(1200, 800), resizable=True, 
                      background_color=BACKGROUND_COLOR, finalize=True)

    selected_file = None
    df = None
    while True:
        event, values = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            break
        elif event == 'Select CSV File':
            file_path = select_file()
            if file_path:
                selected_file = file_path
                window['-OUTPUT-'].update(f"Selected file: {os.path.basename(file_path)}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        preview = ''.join(f.readlines()[:10])
                    window['-FILE_PREVIEW-'].update(preview)
                except Exception as e:
                    window['-FILE_PREVIEW-'].update(f"Error reading file: {str(e)}")
        elif event == 'Parse Data':
            if not selected_file:
                window['-OUTPUT-'].update("No file selected.")
                continue
            try:
                df = parse_csv_file(selected_file)
                table_data = df.values.tolist()
                window['-TABLE-'].update(values=table_data)
                summary = analyze_tracking_data(df)
                window['-SUMMARY-'].update(summary)
                window['-OUTPUT-'].update("Data parsed successfully.")
            except Exception as e:
                window['-OUTPUT-'].update(f"Error: {str(e)}")
        elif event == '-WEB_APP-':
            webbrowser.open('https://myaccount.google.com/data-and-personalization')
        elif event == '-LOCATION-':
            webbrowser.open('https://www.google.com/maps/timeline')
        elif event == '-AD_SETTING-':
            webbrowser.open('https://adssettings.google.com/')
        elif event == '-EXPORT-' and df is not None:
            try:
                output_file = export_analysis(df, window['-SUMMARY-'].get(), os.path.dirname(selected_file))
                window['-OUTPUT-'].update(f"Analysis exported to: {output_file}")
            except Exception as e:
                window['-OUTPUT-'].update(f"Export error: {str(e)}")
    window.close()

if __name__ == '__main__':
    main()