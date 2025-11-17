import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def predict_blood_group(img_path):
    # Use the same model path as the main app; relative to repo root
    model_path = 'code/Lenet/model_blood_group_detection_lenet.keras'
    model = load_model(model_path)

    labels = {0: 'A+', 1: 'A-', 2: 'AB+', 3: 'AB-', 4: 'B+', 5: 'B-', 6: 'O+', 7: 'O-'}

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    result = model.predict(x)
    predicted_class = np.argmax(result)
    return labels[predicted_class]
