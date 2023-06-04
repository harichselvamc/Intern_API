import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
import base64

def add_image_overlay(images, image_data_list):
    images_with_overlay = []

    for image, image_data in zip(images, image_data_list):
        img = Image.open(io.BytesIO(image))
        overlay = Image.new('RGBA', img.size)

        image_name = image_data['image_name']
        font_size = image_data['font_size']
        position = image_data['position']
        font_color = image_data.get('font_color', 'white')
        font = ImageFont.truetype('arial.ttf', font_size)

        if position == 'bottom-left':
            x = 10
            y = img.height - font_size - 10
        elif position == 'bottom-right':
            text_width, _ = font.getsize(image_name)
            x = img.width - text_width - 10
            y = img.height - font_size - 10
        else:
            x = 10
            y = 10

        draw = ImageDraw.Draw(overlay)
        draw.text((x, y), image_name, font=font, fill=font_color)

        img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
        images_with_overlay.append(img_with_overlay)

    return images_with_overlay


def resize_image(image, size):
    width, height = size
    return image.resize((width, height), resample=Image.LANCZOS)


def store_json_data(json_data):
    with open('history.json', 'a') as file:
        file.write(json_data + '\n')


def load_json_data():
    data = []
    with open('history.json', 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data


def save_to_history(data):
    image_name = data['image_name']
    font_size = data['font_size']
    position = data['position']
    font_color = data.get('font_color', 'white')
    altered_size = data.get('altered_size', None)

    image_data = {
        'image_name': image_name,
        'font_size': font_size,
        'position': position,
        'font_color': font_color,
        'altered_size': altered_size
    }

    store_json_data(json.dumps(image_data))
    return {"message": "Data saved to history.json"}


def generate_html(history_data):
    html = """
    <html>
    <head>
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    
    th, td {
        text-align: left;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    </style>
    </head>
    <body>
    
    <h2>History Data</h2>
    
    <table>
      <tr>
        <th>Image Name</th>
        <th>Font Size</th>
        <th>Position</th>
        <th>Font Color</th>
        <th>Altered Size</th>
      </tr>
    """

    for data in history_data:
        image_name = data['image_name']
        font_size = data['font_size']
        position = data['position']
        font_color = data.get('font_color', 'white')
        altered_size = data.get('altered_size', '')

        html += f"""
        <tr>
          <td>{image_name}</td>
          <td>{font_size}</td>
          <td>{position}</td>
          <td>{font_color}</td>
          <td>{altered_size}</td>
        </tr>
        """

    html += """
    </table>
    
    </body>
    </html>
    """
    
    return html


def main():
    st.title('Image Overlay API')

    uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    if uploaded_files:
        image_data_list = []
        images = [uploaded_file.read() for uploaded_file in uploaded_files]

        for i, uploaded_file in enumerate(uploaded_files):
            image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
            font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
            position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
            font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

            image_data_list.append({
                'image_name': image_name,
                'font_size': font_size,
                'position': position,
                'font_color': font_color
            })

        images_with_overlay = add_image_overlay(images, image_data_list)

        for i, image_with_overlay in enumerate(images_with_overlay):
            st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

            if st.checkbox(f"Resize Image {i+1}"):
                unique_key = f"resize_select_{i}"
                image_size = st.selectbox("Select Image Size", (
                    "Default", "1920x1080", "630x900", "720x1080", "900x1260",
                    "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
                    "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
                    "2800x3920", "3025x3850"
                ), key=unique_key)

                if image_size == "Default":
                    resized_image_with_overlay = image_with_overlay
                    altered_size = "Default"
                else:
                    width, height = map(int, image_size.split("x"))
                    resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
                    altered_size = image_size

                st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

                image_data_list[i]['altered_size'] = altered_size

        if st.button('Save to History'):
            for data in image_data_list:
                save_to_history(data)
            st.success('Data saved to history.json')

    if st.button('View History'):
        history_data = load_json_data()
        history_html = generate_html(history_data)
        st.write(history_html, unsafe_allow_html=True)

    if st.button('Download History HTML'):
        history_data = load_json_data()
        history_html = generate_html(history_data)
        b64 = base64.b64encode(history_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
        st.markdown(href, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
