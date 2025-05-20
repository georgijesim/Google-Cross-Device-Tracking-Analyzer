import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import warnings

# Suppress timezone conversion warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Converting to PeriodArray/Index representation will drop timezone information."
)

def create_bar_chart(df):
    """Create a bar chart of activities per app with count labels."""
    fig = Figure(figsize=(6, 6))  # Increased height for better visualization
    ax = fig.add_subplot(111)
    app_counts = df['App Used'].value_counts()
    bars = ax.bar(app_counts.index, app_counts.values)
    ax.set_title("Activities Tracked by App")
    ax.set_xlabel("App Used")
    ax.set_ylabel("Number of Activities")
    ax.tick_params(axis='x', rotation=45)

    # Format the y-axis to add commas
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x):,}'))

    # Set the y-axis limit to 100,000, with ticks every 10,000
    ax.set_ylim(0, 90000)
    ax.yaxis.set_ticks(range(0, 90001, 10000))  # 10,000 intervals

    # Add labels above bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.05*yval, f'{int(yval):,}', ha='center', va='bottom')
    
    fig.tight_layout()
    return fig

def create_pie_chart(df):
    """Create a pie chart of activities by device type."""
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    device_counts = df['Device Type'].value_counts()
    ax.pie(device_counts.values, labels=device_counts.index, autopct='%1.1f%%')
    ax.set_title("Activities by Device Type")
    fig.tight_layout()
    return fig

def create_line_chart(df, timeframe="Daily"):
    """Create a line chart of activities over time with specified timeframe."""
    df = df.copy()
    df['Date'] = df['Timestamp'].dt.floor('D')
    
    if timeframe == "Weekly":
        df['Date'] = df['Timestamp'].dt.to_period('W').dt.start_time
    elif timeframe == "Monthly":
        df['Date'] = df['Timestamp'].dt.to_period('M').dt.start_time
    
    counts = df.groupby('Date').size()
    
    fig = Figure(figsize=(max(8, len(counts)/2), 6))  # Increased height for better visualization
    ax = fig.add_subplot(111)
    ax.plot(counts.index, counts.values, marker='o')
    ax.set_title("Activities Tracked Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Activities")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.tick_params(axis='x', rotation=45)
    
    # Format the y-axis to add commas
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x):,}'))

    fig.tight_layout()
    
    return fig