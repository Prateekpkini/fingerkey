import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, AveragePooling2D, Flatten, Dense, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# ======================================================
# 1️⃣  Build LeNet architecture
# ======================================================
model = Sequential([
    Input(shape=(224, 224, 3)),
    Conv2D(6, kernel_size=(5, 5), activation='relu'),
    AveragePooling2D(pool_size=(2, 2)),
    Conv2D(16, kernel_size=(5, 5), activation='relu'),
    AveragePooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(120, activation='relu'),
    Dense(84, activation='relu'),
    Dense(8, activation='softmax')  # 8 classes (A+, A-, AB+, AB-, B+, B-, O+, O-)
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print("✅ LeNet model built successfully!")

# ======================================================
# 2️⃣  Load and preprocess dataset
# ======================================================
base_dir = r"C:\Users\adith\Desktop\fingerprint-based-blood-group-detection\dataset\dataset_blood_group"


train_datagen = ImageDataGenerator(rescale=1.0/255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# ======================================================
# 3️⃣  Train model
# ======================================================
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10
)

# ======================================================
# 4️⃣  Save trained model
# ======================================================
save_dir = os.path.join(r"C:\Users\adith\Desktop\fingerprint-based-blood-group-detection", "code", "Lenet")
os.makedirs(save_dir, exist_ok=True)

save_path = os.path.join(save_dir, "model_blood_group_detection_lenet.keras")
model.save(save_path)
print("✅ Model saved successfully at:", save_path)
