import numpy as np
import pandas as pd
import tensorflow as tf
from keras.utils import to_categorical
import random
import os
import imghdr
import streamlit as st
import pickle as pk
import cv2
import requests
from PIL import Image
from io import BytesIO
import streamlit as st
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.image import resize
from tensorflow.keras.models import load_model, save_model


with st.sidebar:
    st.image("GreenSortAI_Logo.png", width=200)
    st.title("GreenSortAI")
    selection=st.radio("select your option",options=["upload an image", "Insert Image url"])


def download_and_save_image(image_url, save_path="downloaded_image.png"):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
    
        image_data = BytesIO(response.content)
        img = Image.open(image_data).convert("RGB")
        saved_img_path = "./" + save_path
        img.save(saved_img_path)
        img_array = np.array(img, dtype=np.float32)      # (H, W, 3)
        img_array = np.expand_dims(img_array, axis=0)
     
        loaded_model = load_model("latest_waste_classification_model.keras")

        if st.button("Predict"):
            prediction = loaded_model.predict(img_array)
            predicted_class = np.argmax(prediction)
    
            class_labels = ['Plastic', 'metal', 'paper']
            predicted_category = class_labels[predicted_class].lower()
            confidence = float(prediction[0][predicted_class]) * 100


            if predicted_category == "plastic":

                result=f"This Item is a {predicted_category} with {confidence:.2f}% confidence, it should be recycled"
                # Print the prediction
                st.success(result)
                st.image(img, caption=None)
            elif predicted_category == "metal":
                result=f"This Item is a {predicted_category} with {confidence:.2f}% confidence, it should be recycled"
                # Print the prediction
                st.success(result)
                st.image(img, caption=None)

            elif predicted_category == "paper":
                result=f"This Item is a {predicted_category} with {confidence:.2f}% confidence, it should be disposed"
                # Print the prediction
                st.success(result)
                st.image(img, caption=None)

            else:
                print("")

    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error Connecting: {errc}")
    except requests.exceptions.RequestException as err:
        st.error(f"Failed to download the image, The Image link is not a downloadble link")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def image_url_input():
    st.title("Classification with URL")
    image_url = st.text_input("Enter the image url and press enter", key="akaska")    
    # if st.button("Download Image"):
    if image_url != "":
        download_and_save_image(image_url)










def insert():
    st.title("Upload Image to Classify")
    

    # File uploader widget
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png","bmp"], key="upl")

    if uploaded_file is not None:
        # Convert the uploaded image to RGB
        img = Image.open(uploaded_file).convert("RGB")

        # Convert the resized image to an array
        img_array = np.array(img, dtype=np.float32)      # (H, W, 3)
        img_array = np.expand_dims(img_array, axis=0)
       


        # To load the model
        loaded_model = load_model("latest_waste_classification_model.keras")
        # Make the prediction
        
        if st.button("Predict"):
            prediction = loaded_model.predict(img_array)
            predicted_class = np.argmax(prediction)
    
            class_labels = ['Plastic', 'metal', 'paper']
            predicted_category = class_labels[predicted_class].lower()
            confidence = float(prediction[0][predicted_class]) * 100

            

            if predicted_category == "plastic":
                result=f"This Item is a {predicted_category} with {confidence:.2f}% confidence, it should be recycled"
                # Print the prediction
                st.success(result)
                st.image(img, caption=None)
            elif predicted_category == "metal":
                result=f"This Item is a {predicted_category} with {confidence:.2f}% confidence, it should be recycled"
                # Print the prediction
                st.success(result)
                st.image(img, caption=None)
           
            elif predicted_category == "paper":
                result=f"This Item is a {predicted_category} with {confidence:.2f}% confidence, it should be disposed"
                # Print the prediction
                st.success(result)
                st.image(img, caption=None)





if selection== "upload an image":
    insert()

if selection =="Insert Image url":
    image_url_input()

# if __name__ == "__main__":
#     main()
