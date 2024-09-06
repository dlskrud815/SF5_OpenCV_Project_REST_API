from flask import Flask, request, send_from_directory
import os
import MySQLdb

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'image_db'

def get_db_connection():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Save file info to MySQL
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (filename, filepath) VALUES (%s, %s)", (filename, filepath))
        conn.commit()
        cursor.close()
        conn.close()

        return 'File uploaded successfully', 200
    else:
        return 'Invalid file type', 400

@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename, filepath FROM images WHERE id = %s", (image_id,))
    image = cursor.fetchone()
    cursor.close()
    conn.close()

    if image:
        filename, filepath = image
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return 'Image not found', 404

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
