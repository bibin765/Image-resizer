import flask
import os
from werkzeug.utils import secure_filename
from flask import request,redirect
from PIL import Image
from flask import send_from_directory
from flask import abort
import sqlite3
import datetime
import json
from flask_cors import CORS, cross_origin
import io
import base64

UPLOAD_FOLDER = '/home/bibin/Desktop/image-resizer/api'


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
def retrieveDetails():
    conn = sqlite3.connect('resizeDetails.db')
    cursor = conn.execute("SELECT * FROM Details")
    rows = cursor.fetchall()
    return json.dumps(rows)	





@app.route('/<int:image_size>', methods=['GET','POST'])
def processImage(image_size):
    if 'file' not in request.files:
            abort(500)
    file = request.files['file']
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)

    if(ext != '.jpg'):
        abort(417)
    #saving image
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    newfile = Image.open(file)
    
    #inserting into database
    date = datetime.datetime.now()
    con = sqlite3.connect("resizeDetails.db") 
    con.execute("INSERT INTO Details VALUES (NULL,?,?,?)",(image_size,date,name))
    con.commit()
    con.close()

    #resizing image
    height,width = newfile.size
    height50 =int(height/2)
    height25 = int(height50/2)
    width50 = int(width/2)
    width25 = int(width50/2)
    image50 = newfile.resize((height50,width50))
    filename = os.path.splitext(name)[0]
    image50.save(os.path.join(app.config['UPLOAD_FOLDER'], name + '50.jpg'))
    image25 = newfile.resize((height25,width25))
    image25.save(os.path.join(app.config['UPLOAD_FOLDER'],  name + '25.jpg'))
    
    #returning image
    if image_size==50:
        return send_from_directory(app.config['UPLOAD_FOLDER'],name +'50.jpg', as_attachment=True)
    elif image_size==25:
        return send_from_directory(app.config['UPLOAD_FOLDER'],name +'25.jpg', as_attachment=True)
    else:
        abort(417)
    



app.run()


