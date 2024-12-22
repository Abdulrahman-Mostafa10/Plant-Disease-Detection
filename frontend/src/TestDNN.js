import React, { useState } from "react";
import axios from "axios";
import "./TestDNN.css";

function TestDNN() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    setSelectedImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedImage) {
      alert("Please upload an image");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("image", selectedImage);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/dnn_predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.data && response.data.predicted_class) {
        setPredictions(response.data);
        setError(null);
      } else {
        setError("No predictions returned from the server.");
      }
    } catch (error) {
      setError("Error uploading image. Please try again.");
      console.error("Error uploading image:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="test-dnn"
      style={{
        backgroundImage: `url('/bg.jpg')`,
      }}
    >
      <div className="content">
        <h1 className="heading">DNN Image Classifier</h1>
        <div className="upload-section">
          {loading && <div className="loading-message">Uploading...</div>}
          <form onSubmit={handleSubmit}>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="upload-input"
            />
            <button type="submit" className="submit-button">
              Upload and Predict
            </button>
          </form>
        </div>
        <div className="prediction-results">
          {selectedImage && (
            <img
              src={URL.createObjectURL(selectedImage)}
              alt="Uploaded"
              className="uploaded-image"
            />
          )}
          {predictions && (
            <div className="results">
              <h3>Prediction Results:</h3>
              <p>Predicted Class: {predictions.predicted_class}</p>
              <ul>
                {predictions.prediction_percentages.map((percentage, index) => (
                  <li key={index}>
                    Class {index}: {percentage.toFixed(2)}%
                  </li>
                ))}
              </ul>
            </div>
          )}
          {error && <p className="error-message">{error}</p>}
        </div>
      </div>
    </div>
  );
}

export default TestDNN;
