import tkinter as tk
from tkinter import messagebox
import pyshorteners
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageOps
import random

colors = ['red','green','blue','orange','purple','pink','brown','cyan','magenta']
def colr():
    return random.choice(colors)

def create_gradient(size):
    top = Image.new('RGB', size, color=colr())
    bottom = Image.new('RGB', size, color=colr())
    mask = Image.new('L', size)
    mask_data = []
    for y in range(size[1]):
        mask_data.extend([int(255 * (y / size[1]))] * size[0])
    mask.putdata(mask_data)
    return Image.composite(bottom, top, mask)


# Function to shorten the URL
def shorten_url():
    original_url = url_entry.get()
    if original_url:
        try:
            s = pyshorteners.Shortener()
            shortened_url = s.tinyurl.short(original_url)  # You can use a different shortening service

            # Display the shortened URL
            shortened_url_text.config(text=f"Shortened URL: {shortened_url}")

            # Generate QR code for the shortened URL
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(shortened_url)
            qr.make(fit=True)

            # Create a QR code image
            qr_image = qr.make_image(fill_color='black', back_color="white")
            qr_image = qr_image.convert('RGB')

            gradient = create_gradient(qr_image.size)
            mask = qr_image.convert('L')
            mask = ImageOps.invert(mask)
            finl_img = Image.composite(gradient, qr_image, mask)

            # Convert the QR code image to a PhotoImage for display in Tkinter
            photo = ImageTk.PhotoImage(image=finl_img)

            # Display the QR code
            qr_image_label.config(image=photo)
            qr_image_label.photo = photo  # Store a reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please enter a URL.")

# Create a GUI window
app = tk.Tk()
app.title("URL Shortener and QR Code Generator")

# Label and entry field for the original URL
url_label = tk.Label(app, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(app)
url_entry.pack()

# Button to shorten the URL
shorten_button = tk.Button(app, text="Shorten URL", command=shorten_url)
shorten_button.pack()

# Label to display the shortened URL
shortened_url_text = tk.Label(app, text="")
shortened_url_text.pack()

# Label to display the QR code
qr_image_label = tk.Label(app)
qr_image_label.pack()

# Start the GUI main loop
app.mainloop()