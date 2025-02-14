from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filestore.db'  # You can use other databases

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class File(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('file')
        if not files:
            return 'No file uploaded!', 400

        file_ids = []
        for file in files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            file_id = str(uuid.uuid4())
            new_file = File(id=file_id, filename=filename)
            db.session.add(new_file)
            file_ids.append(file_id)

        db.session.commit()

        # Return a link to the download endpoint for each uploaded file
        links = [url_for('download_file', file_id=id, _external=True) for id in file_ids]
        return jsonify(links)

    return render_template('index.html')

@app.route('/download/<file_id>')
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename)

if __name__ == "__main__":
    app.run(debug=True)