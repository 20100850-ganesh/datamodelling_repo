import tensorflow as tf
import numpy as np
from PIL import Image

# Define the class labels
class_labels = ['bacterial_leaf_blight', 'bacterial_leaf_streak', 'brown_spot', 'grassy_stunt_virus',
                'healthy_rice_plant', 'narrow_brown_spot', 'ragged_stunt_virus', 'rice_blast',
                'rice_false_smut', 'sheath_blight', 'sheath_rot', 'stem_rot', 'tungro_virus']

# Set the input size for MobileNet
input_size = (224, 224)


def preprocess_image(image_file):
    # Open the uploaded image
    image = Image.open(image_file)

    # Resize the image to the input size for MobileNet
    image = image.resize(input_size)

    # Convert the image to a numpy array and scale the pixel values to the range [0, 1]
    image = np.array(image) / 255.0

    # Add a batch dimension to the preprocessed image
    image = np.expand_dims(image, axis=0)

    return image


def predict(image_file, model_name):
    # Load the trained model
    if model_name == 'MobileNet':
        model = tf.keras.models.load_model('models/MobileNet/saved_model.h5')
    elif model_name == 'DenseNet':
        model = tf.keras.models.load_model('models/DenseNet/saved_model.h5')
    else:
        return {'error': 'Invalid model name'}

    # Preprocess the uploaded image
    image = preprocess_image(image_file)

    # Make a prediction using the loaded model
    prediction = model.predict(image)

    # Get the index of the predicted class
    predicted_index = np.argmax(prediction)

    # Get the predicted class label
    predicted_class = class_labels[predicted_index]

    # Return the predicted class label as a dictionary
    return {'result': predicted_class}
