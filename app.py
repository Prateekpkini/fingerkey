import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'please-change-this')

# ---------------------------
# MODEL LOADING (UPDATE PATH IF NEEDED)
# ---------------------------
#MODEL_PATH = r"code/Lenet/model_blood_group_detection_lenet.keras"

#if not os.path.exists(MODEL_PATH):
 #   raise FileNotFoundError("❌ MODEL NOT FOUND at: " + MODEL_PATH)

#model = load_model(MODEL_PATH)
#print("✅ Model Loaded Successfully:", MODEL_PATH)

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
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp'}
ALLOWED_CERT_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.pdf'}


# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/upload')
def upload_page():
    # simple alias to main upload page
    return render_template('upload_fingerprint.html')


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


def _allowed_file(filename, allowed_set):
    if not filename:
        return False
    _, ext = os.path.splitext(filename.lower())
    return ext in allowed_set


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    # POST: save basic info and optional fingerprint
    name = request.form.get('name')
    email = request.form.get('email')

    file = request.files.get('fingerprint')
    saved_path = None
    if file and _allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(file.filename)
        dest = os.path.join(app.config['UPLOAD_FOLDER'], 'registrations')
        os.makedirs(dest, exist_ok=True)
        saved_path = os.path.join(dest, filename)
        file.save(saved_path)

    flash('Registration received. Thank you!')
    return render_template('result.html', message='Registration saved successfully.')


@app.route('/verify_certificate', methods=['POST'])
def verify_certificate():
    # predicted_group comes from a hidden field in the form
    predicted_group = request.form.get('predicted_group')
    file = request.files.get('certificate')

    if not file or not _allowed_file(file.filename, ALLOWED_CERT_EXTENSIONS):
        return render_template('result.html', message='No certificate uploaded or file type not allowed')

    filename = secure_filename(file.filename)
    dest = os.path.join(app.config['UPLOAD_FOLDER'], 'certificates')
    os.makedirs(dest, exist_ok=True)
    cert_path = os.path.join(dest, filename)
    file.save(cert_path)

    # Try to extract bloodgroup using existing helper (if available)
    extracted = None
    try:
        from ai_modules.certificate_scanner import extract_blood_group
        extracted = extract_blood_group(cert_path)
    except Exception:
        extracted = None

    if extracted:
        ok = (extracted == predicted_group)
        msg = f'Certificate read: {extracted}. Predicted: {predicted_group}. Match: {ok}'
    else:
        msg = 'Could not extract blood group from certificate. Manual verification required.'

    return render_template('result.html', message=msg)


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
