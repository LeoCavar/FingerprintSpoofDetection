from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import cv2

def load_dataset(base_dir):
    X, y = [], []
    for label, folder in enumerate(['real', 'fake_Altered-Hard']):
        folder_path = os.path.join(base_dir, folder)
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            try:
                image = load_img(image_path, target_size=(128, 128), color_mode='grayscale')
                image_array = img_to_array(image).astype(np.uint8).squeeze()
                enhanced_image = enhance_image(image_array)  
                X.append(enhanced_image.flatten() / 255.0)  
                y.append(label)
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
    return np.array(X), np.array(y)

def enhance_image(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)

def train_and_evaluate(train_dir, test_dir):
    print("Loading training data...")
    X_train, y_train = load_dataset(train_dir)
    print("Balancing training data with SMOTE...")
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    print("Loading test data...")
    X_test, y_test = load_dataset(test_dir)
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, class_weight={0: 3, 1: 1})
    model.fit(X_train_balanced, y_train_balanced)
    print("Evaluating the model...")
    y_pred = model.predict(X_test)
    return classification_report(y_test, y_pred, target_names=["Real", "Fake"])
