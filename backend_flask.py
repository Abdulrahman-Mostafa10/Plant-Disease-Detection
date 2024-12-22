from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from keras.preprocessing import image
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

model = joblib.load('saved_model.joblib')

TARGET_SIZE = (224, 224)
class_names = ['Healthy', 'Powdery', 'Rust']

@app.route('/predict', methods=['POST'])
def predict():
    print('inside')
    try:

       
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided.'}), 400

        image_file = request.files['image']

        img = Image.open(image_file)

        img = img.resize(TARGET_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  
        predictions = model.predict(img_array)
        print(predictions)  

     
        predicted_class = np.argmax(predictions, axis=1)[0]
        prediction_percentages = predictions[0] * 100  
        print(class_names[int(predicted_class)])
 
        response = {
            'predicted_class': class_names[int(predicted_class)],
            'prediction_percentages': prediction_percentages.tolist()
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
