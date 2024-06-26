import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk

class QRCodeGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR Code Generator")
        self.configure(bg="#333333")
        self.geometry("400x600")

        self.init_ui()
        self.qr_img = None
        self.qr_color = "white"
        self.bg_color = "#333333"
        self.logo_img = None
        self.logo_size = (50, 50)  # Standard size for the logo

    def init_ui(self):
        self.entry_text = tk.StringVar(value="Insert link here")
        self.entry = tk.Entry(self, fg="#AAAAAA", textvariable=self.entry_text, width=40)
        self.entry.bind("<FocusIn>", self.on_entry_click)
        self.entry.bind("<FocusOut>", self.on_focusout)
        self.entry.pack(pady=20)
        self.dark_style(self.entry, "#AAAAAA")
        self.entry.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)

        self.generate_button = tk.Button(self, text="Preview", command=self.update_preview, padx=10, pady=5)
        self.generate_button.pack(pady=10)
        self.dark_style(self.generate_button)

        self.save_button = tk.Button(self, text="Save", command=self.save_qr_code, padx=10, pady=5)
        self.save_button.pack(pady=10)
        self.dark_style(self.save_button)

        self.color_button = tk.Button(self, text="Choose QR Color", command=self.choose_color, padx=10, pady=5)
        self.color_button.pack(pady=10)
        self.dark_style(self.color_button)

        self.bg_color_button = tk.Button(self, text="Choose Background Color", command=self.choose_bg_color, padx=10, pady=5)
        self.bg_color_button.pack(pady=10)
        self.dark_style(self.bg_color_button)

        self.logo_button = tk.Button(self, text="Add Logo", command=self.add_logo, padx=10, pady=5)
        self.logo_button.pack(pady=10)
        self.dark_style(self.logo_button)

        self.preview_label = tk.Label(self, bg="#333333")
        self.preview_label.pack(pady=20)

    def on_entry_click(self, event):
        """When the entry is clicked, delete the default text."""
        if self.entry_text.get() == "Insert link here":
            self.entry.delete(0, tk.END)
            self.entry.config(fg='white')

    def on_focusout(self, event):
        """When the entry loses focus and is empty, set the default text."""
        if not self.entry.get():
            self.entry.insert(0, 'Insert link here')
            self.entry.config(fg='#AAAAAA')

    def update_preview(self):
        url = self.entry.get()
        if url == "Insert link here" or not url:
            messagebox.showerror("Error", "Please enter a valid link.")
            return
        
        self.qr_img = self.generate_qr_code(url)
        qr_photo = ImageTk.PhotoImage(self.qr_img.resize((200, 200)))
        self.preview_label.config(image=qr_photo)
        self.preview_label.image = qr_photo

    def save_qr_code(self):
        if self.qr_img is None:
            messagebox.showerror("Error", "Generate a QR code first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.qr_img.save(file_path)

    def generate_qr_code(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color=self.qr_color, back_color=self.bg_color).convert('RGB')
        if self.logo_img:
            logo = self.logo_img.resize(self.logo_size)  # Resize logo
            qr_img.paste(logo, ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2))
        return qr_img

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose QR Color", initialcolor=self.qr_color)
        if color_code:
            self.qr_color = color_code[1]
            self.update_preview()

    def choose_bg_color(self):
        color_code = colorchooser.askcolor(title="Choose Background Color", initialcolor=self.bg_color)
        if color_code:
            self.bg_color = color_code[1]
            self.update_preview()

    def add_logo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.logo_img = Image.open(file_path)
            self.update_preview()

    def dark_style(self, widget, fg_color="#FFFFFF", bg_color="#333333"):
        widget.configure(bg=bg_color, fg=fg_color, highlightthickness=0, font=("Arial", 10))
        widget["borderwidth"] = 1
        widget["highlightthickness"] = 1
        widget["relief"] = "solid"

if __name__ == "__main__":
    app = QRCodeGenerator()
    app.mainloop()
