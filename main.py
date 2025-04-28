import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import os
from datetime import datetime
from parsers import parse_activity_csv, parse_device_csv
from utils import create_bar_chart, create_pie_chart, create_line_chart

# Color scheme
BACKGROUND_COLOR = '#F5F7FA'
BUTTON_COLOR = '#4A90E2'
TEXT_COLOR = '#2C3E50'
FRAME_COLOR = '#FFFFFF'
TABLE_HEADER_COLOR = '#4A90E2'
TABLE_ALTERNATE_COLOR = '#F8F9FA'

class TrackingAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Cross Device Tracking Analyzer")
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Initialize variables
        self.df = None
        self.selected_file = None
        self.parser = None
        
        # Setup scrollable main frame
        self.canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Layout
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.setup_gui()
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def setup_gui(self):
        # Title
        tk.Label(
            self.scrollable_frame,
            text="Google Cross Device Tracking Analyzer",
            font=("Segoe UI", 20, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)
        
        # Two-column frame
        columns_frame = tk.Frame(self.scrollable_frame, bg=BACKGROUND_COLOR)
        columns_frame.pack(fill="x", padx=20)
        
        # Left column
        left_column = tk.Frame(columns_frame, bg=FRAME_COLOR, bd=2, relief="ridge")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(
            left_column,
            text="File Upload",
            font=("Segoe UI", 16, "bold"),
            bg=FRAME_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(10, 15))
        
        # CSV type dropdown
        tk.Label(
            left_column,
            text="Select CSV Type:",
            font=("Segoe UI", 12),
            bg=FRAME_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w", padx=10)
        
        self.csv_type_var = tk.StringVar(value="Activity Logs")
        csv_type_menu = ttk.Combobox(
            left_column,
            textvariable=self.csv_type_var,
            values=["Activity Logs", "Device Logs"],
            state="readonly"
        )
        csv_type_menu.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            left_column,
            text="Select CSV File",
            bg=BUTTON_COLOR,
            fg="white",
            font=("Segoe UI", 10),
            command=self.select_file
        ).pack(pady=10)
        
        # Create output_text widget and pack separately
        self.output_text = tk.Text(
            left_column,
            height=5,
            width=50,
            bg=FRAME_COLOR,
            fg=TEXT_COLOR,
            font=("Segoe UI", 10),
            state="disabled"
        )
        self.output_text.pack(padx=10, pady=5, fill="x")
        
        tk.Button(
            left_column,
            text="Parse Data",
            bg=BUTTON_COLOR,
            fg="white",
            font=("Segoe UI", 10),
            command=self.parse_data
        ).pack(pady=15)
        
        tk.Label(
            left_column,
            text="File Preview",
            font=("Segoe UI", 12, "bold"),
            bg=FRAME_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(10, 5))
        
        # Create preview_text widget and pack separately
        self.preview_text = tk.Text(
            left_column,
            height=15,
            width=50,
            bg=FRAME_COLOR,
            fg=TEXT_COLOR,
            font=("Segoe UI", 10),
            state="disabled"
        )
        self.preview_text.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Right column
        right_column = tk.Frame(columns_frame, bg=FRAME_COLOR, bd=2, relief="ridge")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(
            right_column,
            text="Device Access History",
            font=("Segoe UI", 16, "bold"),
            bg=FRAME_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(10, 15))
        
        # Table (using Treeview)
        self.tree = ttk.Treeview(
            right_column,
            columns=("Timestamp", "IP Address", "Device Type", "Location", "App Used"),
            show="headings",
            height=15
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", padx=10, pady=5, expand=True)
        
        tk.Label(
            right_column,
            text="Tracking Summary",
            font=("Segoe UI", 12, "bold"),
            bg=FRAME_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(10, 5))
        
        # Create summary_text widget and pack separately
        self.summary_text = tk.Text(
            right_column,
            height=10,
            width=50,
            bg=FRAME_COLOR,
            fg=TEXT_COLOR,
            font=("Segoe UI", 12),
            state="disabled"
        )
        self.summary_text.pack(padx=10, pady=5, fill="x")
        
        # Privacy controls
        privacy_frame = tk.Frame(right_column, bg=FRAME_COLOR)
        privacy_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            privacy_frame,
            text="Google uses this data to link activities across devices.",
            font=("Segoe UI", 10),
            bg=FRAME_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(10, 5))
        
        tk.Button(
            privacy_frame,
            text="Manage Web & App Activity",
            bg=BUTTON_COLOR,
            fg="white",
            font=("Segoe UI", 10),
            command=lambda: webbrowser.open("https://myaccount.google.com/data-and-personalization")
        ).pack(fill="x", pady=2)
        
        tk.Button(
            privacy_frame,
            text="Manage Location History",
            bg=BUTTON_COLOR,
            fg="white",
            font=("Segoe UI", 10),
            command=lambda: webbrowser.open("https://www.google.com/maps/timeline")
        ).pack(fill="x", pady=2)
        
        tk.Button(
            privacy_frame,
            text="Manage Ad Settings",
            bg=BUTTON_COLOR,
            fg="white",
            font=("Segoe UI", 10),
            command=lambda: webbrowser.open("https://adssettings.google.com/")
        ).pack(fill="x", pady=2)
        
        tk.Button(
            privacy_frame,
            text="Export Analysis",
            bg=BUTTON_COLOR,
            fg="white",
            font=("Segoe UI", 10),
            command=self.export_analysis
        ).pack(fill="x", pady=2)
        
        tk.Button(
            privacy_frame,
            text="Exit",
            bg=BUTTON_COLOR,
            fg="white",
            font=("Segoe UI", 10),
            command=self.root.quit
        ).pack(fill="x", pady=2)
        
        # Visualizations section (hidden initially)
        self.viz_frame = tk.Frame(self.scrollable_frame, bg=FRAME_COLOR, bd=2, relief="ridge")
        # Calculate 10% of initial window width (1200 pixels) = 120 pixels
        padding_x = 120  # Alternatively, use self.root.winfo_width() * 0.1 for dynamic sizing
        self.viz_frame.pack(fill="x", padx=padding_x, pady=(20,40))
        self.viz_frame.pack_forget()  # Hide initially
        
        tk.Label(
            self.viz_frame,
            text="Data Visualizations",
            font=("Segoe UI", 16, "bold"),
            bg=FRAME_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(10, 15))
        
        # Visualization canvases
        self.bar_canvas = None
        self.pie_canvas = None
        self.line_canvas = None
        self.line_scroll_canvas = None

        # Timeframe dropdown for line chart
        tk.Label(
            self.viz_frame,
            text="Choose breakdown timeframe:",
            font=("Segoe UI", 12),
            bg=FRAME_COLOR,
            fg=TEXT_COLOR
        ).pack()
        
        self.timeframe_var = tk.StringVar(value="Daily")
        timeframe_menu = ttk.Combobox(
            self.viz_frame,
            textvariable=self.timeframe_var,
            values=["Daily", "Weekly", "Monthly", "5-day", "10-day"],
            state="readonly"
        )
        timeframe_menu.pack(pady=5)
        timeframe_menu.bind("<<ComboboxSelected>>", self.update_line_chart)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.selected_file = file_path
            self.update_output(f"Selected file: {os.path.basename(file_path)}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    preview = ''.join(f.readlines()[:10])
                self.update_text(self.preview_text, preview)
            except Exception as e:
                self.update_text(self.preview_text, f"Error reading file: {str(e)}")
                
    def parse_data(self):
        if not self.selected_file:
            self.update_output("No file selected.")
            return
        
        csv_type = self.csv_type_var.get()
        self.parser = parse_activity_csv if csv_type == "Activity Logs" else parse_device_csv
        
        try:
            self.df = self.parser(self.selected_file)
            self.update_table()
            summary = self.analyze_tracking_data()
            self.update_summary(summary)
            self.update_output("Data parsed successfully.")
            self.show_visualizations()
        except Exception as e:
            self.update_output(f"Error: {str(e)}")
            
    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=tuple(row))
            
    def analyze_tracking_data(self):
        unique_devices = self.df['Device Type'].nunique()
        unique_ips = self.df['IP Address'].nunique()
        login_count = len(self.df)
        earliest = self.df['Timestamp'].min()
        latest = self.df['Timestamp'].max()
        days_tracked = (latest - earliest).days if pd.notna(earliest) and pd.notna(latest) else 0
        apps_used = self.df['App Used'].value_counts().to_dict()
        
        summary = (
            "Cross-Device Tracking Analysis\n\n"
            "• Unique Devices Tracked: {}\n"
            "• Unique IP Addresses: {}\n"
            "• Total Activities Recorded: {}\n"
            "• Tracking Period: {} days (from {} to {})\n"
            "• Apps Used:\n{}".format(
                unique_devices,
                unique_ips,
                login_count,
                days_tracked,
                earliest,
                latest,
                "\n".join([f"  - {app}: {count}" for app, count in apps_used.items()])
            )
        )
        return summary
    
    def update_output(self, text):
        self.update_text(self.output_text, text)
        
    def update_summary(self, summary):
        self.update_text(self.summary_text, summary)
        
    def update_text(self, text_widget, content):
        text_widget.configure(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, content)
        text_widget.configure(state="disabled")
        
    def export_analysis(self):
        if self.df is None:
            self.update_output("No data to export.")
            return
        try:
            output_file = os.path.join(
                os.path.dirname(self.selected_file),
                f"tracking_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            with open(output_file, 'w') as f:
                f.write(self.summary_text.get("1.0", tk.END))
                f.write("\n\nDetailed Data:\n")
                self.df.to_string(f)
            self.update_output(f"Analysis exported to: {output_file}")
        except Exception as e:
            self.update_output(f"Export error: {str(e)}")
            
    def show_visualizations(self):
        # Clear existing visualizations
        if self.bar_canvas:
            self.bar_canvas.get_tk_widget().destroy()
        if self.pie_canvas:
            self.pie_canvas.get_tk_widget().destroy()
        if self.line_canvas:
            self.line_canvas.get_tk_widget().destroy()
        if self.line_scroll_canvas:
            self.line_scroll_canvas.destroy()
            
        # Show viz frame
        self.viz_frame.pack(fill="x", padx=120, pady=20)
        
        # Bar chart
        fig_bar = create_bar_chart(self.df)
        self.bar_canvas = FigureCanvasTkAgg(fig_bar, master=self.viz_frame)
        self.bar_canvas.draw()
        self.bar_canvas.get_tk_widget().pack(pady=10)
        
        # Pie chart
        fig_pie = create_pie_chart(self.df)
        self.pie_canvas = FigureCanvasTkAgg(fig_pie, master=self.viz_frame)
        self.pie_canvas.draw()
        self.pie_canvas.get_tk_widget().pack(pady=10)
        
        # Line chart
        self.update_line_chart()
        
    def update_line_chart(self, event=None):
        if self.line_canvas:
            self.line_canvas.get_tk_widget().destroy()
        if self.line_scroll_canvas:
            self.line_scroll_canvas.destroy()
            
        timeframe = self.timeframe_var.get()
        
        # Create scrollable canvas
        scroll_frame = tk.Frame(self.viz_frame, bg=FRAME_COLOR)
        scroll_frame.pack(fill="x", pady=10)
        
        canvas = tk.Canvas(scroll_frame, bg=FRAME_COLOR, height=600) # Defines the space where the visuzalizations go
        scrollbar = ttk.Scrollbar(scroll_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg=FRAME_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="top", fill="x")
        
        self.line_scroll_canvas = canvas
        
        # Line chart
        fig_line = create_line_chart(self.df, timeframe)
        self.line_canvas = FigureCanvasTkAgg(fig_line, master=scrollable_frame)
        self.line_canvas.draw()
        self.line_canvas.get_tk_widget().pack()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    app = TrackingAnalyzerApp(root)
    root.mainloop()