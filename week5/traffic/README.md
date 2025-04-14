# Traffic Sign Classifier

## What the Project Does
This program looks at pictures of traffic signs and learns to tell which sign is which. It uses machine learning (a type of AI) to look at lots of example images and then guesses the correct sign when it sees a new one.

## How to Use It
1. Download and unzip the project code and the dataset (GTSRB).
2. Put the `gtsrb` folder inside the `traffic` folder.
3. Install the needed tools:
   ```bash
   pip3 install -r requirements.txt
   ```
4. Run the program like this:
   ```bash
   python traffic.py gtsrb
   ```
   If a trained model needs to be saved:
   ```bash
   python traffic.py gtsrb model.h5
   ```

## Project Explanation (Step-by-Step)

### Step 1: Load the Data
The `load_data` function is used.
- It checks each folder from 0 to 42. Each folder contains pictures of one traffic sign type.
- Each image is opened using OpenCV (cv2), resized to 30x30 pixels, and added to a list.
- The folder number (which is the label) is also stored in another list.
- The function returns two lists: one with images and one with labels.

### Step 2: Build the Model
The `get_model` function is used to create a model.
- TensorFlow is used to build a CNN (Convolutional Neural Network).
- The model includes:
  - 2 convolutional layers to help the model learn patterns in the images.
  - 2 pooling layers to reduce image size and speed up learning.
  - A flatten layer to convert the image to a simple list.
  - A dense (fully connected) layer to process the image.
  - A dropout layer to reduce overfitting.
  - An output layer with 43 units (one for each type of sign).
- The model is compiled using the 'adam' optimizer and 'categorical_crossentropy' loss.

### Step 3: Train and Test
- The images and labels are split into 60% training data and 40% testing data.
- The model is trained for 10 rounds (epochs).
- After training, the model is tested to check how well it learned.
- The model prints the accuracy score for the test data.
- If a filename is provided (e.g., model.h5), the model is saved to that file.

## What Was Learned
- How to use OpenCV to read and resize images.
- How to build a CNN using TensorFlow.
- The process of training and testing a machine learning model.
- How model accuracy improves over time.

## Final Results
After training for 10 epochs, the model reached about **95% accuracy** on the test data.

This project shows how a computer can learn to understand images using simple steps and common tools.

