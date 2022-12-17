from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename 
import os

UPLOAD_FOLDER = 'static/upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/upload',methods= ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect("/") 


if __name__ == "__main__":
    app.run(debug=True)    