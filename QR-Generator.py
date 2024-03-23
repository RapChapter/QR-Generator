import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk

class QRCodeGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR-Code Generator")
        self.configure(bg="#333333")
        self.geometry("400x600")

        self.init_ui()
        self.qr_img = None
        self.qr_color = "white"
        self.bg_color = "#333333"
        self.color_button_bg = self.bg_color

    def init_ui(self):
        self.entry_text = tk.StringVar(value="Link hier einfügen")
        self.entry = tk.Entry(self, fg="#AAAAAA", textvariable=self.entry_text, width=40)
        self.entry.bind("<FocusIn>", self.on_entry_click)
        self.entry.bind("<FocusOut>", self.on_focusout)
        self.entry.pack(pady=20)
        self.dark_style(self.entry, "#AAAAAA")
        self.entry.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)

        self.generate_button = tk.Button(self, text="Vorschau", command=self.update_preview, padx=10, pady=5)
        self.generate_button.pack(pady=10)
        self.dark_style(self.generate_button)

        self.save_button = tk.Button(self, text="Speichern", command=self.save_qr_code, padx=10, pady=5)
        self.save_button.pack(pady=10)
        self.dark_style(self.save_button)

        self.color_button = tk.Button(self, text="QR-Farbe wählen", command=self.choose_color, padx=10, pady=5)
        self.color_button.pack(pady=10)
        self.dark_style(self.color_button)

        self.bg_color_button = tk.Button(self, text="Hintergrund wählen", command=self.choose_bg_color, padx=10, pady=5)
        self.bg_color_button.pack(pady=10)
        self.dark_style(self.bg_color_button)

        self.preview_label = tk.Label(self, bg="#333333")
        self.preview_label.pack(pady=20)

    def on_entry_click(self, event):
        """Wenn das Textfeld angeklickt wird, lösche den vordefinierten Text."""
        if self.entry_text.get() == "Link hier einfügen":
            self.entry.delete(0, tk.END)
            self.entry.insert(0, '')
            self.entry.config(fg='white')

    def on_focusout(self, event):
        """Wenn das Textfeld den Fokus verliert und leer ist, setze den vordefinierten Text."""
        if not self.entry.get():
            self.entry.insert(0, 'Link hier einfügen')
            self.entry.config(fg='#AAAAAA')

    def update_preview(self):
        url = self.entry.get()
        if url == "Link hier einfügen" or not url:
            messagebox.showerror("Fehler", "Bitte gib einen gültigen Link ein.")
            return
        
        self.qr_img = self.generate_qr_code(url)
        qr_photo = ImageTk.PhotoImage(self.qr_img.resize((200, 200)))
        self.preview_label.config(image=qr_photo)
        self.preview_label.image = qr_photo

    def save_qr_code(self):
        if self.qr_img is None:
            messagebox.showerror("Fehler", "Generiere zuerst einen QR-Code.")
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

        img = qr.make_image(fill_color=self.qr_color, back_color=self.bg_color).convert('RGB')
        return img

    def choose_color(self):
        color_code = colorchooser.askcolor(title="QR-Code Farbe wählen", initialcolor=self.qr_color)
        if color_code:
            self.qr_color = color_code[1]
            self.update_preview()

    def choose_bg_color(self):
        color_code = colorchooser.askcolor(title="Hintergrundfarbe wählen", initialcolor=self.bg_color)
        if color_code:
            self.bg_color = color_code[1]
            self.update_preview()

    def dark_style(self, widget, fg_color="#FFFFFF", bg_color="#333333"):
        widget.configure(bg=bg_color, fg=fg_color, highlightthickness=0, font=("Arial", 10))
        widget["borderwidth"] = 1
        widget["highlightthickness"] = 1
        widget["relief"] = "solid"

if __name__ == "__main__":
    app = QRCodeGenerator()
    app.mainloop()
