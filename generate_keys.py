import customtkinter as ctk
import subprocess
from pathlib import Path

class GenerateKeys(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Generated Keys")
        self.geometry("400x200")
        self.resizable(width=False,height=False)
        self.center_window()

        self.config_dir = Path.home() / "wireguard_keys"  # Store keys in the user's home directory
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.create_widgets()

    def center_window(self):
        """Center the window on the screen."""
        window_width = 500
        window_height = 200

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    def create_widgets(self):
        """Create UI elements to display generated keys."""

        self.label_private = ctk.CTkLabel(self, text="Private Key:")
        self.label_private.pack(pady=5)

        self.private_key_entry = ctk.CTkEntry(self, width=400)
        self.private_key_entry.pack(pady=5)

        self.label_public = ctk.CTkLabel(self, text="Public Key:")
        self.label_public.pack(pady=5)

        self.public_key_entry = ctk.CTkEntry(self, width=400)
        self.public_key_entry.pack(pady=5)

        self.generate_button = ctk.CTkButton(self, text="Generate Keys", command=self.generate_keys)
        self.generate_button.pack(pady=10)

    def generate_keys(self):
        """Generate WireGuard keys using a one-liner command and read them."""

        private_key_path = self.config_dir / "privatekey"
        public_key_path = self.config_dir / "publickey"

        try:
            # Run the one-liner command
            subprocess.run(
                f"wg genkey | tee {private_key_path} | wg pubkey > {public_key_path}",
                shell=True, check=True, text=True
            )

            # Read the keys from files
            private_key = private_key_path.read_text().strip()
            public_key = public_key_path.read_text().strip()

            # Update the UI fields
            self.private_key_entry.delete(0, ctk.END)
            self.private_key_entry.insert(0, private_key)

            self.public_key_entry.delete(0, ctk.END)
            self.public_key_entry.insert(0, public_key)

        except subprocess.CalledProcessError as e:
            self.private_key_entry.insert(0, "Error generating keys")
            self.public_key_entry.insert(0, f"Error: {e}")
        except PermissionError:
            self.private_key_entry.insert(0, "Permission Denied")
            self.public_key_entry.insert(0, "Run with sudo")
