import pandas as pd

def parse_device_csv(file_path):
    # Placeholder: Currently mimics activity parsing; extend for device-specific logic
    try:
        df = pd.read_csv(file_path, sep=',', parse_dates=['Activity Timestamp'], 
                         on_bad_lines='skip', encoding='utf-8')
        
        def extract_device_type(ua):
            if pd.isna(ua):
                return 'Unknown'
            if 'Device Type :' in ua:
                parts = ua.split('Device Type :')[1].split('.')[0].strip()
                return parts
            return 'Unknown'
        
        df['Timestamp'] = df['Activity Timestamp'].fillna(pd.NaT)
        df['IP Address'] = df.get('IP Address', 'N/A')
        df['Device Type'] = df['User Agent String'].apply(extract_device_type)
        df['Location'] = df.get('Activity Country', 'N/A').fillna('N/A')
        df['App Used'] = df.get('Product Name', 'N/A')
        
        df['Device Type'] = df['Device Type'].replace('UNKNOWN', 'Unknown')
        
        required_columns = ['Timestamp', 'IP Address', 'Device Type', 'Location', 'App Used']
        return df[required_columns].dropna(subset=['Timestamp'])
    except Exception as e:
        raise ValueError(f"Error reading device CSV: {str(e)}")