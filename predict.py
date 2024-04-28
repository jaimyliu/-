import datetime
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# 001 違反規定 / 002 合乎規定
image1 = Image.open("003.png").convert("RGB")
image2 = Image.open("002.png").convert("RGB")
# resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image1 = ImageOps.fit(image1, size, Image.Resampling.LANCZOS)
image2 = ImageOps.fit(image2, size, Image.Resampling.LANCZOS)
# turn the image into a numpy array
image_array1 = np.asarray(image1)
image_array2 = np.asarray(image2)

# Normalize the image
normalized_image_array1 = (image_array1.astype(np.float32) / 127.5) - 1
normalized_image_array2 = (image_array2.astype(np.float32) / 127.5) - 1
# Load the image into the array
data[0] = normalized_image_array1

# Predicts the model
prediction = model.predict(data)
data[0] = normalized_image_array2
prediction2 = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

# Print prediction and confidence score
print("Class:", class_name[2:], end="")
print("Confidence Score:", confidence_score)

# Write to csv
f = open("log.csv", "a")
x = datetime.datetime.now()
formatted_time = x.strftime("%H:%M")
f.write(str(formatted_time) + "," + class_name[2:])
f.close() 
