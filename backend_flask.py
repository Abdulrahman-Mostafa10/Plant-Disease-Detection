import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from keras.preprocessing import image
from PIL import Image
import pandas as pd
from skimage.color import rgb2hsv
from skimage.io import imread

app = Flask(__name__)
CORS(app)

model = joblib.load("saved_model.joblib")
scaler = joblib.load("scaler_hsv.pkl")
pca = joblib.load("pca_hsv_model.pkl")
xgb_model = joblib.load("best_xgboost_model.pkl")
class_names = ["Healthy", "Powdery", "Rust"]


def extract_hsv_features(image):
    nbins = 256
    img_hsv = (rgb2hsv(image) * 255).astype(np.uint8)
    print(f"HSV Image Shape: {img_hsv.shape}")

    h_hist, _ = np.histogram(img_hsv[:, :, 0], bins=nbins, range=(0, 255))
    s_hist, _ = np.histogram(img_hsv[:, :, 1], bins=nbins, range=(0, 255))
    v_hist, _ = np.histogram(img_hsv[:, :, 2], bins=nbins, range=(0, 255))
    print(f"Histogram lengths - H: {len(h_hist)}, S: {len(s_hist)}, V: {len(v_hist)}")

    # Combine histograms
    histograms = np.concatenate([h_hist, s_hist, v_hist])
    print(f"Combined Histogram Length: {len(histograms)}")
    return histograms


def create_column_hsv_feature(nbins):
    labels = np.zeros(3 * nbins, dtype="<U20")
    for i in range(nbins):
        labels[i] = f"Hue_{i}"
        labels[i + 256] = f"Saturation_{i}"
        labels[i + 512] = f"Value_{i}"
    return labels


@app.route("/predict", methods=["POST"])
def predict():
    print("inside")
    try:

        if "image" not in request.files:
            return jsonify({"error": "No image file provided."}), 400

        image_file = request.files["image"]

        img = Image.open(image_file)

        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        predictions = model.predict(img_array)
        print(predictions)

        predicted_class = np.argmax(predictions, axis=1)[0]
        prediction_percentages = predictions[0] * 100
        print(class_names[int(predicted_class)])

        response = {
            "predicted_class": class_names[int(predicted_class)],
            "prediction_percentages": prediction_percentages.tolist(),
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ///////////////////////////////////////////////
@app.route("/predict_ml", methods=["POST"])
def predict_ml():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided."}), 400
        print("insidee")
        image_file = request.files["image"]

        print("File uploaded:", image_file.filename)

        # Read the image data and open it with PIL
        img = imread(image_file.stream)

        hsv_features = extract_hsv_features(img)
        # print(hsv_features)
        columns = create_column_hsv_feature(256)
        hsv_features_df = pd.DataFrame([hsv_features], columns=columns)

        hsv_features_scaled = scaler.transform(hsv_features_df)
        hsv_features_scaled = pd.DataFrame(hsv_features_scaled, columns=columns)

        hsv_features_pca = pca.transform(hsv_features_scaled)
        hsv_features_pca = pd.DataFrame(hsv_features_pca)
        print(hsv_features_df)
        predictions = xgb_model.predict(hsv_features_pca)

        prediction_probabilities = xgb_model.predict_proba(hsv_features_pca)
        print("Prediction Probabilities:", prediction_probabilities)

        # Get the predicted class based on the highest probability
        predicted_class = np.argmax(prediction_probabilities, axis=1)[0]
        prediction_percentages = (
            prediction_probabilities[0] * 100
        )  # Multiply by 100 for percentage

        response = {
            "predicted_class": class_names[int(predicted_class)],
            "prediction_percentages": prediction_percentages.tolist(),  # These are in percentage
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
