import customtkinter as ctk

class ConfirmationDialog(ctk.CTkToplevel):
    def __init__(self, parent, message, on_confirm):
        super().__init__(parent)
        self.title("Confirm Deletion")
        self.geometry("300x150")
        self.resizable(width=False,height=False)
        self.center_window()

        # Message Label
        self.label = ctk.CTkLabel(self, text=message)
        self.label.pack(pady=20, padx=10)

        # Buttons
        self.confirm_button = ctk.CTkButton(self, text="Yes", fg_color="red", hover_color="darkred", command=lambda: self.confirm(on_confirm))
        self.confirm_button.pack(side="left", padx=10, pady=10)

        self.cancel_button = ctk.CTkButton(self, text="No", command=self.destroy)
        self.cancel_button.pack(side="right", padx=10, pady=10)

    def confirm(self, on_confirm):
        on_confirm()  # Call the provided confirmation handler function
        self.destroy()

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