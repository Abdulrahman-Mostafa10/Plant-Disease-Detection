# **_🌱 Plant Disease Detection Project_** 


![back](readme_background.jpg)


📋 Project Overview

This project leverages advanced image processing, machine learning, and deep learning to detect plant diseases from leaf images. A complete pipeline has been developed, combining:

Preprocessing:

🖼️ Image Augmentation

❌ Noise Removal

🌟 Contrast Enhancement

Texture Analysis:

Feature extraction using:

📊 GLCM (Gray Level Co-occurrence Matrix)

🖼️ LBP (Local Binary Patterns)

🌈 RGB Histogram

🎨 HSV Histogram

Machine Learning Models:

![back](Modeling_image.jpeg)


Hyperparameter tuning with Optuna on:
🌟 XGBoost
🌳 Random Forest
📈 KNN
📉 SVM
🌲 Decision Tree
Best Results:
XGBoost with HSV features:
✅ Validation Accuracy: 96%
✅ Test Accuracy: 84%
Deep Learning with MobileNet:

Achieved:
✅ Test Accuracy: 95%

Deployment:

![back](Deployment_image.PNG)

🔧 Backend: Flask
🌐 Frontend: React

📂 Dataset
You can download the dataset from the following link:

[🔗 Plant Disease Dataset](https://www.kaggle.com/datasets/rashikrahmanpritom/plant-disease-recognition-dataset)

🚀 How to Operate the Project

🛠️ Step 1: Start the Backend (Flask)

Install required libraries:

Run the Flask app:
python app.py  

🌐 Step 2: Start the Frontend (React)

* Navigate to the frontend directory:
cd frontend  

* Install required packages:
npm install  

* Run the React app:

npm start  

🖼️ Step 3: Test with Images

Open your browser and navigate to http://localhost:3000.
Upload an image of a plant leaf.
View the predictions and analysis in real-time!

📊 Key Results
Machine Learning (XGBoost + HSV Features):

✅ Validation Accuracy: 96%
✅ Test Accuracy: 84%

MobileNet:

✅ Test Accuracy: 95%

Deployment:

🌟 Fully functional web app with Flask backend and React frontend.
