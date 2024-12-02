import os
import shutil
from sklearn.model_selection import train_test_split

def split_dataset(base_path, subfolder, output_dir, test_size=0.3):
    input_dir = os.path.join(base_path, subfolder)
    train_dir = os.path.join(output_dir, 'train', subfolder.replace('/', '_'))
    test_dir = os.path.join(output_dir, 'test', subfolder.replace('/', '_'))

    if os.path.exists(train_dir):
        shutil.rmtree(train_dir)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    images = os.listdir(input_dir)
    train_images, test_images = train_test_split(images, test_size=test_size, random_state=42)

    for image in train_images:
        shutil.copy(os.path.join(input_dir, image), os.path.join(train_dir, image))
    for image in test_images:
        shutil.copy(os.path.join(input_dir, image), os.path.join(test_dir, image))

    return len(train_images), len(test_images)
