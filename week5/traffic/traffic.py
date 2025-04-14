import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43  # Total number of traffic sign types
TEST_SIZE = 0.4  # 40% of data will be used for testing


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []  # List to store image data
    labels = []  # List to store label (folder number)

    # Go through each category folder (0 to 42)
    for category in range(NUM_CATEGORIES):
        category_path = os.path.join(data_dir, str(category))  # Path to this category's folder
        for file in os.listdir(category_path):  # Go through each image in the folder
            file_path = os.path.join(category_path, file)
            try:
                img = cv2.imread(file_path)  # Read image using OpenCV
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))  # Resize image to 30x30 pixels
                images.append(img)  # Add image to list
                labels.append(category)  # Add label (folder number)
            except:
                continue  # Skip files that can't be read

    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([

        # First convolutional layer with 32 filters
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Second convolutional layer with 64 filters
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten the image to a 1D array
        tf.keras.layers.Flatten(),

        # Fully connected layer with 128 neurons
        tf.keras.layers.Dense(128, activation='relu'),

        # Dropout layer to prevent overfitting (randomly drops 50% of neurons)
        tf.keras.layers.Dropout(0.5),

        # Output layer with 43 neurons (one for each category), using softmax for probabilities
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    # Compile the model using Adam optimizer and categorical crossentropy loss
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


if __name__ == "__main__":
    main()
