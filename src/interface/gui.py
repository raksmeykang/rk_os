"""
gui.py - Graphical user interface for RK-OS system management  
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class GraphicalUserInterface:
    """
    Graphical user interface for RK-OS management and monitoring
    """
    
    def __init__(self):
        """Initialize the GUI"""
        self.root = None
        self.engine = None
        
        logger.info("Graphical User Interface initialized")
        
    def create_main_window(self) -> tk.Tk:
        """
        Create main application window
        
        Returns:
            Tk: Main window instance
        """
        try:
            # Create main window
            self.root = tk.Tk()
            self.root.title("RK-OS - Logical Operating System")
            self.root.geometry("800x600")
            
            # Configure styles
            style = ttk.Style()
            style.theme_use('clam')
            
            # Set up menu bar
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)
            
            # File menu  
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="Exit", command=self._on_exit)
            
            # System menu
            system_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="System", menu=system_menu) 
            system_menu.add_command(label="Start", command=self.start_system)
            system_menu.add_command(label="Stop", command=self.stop_system)
            system_menu.add_separator()
            system_menu.add_command(label="Status", command=self.show_status)
            
            # Tools menu
            tools_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Tools", menu=tools_menu)
            tools_menu.add_command(label="Run Tests", command=self.run_tests)
            tools_menu.add_command(label="View Metrics", command=self.view_metrics)
            
            # Create main content frame
            self._create_main_content()
            
            return self.root
            
        except Exception as e:
            logger.error(f"Failed to create main window: {str(e)}")
            raise
    
    def _create_main_content(self):
        """Create the main content area"""
        try:
            # Main notebook for tabs
            notebook = ttk.Notebook(self.root)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # System Status Tab
            status_frame = ttk.Frame(notebook)
            notebook.add(status_frame, text="System Status")
            self._create_status_tab(status_frame)
            
            # Performance Metrics Tab  
            metrics_frame = ttk.Frame(notebook)
            notebook.add(metrics_frame, text="Performance Metrics")
            self._create_metrics_tab(metrics_frame)
            
            # Operations Tab
            operations_frame = ttk.Frame(notebook)
            notebook.add(operations_frame, text="Operations") 
            self._create_operations_tab(operations_frame)
            
        except Exception as e:
            logger.error(f"Failed to create main content: {str(e)}")
    
    def _create_status_tab(self, parent):
        """Create system status tab"""
        try:
            # Status display
            status_label = ttk.Label(parent, text="System Status", font=('Arial', 14, 'bold'))
            status_label.pack(pady=10)
            
            self.status_text = tk.Text(parent, height=15, width=70)
            scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.status_text.yview)
            self.status_text.configure(yscrollcommand=scrollbar.set)
            
            # Pack with grid
            self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5) 
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=5)
            
            # Control buttons  
            button_frame = ttk.Frame(parent)
            button_frame.pack(pady=10)
            
            start_btn = ttk.Button(button_frame, text="Start System", command=self.start_system)
            start_btn.pack(side=tk.LEFT, padx=5)
            
            stop_btn = ttk.Button(button_frame, text="Stop System", command=self.stop_system)  
            stop_btn.pack(side=tk.LEFT, padx=5)
            
            refresh_btn = ttk.Button(button_frame, text="Refresh Status", command=self.refresh_status)
            refresh_btn.pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            logger.error(f"Failed to create status tab: {str(e)}")
    
    def _create_metrics_tab(self, parent):
        """Create performance metrics tab"""
        try:
            # Metrics display
            metrics_label = ttk.Label(parent, text="Performance Metrics", font=('Arial', 14, 'bold'))
            metrics_label.pack(pady=10)
            
            self.metrics_text = tk.Text(parent, height=20, width=70)
            scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.metrics_text.yview)
            self.metrics_text.configure(yscrollcommand=scrollbar.set) 
            
            # Pack with grid
            self.metrics_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=5)
            
        except Exception as e:
            logger.error(f"Failed to create metrics tab: {str(e)}")
    
    def _create_operations_tab(self, parent):
        """Create operations tab"""
        try:
            # Operations panel
            op_label = ttk.Label(parent, text="Logical Operations", font=('Arial', 14, 'bold'))
            op_label.pack(pady=10)
            
            # Input frame for operations  
            input_frame = ttk.Frame(parent)
            input_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # AND operation
            and_frame = ttk.Frame(input_frame)
            and_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(and_frame, text="AND:").pack(side=tk.LEFT)
            self.and_operand1 = tk.StringVar()
            self.and_operand2 = tk.StringVar()
            
            entry1 = ttk.Entry(and_frame, textvariable=self.and_operand1, width=5) 
            entry1.pack(side=tk.LEFT, padx=5)
            ttk.Label(and_frame, text="AND").pack(side=tk.LEFT)
            entry2 = ttk.Entry(and_frame, textvariable=self.and_operand2, width=5)
            entry2.pack(side=tk.LEFT, padx=5)
            
            and_btn = ttk.Button(input_frame, text="Evaluate", command=self.evaluate_and_operation)  
            and_btn.pack(side=tk.RIGHT, padx=5)
            
            # Result display
            self.result_text = tk.Text(parent, height=10, width=70)
            scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.result_text.yview)
            self.result_text.configure(yscrollcommand=scrollbar.set)
            
            # Pack with grid
            self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5) 
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=5)
            
        except Exception as e:
            logger.error(f"Failed to create operations tab: {str(e)}")
    
    def start_system(self):
        """Start the RK-OS system"""
        try:
            if not self.engine:
                # Initialize the engine in a separate thread
                threading.Thread(target=self._initialize_engine, daemon=True).start()
                
            messagebox.showinfo("RK-OS", "System starting...")
            
        except Exception as e:
            logger.error(f"Failed to start system: {str(e)}")
            messagebox.showerror("Error", f"Failed to start system: {str(e)}")
    
    def stop_system(self):
        """Stop the RK-OS system"""
        try:
            if self.engine:
                # In a real implementation, we would shut down the engine
                messagebox.showinfo("RK-OS", "System stopping...")
                self.engine = None
                
        except Exception as e:
            logger.error(f"Failed to stop system: {str(e)}")
            messagebox.showerror("Error", f"Failed to stop system: {str(e)}")
    
    def _initialize_engine(self):
        """Initialize the RK-OS engine in background thread"""
        try:
            from src.core.engine import initialize_rkos
            
            self.engine = initialize_rkos()
            
            if self.engine:
                # Update GUI with status
                self.root.after(0, lambda: self._update_status_display("System initialized successfully"))
                
            else:
                raise Exception("Failed to initialize RK-OS engine")
                
        except Exception as e:
            logger.error(f"Engine initialization failed: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Engine initialization failed: {str(e)}"))
    
    def refresh_status(self):
        """Refresh system status"""
        try:
            if self.engine:
                # Get current metrics
                threading.Thread(target=self._get_system_metrics, daemon=True).start()
                
            else:
                self.status_text.delete(1.0, tk.END)
                self.status_text.insert(tk.END, "System not initialized")
                
        except Exception as e:
            logger.error(f"Failed to refresh status: {str(e)}")
    
    def _get_system_metrics(self):
        """Get system metrics in background thread"""
        try:
            if self.engine:
                metrics = self.engine.get_system_metrics()
                
                # Update GUI with results
                self.root.after(0, lambda: self._display_metrics(metrics))
                
        except Exception as e:
            logger.error(f"Failed to get metrics: {str(e)}")
    
    def _display_metrics(self, metrics):
        """Display metrics in the GUI"""
        try:
            self.metrics_text.delete(1.0, tk.END)
            
            if 'system_status' in metrics:
                self.metrics_text.insert(tk.END, f"Status: {metrics['system_status']}\n")
                
            if 'uptime_seconds' in metrics:
                self.metrics_text.insert(tk.END, f"Uptime: {metrics['uptime_seconds']:.2f} seconds\n")
                
            if 'metrics' in metrics and 'system_stats' in metrics['metrics']:
                stats = metrics['metrics']['system_stats']
                self.metrics_text.insert(tk.END, "\nSystem Statistics:\n")
                for key, value in stats.items():
                    self.metrics_text.insert(tk.END, f"  {key}: {value}\n")
                    
        except Exception as e:
            logger.error(f"Failed to display metrics: {str(e)}")
    
    def show_status(self):
        """Show system status dialog"""
        try:
            if not self.engine:
                messagebox.showwarning("RK-OS", "System not initialized") 
                return
                
            # Show current status
            status = self.engine.get_system_metrics()
            
            status_msg = f"System Status: {status['system_status']}\n"
            status_msg += f"Uptime: {status['uptime_seconds']:.2f} seconds\n"
            
            messagebox.showinfo("RK-OS - System Status", status_msg)
            
        except Exception as e:
            logger.error(f"Failed to show status: {str(e)}")
    
    def run_tests(self):
        """Run system tests"""
        try:
            # This would actually run the test suite
            messagebox.showinfo("RK-OS", "Running system tests...")
            
        except Exception as e:
            logger.error(f"Failed to run tests: {str(e)}")
            messagebox.showerror("Error", f"Failed to run tests: {str(e)}")
    
    def view_metrics(self):
        """View performance metrics"""
        try:
            self.refresh_status()
            messagebox.showinfo("RK-OS", "Metrics refreshed")
            
        except Exception as e:
            logger.error(f"Failed to view metrics: {str(e)}")
            messagebox.showerror("Error", f"Failed to view metrics: {str(e)}")
    
    def evaluate_and_operation(self):
        """Evaluate AND operation"""
        try:
            operand1 = self.and_operand1.get()
            operand2 = self.and_operand2.get()
            
            if not operand1 or not operand2:
                messagebox.showwarning("RK-OS", "Please enter both operands") 
                return
                
            # Simple evaluation for demonstration
            result = f"{operand1} AND {operand2} = {bool(operand1 == 'True' and operand2 == 'True')}"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result) 
            
        except Exception as e:
            logger.error(f"Failed to evaluate operation: {str(e)}")
    
    def _update_status_display(self, message):
        """Update status display in GUI"""
        try:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"{message}\n")
            
        except Exception as e:
            logger.error(f"Failed to update status: {str(e)}")
    
    def _on_exit(self):
        """Handle exit command"""
        try:
            if messagebox.askokcancel("RK-OS", "Do you want to quit?"):
                self.root.destroy()
                
        except Exception as e:
            logger.error(f"Error during exit: {str(e)}")
            self.root.destroy()

# Main GUI instance
gui = GraphicalUserInterface()

def main():
    """Main function for GUI execution"""
    try:
        # Create and run the GUI
        window = gui.create_main_window()
        
        # Start event loop  
        window.mainloop()
        
    except Exception as e:
        logger.error(f"GUI failed to start: {str(e)}")
        print(f"Failed to start GUI: {str(e)}")

if __name__ == "__main__":
    main()
