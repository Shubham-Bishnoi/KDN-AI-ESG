import numpy as np
import rasterio
import os
import cv2
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#  Define Image Size & Paths
IMG_SIZE = (128, 128)
TRAIN_PATH = "data/deforestation/train"
TEST_PATH = "data/deforestation/test"
# MODEL_PATH = "models/deforestation_model.h5"

# Function to Load & Process TIFF Images (with Contrast Stretching)
def load_tiff_images(folder):
    images, labels = [], []
    for filename in os.listdir(folder):
        if filename.endswith(".tif"):  # Process only TIFF images
            file_path = os.path.join(folder, filename)
            with rasterio.open(file_path) as dataset:
                image = dataset.read(1)  # Read as grayscale
                image = (image - image.min()) / (image.max() - image.min() + 1e-7)  # Normalize (0-1)
                image_resized = cv2.resize(image, IMG_SIZE)  # Resize properly
                
                # Apply Contrast Stretching
                image_rescaled = (image_resized * 255).astype(np.uint8)  # Convert to 8-bit
                image_contrast = cv2.equalizeHist(image_rescaled)  # Apply histogram equalization
                
                images.append(image_contrast)
                labels.append(1 if "deforested" in filename else 0)  # Assign label
    return np.array(images), np.array(labels)

# Load Training & Testing Data
X_train, y_train = load_tiff_images(TRAIN_PATH)
X_test, y_test = load_tiff_images(TEST_PATH)

# Reshape Data for CNN Model (Add Channel Dimension)
X_train = X_train.reshape(-1, IMG_SIZE[0], IMG_SIZE[1], 1)
X_test = X_test.reshape(-1, IMG_SIZE[0], IMG_SIZE[1], 1)

#  Enhanced Data Augmentation
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.3,
    height_shift_range=0.3,
    brightness_range=[0.6, 1.4],
    zoom_range=0.3,
    horizontal_flip=True
)
train_generator = datagen.flow(X_train, y_train, batch_size=32, shuffle=True)

# CNN Model for Deforestation Detection
model = models.Sequential([
    layers.Conv2D(64, (3, 3), activation='relu', input_shape=(128, 128, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(512, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.5),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(1, activation='sigmoid')  # Binary classification
])

# Compile Model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='binary_crossentropy', metrics=['accuracy'])

# Learning Rate Scheduler
def scheduler(epoch, lr):
    if epoch % 50 == 0 and epoch != 0:
        return lr * 0.5  # Reduce LR every 50 epochs
    return lr

lr_callback = callbacks.LearningRateScheduler(scheduler)
early_stopping = callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
checkpoint = callbacks.ModelCheckpoint("models/best_model.keras", save_best_only=True, monitor='val_accuracy')


# Train Model with Augmented Data & Callbacks
history = model.fit(
    train_generator, epochs=300,
    validation_data=(X_test, y_test),
    callbacks=[lr_callback, early_stopping, checkpoint]
)

# Save Final Model
model.save("models/deforestation_model.h5")
print(" Deforestation Model Trained & Saved Successfully!")
