import wikipediaapi
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import textwrap

headers = {'User-Agent': 'Kaname/1.0; (https://funthingsare.fun; 7emen8wlk@mozmail.com)'}
wiki_wiki = wikipediaapi.Wikipedia('en', headers=headers)

def get_wiki_content(page_title):
    page_py = wiki_wiki.page(page_title)
    if len(page_py.text)==0:
        return False
    else:
        return page_py.text

def get_wiki_content_title(page_title):
    page_py = wiki_wiki.page(page_title)
    return page_py.title.upper()

def save_content_to_pdf(text, title, font_style, page_theme):
    # Create a byte object for streaming
    pdf_bytesio = BytesIO()

    c = canvas.Canvas(pdf_bytesio, pagesize=letter)
    width, height = letter  # Should I add A4 format option?
    font_name = font_style
    font_size = 11
    title_font_size = 14
    margin = 32
    y_position = height - margin
    if font_style == 'Times-Roman':
        wrap_width = 108
    elif font_style == 'Helvetica':
        wrap_width = 100
    elif font_style == 'Courier':
        wrap_width = 84

    c.setTitle(title)
    c.setAuthor('Kaname/1.0')

    line_height = font_size * 2 # Initialize Y position and line height

    if page_theme == 'parch':
        c.setFillColorRGB(0.96, 0.90, 0.71)
        c.rect(0, 0, width, height, fill=1)
        c.setFillColorRGB(0.25, 0.14, 0.08)
    elif page_theme == 'dark':
        c.setFillColorRGB(0.05, 0.05, 0.05)
        c.rect(0, 0, width, height, fill=1)
        c.setFillColorRGB(0.90, 0.90, 0.90)
    else:
        c.setFillColorRGB(0.95, 0.95, 0.95)
        c.rect(0, 0, width, height, fill=1)
        c.setFillColorRGB(0, 0, 0)

    c.setFont(font_name, title_font_size)
    title_width = c.stringWidth(title, font_name, title_font_size)
    title_x_position = (width - title_width) / 2
    c.drawString(title_x_position, y_position, title)
    y_position -= (line_height + margin / 2)

    # Set font for the canvas
    c.setFont(font_name, font_size)

    for paragraph in text.split('\n'):
        wrapped_text = textwrap.fill(paragraph, wrap_width)
        for line in wrapped_text.split('\n'):
            if y_position < margin:  # Check to go on new page
                c.showPage()
                if page_theme == 'parch':
                    c.setFillColorRGB(0.96, 0.90, 0.71)
                    c.rect(0, 0, width, height, fill=1)
                    c.setFillColorRGB(0.25, 0.14, 0.08)
                elif page_theme == 'dark':
                    c.setFillColorRGB(0.05, 0.05, 0.05)
                    c.rect(0, 0, width, height, fill=1)
                    c.setFillColorRGB(0.90, 0.90, 0.90)
                else:
                    c.setFillColorRGB(0.95, 0.95, 0.95)
                    c.rect(0, 0, width, height, fill=1)
                    c.setFillColorRGB(0, 0, 0)
                c.setFont(font_name, font_size)
                y_position = height - margin  # Reset y_position

            c.drawString(margin, y_position, line)
            y_position -= line_height  # Move to the next line

        y_position -= line_height * 0.4

    c.save()

    pdf_bytes = pdf_bytesio.getvalue()
    pdf_bytesio.close()

    return pdf_bytes