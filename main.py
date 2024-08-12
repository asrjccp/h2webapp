import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
    
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and \
        request.files and 'image' in request.files:
        # Save file
        image = request.files['image']
        filename = secure_filename(image.filename)
        path = os.path.join('uploads', filename)
        image.save(path)
        # Add filename to text file
        file = open('all.txt', 'a')
        file.write(filename + '\n')
        file.close()
        return render_template('index.html', status='ok')
    return render_template('index.html')

@app.route('/view')
def view():
    file = open('all.txt', 'r')
    filenames = file.readlines()
    images = []
    for filename in filenames:
        images.append(filename.strip())
    file.close()
    return render_template('view.html', images=images)

@app.route('/images/<filename>')
def get_file(filename):
    return send_from_directory('uploads', filename)

app.run()
