"""
===========================================
    Exponential Backoff Demo - FINAL VERSION
    For Team H Presentation
    
    Features:
    - Number of Clients (instead of failure rate)
    - Visual exponential graph
    - Server load indicator
    - Request counter
    - Key takeaways summary
===========================================
"""

import tkinter as tk
from tkinter import ttk
import random
import threading
import time

class ExponentialBackoffDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Exponential Backoff Demo - Team H")
        self.root.geometry("1100x800")
        self.root.configure(bg="#1a1a2e")
        
        # State variables
        self.is_running = False
        self.speed = 1.0
        
        # Server capacity (max clients it can handle smoothly)
        self.server_capacity = 50
        
        # Colors
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'accent': '#0f3460',
            'success': '#00b894',
            'error': '#e74c3c',
            'warning': '#f39c12',
            'text': '#ffffff',
            'text_dim': '#a0a0a0',
            'blue': '#3498db',
            'purple': '#9b59b6'
        }
        
        self.setup_ui()
    
    def calculate_failure_rate(self, num_clients, server_load_modifier=0):
        """
        Calculate failure rate based on number of clients
        More clients = higher failure rate
        Server capacity is 50 clients
        """
        # Base failure rate depends on how overloaded the server is
        load_ratio = num_clients / self.server_capacity
        
        if load_ratio <= 0.5:
            base_rate = 0.1  # 10% failure - light load
        elif load_ratio <= 1.0:
            base_rate = 0.3  # 30% failure - normal load
        elif load_ratio <= 2.0:
            base_rate = 0.6  # 60% failure - heavy load
        elif load_ratio <= 4.0:
            base_rate = 0.8  # 80% failure - very heavy
        else:
            base_rate = 0.95  # 95% failure - overloaded
        
        # Apply modifier (for backoff recovery)
        adjusted_rate = max(0.05, min(0.99, base_rate + server_load_modifier))
        return adjusted_rate
    
    def calculate_server_load(self, num_clients):
        """Calculate server load percentage based on number of clients"""
        load = (num_clients / self.server_capacity) * 50  # 50 clients = 50% load
        return min(100, int(load))
    
    def setup_ui(self):
        """Setup the main UI"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=15)
        
        title = tk.Label(
            title_frame,
            text="EXPONENTIAL BACKOFF",
            font=("Helvetica", 28, "bold"),
            fg=self.colors['blue'],
            bg=self.colors['bg']
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="A Smart Retry Strategy for Network Systems",
            font=("Helvetica", 11),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        )
        subtitle.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg=self.colors['card'], width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.setup_controls(left_panel)
        
        # Right panel - Visualization
        right_panel = tk.Frame(main_frame, bg=self.colors['card'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.setup_visualization(right_panel)
        
        # Bottom - Log and Stats
        bottom_frame = tk.Frame(self.root, bg=self.colors['bg'])
        bottom_frame.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        self.setup_bottom_panel(bottom_frame)
    
    def setup_controls(self, parent):
        """Setup control panel"""
        # Title
        tk.Label(
            parent,
            text="Controls",
            font=("Helvetica", 13, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(15, 10))
        
        # Demo selection
        tk.Label(
            parent,
            text="Select Demo:",
            font=("Helvetica", 9),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=15)
        
        self.demo_var = tk.StringVar(value="comparison")
        
        demos = [
            ("Side-by-Side Comparison", "comparison"),
            ("Without Backoff", "no_backoff"),
            ("With Backoff", "with_backoff"),
            ("With Jitter", "with_jitter"),
            ("Exponential Graph", "graph")
        ]
        
        for text, value in demos:
            rb = tk.Radiobutton(
                parent,
                text=text,
                variable=self.demo_var,
                value=value,
                font=("Helvetica", 9),
                fg=self.colors['text'],
                bg=self.colors['card'],
                selectcolor=self.colors['accent'],
                activebackground=self.colors['card'],
                activeforeground=self.colors['text']
            )
            rb.pack(anchor='w', padx=25, pady=1)
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=15, pady=10)
        
        # Parameters
        tk.Label(
            parent,
            text="Parameters:",
            font=("Helvetica", 9),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=15)
        
        # Base wait time
        param_frame1 = tk.Frame(parent, bg=self.colors['card'])
        param_frame1.pack(fill='x', padx=15, pady=3)
        
        tk.Label(
            param_frame1,
            text="Base Wait (s):",
            font=("Helvetica", 9),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.base_wait_var = tk.StringVar(value="1")
        tk.Entry(
            param_frame1,
            textvariable=self.base_wait_var,
            width=5,
            font=("Helvetica", 9),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        ).pack(side='right')
        
        # Number of Clients
        param_frame2 = tk.Frame(parent, bg=self.colors['card'])
        param_frame2.pack(fill='x', padx=15, pady=3)
        
        tk.Label(
            param_frame2,
            text="Number of Clients:",
            font=("Helvetica", 9),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.num_clients_var = tk.StringVar(value="100")
        tk.Entry(
            param_frame2,
            textvariable=self.num_clients_var,
            width=5,
            font=("Helvetica", 9),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        ).pack(side='right')
        
        # Client hint
        tk.Label(
            parent,
            text="(50 = normal, 100+ = overload)",
            font=("Helvetica", 8),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(anchor='e', padx=15)
        
        # Max Attempts (NEW!)
        param_frame_attempts = tk.Frame(parent, bg=self.colors['card'])
        param_frame_attempts.pack(fill='x', padx=15, pady=3)
        
        tk.Label(
            param_frame_attempts,
            text="Max Attempts:",
            font=("Helvetica", 9),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.max_attempts_var = tk.StringVar(value="5")
        tk.Entry(
            param_frame_attempts,
            textvariable=self.max_attempts_var,
            width=5,
            font=("Helvetica", 9),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        ).pack(side='right')
        
        # Attempts hint
        tk.Label(
            parent,
            text="(3 = quick, 5 = normal, 7 = long)",
            font=("Helvetica", 8),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(anchor='e', padx=15)
        
        # Animation Speed
        param_frame3 = tk.Frame(parent, bg=self.colors['card'])
        param_frame3.pack(fill='x', padx=15, pady=3)
        
        tk.Label(
            param_frame3,
            text="Speed:",
            font=("Helvetica", 9),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.speed_var = tk.StringVar(value="Normal")
        speed_combo = ttk.Combobox(
            param_frame3,
            textvariable=self.speed_var,
            values=["Slow", "Normal", "Fast"],
            width=7,
            state="readonly"
        )
        speed_combo.pack(side='right')
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=15, pady=10)
        
        # Buttons
        self.start_btn = tk.Button(
            parent,
            text="START DEMO",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text'],
            bg=self.colors['success'],
            activebackground="#00a884",
            activeforeground=self.colors['text'],
            border=0,
            cursor="hand2",
            command=self.start_demo
        )
        self.start_btn.pack(fill='x', padx=15, pady=3)
        
        self.stop_btn = tk.Button(
            parent,
            text="STOP",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text'],
            bg=self.colors['error'],
            activebackground="#c0392b",
            activeforeground=self.colors['text'],
            border=0,
            cursor="hand2",
            command=self.stop_demo,
            state='disabled'
        )
        self.stop_btn.pack(fill='x', padx=15, pady=3)
        
        self.reset_btn = tk.Button(
            parent,
            text="RESET",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text'],
            bg=self.colors['accent'],
            activebackground="#0d2d4d",
            activeforeground=self.colors['text'],
            border=0,
            cursor="hand2",
            command=self.reset_demo
        )
        self.reset_btn.pack(fill='x', padx=15, pady=3)
        
        # Formula display
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            parent,
            text="Formula:",
            font=("Helvetica", 9, "bold"),
            fg=self.colors['blue'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=15)
        
        tk.Label(
            parent,
            text="wait = base x 2^attempt",
            font=("Courier", 10),
            fg=self.colors['warning'],
            bg=self.colors['card']
        ).pack(pady=3)
        
        tk.Label(
            parent,
            text="1s -> 2s -> 4s -> 8s -> 16s",
            font=("Helvetica", 8),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack()
        
        # Server info
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            parent,
            text="Server Capacity:",
            font=("Helvetica", 9, "bold"),
            fg=self.colors['success'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=15)
        
        tk.Label(
            parent,
            text="50 clients max\n\nMore clients = Overload!\nOverload = More failures!",
            font=("Helvetica", 8),
            fg=self.colors['text_dim'],
            bg=self.colors['card'],
            justify='left'
        ).pack(anchor='w', padx=15)
    
    def setup_visualization(self, parent):
        """Setup visualization area"""
        # Title
        tk.Label(
            parent,
            text="Visualization",
            font=("Helvetica", 13, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(15, 5))
        
        # Canvas for animation
        self.canvas = tk.Canvas(
            parent,
            bg=self.colors['bg'],
            highlightthickness=0,
            height=450
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Draw initial state after window is fully loaded
        self.root.after(200, self.draw_initial_state)
        
        # Redraw when canvas is resized
        self.canvas.bind("<Configure>", lambda e: self.draw_initial_state() if not self.is_running else None)
    
    def setup_bottom_panel(self, parent):
        """Setup bottom panel with stats and log"""
        # Stats panel
        stats_frame = tk.Frame(parent, bg=self.colors['card'], height=120)
        stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(
            stats_frame,
            text="Statistics",
            font=("Helvetica", 11, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=10, pady=(8, 5))
        
        # Stats container
        stats_container = tk.Frame(stats_frame, bg=self.colors['card'])
        stats_container.pack(fill=tk.X, padx=10)
        
        # Left stats
        left_stats = tk.Frame(stats_container, bg=self.colors['card'])
        left_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.stat_clients = tk.Label(
            left_stats,
            text="Clients: 0",
            font=("Helvetica", 10),
            fg=self.colors['blue'],
            bg=self.colors['card']
        )
        self.stat_clients.pack(anchor='w')
        
        self.stat_requests = tk.Label(
            left_stats,
            text="Requests Sent: 0",
            font=("Helvetica", 10),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        self.stat_requests.pack(anchor='w')
        
        self.stat_failures = tk.Label(
            left_stats,
            text="Failed: 0",
            font=("Helvetica", 10),
            fg=self.colors['error'],
            bg=self.colors['card']
        )
        self.stat_failures.pack(anchor='w')
        
        # Right stats
        right_stats = tk.Frame(stats_container, bg=self.colors['card'])
        right_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.stat_total_wait = tk.Label(
            right_stats,
            text="Total Wait: 0s",
            font=("Helvetica", 10),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        self.stat_total_wait.pack(anchor='w')
        
        self.stat_server_load = tk.Label(
            right_stats,
            text="Server Load: 0%",
            font=("Helvetica", 10),
            fg=self.colors['warning'],
            bg=self.colors['card']
        )
        self.stat_server_load.pack(anchor='w')
        
        self.stat_status = tk.Label(
            right_stats,
            text="Status: Ready",
            font=("Helvetica", 10),
            fg=self.colors['blue'],
            bg=self.colors['card']
        )
        self.stat_status.pack(anchor='w')
        
        # Log panel
        log_frame = tk.Frame(parent, bg=self.colors['card'], height=120, width=400)
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        log_frame.pack_propagate(False)
        
        tk.Label(
            log_frame,
            text="Event Log",
            font=("Helvetica", 11, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=10, pady=(8, 5))
        
        # Log text
        log_container = tk.Frame(log_frame, bg=self.colors['card'])
        log_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))
        
        scrollbar = tk.Scrollbar(log_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_container,
            font=("Courier", 8),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            height=4,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Configure tags
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('error', foreground=self.colors['error'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
        self.log_text.tag_config('info', foreground=self.colors['blue'])
    
    def draw_initial_state(self):
        """Draw initial visualization"""
        self.canvas.delete("all")
        
        # Force canvas to update its size
        self.canvas.update_idletasks()
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Fallback if size not available yet
        if width < 100:
            width = 600
        if height < 100:
            height = 400
        
        # Center text properly
        center_x = width // 2
        center_y = height // 2
        
        self.canvas.create_text(
            center_x, center_y - 20,
            text="Press START to begin the demo",
            font=("Helvetica", 16),
            fill=self.colors['text_dim'],
            anchor="center"
        )
        
        self.canvas.create_text(
            center_x, center_y + 20,
            text="Select a demo type from the controls panel",
            font=("Helvetica", 11),
            fill=self.colors['text_dim'],
            anchor="center"
        )
    
    def log(self, message, tag=None):
        """Add message to log"""
        self.log_text.config(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        
        if tag:
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        else:
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def update_stats(self, clients=None, requests=None, failures=None, total_wait=None, server_load=None, status=None):
        """Update statistics display"""
        if clients is not None:
            self.stat_clients.config(text=f"Clients: {clients}")
        if requests is not None:
            self.stat_requests.config(text=f"Requests Sent: {requests}")
        if failures is not None:
            self.stat_failures.config(text=f"Failed: {failures}")
        if total_wait is not None:
            self.stat_total_wait.config(text=f"Total Wait: {total_wait}s")
        if server_load is not None:
            self.stat_server_load.config(text=f"Server Load: {server_load}%")
            # Change color based on load
            if server_load > 80:
                self.stat_server_load.config(fg=self.colors['error'])
            elif server_load > 50:
                self.stat_server_load.config(fg=self.colors['warning'])
            else:
                self.stat_server_load.config(fg=self.colors['success'])
        if status is not None:
            self.stat_status.config(text=f"Status: {status}")
    
    def reset_stats(self):
        """Reset all statistics"""
        self.update_stats(clients=0, requests=0, failures=0, total_wait=0, server_load=0, status="Ready")
    
    def get_speed_multiplier(self):
        """Get animation speed multiplier"""
        speed = self.speed_var.get()
        if speed == "Slow":
            return 2.0
        elif speed == "Fast":
            return 0.5
        return 1.0
    
    def start_demo(self):
        """Start the selected demo"""
        self.is_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        demo_type = self.demo_var.get()
        
        # Clear log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Reset stats
        self.reset_stats()
        self.update_stats(status="Running...")
        
        self.log(f"Starting demo: {demo_type}", 'info')
        
        # Run demo in separate thread
        thread = threading.Thread(target=self.run_demo, args=(demo_type,))
        thread.daemon = True
        thread.start()
    
    def stop_demo(self):
        """Stop the current demo"""
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.update_stats(status="Stopped")
        self.log("Demo stopped by user", 'warning')
    
    def reset_demo(self):
        """Reset the demo"""
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
        # Clear log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Reset stats
        self.reset_stats()
        
        # Reset canvas
        self.draw_initial_state()
    
    def run_demo(self, demo_type):
        """Run the selected demo"""
        try:
            base_wait = float(self.base_wait_var.get())
            num_clients = int(self.num_clients_var.get())
            max_attempts = int(self.max_attempts_var.get())
            # Limit attempts to reasonable range
            max_attempts = max(1, min(10, max_attempts))
        except ValueError:
            self.log("Invalid parameters! Using defaults.", 'error')
            base_wait = 1
            num_clients = 100
            max_attempts = 5
        
        self.update_stats(clients=num_clients)
        
        if demo_type == "comparison":
            self.run_comparison_demo(base_wait, num_clients, max_attempts)
        elif demo_type == "no_backoff":
            self.run_single_demo(base_wait, num_clients, max_attempts, use_backoff=False)
        elif demo_type == "with_backoff":
            self.run_single_demo(base_wait, num_clients, max_attempts, use_backoff=True)
        elif demo_type == "with_jitter":
            self.run_jitter_demo(base_wait, num_clients, max_attempts)
        elif demo_type == "graph":
            self.run_graph_demo(base_wait, max_attempts)
        
        if self.is_running:
            self.root.after(0, self.demo_complete)
    
    def demo_complete(self):
        """Called when demo completes"""
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.update_stats(status="Completed")
        self.log("Demo completed!", 'success')
    
    def run_comparison_demo(self, base_wait, num_clients, max_attempts):
        """Run side-by-side comparison with server load indicators"""
        self.canvas.delete("all")
        speed = self.get_speed_multiplier()
        
        width = self.canvas.winfo_width() or 700
        height = self.canvas.winfo_height() or 450
        
        # ===== HEADERS =====
        self.canvas.create_rectangle(20, 10, width // 2 - 10, 50, fill=self.colors['error'], outline="")
        self.canvas.create_text(width // 4, 30, text="BAD: No Backoff", font=("Helvetica", 14, "bold"), fill="white")
        
        self.canvas.create_rectangle(width // 2 + 10, 10, width - 20, 50, fill=self.colors['success'], outline="")
        self.canvas.create_text(3 * width // 4, 30, text="GOOD: With Backoff", font=("Helvetica", 14, "bold"), fill="white")
        
        # Divider
        self.canvas.create_line(width // 2, 60, width // 2, height - 10, fill=self.colors['text_dim'], width=2, dash=(5, 5))
        
        # ===== CLIENT COUNT DISPLAY =====
        self.canvas.create_text(width // 4, 70, text=f"{num_clients} clients hitting server", font=("Helvetica", 10), fill=self.colors['warning'])
        self.canvas.create_text(3 * width // 4, 70, text=f"{num_clients} clients hitting server", font=("Helvetica", 10), fill=self.colors['warning'])
        
        # ===== SERVER LOAD BARS =====
        left_load_x = 40
        left_load_y = 90
        load_width = width // 2 - 80
        load_height = 25
        
        right_load_x = width // 2 + 40
        right_load_y = 90
        
        # Draw initial load bars
        self.canvas.create_rectangle(left_load_x, left_load_y, left_load_x + load_width, left_load_y + load_height,
                                     fill=self.colors['accent'], outline="", tags="left_load_bg")
        self.canvas.create_rectangle(right_load_x, right_load_y, right_load_x + load_width, right_load_y + load_height,
                                     fill=self.colors['accent'], outline="", tags="right_load_bg")
        
        # ===== RUN SIMULATION =====
        left_y = 135
        right_y = 135
        
        left_total_time = 0
        right_total_time = 0
        left_requests = 0
        right_requests = 0
        left_failures = 0
        right_failures = 0
        left_success = False
        right_success = False
        
        # Initial server load based on number of clients
        left_server_load = self.calculate_server_load(num_clients)
        right_server_load = self.calculate_server_load(num_clients)
        
        self.log(f"Server capacity: {self.server_capacity} clients", 'info')
        self.log(f"Current clients: {num_clients} -> Initial load: {left_server_load}%", 'info')
        
        for attempt in range(max_attempts):
            if not self.is_running:
                break
            
            # ----- LEFT SIDE: No backoff -----
            left_requests += 1
            left_server_load = min(100, left_server_load + 10)  # Load increases!
            
            # Update load bar
            self.canvas.delete("left_load")
            load_color = self.colors['error'] if left_server_load > 80 else self.colors['warning'] if left_server_load > 50 else self.colors['success']
            self.canvas.create_rectangle(
                left_load_x, left_load_y,
                left_load_x + (left_server_load / 100) * load_width, left_load_y + load_height,
                fill=load_color, outline="", tags="left_load"
            )
            self.canvas.create_text(
                left_load_x + load_width // 2, left_load_y + load_height // 2,
                text=f"Load: {left_server_load}%", font=("Helvetica", 9, "bold"), fill="white", tags="left_load"
            )
            
            # Calculate failure based on load
            failure_rate = self.calculate_failure_rate(num_clients, (left_server_load - 50) * 0.01)
            success_left = random.random() > failure_rate
            
            if success_left:
                left_success = True
                symbol = "SUCCESS"
                color = self.colors['success']
            else:
                left_failures += 1
                symbol = "FAILED"
                color = self.colors['error']
            
            self.canvas.create_rectangle(30, left_y, width // 2 - 20, left_y + 30, fill=self.colors['accent'], outline="")
            self.canvas.create_text(width // 4, left_y + 15, text=f"Try {attempt + 1}: {symbol} | Wait: 0s",
                                   font=("Helvetica", 10, "bold"), fill=color)
            
            self.log(f"[NO BACKOFF] Attempt {attempt + 1}: {symbol} (Load: {left_server_load}%)", 
                    'success' if success_left else 'error')
            
            left_y += 40
            
            # ----- RIGHT SIDE: With backoff -----
            right_requests += 1
            wait_right = base_wait * (2 ** attempt)
            right_total_time += wait_right
            
            # Show waiting
            self.canvas.create_text(
                3 * width // 4, right_y + 15,
                text=f"Waiting {wait_right}s...",
                font=("Helvetica", 10), fill=self.colors['warning'], tags="wait_anim"
            )
            self.canvas.update()
            
            # During wait, server load decreases!
            time.sleep(min(wait_right * 0.4, 2.0) * speed)
            right_server_load = max(20, right_server_load - 15)
            
            # Update right load bar
            self.canvas.delete("right_load")
            load_color = self.colors['error'] if right_server_load > 80 else self.colors['warning'] if right_server_load > 50 else self.colors['success']
            self.canvas.create_rectangle(
                right_load_x, right_load_y,
                right_load_x + (right_server_load / 100) * load_width, right_load_y + load_height,
                fill=load_color, outline="", tags="right_load"
            )
            self.canvas.create_text(
                right_load_x + load_width // 2, right_load_y + load_height // 2,
                text=f"Load: {right_server_load}%", font=("Helvetica", 9, "bold"), fill="white", tags="right_load"
            )
            
            self.canvas.delete("wait_anim")
            
            # Better success rate as server recovers
            failure_rate = self.calculate_failure_rate(num_clients, (right_server_load - 80) * 0.01)
            success_right = random.random() > failure_rate
            
            if success_right:
                right_success = True
                symbol = "SUCCESS"
                color = self.colors['success']
            else:
                right_failures += 1
                symbol = "FAILED"
                color = self.colors['error']
            
            self.canvas.create_rectangle(width // 2 + 20, right_y, width - 30, right_y + 30, fill=self.colors['accent'], outline="")
            self.canvas.create_text(3 * width // 4, right_y + 15, text=f"Try {attempt + 1}: {symbol} | Wait: {wait_right}s",
                                   font=("Helvetica", 10, "bold"), fill=color)
            
            self.log(f"[BACKOFF] Attempt {attempt + 1}: {symbol} (Load: {right_server_load}%)", 
                    'success' if success_right else 'error')
            
            right_y += 40
            
            # Update stats
            self.update_stats(
                requests=left_requests + right_requests,
                failures=left_failures + right_failures,
                total_wait=right_total_time,
                server_load=right_server_load
            )
            
            self.canvas.update()
            time.sleep(0.5 * speed)
            
            if right_success:
                break
        
        # ===== SUMMARY =====
        summary_y = height - 90
        
        # Left summary
        self.canvas.create_rectangle(30, summary_y, width // 2 - 20, summary_y + 70, fill=self.colors['error'], outline="")
        self.canvas.create_text(width // 4, summary_y + 15, text="Server Overwhelmed!", font=("Helvetica", 11, "bold"), fill="white")
        self.canvas.create_text(width // 4, summary_y + 35, text=f"Requests: {left_requests} | Wait: {left_total_time}s", font=("Helvetica", 9), fill="white")
        self.canvas.create_text(width // 4, summary_y + 55, text=f"Final Load: {left_server_load}%", font=("Helvetica", 9), fill="white")
        
        # Right summary
        right_color = self.colors['success'] if right_success else self.colors['error']
        self.canvas.create_rectangle(width // 2 + 20, summary_y, width - 30, summary_y + 70, fill=right_color, outline="")
        self.canvas.create_text(3 * width // 4, summary_y + 15, text="Server Recovered!" if right_success else "Still Failed", font=("Helvetica", 11, "bold"), fill="white")
        self.canvas.create_text(3 * width // 4, summary_y + 35, text=f"Requests: {right_requests} | Wait: {right_total_time}s", font=("Helvetica", 9), fill="white")
        self.canvas.create_text(3 * width // 4, summary_y + 55, text=f"Final Load: {right_server_load}%", font=("Helvetica", 9), fill="white")
    
    def run_single_demo(self, base_wait, num_clients, max_attempts, use_backoff):
        """Run single mode demo with server load visualization"""
        self.canvas.delete("all")
        speed = self.get_speed_multiplier()
        
        width = self.canvas.winfo_width() or 700
        height = self.canvas.winfo_height() or 450
        
        # Header
        if use_backoff:
            title = "WITH EXPONENTIAL BACKOFF"
            header_color = self.colors['success']
        else:
            title = "WITHOUT BACKOFF"
            header_color = self.colors['error']
        
        self.canvas.create_rectangle(50, 10, width - 50, 50, fill=header_color, outline="")
        self.canvas.create_text(width // 2, 30, text=title, font=("Helvetica", 16, "bold"), fill="white")
        
        # Client count
        self.canvas.create_text(width // 2, 65, text=f"{num_clients} clients hitting server (capacity: {self.server_capacity})",
                               font=("Helvetica", 10), fill=self.colors['warning'])
        
        # Server load bar
        load_x = 100
        load_y = 85
        load_width = width - 200
        load_height = 30
        
        self.canvas.create_text(60, load_y + 15, text="Server:", font=("Helvetica", 10, "bold"), fill=self.colors['text'])
        self.canvas.create_rectangle(load_x, load_y, load_x + load_width, load_y + load_height,
                                     fill=self.colors['accent'], outline="", tags="load_bg")
        
        bar_y = 135
        bar_width = 450
        bar_height = 40
        bar_x = (width - bar_width) // 2
        
        total_wait = 0
        total_requests = 0
        total_failures = 0
        server_load = self.calculate_server_load(num_clients)
        
        for attempt in range(max_attempts):
            if not self.is_running:
                break
            
            total_requests += 1
            wait_time = base_wait * (2 ** attempt) if use_backoff else 0.1
            total_wait += wait_time
            
            # Update server load
            if use_backoff:
                server_load = max(20, server_load - 15)
            else:
                server_load = min(100, server_load + 10)
            
            # Draw load bar
            self.canvas.delete("server_load")
            load_color = self.colors['error'] if server_load > 80 else self.colors['warning'] if server_load > 50 else self.colors['success']
            self.canvas.create_rectangle(
                load_x, load_y, load_x + (server_load / 100) * load_width, load_y + load_height,
                fill=load_color, outline="", tags="server_load"
            )
            self.canvas.create_text(
                load_x + load_width // 2, load_y + load_height // 2,
                text=f"Load: {server_load}%", font=("Helvetica", 10, "bold"), fill="white", tags="server_load"
            )
            
            # Attempt label
            self.canvas.create_text(bar_x - 30, bar_y + bar_height // 2, text=f"#{attempt + 1}",
                                   font=("Helvetica", 12, "bold"), fill=self.colors['text'])
            
            # Progress bar background
            self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                                        fill=self.colors['accent'], outline="")
            
            # Animate progress
            steps = 20
            for i in range(steps + 1):
                if not self.is_running:
                    break
                
                self.canvas.delete("progress")
                self.canvas.delete("wait_text")
                
                progress = (i / steps) * bar_width
                self.canvas.create_rectangle(bar_x, bar_y, bar_x + progress, bar_y + bar_height,
                                            fill=self.colors['warning'], outline="", tags="progress")
                
                current_wait = wait_time * (i / steps)
                self.canvas.create_text(width // 2, bar_y + bar_height // 2,
                                       text=f"Waiting: {current_wait:.1f}s / {wait_time}s",
                                       font=("Helvetica", 11, "bold"), fill=self.colors['text'], tags="wait_text")
                
                self.canvas.update()
                time.sleep(min(wait_time / steps, 0.15) * speed)
            
            # Check success based on load
            if use_backoff:
                failure_rate = self.calculate_failure_rate(num_clients, (server_load - 80) * 0.01)
            else:
                failure_rate = self.calculate_failure_rate(num_clients, (server_load - 50) * 0.01)
            
            success = random.random() > failure_rate
            
            # Show result
            self.canvas.delete("progress")
            self.canvas.delete("wait_text")
            
            result_color = self.colors['success'] if success else self.colors['error']
            self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                                        fill=result_color, outline="")
            
            result_text = "SUCCESS!" if success else "FAILED"
            if not success:
                total_failures += 1
            
            self.canvas.create_text(width // 2, bar_y + bar_height // 2,
                                   text=f"{result_text} (waited {wait_time}s)",
                                   font=("Helvetica", 12, "bold"), fill="white")
            
            self.log(f"Attempt {attempt + 1}: {result_text} (waited {wait_time}s, load: {server_load}%)",
                    'success' if success else 'error')
            
            self.update_stats(
                requests=total_requests,
                failures=total_failures,
                total_wait=total_wait,
                server_load=server_load
            )
            
            bar_y += 55
            
            if success:
                self.canvas.create_text(width // 2, bar_y + 20, text="Request completed successfully!",
                                       font=("Helvetica", 14, "bold"), fill=self.colors['success'])
                break
            
            time.sleep(0.4 * speed)
        
        # Total time
        self.canvas.create_text(width // 2, height - 30, text=f"Total waiting time: {total_wait}s",
                               font=("Helvetica", 12), fill=self.colors['text_dim'])
    
    def run_jitter_demo(self, base_wait, num_clients, max_attempts):
        """Demo showing jitter effect"""
        self.canvas.delete("all")
        speed = self.get_speed_multiplier()
        
        width = self.canvas.winfo_width() or 700
        height = self.canvas.winfo_height() or 450
        
        # Header
        self.canvas.create_rectangle(50, 10, width - 50, 50, fill=self.colors['purple'], outline="")
        self.canvas.create_text(width // 2, 30, text="EXPONENTIAL BACKOFF + JITTER",
                               font=("Helvetica", 16, "bold"), fill="white")
        
        # Explanation
        client_word = "client" if num_clients == 1 else "clients"
        self.canvas.create_text(width // 2, 70, text=f"Problem: {num_clients} {client_word} ALL retry at the exact same time!",
                               font=("Helvetica", 10), fill=self.colors['error'])
        self.canvas.create_text(width // 2, 90, text="Solution: Add random delay to spread out the retries",
                               font=("Helvetica", 10), fill=self.colors['success'])
        
        # Show up to 4 sample clients (or fewer if num_clients is smaller)
        display_count = min(num_clients, 4)
        sample_labels = ['A', 'B', 'C', 'D'][:display_count]
        clients = [f"Sample {label}" for label in sample_labels]
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12'][:display_count]
        
        bar_y = 130
        bar_width = 400
        bar_height = 30
        bar_x = 180  # Back to original position
        
        if num_clients <= 4:
            self.log(f"Simulating {num_clients} client(s)...", 'info')
        else:
            self.log(f"Simulating {num_clients} clients (showing 4 samples)...", 'info')
        
        # Use max_attempts for number of rounds (limit to reasonable display)
        num_rounds = min(max_attempts, 5)
        
        for round_num in range(num_rounds):
            if not self.is_running:
                break
            
            # Round label
            self.canvas.delete("round_label")
            base = base_wait * (2 ** round_num)
            self.canvas.create_text(width // 2, 115, text=f"Round {round_num + 1} | Base wait: {base}s",
                                   font=("Helvetica", 11, "bold"), fill=self.colors['warning'], tags="round_label")
            
            self.canvas.delete("client_bars")
            
            for i, (client, color) in enumerate(zip(clients, colors)):
                if not self.is_running:
                    break
                
                y = bar_y + i * 50
                
                jitter = random.uniform(0, base * 0.5)
                total_wait = base + jitter
                
                # Client label
                self.canvas.create_text(100, y + bar_height // 2, text=client,
                                       font=("Helvetica", 10, "bold"), fill=color, tags="client_bars")
                
                # Background
                self.canvas.create_rectangle(bar_x, y, bar_x + bar_width, y + bar_height,
                                            fill=self.colors['accent'], outline="", tags="client_bars")
                
                # Progress bar
                max_wait = base * 1.6
                progress = min((total_wait / max_wait) * bar_width, bar_width)
                self.canvas.create_rectangle(bar_x, y, bar_x + progress, y + bar_height,
                                            fill=color, outline="", tags="client_bars")
                
                # Time label
                self.canvas.create_text(bar_x + bar_width + 60, y + bar_height // 2,
                                       text=f"{total_wait:.2f}s", font=("Helvetica", 10, "bold"),
                                       fill=self.colors['text'], tags="client_bars")
                
                self.log(f"{client}: {total_wait:.2f}s (base {base}s + jitter {jitter:.2f}s)", 'info')
            
            self.update_stats(requests=display_count * (round_num + 1))
            self.canvas.update()
            time.sleep(1.5 * speed)
        
        # Final message
        self.canvas.create_rectangle(50, height - 80, width - 50, height - 20, fill=self.colors['success'], outline="")
        self.canvas.create_text(width // 2, height - 60, text=f"Jitter spreads {num_clients} {client_word} over time!",
                               font=("Helvetica", 12, "bold"), fill="white")
        self.canvas.create_text(width // 2, height - 40, text="Result: Less server congestion, better performance",
                               font=("Helvetica", 10), fill="white")
    
    def run_graph_demo(self, base_wait, max_attempts):
        """Show exponential growth graph"""
        self.canvas.delete("all")
        speed = self.get_speed_multiplier()
        
        width = self.canvas.winfo_width() or 700
        height = self.canvas.winfo_height() or 450
        
        # Header
        self.canvas.create_rectangle(50, 10, width - 50, 50, fill=self.colors['blue'], outline="")
        self.canvas.create_text(width // 2, 30, text="EXPONENTIAL GROWTH VISUALIZATION",
                               font=("Helvetica", 16, "bold"), fill="white")
        
        # Graph area
        graph_x = 100
        graph_y = 80
        graph_width = width - 200
        graph_height = height - 180
        
        # Draw axes
        self.canvas.create_line(graph_x, graph_y + graph_height, graph_x + graph_width, graph_y + graph_height,
                               fill=self.colors['text'], width=2)  # X axis
        self.canvas.create_line(graph_x, graph_y, graph_x, graph_y + graph_height,
                               fill=self.colors['text'], width=2)  # Y axis
        
        # Labels
        self.canvas.create_text(graph_x + graph_width // 2, graph_y + graph_height + 30,
                               text="Attempt Number", font=("Helvetica", 10), fill=self.colors['text'])
        self.canvas.create_text(graph_x - 40, graph_y + graph_height // 2,
                               text="Wait\nTime\n(s)", font=("Helvetica", 10), fill=self.colors['text'])
        
        # Calculate points using max_attempts
        max_wait = base_wait * (2 ** (max_attempts - 1))
        
        points = []
        for i in range(max_attempts):
            wait = base_wait * (2 ** i)
            x = graph_x + (i / (max_attempts - 1)) * graph_width if max_attempts > 1 else graph_x
            y = graph_y + graph_height - (wait / max_wait) * graph_height
            points.append((x, y, wait, i + 1))
        
        # Draw grid lines and labels
        for i in range(max_attempts):
            x = graph_x + (i / (max_attempts - 1)) * graph_width
            self.canvas.create_line(x, graph_y + graph_height, x, graph_y + graph_height + 5,
                                   fill=self.colors['text'])
            self.canvas.create_text(x, graph_y + graph_height + 15, text=str(i + 1),
                                   font=("Helvetica", 9), fill=self.colors['text'])
        
        # Animate the graph
        self.log("Showing exponential growth...", 'info')
        
        prev_point = None
        for i, (x, y, wait, attempt) in enumerate(points):
            if not self.is_running:
                break
            
            # Draw line from previous point
            if prev_point:
                self.canvas.create_line(prev_point[0], prev_point[1], x, y,
                                       fill=self.colors['warning'], width=3)
            
            # Draw point
            self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill=self.colors['error'], outline="")
            
            # Draw label
            self.canvas.create_text(x, y - 20, text=f"{wait}s",
                                   font=("Helvetica", 10, "bold"), fill=self.colors['text'])
            
            # Update info box
            self.canvas.delete("info_box")
            info_x = width - 150
            info_y = 100
            self.canvas.create_rectangle(info_x - 60, info_y, info_x + 60, info_y + 80,
                                        fill=self.colors['card'], outline=self.colors['accent'], tags="info_box")
            self.canvas.create_text(info_x, info_y + 15, text=f"Attempt: {attempt}",
                                   font=("Helvetica", 10), fill=self.colors['text'], tags="info_box")
            self.canvas.create_text(info_x, info_y + 35, text=f"Wait: {wait}s",
                                   font=("Helvetica", 12, "bold"), fill=self.colors['warning'], tags="info_box")
            self.canvas.create_text(info_x, info_y + 55, text=f"= {base_wait} x 2^{i}",
                                   font=("Helvetica", 9), fill=self.colors['text_dim'], tags="info_box")
            
            self.log(f"Attempt {attempt}: wait = {base_wait} x 2^{i} = {wait}s", 'info')
            self.update_stats(requests=attempt, total_wait=sum(p[2] for p in points[:i+1]))
            
            prev_point = (x, y)
            self.canvas.update()
            time.sleep(1.0 * speed)
        
        # Summary
        total = sum(p[2] for p in points)
        self.canvas.create_rectangle(50, height - 70, width - 50, height - 20,
                                     fill=self.colors['accent'], outline="")
        self.canvas.create_text(width // 2, height - 55, text="Key Insight: Wait time DOUBLES with each attempt",
                               font=("Helvetica", 11, "bold"), fill=self.colors['warning'])
        self.canvas.create_text(width // 2, height - 35, text=f"Total wait after {max_attempts} attempts: {total}s",
                               font=("Helvetica", 10), fill=self.colors['text'])


def main():
    root = tk.Tk()
    app = ExponentialBackoffDemo(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 1100) // 2
    y = (root.winfo_screenheight() - 800) // 2
    root.geometry(f"1100x800+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()