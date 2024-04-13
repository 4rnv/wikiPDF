from flask import Flask, render_template, request, send_from_directory, make_response
from logik import get_wiki_content, get_wiki_content_title, save_content_to_pdf
import threading
import time
import os

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
    timestamp = int(time.time()*1000000)
    filename = f"{timestamp}.pdf"
    if content==False:
        return 'No such Wikipedia page exists.'
    save_content_to_pdf(content, content_title, f"./static/{filename}", font_style, page_theme)
    pdf_folder = 'static'
    if not pdf_folder:
        os.makedirs(pdf_folder)
    file_path = os.path.join(app.root_path, 'static', filename)
    print(file_path)
    delete_file_later(file_path, 300)
    returning = make_response(send_from_directory(directory=pdf_folder, path=filename, as_attachment=False))
    returning.headers['Content-Type'] = 'application/pdf'
    returning.headers['Content-Disposition'] = f'inline; filename={filename}'
    return returning

def delete_file_later(path, delay):
    def delete():
        time.sleep(delay) # Keep file on server for some time
        os.remove(path)

    thread = threading.Thread(target=delete)
    thread.start()

if __name__ == '__main__':
    app.run(debug=True)