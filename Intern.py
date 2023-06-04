import streamlit as st
import cv2
import numpy as np
import os
import urllib.parse

def process_image(image, name):
    # Load the image
    img = cv2.imread(image)

    # Add the image name overlay
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_corner = (10, img.shape[0] - 10)
    font_scale = 1
    font_color = (255, 255, 255)
    thickness = 2
    cv2.putText(img, name, bottom_left_corner, font, font_scale, font_color, thickness, cv2.LINE_AA)

    # Save the processed image
    output_path = "output.jpg"
    cv2.imwrite(output_path, img)

    return output_path

def generate_download_link(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
        base64_data = urllib.parse.quote(data)

    return f'<a href="data:image/jpg;base64,{base64_data}" download="processed_image.jpg">Download processed image</a>'

# Streamlit app
def main():
    st.title("Image Processing API")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        name = st.text_input("Enter image name")

        if st.button("Process"):
            processed_image = process_image(uploaded_file, name)
            download_link = generate_download_link(processed_image)
            st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
