from app_ml import app
from app_ml.predictModel import extract_hsv_features, create_column_hsv_feature
from flask import render_template, request,jsonify
import joblib
import pandas as pd
import numpy as np
from PIL import Image
import os
from skimage.io import imread
# @app.route('/')
model = joblib.load('saved_model.joblib')
scaler = joblib.load('scaler_hsv.pkl') 
pca = joblib.load('pca_hsv_model.pkl')  
xgb_model = joblib.load('best_xgboost_model.pkl')
class_names = ['Healthy', 'Powdery', 'Rust']


# def home_page():
#     return render_template('home.html')


# app.add_url_rule('/', 'home', home_page)


@app.route('/dnn_predict', methods=['POST'])
def predict():
    print('inside')
    try:
        TARGET_SIZE = (224, 224)
       
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided.'}), 400

        image_file = request.files['image']

        img = Image.open(image_file)
      
        img = img.resize(TARGET_SIZE)

        img_array = np.array(img)

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

# ///////////////////////////////////////////////
@app.route('/predict_ml', methods=['POST'])
def predict_ml():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided.'}), 400
        print('insidee')
        image_file = request.files['image']
       
        print("File uploaded:", image_file.filename)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)


        image_file.save(filepath)

        img = imread(filepath)
        
        # Convert the image to RGB (in case it's in a different mode)
        # img = img.convert('RGB')
        
        # Convert to numpy array (this is needed for processing in scikit-image)
        # img_array = np.array(img)

        # print(img)
        # # Convert image to numpy array
        # img_array = np.array(img)
        
    
        hsv_features = extract_hsv_features(img)

        columns = create_column_hsv_feature(256)

        hsv_features_df = pd.DataFrame([hsv_features], columns=columns)
        hsv_features_df.to_csv('test.csv',index=False)
      

        hsv_features_scaled = scaler.transform(hsv_features_df)
        hsv_features_scaled = pd.DataFrame(hsv_features_scaled, columns=columns)
        
        hsv_features_pca = pca.transform(hsv_features_scaled)
        hsv_features_pca= pd.DataFrame(hsv_features_pca)

        predictions = xgb_model.predict(hsv_features_pca)

        
        prediction_percentages = predictions[0] * 100
        prediction_probabilities = xgb_model.predict_proba(hsv_features_pca)
        print("Prediction Probabilities:", prediction_probabilities)

        # Get the predicted class based on the highest probability
        predicted_class = np.argmax(prediction_probabilities, axis=1)[0]
        prediction_percentages = prediction_probabilities[0] * 100  # Multiply by 100 for percentage

        response = {
            'predicted_class': class_names[int(predicted_class)],
            'prediction_percentages': prediction_percentages.tolist()  # These are in percentage
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500