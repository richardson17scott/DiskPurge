import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Import your original backend functions from your analyzer package
from analyzer.core import directory_scanner, largest_files

# Set the overall look and feel
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DiskPurgeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("DiskPurge - Storage Analyzer")
        self.geometry("700x550") # Made slightly taller for the new stat label
        self.selected_path = ""

        # --- UI ELEMENTS ---
        
        # 1. Title Banner
        self.title_label = ctk.CTkLabel(self, text="💾 DISKPURGE DASHBOARD", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(pady=20)

        # 2. Folder Selection Frame
        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.pack(pady=10, fill="x", padx=20)

        self.path_entry = ctk.CTkEntry(self.selection_frame, placeholder_text="No folder selected...", width=450)
        self.path_entry.pack(side="left", padx=10, pady=10)

        self.browse_btn = ctk.CTkButton(self.selection_frame, text="Browse", command=self.browse_folder, width=100)
        self.browse_btn.pack(side="right", padx=10, pady=10)

        # 3. Scan Settings Frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(pady=10, fill="x", padx=20)
        
        self.limit_label = ctk.CTkLabel(self.settings_frame, text="Show top X largest files:")
        self.limit_label.pack(side="left", padx=10, pady=10)
        
        self.limit_entry = ctk.CTkEntry(self.settings_frame, width=60)
        self.limit_entry.insert(0, "10") 
        self.limit_entry.pack(side="left", padx=5, pady=10)

        # 4. Action Button
        self.scan_btn = ctk.CTkButton(self, text="START SCAN", fg_color="#D35400", hover_color="#E67E22", command=self.start_scan)
        self.scan_btn.pack(pady=15)

        # ⭐ NEW FEATURE: Total Storage Display Label
        self.stats_label = ctk.CTkLabel(
            self, 
            text="Total Storage Used: --", 
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#3498DB" # Nice bright blue accent color
        )
        self.stats_label.pack(pady=5)

        # 5. Results Box
        self.results_box = ctk.CTkTextbox(self, width=660, height=220, font=ctk.CTkFont(family="Courier", size=12))
        self.results_box.pack(pady=10, padx=20)
        self.results_box.insert("0.0", "Select a folder and click 'START SCAN' to view details...")

    # --- BUTTON FUNCTIONS ---

    def browse_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_path = directory
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, directory)

    def start_scan(self):
        target_dir = self.path_entry.get().strip()
        
        if not target_dir or not os.path.exists(target_dir):
            messagebox.showerror("Error", "Please select a valid directory path first!")
            return

        try:
            limit = int(self.limit_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the file limit.")
            return

        # UI Reset
        self.results_box.delete("1.0", ctk.END)
        self.results_box.insert(ctk.END, f"Scanning: {target_dir}...\n\n")
        self.stats_label.configure(text="Total Storage Used: Calculating...")
        self.update_idletasks() 

        try:
            # Consume your generator to analyze files
            all_files = list(directory_scanner(target_dir)) 
            
            # ⭐ CALCULATE TOTAL SIZE
            # Sums up the size of every file object caught in the directory scan
            total_bytes = sum(size for _, size in all_files)
            
            # Convert total bytes to human-readable text
            if total_bytes > 1024**3:
                total_str = f"{total_bytes / (1024**3):.2f} GB"
            else:
                total_str = f"{total_bytes / (1024**2):.2f} MB"
            
            # Update our brand new label dynamically!
            self.stats_label.configure(text=f"Total Storage Used: {total_str}")

            # Grab top heavy-hitters using your original function
            top_files = largest_files(all_files, limit)

            if not top_files:
                self.results_box.insert(ctk.END, "No files found inside the selected directory.")
                return

            # Print layout inside the custom text box
            self.results_box.insert(ctk.END, f"{'FILE PATH':<50} | {'SIZE'}\n")
            self.results_box.insert(ctk.END, "-" * 65 + "\n")
            
            for file_path, size_bytes in top_files:
                if size_bytes > 1024**3:
                    file_size_str = f"{size_bytes / (1024**3):.2f} GB"
                else:
                    file_size_str = f"{size_bytes / (1024**2):.2f} MB"
                    
                self.results_box.insert(ctk.END, f"{file_path:<50} | {file_size_str}\n")

        except Exception as e:
            messagebox.showerror("Scan Failure", f"An error occurred: {str(e)}")
            self.stats_label.configure(text="Total Storage Used: Error")

if __name__ == "__main__":
    app = DiskPurgeGUI()
    app.mainloop()