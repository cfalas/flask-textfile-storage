import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from app import app, db
from app.models import TextFile


UPLOAD_FOLDER = 'app/files'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def show_files():
    all_posts = TextFile.query.all()
    return render_template('show_list.html', posts=all_posts)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(request.form['name'])
            entry = TextFile(name=request.form['name'])
            db.session.add(entry)
            db.session.commit()
            filename = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], str(entry.id) + '.txt'))
            print(filename)
            file.save(filename)
            return redirect(url_for('uploaded_file',
                                    filename=entry.id))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type='text' name='name'>
      <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print((os.path.abspath(app.config['UPLOAD_FOLDER']),
                               filename+'.txt'))
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']),
                               filename+'.txt')
