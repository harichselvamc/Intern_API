import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
font_path = "/path/to/arial.ttf" 


def add_image_name_overlay(image, image_name, font_size, position):
    
    img = Image.open(io.BytesIO(image))

  
    overlay = Image.new('RGBA', img.size)
    
    text = image_name
    font = ImageFont.truetype(font_path, font_size)

    text_color = (255, 255, 255, 128)  # RGBA format, adjust the color as needed


    if position == 'bottom-left':
        x = 10
        y = img.height - font_size - 10
    elif position == 'bottom-right':
        text_width, _ = font.getsize(text)
        x = img.width - text_width - 10
        y = img.height - font_size - 10
    else:
        x = 10
        y = 10

   
    draw = ImageDraw.Draw(overlay)
    draw.text((x, y), text, font=font, fill=text_color)

   
    img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)

    return img_with_overlay

def create_downloadable_link(image):
    
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

  
    img_base64 = base64.b64encode(img_bytes.read()).decode()
    download_link = f'<a href="data:file/png;base64,{img_base64}" download="overlay_image.png">Download Overlay Image</a>'

    return download_link


def main():
    st.title('Image Overlay API')

   
    uploaded_file = st.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        
        image_name = st.text_input('Enter image name', value=uploaded_file.name)
        font_size = st.number_input('Overlay font size', min_value=1, value=20)
        position = st.selectbox('Overlay position', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))


        image_data = uploaded_file.read()
        image_with_overlay = add_image_name_overlay(image_data, image_name, font_size, position)

        
        st.image(image_with_overlay, caption='Image with Overlay', use_column_width=True)

        
        download_link = create_downloadable_link(image_with_overlay)
        st.markdown(download_link, unsafe_allow_html=True)


        response = {
            'image_name': image_name,
            'font_size': font_size,
            'position': position,
            'download_link': download_link
        }

       
        download_json = st.checkbox('Download JSON file')
        if download_json:
           
            json_data = json.dumps(response, indent=4)


            json_base64 = base64.b64encode(json_data.encode()).decode()
            json_download_link = f'<a href="data:application/json;base64,{json_base64}" download="overlay_image.json">Download JSON File</a>'
            st.markdown(json_download_link, unsafe_allow_html=True)

        
        st.subheader('API Response')
        st.json(response)

if __name__ == '__main__':
    main()
