import numpy as np
import rasterio
import tensorflow as tf
import os
import cv2
from tensorflow.keras import layers, models, callbacks

#  Constants
IMG_SIZE = (128, 128)
TRAIN_PATH = "data/water_pollution/train"
TEST_PATH = "data/water_pollution/test"
MODEL_PATH = "models/water_pollution_model.h5"
HISTORY_PATH = "models/water_pollution_training_history.npy"

# Function to load and preprocess NDWI images
def load_ndwi_data(folder):
    images, labels = [], []
    for filename in os.listdir(folder):
        if filename.endswith(".tif"):
            file_path = os.path.join(folder, filename)
            with rasterio.open(file_path) as dataset:
                ndwi = dataset.read(1)
                ndwi = (ndwi + 1) / 2.0  # Normalize to 0–1
                ndwi_resized = cv2.resize(ndwi, IMG_SIZE)

                images.append(ndwi_resized)

                #  Label: 1 = clean, 0 = polluted
                label = 1 if "clean" in filename.lower() else 0
                labels.append(label)
    return np.array(images), np.array(labels)

# Load and preprocess data
X_train, y_train = load_ndwi_data(TRAIN_PATH)
X_test, y_test = load_ndwi_data(TEST_PATH)

#  Reshape for CNN input
X_train = X_train.reshape(-1, IMG_SIZE[0], IMG_SIZE[1], 1)
X_test = X_test.reshape(-1, IMG_SIZE[0], IMG_SIZE[1], 1)

# Define CNN Model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

#  Compile
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Callbacks
early_stopping = callbacks.EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True)
lr_scheduler = callbacks.LearningRateScheduler(lambda epoch, lr: lr * 0.5 if epoch > 0 and epoch % 100 == 0 else lr)

#  Train
history = model.fit(
    X_train, y_train,
    epochs=500,
    batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[early_stopping, lr_scheduler]
)

#  Save Model & Training History
os.makedirs("models", exist_ok=True)
model.save(MODEL_PATH)
np.save(HISTORY_PATH, history.history)

print(" Water Pollution Model trained & saved successfully!")
