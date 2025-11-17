import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Load trained model
model_path = os.path.join("code", "Lenet", "model_blood_group_detection_lenet.keras")
model = load_model(model_path)
print(f"✅ Loaded model from: {os.path.abspath(model_path)}")

# Blood group labels
labels = {0: 'A+', 1: 'A-', 2: 'AB+', 3: 'AB-', 4: 'B+', 5: 'B-', 6: 'O+', 7: 'O-'}

# Test image path
img_path = r"dataset\dataset_blood_group\A+\cluster_0_1001.BMP"

img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = x / 255.0

result = model.predict(x)
predicted_class = np.argmax(result)
predicted_label = labels[predicted_class]
confidence = result[0][predicted_class] * 100

plt.imshow(image.array_to_img(x[0]))
plt.axis('off')
plt.title(f"Prediction: {predicted_label} ({confidence:.2f}%)")
plt.show()

print(f"🩸 Predicted Blood Group: {predicted_label}")
print(f"🎯 Confidence: {confidence:.2f}%")
