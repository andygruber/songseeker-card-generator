import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import qrcode
from qrcode.image.styledpil import StyledPilImage
import hashlib
import argparse
import textwrap
import os


def generate_qr_code(url, file_path, icon_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    if icon_path is None:
        img = qr.make_image(fill_color="black", back_color="white")
    else:
        img = qr.make_image(image_factory=StyledPilImage, embeded_image_path=icon_path)
    img.save(file_path)

def add_qr_code_with_border(c, url, position, box_size, icon_path):
    hash_object = hashlib.sha256(url.encode())
    hex_dig = hash_object.hexdigest()

    qr_code_path = f"qr_{hex_dig}.png"  # Unique path for each QR code
    generate_qr_code(url, qr_code_path, icon_path)
    x, y = position
    c.drawImage(qr_code_path, x, y, width=box_size, height=box_size)
    c.rect(x, y, box_size, box_size)
    os.remove(qr_code_path)

def add_text_box(c, info, position, box_size):
    x, y = position
    text_margin = 2
    c.setFont("Helvetica", 10)
    artist_text = f"{info['Artist']}"
    title_text = f"{info['Title']}"
    year_text = f"{info['Year']}"

    # Calculate the centered position for each line of text
    artist_x = x + (box_size - c.stringWidth(artist_text, "Helvetica", 10)) / 2
    title_x = x + (box_size - c.stringWidth(title_text, "Helvetica", 10)) / 2
    year_x = x + (box_size - c.stringWidth(year_text, "Helvetica-Bold", 30)) / 2

    # Split the text into multiple lines if it doesn't fit in the width
    artist_lines = textwrap.wrap(artist_text, width=int(len(artist_text) / c.stringWidth(artist_text, "Helvetica", 10) * (box_size - text_margin)))
    title_lines = textwrap.wrap(title_text, width=int(len(title_text) / c.stringWidth(title_text, "Helvetica", 10) * (box_size - text_margin)))

    # Calculate the centered position for each line of text
    artist_y = y + box_size - 15
    title_y = y + (len(title_lines) * 12)
    year_y = y + box_size / 2 - 15 / 2

    # Draw each line of text
    for line in artist_lines:
        artist_x = x + (box_size - c.stringWidth(line, "Helvetica", 10)) / 2
        c.drawString(artist_x, artist_y, line)
        artist_y -= 12

    for line in title_lines:
        title_x = x + (box_size - c.stringWidth(line, "Helvetica", 10)) / 2
        c.drawString(title_x, title_y, line)
        title_y -= 12

    c.setFont("Helvetica-Bold", 30)
    c.drawString(year_x, year_y, year_text)

    c.rect(x, y, box_size, box_size)

def main(csv_file_path, output_pdf_path, icon_path=None):
    data = pd.read_csv(csv_file_path)
    data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x) # Remove leading and trailing whitespaces

    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    page_width, page_height = A4
    box_size = 4.6 * cm
    boxes_per_row = int(page_width // box_size)
    boxes_per_column = int(page_height // box_size)
    boxes_per_page = boxes_per_row * boxes_per_column
    vpageindent = 0.8 * cm
    hpageindent = (page_width - (box_size * boxes_per_row)) / 2

    for i in range(0, len(data), boxes_per_page):
    # Generate QR codes
        for index in range(i, min(i + boxes_per_page, len(data))):
            row = data.iloc[index]
            position_index = index % (boxes_per_row * boxes_per_column)
            column_index = position_index % boxes_per_row
            row_index = position_index // boxes_per_row
            x = hpageindent + (column_index * box_size)
            y = page_height - vpageindent - (row_index + 1) * box_size
            add_qr_code_with_border(c, row['URL'], (x, y), box_size, icon_path)

        c.showPage()

        # Add text information
        for index in range(i, min(i + boxes_per_page, len(data))):
            row = data.iloc[index]
            position_index = index % boxes_per_page
            column_index = (boxes_per_row-1) - position_index % boxes_per_row
            row_index = position_index // boxes_per_row
            x = hpageindent + (column_index * box_size)
            y = page_height - vpageindent - (row_index + 1) * box_size
            add_text_box(c, row, (x, y), box_size)

        c.showPage()

    c.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("output_pdf", help="Path to the output PDF file")
    parser.add_argument("--icon", help="path to icon to embedd to QR Code, should not exeed 300x300px and using transparent background", required = False)
    args = parser.parse_args()
    main(args.csv_file, args.output_pdf, args.icon)
