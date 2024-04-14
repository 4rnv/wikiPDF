from flask import Flask, render_template, request, send_file
from logik import get_wiki_content, get_wiki_content_title, save_content_to_pdf
from io import BytesIO
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/download', methods=['POST'])
def userquery():
    query = request.form['query'].strip()
    font_style = request.form['font_style'].strip()
    page_theme = request.form['theme'].strip()
    if len(query) > 32:
        return 'Your search is too long.'

    content = get_wiki_content(query)
    content_title = get_wiki_content_title(query)

    if content == False:
        return 'No such Wikipedia page exists.'

    timestamp = str(int(time.time()*1000000))
    filename = query+timestamp
    pdf_bytes = save_content_to_pdf(content, content_title, font_style, page_theme)
    pdf_stream = BytesIO(pdf_bytes)
    return send_file(pdf_stream, download_name=f"{filename}.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run()