import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
from fastapi import FastAPI

app = FastAPI()


def add_image_name_overlay(image, image_name, font_size, position):
    img = Image.open(io.BytesIO(image))
    overlay = Image.new('RGBA', img.size)
    text = image_name
    font = ImageFont.truetype('arial.ttf', font_size)
    text_color = (255, 255, 255, 128)  

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


def store_json_data(json_data):
    with open('history.json', 'a') as file:
        file.write(json_data + '\n')

def load_json_data():
    data = []
    with open('history.json', 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

@app.get("/history")
def get_history():
    history_data = load_json_data()
    return history_data

@app.post("/save")
def save_to_history(data: dict):
    json_data = json.dumps(data)
    store_json_data(json_data)
    return {"message": "Data saved to history.json"}

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

        response = {
            'image_name': image_name,
            'font_size': font_size,
            'position': position,
        }

      
        if st.button('Save'):
            save_to_history(response)
            st.success('Data saved to history.json')

       
        if st.button('Download Previewed Image'):
            img_bytes = io.BytesIO()
            image_with_overlay.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            st.download_button(
                label='Download Image',
                data=img_bytes,
                file_name='previewed_image.png',
                mime='image/png'
            )

        st.subheader('API Response')
        st.json(response)

        
        st.subheader('History Data')
        history_data = load_json_data()
        for data in history_data:
            st.write(data)

        current_url = st.experimental_get_query_params()
        query_params = []
        for key, value in current_url.items():
            query_params.append(f"{key}={value[0]}")
        query_string = "&".join(query_params)
        sharable_link = f"[Sharable Link](?{query_string})"
        st.markdown(sharable_link)

if __name__ == '__main__':
    main()

