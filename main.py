import subprocess
import customtkinter as ctk
import os
import re
from os import path
from PIL import Image, ImageTk
from pathlib import Path


from custom_dialog import CustomDialog
from new_connection_form import NewConnectionForm
from confirm_delete import ConfirmationDialog
from generate_keys import GenerateKeys

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class WireGuardFrontend(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WireGuard")
        self.geometry("450x400")
        self.resizable(width=False,height=False)

        # Center the window
        self.center_window()

        # Get the absolute path to the icon
        icon_image = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets/wireguard_logo.png'))

        # Load the image and convert it to a Tkinter-compatible format
        icon = Image.open(icon_image)
        icon_photo = ImageTk.PhotoImage(icon)

        # Set the icon for the window
        self.iconphoto(False, icon_photo)

        # Configure grid layout
        self.columnconfigure(0, weight=1)

        #image_path = "assets/wireguard_logo.png" 
        image_path = path.abspath(path.join(path.dirname(__file__), 'assets/wireguard_logo.png'))
        image = ctk.CTkImage(light_image=Image.open(image_path), size=(100, 100))  

        # Create a label to display the image
        self.image_label = ctk.CTkLabel(self, image=image, text="")  
        self.image_label.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        # Status label
        self.status_label = ctk.CTkLabel(self, text="WireGuard Status: Disconnected")
        self.status_label.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        # network stats
        self.transfer_label = ctk.CTkLabel(self, text="Data Transfer: No data available")
        self.transfer_label.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        self.check_status()

        # Select Config File
        self.config_files_dropdown = ctk.CTkOptionMenu(self, values=[], command=self.on_config_selected)
        self.config_files_dropdown.grid(row=3, column=0, pady=5, padx=5)
        
        # Load all WireGuard .conf files into the dropdown
        self.load_config_files()

        # Delete Connection button
        self.delete_connection_button = ctk.CTkButton(self, text="Delete Config", fg_color="red", hover_color="darkred", command=self.delete_config)
        self.delete_connection_button.grid(row=5, column=0, pady=30, padx=5)

        # Generate Keys
        self.generate_keys = ctk.CTkButton(self, text="Generate Keys", command=self.generate_keys)
        self.generate_keys.grid(row=6, column=0, pady=5, padx=5)

        # New Connection button
        self.new_connection_button = ctk.CTkButton(self, text="Create New Connection", command=self.open_new_connection_form)
        self.new_connection_button.grid(row=7, column=0, pady=5, padx=5)

    def center_window(self):
        """Center the window on the screen."""
        window_width = 400
        window_height = 450

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        # Set the geometry
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    def refresh_buttons(self):
        # Remove existing buttons (if any)
        if hasattr(self, "start_button"):
            self.start_button.pack_forget()  # Remove the "Connect" button
        if hasattr(self, "stop_button"):
            self.stop_button.pack_forget()  # Remove the "Disconnect" button

        # Add the appropriate button based on the current status
        if self.status_label.cget("text") == "WireGuard Status: Disconnected":
            # Show the "Connect" button
            self.start_button = ctk.CTkButton(self, text="Connect", command=self.start_wireguard)
            self.start_button.grid(row=4, column=0, pady=5, padx=5)
        else:
            # Show the "Disconnect" button
            self.stop_button = ctk.CTkButton(self, text="Disconnect", fg_color="red", hover_color="darkred", command=self.stop_wireguard)
            self.stop_button.grid(row=4, column=0, pady=5, padx=5)
    
    def load_config_files(self):
        # Path to the WireGuard configuration directory
        config_dir = Path("/etc/wireguard/")
        
        # Get all files in the directory
        try:
            # Get all .conf files in the directory (non-recursive)
            conf_files = [f for f in config_dir.iterdir() if f.suffix == ".conf"]

            # Remove the .conf extension using os.path.splitext() and add to the dropdown
            conf_files_without_extension = [os.path.splitext(f.name)[0] for f in conf_files]

            # If there are .conf files, set the first one as the default
            if conf_files_without_extension:
                self.config_files_dropdown.configure(values=conf_files_without_extension)
                self.config_files_dropdown.set(conf_files_without_extension[0])  # Set the first file as default
                self.selected_config = conf_files_without_extension[0]  # Set the initial selection to the first file
                    
        except FileNotFoundError:
            CustomDialog(self, title="Error", message="Error: Directory not found.")
        except PermissionError:
            CustomDialog(self, title="Error", message="Error: Permission denied. Make sure you have access to the directory.")

    def on_config_selected(self, selected_config):
        # Update the selected configuration when a new one is chosen from the dropdown
        self.selected_config = selected_config

    def delete_config(self):
        # Function to perform the actual deletion of the config
        def perform_delete():
            conf_path = f"/etc/wireguard/{self.selected_config}.conf" 
            try:
                subprocess.run(["sudo", "rm", conf_path], check=True) 
                self.load_config_files()  
            except subprocess.CalledProcessError as e:
                self.show_error(f"Failed to delete configuration:\n{e}")

        # Show confirmation dialog before proceeding with the deletion
        ConfirmationDialog(self, message=f"Are you sure you want to delete {self.selected_config}.conf?", on_confirm=perform_delete)

    def start_wireguard(self):
        try:
            subprocess.run(["wg-quick", "up", self.selected_config], check=True)
            self.check_status()
            self.update_transfer_stats()
        except subprocess.CalledProcessError as e:
            self.show_error(f"Failed to start WireGuard:\n{e}")

    def stop_wireguard(self):
        try:
            subprocess.run(
                ["wg-quick", "down", self.selected_config],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.check_status()
        except subprocess.CalledProcessError as e:
            self.show_error(f"Failed to stop WireGuard:\n{e}")

    def check_status(self):
        result = subprocess.run(
                ["wg"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)

        if result.returncode == 0 and "interface:" in result.stdout:
            self.update_status("Connected")
            self.update_transfer_stats()
        else:
            self.update_status("Disconnected")

    def update_status(self, status):
        self.status_label.configure(text=f"WireGuard Status: {status}")
        self.refresh_buttons()

    def show_error(self, message):
        CustomDialog(self, message=message)

    def open_new_connection_form(self):
        NewConnectionForm(self, self.load_config_files)

    def generate_keys(self):
        GenerateKeys(self)

    def update_transfer_stats(self):
        try:
            # Run the "wg" command to get WireGuard stats
            result = subprocess.run(
                ["wg"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                output = result.stdout

                # Use regex to extract transfer stats (received and sent)
                transfer_match = re.search(r"transfer:\s+([\d.]+\s\w+)\sreceived,\s([\d.]+\s\w+)\ssent", output)

                if transfer_match:
                    received = transfer_match.group(1)
                    sent = transfer_match.group(2)

                    # Update the label text
                    self.transfer_label.configure(text=f"Data Transfer: {received} received, {sent} sent")
                else:
                    self.transfer_label.configure(text="Data Transfer: No data available")

            else:
                self.transfer_label.configure(text="Error fetching WireGuard stats")

        except Exception as e:
            self.transfer_label.configure(text=f"Error: {e}")

        # Schedule the function to run again in 2000ms (2 seconds)
        self.after(2000, self.update_transfer_stats)


# Run the app
if __name__ == "__main__":
    app = WireGuardFrontend()
    app.mainloop()
