import customtkinter as ctk

class CustomDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Error", message=""):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")

        self.center_window()

        # Message Label
        self.label = ctk.CTkLabel(self, text=message, wraplength=250)
        self.label.pack(pady=20, padx=10)

        # Close Button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.pack(pady=10)

    def center_window(self):
        """Center the window on the screen."""
        window_width = 300
        window_height = 150

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        # Set the geometry
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
