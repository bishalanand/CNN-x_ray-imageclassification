import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

IMAGE_SIZE = (100, 100)
CATEGORIES = ['Normal', 'Pneumonia']

model = load_model('x_ray_image_model.h5')
print('Model loaded successfully')

st.subheader('Upload an X-ray Image')

file = st.file_uploader(
    'Choose an image...',
    type=['jpg', 'png', 'jpeg']
)

if file is not None:
    image = Image.open(file).convert('L')  # grayscale
    st.image(image, caption='Uploaded Image', use_container_width=True)

    image = image.resize(IMAGE_SIZE)

    image_array = np.array(image) / 255.0

    image_array = np.expand_dims(image_array, axis=-1)  # (100,100,1)
    image_array = np.expand_dims(image_array, axis=0)   # (1,100,100,1)

    if st.button('Predict'):
        prediction = model.predict(image_array)

        pred_class = CATEGORIES[int(prediction[0][0] > 0.5)]

        st.write(
            f'This is a {pred_class} patient with '
            f'{prediction[0][0]*100:.2f}% prediction rate.'
        )