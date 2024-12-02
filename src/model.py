import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import ADASYN
from preprocessing import preprocess_image

def load_dataset(base_dir):
    X, y = [], []
    for label, folder in enumerate(['real', 'fake_Altered-Hard']):
        folder_path = os.path.join(base_dir, folder)
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            try:
                image = preprocess_image(image_path)
                X.append(image.flatten())
                y.append(label)
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
    return np.array(X), np.array(y)

def train_and_evaluate(train_dir, test_dir):
    print("Loading training data...")
    X_train, y_train = load_dataset(train_dir)
    print("Loading test data...")
    X_test, y_test = load_dataset(test_dir)
    print("Applying ADASYN to balance the training data...")
    adasyn = ADASYN(random_state=42)
    X_train_balanced, y_train_balanced = adasyn.fit_resample(X_train, y_train)
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight={0: 3, 1: 1})
    model.fit(X_train_balanced, y_train_balanced)
    print("Evaluating the model...")
    y_pred = model.predict(X_test)
    return classification_report(y_test, y_pred, target_names=["Real", "Fake"])
