#Importing Setup
import os
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

model = tf.keras.models.load_model('BrainTumour10EpochsCategorical.h5')

#Model Functions
def brain_classification(classType):
    if classType == 0:
        return "No Brain Tumour"
    elif classType == 1:
        return "Brain Tumour Present"

def getResult(img):
    image = cv2.imread(img)
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64, 64))
    image = np.array(image)
    input_img = np.expand_dims(image, axis = 0)
    result = np.argmax(model.predict(input_img), axis = -1)
    return result

#App Setup
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, secure_filename(f.filename))
        f.save(file_path)
        value = getResult(file_path)
        result = brain_classification(value)
        return result
    return None

if __name__ == '__main__':
    app.run(debug = True)
