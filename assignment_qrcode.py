
import qrcode

# URL to be encoded in the QR code
url = "https://www.formula1.com/en/results.html"

# Generate the QR code
qr = qrcode.QRCode(
    version=1,  # QR code version (adjust if needed)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each QR code "box"
    border=4,  # Border space around the QR code
)
qr.add_data(url)
qr.make(fit=True)

# Create an image of the QR code
img = qr.make_image(fill_color="black", back_color="white")

# Save the QR code image to a file (e.g., qr_code.png)
img.save("qr_code.png")

# Display the QR code (optional)
img.show()