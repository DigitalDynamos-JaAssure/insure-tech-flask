from flask import Flask, render_template, request
from roboflow import Roboflow
import requests
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
    response = rf.upload(image_file)

    # Get the URL of the uploaded image
    image_url = response['url']

    # Get the Roboflow project and model
    project = rf.workspace().project("pipe-analysis")
    model = project.version(2).model

    # Infer on the uploaded image
    prediction = model.predict(image_url).json()

    # Save the annotated image
    annotated_image_url = prediction['outputs'][0]['annotation']
    response = requests.get(annotated_image_url)
    with open("prediction.jpg", "wb") as f:
        f.write(response.content)
        print("Annotated image has been saved as prediction.jpg")

    return Response(response=base64_image, content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)