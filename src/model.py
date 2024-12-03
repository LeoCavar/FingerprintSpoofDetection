from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import cv2

def load_dataset(base_directory):
    feature_vectors = []
    labels = []
    for label, folder_name in enumerate(['real', 'fake_Altered-Hard']):
        folder_path = os.path.join(base_directory, folder_name)
        for image_filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_filename)
            try:
                image = load_img(image_path, target_size=(128, 128), color_mode='grayscale')
                image_array = img_to_array(image).astype(np.uint8).squeeze()
                enhanced_image = enhance_image(image_array)  
                feature_vectors.append(enhanced_image.flatten() / 255.0) 
                labels.append(label)
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
    return np.array(feature_vectors), np.array(labels)

def enhance_image(grayscale_image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(grayscale_image)

def train_and_evaluate(training_directory, testing_directory):
    print("Loading training data...")
    training_features, training_labels = load_dataset(training_directory)
    print("Balancing training data with SMOTE...")
    smote = SMOTE(random_state=42)
    balanced_features, balanced_labels = smote.fit_resample(training_features, training_labels)
    
    print("Loading test data...")
    testing_features, testing_labels = load_dataset(testing_directory)
    
    print("Training Random Forest model...")
    random_forest_model = RandomForestClassifier(
        n_estimators=200,       
        max_depth=20,           
        random_state=42,        
        class_weight={0: 3, 1: 1}  
    )
    random_forest_model.fit(balanced_features, balanced_labels)
    
    print("Evaluating the model...")
    predictions = random_forest_model.predict(testing_features)
    return classification_report(testing_labels, predictions, target_names=["Real", "Fake"])
