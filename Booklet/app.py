from PyPDF2 import PdfFileReader, PdfFileWriter
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import PDF_To_Booklet as PTB
import os
app = Flask(__name__,
            template_folder='./template/',
            static_folder='./static/')


@app.route('/')
def index_html():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def save_file():
    file = request.files['file']
    filename = secure_filename(file.filename)

    upload_path= "./static/pdf/uploaded.pdf"
    file.save(upload_path)

    PTB.Make_Booklet(upload_path,"./static/pdf/booklet.pdf")
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)