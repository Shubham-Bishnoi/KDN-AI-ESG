import os
import numpy as np
import rasterio
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator


aug_train_folder = "data/deforestation/augmented_train"
aug_test_folder = "data/deforestation/augmented_test"
os.makedirs(aug_train_folder, exist_ok=True)
os.makedirs(aug_test_folder, exist_ok=True)

datagen = ImageDataGenerator(
    rotation_range=45,  
    width_shift_range=0.3,  
    height_shift_range=0.3,  
    brightness_range=[0.6, 1.4],  
    zoom_range=0.3,  
    shear_range=0.2,  
    horizontal_flip=True  
)

def augment_images(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".tif"):
            file_path = os.path.join(input_folder, filename)

            with rasterio.open(file_path) as dataset:
                image = dataset.read(1)  

                image = (image - image.min()) / (image.max() - image.min() + 1e-7) * 255
                image = image.astype(np.uint8)  
                
                image = cv2.resize(image, (128, 128))

                # Reshape for augmentation
                image = image.reshape((1, 128, 128, 1))  

                i = 0
                for batch in datagen.flow(image, batch_size=1, save_to_dir=output_folder, 
                                          save_prefix="aug", save_format="jpg"):
                    i += 1
                    if i >= 5:  # Generate 5 augmentations per image
                        break  

#  Apply augmentation to train & test
augment_images("data/deforestation/train", aug_train_folder)
augment_images("data/deforestation/test", aug_test_folder)

print(" Data augmentation complete! Augmented images saved.")
