import pandas as pd

def parse_activity_csv(file_path):
    try:
        # Read CSV with flexible column handling
        df = pd.read_csv(file_path, sep=',', parse_dates=['Activity Timestamp'], 
                         on_bad_lines='skip', encoding='utf-8')
        
        # Extract device type from User Agent String
        def extract_device_type(ua):
            if pd.isna(ua):
                return 'Unknown'
            if 'Device Type :' in ua:
                parts = ua.split('Device Type :')[1].split('.')[0].strip()
                return parts
            return 'Unknown'
        
        # Ensure required columns, fill missing with 'N/A'
        df['Timestamp'] = df['Activity Timestamp'].fillna(pd.NaT)
        df['IP Address'] = df.get('IP Address', 'N/A')
        df['Device Type'] = df['User Agent String'].apply(extract_device_type)
        df['Location'] = df.get('Activity Country', 'N/A').fillna('N/A')
        df['App Used'] = df.get('Product Name', 'N/A')
        
        # Combine "Unknown" and "UNKNOWN" for consistency
        df['Device Type'] = df['Device Type'].replace('UNKNOWN', 'Unknown')
        
        # Generate breakdown
        unique_devices = df['Device Type'].nunique()
        unique_ips = df['IP Address'].nunique()
        total_activities = len(df)
        earliest = df['Timestamp'].min()
        latest = df['Timestamp'].max()
        days_tracked = (latest - earliest).days if pd.notna(earliest) and pd.notna(latest) else 0
        apps_used = df['App Used'].value_counts().to_dict()
        
        breakdown = (
            "Activity Tracking Analysis\n\n"
            "• Unique Devices Tracked: {}\n"
            "• Unique IP Addresses: {}\n"
            "• Total Activities Recorded: {}\n"
            "• Tracking Period: {} days (from {} to {})\n"
            "• Apps Used:\n{}".format(
                unique_devices,
                unique_ips,
                total_activities,
                days_tracked,
                earliest,
                latest,
                "\n".join([f"  - {app}: {count}" for app, count in apps_used.items()])
            )
        )
        
        # Select relevant columns
        required_columns = ['Timestamp', 'IP Address', 'Device Type', 'Location', 'App Used']
        return df[required_columns].dropna(subset=['Timestamp']), breakdown
    except Exception as e:
        raise ValueError(f"Error reading activity CSV: {str(e)}")