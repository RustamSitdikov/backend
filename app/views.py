#!/usr/bin/env python

from app import app
from flask import request, redirect, url_for, jsonify, flash, send_from_directory
from werkzeug.utils import secure_filename
import os

from app import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, STATIC_FOLDER


@app.route('/<string:name>/')
@app.route('/')
def index(name='world'):
    return "Hello, {}!".format(name)


@app.route('/form/', methods={'GET', 'POST'})
def form():
    if request.method == 'GET':
        return """
        <html>
            <head>
            </head>
            <body>
                <form method="POST" action="/form/">
                    <input name="first_name">
                    <input name="last_name">
                    <input type="submit">
                </form>
            </body>
        </html>
        """
    else:
        return jsonify(request.form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/{}/<filename>'.format(STATIC_FOLDER))
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
