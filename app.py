import os
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

# ---------------------------
# MODEL LOADING (UPDATE PATH IF NEEDED)
# ---------------------------
MODEL_PATH = r"code/Lenet/model_blood_group_detection_lenet.keras"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ MODEL NOT FOUND at: " + MODEL_PATH)

model = load_model(MODEL_PATH)
print("✅ Model Loaded Successfully:", MODEL_PATH)

# ---------------------------
# LABELS
# ---------------------------
labels = {
    0: 'A+',
    1: 'A-',
    2: 'AB+',
    3: 'AB-',
    4: 'B+',
    5: 'B-',
    6: 'O+',
    7: 'O-'
}

# ---------------------------
# UPLOADS FOLDER
# ---------------------------
UPLOAD_FOLDER = "uploads/fingerprints"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------
# PREDICT BLOOD GROUP
# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():
    # Check file availability
    if "fingerprint" not in request.files:
        return render_template(
            "index.html",
            prediction="No file uploaded",
            confidence="0%"
        )

    file = request.files["fingerprint"]

    if file.filename == "":
        return render_template(
            "index.html",
            prediction="No file selected",
            confidence="0%"
        )

    # Save uploaded fingerprint
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Preprocess image
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Model prediction
    result = model.predict(img_array)
    predicted_class = np.argmax(result)
    predicted_label = labels[predicted_class]
    confidence_value = result[0][predicted_class] * 100
    confidence = f"{confidence_value:.2f}%"

    # Return prediction to frontend
    return render_template(
        "index.html",
        prediction=predicted_label,
        confidence=confidence
    )


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
