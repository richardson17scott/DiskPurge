import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

from analyzer.core import directory_scanner, largest_files

# --- GLOSSY MODERN STYLING CONFIGURATION ---
ctk.set_appearance_mode("Dark")

# Premium Cyber-Gloss Palette
BG_PITCH_BLACK = "#000000"      # True black backdrop
PANEL_GLOSS_DARK = "#0B0B0E"    # Deep obsidian glass panel
BORDER_GLOSS_SLATE = "#1F2937"  # Metallic/slate subtle border outline
ACCENT_ELECTRIC_BLUE = "#00D2FF"# High-tech glowing neon blue
BUTTON_SCAN_BLUE = "#0052D4"    # Deep glossy sapphire blue
BUTTON_SCAN_HOVER = "#4364F7"   # Glowing hover state
BUTTON_DELETE_RED = "#8A2387"   # Deep metallic magenta/red 
BUTTON_DELETE_HOVER = "#E94057" # Vibrant ruby hover

class DiskPurgeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DiskPurge - Storage Analyzer")
        self.geometry("750x620")
        
        # Inject true black into the main window window
        self.configure(fg_color=BG_PITCH_BLACK)
        
        self.file_checkboxes = {} 
        self.scanned_files_list = []

        # --- UI ELEMENTS ---
        
        # 1. Title Banner (Neon Glow effect using font weight and accent colors)
        self.title_label = ctk.CTkLabel(
            self, 
            text="💾  DiskPurge", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=ACCENT_ELECTRIC_BLUE
        )
        self.title_label.pack(pady=20)

        # 2. Folder Selection Frame (Glossy Panel with Slate Border)
        self.selection_frame = ctk.CTkFrame(
            self, fg_color=PANEL_GLOSS_DARK, border_color=BORDER_GLOSS_SLATE, border_width=1
        )
        self.selection_frame.pack(pady=8, fill="x", padx=25)

        self.path_entry = ctk.CTkEntry(
            self.selection_frame, placeholder_text="No folder selected...", 
            width=480, fg_color="#16161D", border_color=BORDER_GLOSS_SLATE, text_color="#FFFFFF"
        )
        self.path_entry.pack(side="left", padx=15, pady=15)

        self.browse_btn = ctk.CTkButton(
            self.selection_frame, text="Browse", command=self.browse_folder, 
            width=110, fg_color="#1F2937", hover_color="#374151", border_color=BORDER_GLOSS_SLATE, border_width=1
        )
        self.browse_btn.pack(side="right", padx=15, pady=15)

        # 3. Scan Settings Frame
        self.settings_frame = ctk.CTkFrame(
            self, fg_color=PANEL_GLOSS_DARK, border_color=BORDER_GLOSS_SLATE, border_width=1
        )
        self.settings_frame.pack(pady=8, fill="x", padx=25)
        
        self.limit_label = ctk.CTkLabel(self.settings_frame, text="Show top X largest files:", text_color="#A0AEC0")
        self.limit_label.pack(side="left", padx=15, pady=12)
        
        self.limit_entry = ctk.CTkEntry(
            self.settings_frame, width=70, fg_color="#16161D", border_color=BORDER_GLOSS_SLATE, text_color="#FFFFFF"
        )
        self.limit_entry.insert(0, "10") 
        self.limit_entry.pack(side="left", padx=5, pady=12)

        # 4. Control Buttons Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=15)

        self.scan_btn = ctk.CTkButton(
            self.button_frame, text="START SCAN", 
            fg_color=BUTTON_SCAN_BLUE, hover_color=BUTTON_SCAN_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"), width=150, height=38
        )
        self.scan_btn.configure(command=self.start_scan)
        self.scan_btn.pack(side="left", padx=12)

        self.purge_btn = ctk.CTkButton(
            self.button_frame, text="DELETE SELECTED", 
            fg_color=BUTTON_DELETE_RED, hover_color=BUTTON_DELETE_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"), width=150, height=38
        )

        # 5. Storage Tracker Info
        self.stats_label = ctk.CTkLabel(
            self, text="Total Storage Used: --", 
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
            text_color="#A0AEC0"
        )
        self.stats_label.pack(pady=8)

        # 6. Scrollable Container Frame (True Obsidian Look)
        self.results_frame = ctk.CTkScrollableFrame(
            self, width=680, height=260, 
            fg_color=PANEL_GLOSS_DARK, border_color=BORDER_GLOSS_SLATE, border_width=1
        )
        self.results_frame.pack(pady=10, padx=25, fill="both", expand=True)

    # --- CORE FUNCTIONS ---

    def browse_folder(self):
        directory = filedialog.askdirectory()
        if directory:
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

        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.file_checkboxes.clear()
        self.purge_btn.pack_forget()

        self.stats_label.configure(text="Total Storage Used: Calculating...", text_color=ACCENT_ELECTRIC_BLUE)
        self.update_idletasks() 

        try:
            self.scanned_files_list = list(directory_scanner(target_dir)) 
            total_bytes = sum(size for _, size in self.scanned_files_list)
            
            if total_bytes > 1024**3:
                total_str = f"{total_bytes / (1024**3):.2f} GB"
            else:
                total_str = f"{total_bytes / (1024**2):.2f} MB"
            
            self.stats_label.configure(text=f"Total Storage Used: {total_str}", text_color=ACCENT_ELECTRIC_BLUE)

            top_files = largest_files(self.scanned_files_list, limit)

            if not top_files:
                no_files_lbl = ctk.CTkLabel(self.results_frame, text="No heavy files found inside this directory.", text_color="#718096")
                no_files_lbl.pack(pady=20)
                return

            for file_path, size_bytes in top_files:
                if size_bytes > 1024**3:
                    file_size_str = f"[{size_bytes / (1024**3):.2f} GB]"
                else:
                    file_size_str = f"[{size_bytes / (1024**2):.2f} MB]"

                display_text = f"  {file_size_str:<12}  {file_path}"
                
                chk_var = ctk.StringVar(value="off")
                
                # Checkbox tailored to match modern sleek look
                cb = ctk.CTkCheckBox(
                    self.results_frame, text=display_text, variable=chk_var, 
                    onvalue="on", offvalue="off",
                    font=ctk.CTkFont(family="Segoe UI", size=13),
                    text_color="#E2E8F0", 
                    fg_color=BUTTON_SCAN_BLUE,       # This colors the box when checked!
                    hover_color=ACCENT_ELECTRIC_BLUE
                )
                cb.pack(anchor="w", pady=8, padx=15)
                
                self.file_checkboxes[file_path] = chk_var

            self.purge_btn.pack(side="left", padx=12)

        except Exception as e:
            messagebox.showerror("Scan Failure", f"An error occurred: {str(e)}")
            self.stats_label.configure(text="Total Storage Used: Error", text_color="#E53E3E")

    def delete_selected_files(self):
        targets_to_delete = [path for path, var in self.file_checkboxes.items() if var.get() == "on"]

        if not targets_to_delete:
            messagebox.showinfo("Attention", "No targets selected. Check some boxes first!")
            return

        confirm = messagebox.askyesno("Confirm Destruction", f"Are you sure you want to permanently delete these {len(targets_to_delete)} files?\nThis action cannot be undone.")
        
        if confirm:
            deleted_count = 0
            for file_path in targets_to_delete:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    messagebox.showerror("Error Removing File", f"Could not remove:\n{file_path}\nError: {e}")
            
            messagebox.showinfo("Success", f"Successfully expunged {deleted_count} files from your system.")
            self.start_scan()

if __name__ == "__main__":
    app = DiskPurgeGUI()
    app.mainloop()