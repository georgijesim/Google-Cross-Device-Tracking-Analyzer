import pandas as pd
import re

def parse_device_csv(file_path):
    try:
        # Read CSV with comma separator, using Python engine for complex fields
        df = pd.read_csv(file_path, sep=',', encoding='utf-8', on_bad_lines='warn', 
                         keep_default_na=False, engine='python')
        
        # Check if Device Last Location column exists (case-insensitive)
        columns = df.columns.str.strip().str.lower()
        location_col = None
        for col in columns:
            if 'device last location' in col:
                location_col = df.columns[columns == col][0]
                break
        
        if location_col is None:
            raise ValueError(f"Column 'Device Last Location' not found in CSV. Available columns: {df.columns.tolist()}")
        
        # Check if Device Type column exists (case-insensitive)
        device_type_col = None
        for col in columns:
            if 'device type' in col:
                device_type_col = df.columns[columns == col][0]
                break
        
        # Function to extract timestamp and country from Device Last Location
        def extract_location_info(location):
            # Handle empty or whitespace-only cells
            if pd.isna(location) or str(location).strip() == '':
                return pd.NaT, 'N/A'
            # Use regex to find timestamp and country
            time_match = re.search(r'Last Activity Time: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC)', location)
            country_match = re.search(r'Country ISO: (\w{2})', location)
            timestamp = pd.to_datetime(time_match.group(1), format='%Y-%m-%d %H:%M:%S UTC', errors='coerce') if time_match else pd.NaT
            country = country_match.group(1) if country_match else 'N/A'
            return timestamp, country
        
        # Apply extraction, ensuring row count consistency
        location_results = df[location_col].apply(extract_location_info)
        if len(location_results) != len(df):
            raise ValueError(f"Mismatch in row counts: DataFrame has {len(df)} rows, but location extraction produced {len(location_results)} rows")
        
        df['Timestamp'], df['Location'] = zip(*location_results)
        
        # Assign Device Type
        if device_type_col is None:
            df['Device Type'] = 'Unknown'
        else:
            df['Device Type'] = df[device_type_col].apply(
                lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' else 'Unknown'
            ).replace('UNKNOWN', 'Unknown')
        
        # Fill other required columns
        df['IP Address'] = 'N/A'
        df['App Used'] = 'N/A'
        
        # Filter out rows with invalid timestamps
        filtered_df = df.dropna(subset=['Timestamp'])
        
        # Generate breakdown
        unique_devices = filtered_df['Device Type'].nunique()
        unique_locations = filtered_df['Location'].nunique()
        total_records = len(filtered_df)
        earliest = filtered_df['Timestamp'].min()
        latest = filtered_df['Timestamp'].max()
        days_tracked = (latest - earliest).days if pd.notna(earliest) and pd.notna(latest) else 0
        device_types = filtered_df['Device Type'].value_counts().to_dict()
        
        breakdown = (
            "Device Tracking Analysis\n\n"
            "• Unique Device Types: {}\n"
            "• Unique Locations: {}\n"
            "• Total Records: {}\n"
            "• Tracking Period: {} days (from {} to {})\n"
            "• Device Types:\n{}".format(
                unique_devices,
                unique_locations,
                total_records,
                days_tracked,
                earliest,
                latest,
                "\n".join([f"  - {device}: {count}" for device, count in device_types.items()])
            )
        )
        
        # Select required columns
        required_columns = ['Timestamp', 'IP Address', 'Device Type', 'Location', 'App Used']
        return filtered_df[required_columns], breakdown
    except Exception as e:
        raise ValueError(f"Error reading device CSV: {str(e)}")