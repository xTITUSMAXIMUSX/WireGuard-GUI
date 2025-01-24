import customtkinter as ctk
from custom_dialog import CustomDialog
from pathlib import Path

class NewConnectionForm(ctk.CTkToplevel):
    def __init__(self, parent, update_dropdown_callback):
        super().__init__(parent)
        self.title("New WireGuard Connection")
        self.geometry("800x700")
        self.resizable(width=False,height=False)
        self.center_window()

        self.update_dropdown_callback = update_dropdown_callback

        # Configure grid layout
        self.columnconfigure(0, weight=1)  # Adjust column 0 for labels
        self.columnconfigure(1, weight=2)  # Adjust column 1 for entries
        self.columnconfigure(2, weight=3)  # Adjust column 1 for entries

        ### INTERFACE
        self.label_interface_top = ctk.CTkLabel(self, text="[Interface]")
        self.label_interface_top.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        self.label_interface = ctk.CTkLabel(self, text="**Interface Name (e.g., wg1):")
        self.label_interface.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.entry_interface = ctk.CTkEntry(self)
        self.entry_interface.grid(row=1, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_private_key = ctk.CTkLabel(self, text="**Private Key:")
        self.label_private_key.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.entry_private_key = ctk.CTkEntry(self)
        self.entry_private_key.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky="ew")

        self.label_address = ctk.CTkLabel(self, text="**Address (e.g., 10.0.0.1/24):")
        self.label_address.grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.entry_address = ctk.CTkEntry(self)
        self.entry_address.grid(row=3, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_listenport = ctk.CTkLabel(self, text="Listen Port:")
        self.label_listenport.grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.entry_listenport = ctk.CTkEntry(self)
        self.entry_listenport.grid(row=4, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_table = ctk.CTkLabel(self, text="Table:")
        self.label_table.grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.entry_table = ctk.CTkEntry(self)
        self.entry_table.grid(row=5, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_mtu = ctk.CTkLabel(self, text="MTU:")
        self.label_mtu.grid(row=6, column=0, pady=5, padx=5, sticky="e")
        self.entry_mtu = ctk.CTkEntry(self)
        self.entry_mtu.grid(row=6, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_preup = ctk.CTkLabel(self, text="PreUp:")
        self.label_preup.grid(row=7, column=0, pady=5, padx=5, sticky="e")
        self.entry_preup = ctk.CTkEntry(self)
        self.entry_preup.grid(row=7, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_postup = ctk.CTkLabel(self, text="PostUp:")
        self.label_postup.grid(row=8, column=0, pady=5, padx=5, sticky="e")
        self.entry_postup = ctk.CTkEntry(self)
        self.entry_postup.grid(row=8, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_predown = ctk.CTkLabel(self, text="PreDown:")
        self.label_predown.grid(row=9, column=0, pady=5, padx=5, sticky="e")
        self.entry_predown = ctk.CTkEntry(self)
        self.entry_predown.grid(row=9, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_postdown = ctk.CTkLabel(self, text="PostDown:")
        self.label_postdown.grid(row=10, column=0, pady=5, padx=5, sticky="e")
        self.entry_postdown = ctk.CTkEntry(self)
        self.entry_postdown.grid(row=10, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_dns = ctk.CTkLabel(self, text="DNS (optional):")
        self.label_dns.grid(row=11, column=0, pady=5, padx=5, sticky="e")
        self.entry_dns = ctk.CTkEntry(self)
        self.entry_dns.grid(row=11, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        ### PEER

        self.label_peer = ctk.CTkLabel(self, text="[Peer]")
        self.label_peer.grid(row=12, column=1, pady=5, padx=5, sticky="ew")

        self.label_public_key = ctk.CTkLabel(self, text="**Public Key:")
        self.label_public_key.grid(row=13, column=0, pady=5, padx=10, sticky="e")
        self.entry_public_key = ctk.CTkEntry(self)
        self.entry_public_key.grid(row=13, column=1, columnspan=2, pady=5, padx=5, sticky="ew")

        self.label_endpoint = ctk.CTkLabel(self, text="Endpoint (IP:PortNumber):")
        self.label_endpoint.grid(row=14, column=0, pady=5, padx=5, sticky="e")
        self.entry_endpoint = ctk.CTkEntry(self)
        self.entry_endpoint.grid(row=14, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_allowedips = ctk.CTkLabel(self, text="AllowedIPs (e.g., 8.8.8.8,9.9.9.9):")
        self.label_allowedips.grid(row=15, column=0, pady=5, padx=5, sticky="e")
        self.entry_allowedips = ctk.CTkEntry(self)
        self.entry_allowedips.grid(row=15, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        self.label_keepalive = ctk.CTkLabel(self, text="Persistent Keepalive:")
        self.label_keepalive.grid(row=16, column=0, pady=5, padx=5, sticky="e")
        self.entry_keepalive = ctk.CTkEntry(self)
        self.entry_keepalive.grid(row=16, column=1, columnspan=1, pady=5, padx=5, sticky="ew")

        # Save button spans both columns
        self.save_button = ctk.CTkButton(self, text="Save Connection", command=self.save_connection)
        self.save_button.grid(row=17, column=1, pady=15, padx=5)

    def save_connection(self):
        # Get form data
        interface = self.entry_interface.get()
        private_key = self.entry_private_key.get()
        address = self.entry_address.get()
        listen_port  = self.entry_listenport.get()
        address = self.entry_address.get()
        table = self.entry_table.get()
        mtu = self.entry_mtu.get()
        preup = self.entry_preup.get()
        postup = self.entry_postup.get()
        predown = self.entry_predown.get()
        postdown = self.entry_postdown.get()
        dns = self.entry_dns.get()
        publickey = self.entry_public_key.get()
        allowedips = self.entry_allowedips.get()
        endpoint = self.entry_endpoint.get()
        keepalive = self.entry_keepalive.get()

        # Ensure required fields are filled
        if not all([interface, private_key, address, publickey]):
            CustomDialog(self, message="Please fill in all required fields.")
            return

        # Create the config content
        config_content = "[Interface]\n"
                            
        if private_key:
            config_content +=  f"PrivateKey = {private_key}\n"
        if address:
            config_content += f"Address = {address}\n"
        if listen_port:
            config_content += f"ListenPort = {listen_port}\n"
        if table:
            config_content += f"Table = {table}\n"
        if mtu:
            config_content += f"MTU = {mtu}\n"
        if preup:
            config_content += f"PreUp = {preup}\n"
        if postup:
            config_content += f"PostUp = {postup}\n"
        if predown:
            config_content += f"PreDown = {predown}\n"
        if postdown:
            config_content += f"PostDown = {postdown}\n"
        if dns:
            config_content += f"DNS = {dns}\n"

        config_content += "\n[Peer]\n"

        if publickey:
            config_content += f"PublicKey = {publickey}\n"
        if endpoint:
            config_content += f"Endpoint = {endpoint}\n"
        if allowedips:
            config_content += f"AllowedIPs = {allowedips}\n"
        if keepalive:
            config_content += f"PersistentKeepalive = {keepalive}"

        # Save to file
        config_path = f"/etc/wireguard/{interface}.conf"  # Adjust path as necessary
        try:
            with open(config_path, "w") as config_file:
                config_file.write(config_content)
                self.update_dropdown_callback()
                self.destroy()
        except Exception as e:
            CustomDialog(self, title="Error", message=f"Failed to save configuration:\n{e}")

    def center_window(self):
        """Center the window on the screen."""
        window_width = 800
        window_height = 700

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        # Set the geometry
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    def load_config_files(self):
    # Path to the WireGuard configuration directory
        config_dir = Path("/etc/wireguard/")

        # Get all files in the directory
        try:
            conf_files = [f for f in config_dir.iterdir() if f.suffix == ".conf"]

            # Remove .conf extension using with_suffix('') and add to the dropdown
            conf_files_without_extension = [f.with_suffix('') for f in conf_files]

            # If there are .conf files, set the first one as the default
            if conf_files_without_extension:
                self.config_files_dropdown.configure(values=[str(f) for f in conf_files_without_extension])
                self.config_files_dropdown.set(str(conf_files_without_extension[0]))  # Set the first file as default
                self.selected_config = conf_files_without_extension[0]  # Set the initial selection to the first file

        except FileNotFoundError:
            CustomDialog(self, message="Error: Directory not found.")
        except PermissionError:
            CustomDialog(self, title="Error", message="Error: Permission denied.")

    