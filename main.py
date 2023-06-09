from flask import Flask, render_template, request
from roboflow import Roboflow
import requests
import os
import base64
app = Flask(__name__)


@app.route('/')
def home():
  return "Welcome!"

# Replace with your Roboflow API key
api_key = "ULwHCYvJfot1qaMRzNwT"

# Initialize the Roboflow client
rf = Roboflow(api_key=api_key)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the uploaded image file from the request
    image_file = request.files['image']

    # Upload the image file to Roboflow
    response = image_file.save('./img.png')

    # Get the Roboflow project and model
    project = rf.workspace().project("pipe-analysis")
    model = project.version(4).model

    # Infer on the uploaded image
    prediction = model.predict('./img.png').save('./response.png')

    
    with open("./response.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())

    return my_string
  
@app.route('/detectDamage', methods=['POST'])
def detect():
    # Get the uploaded image file from the request
    image_file = request.files['image']

    # Upload the image file to Roboflow
    response = image_file.save('./img.png')

    # Get the Roboflow project and model
    project = rf.workspace().project("cda-is")
    model = project.version(6).model

    # Infer on the uploaded image
    prediction = model.predict('./img.png').save('./response.png')

    
    with open("./response.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())

    return my_string

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
