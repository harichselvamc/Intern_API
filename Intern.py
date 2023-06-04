# # # # # # # # # # # import streamlit as st
# # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # import io
# # # # # # # # # # # import json
# # # # # # # # # # # import base64

# # # # # # # # # # # from flask import Flask, jsonify, request

# # # # # # # # # # # app = Flask(__name__)

# # # # # # # # # # # def add_image_overlay(images, image_data_list):
# # # # # # # # # # #     images_with_overlay = []

# # # # # # # # # # #     for image, image_data in zip(images, image_data_list):
# # # # # # # # # # #         img = Image.open(io.BytesIO(image))
# # # # # # # # # # #         overlay = Image.new('RGBA', img.size)

# # # # # # # # # # #         image_name = image_data['image_name']
# # # # # # # # # # #         font_size = image_data['font_size']
# # # # # # # # # # #         position = image_data['position']
# # # # # # # # # # #         text_color = image_data['text_color']
# # # # # # # # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # # # # # # # #         if position == 'bottom-left':
# # # # # # # # # # #             x = 10
# # # # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # # # #         elif position == 'bottom-right':
# # # # # # # # # # #             text_width, _ = font.getsize(image_name)
# # # # # # # # # # #             x = img.width - text_width - 10
# # # # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # # # #         else:
# # # # # # # # # # #             x = 10
# # # # # # # # # # #             y = 10

# # # # # # # # # # #         draw = ImageDraw.Draw(overlay)
# # # # # # # # # # #         draw.text((x, y), image_name, font=font, fill=text_color)

# # # # # # # # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # # # # # # # #         images_with_overlay.append(img_with_overlay)

# # # # # # # # # # #     return images_with_overlay


# # # # # # # # # # # def resize_image(image, size):
# # # # # # # # # # #     width, height = size
# # # # # # # # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # # # # # # # def store_json_data(json_data):
# # # # # # # # # # #     with open('history.json', 'a') as file:
# # # # # # # # # # #         file.write(json_data + '\n')


# # # # # # # # # # # def load_json_data():
# # # # # # # # # # #     data = []
# # # # # # # # # # #     with open('history.json', 'r') as file:
# # # # # # # # # # #         for line in file:
# # # # # # # # # # #             data.append(json.loads(line))
# # # # # # # # # # #     return data


# # # # # # # # # # # def save_to_history(data):
# # # # # # # # # # #     image_name = data['image_name']
# # # # # # # # # # #     font_size = data['font_size']
# # # # # # # # # # #     position = data['position']
# # # # # # # # # # #     text_color = data['text_color']
# # # # # # # # # # #     altered_size = data.get('altered_size', None)

# # # # # # # # # # #     image_data = {
# # # # # # # # # # #         'image_name': image_name,
# # # # # # # # # # #         'font_size': font_size,
# # # # # # # # # # #         'position': position,
# # # # # # # # # # #         'text_color': text_color,
# # # # # # # # # # #         'altered_size': altered_size
# # # # # # # # # # #     }

# # # # # # # # # # #     store_json_data(json.dumps(image_data))
# # # # # # # # # # #     return {"message": "Data saved to history.json"}


# # # # # # # # # # # @app.route('/api/history', methods=['GET'])
# # # # # # # # # # # def get_history():
# # # # # # # # # # #     history_data = load_json_data()
# # # # # # # # # # #     return jsonify(history_data)


# # # # # # # # # # # @app.route('/api/image-overlay', methods=['POST'])
# # # # # # # # # # # def process_image_overlay():
# # # # # # # # # # #     uploaded_files = request.files.getlist('files')
# # # # # # # # # # #     image_data_list = json.loads(request.form.get('data'))

# # # # # # # # # # #     images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # # # # # # # # # #     images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # # # #     response_data = []

# # # # # # # # # # #     for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # # # #         resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
# # # # # # # # # # #         image_path = f"image_{i+1}.png"
# # # # # # # # # # #         resized_image_with_overlay.save(image_path, 'PNG')

# # # # # # # # # # #         with open(image_path, 'rb') as file:
# # # # # # # # # # #             image_data = file.read()

# # # # # # # # # # #         image_base64 = base64.b64encode(image_data).decode('utf-8')

# # # # # # # # # # #         response_data.append({
# # # # # # # # # # #             'image_name': image_data_list[i]['image_name'],
# # # # # # # # # # #             'image': image_base64
# # # # # # # # # # #         })

# # # # # # # # # # #     return jsonify(response_data)


# # # # # # # # # # # def main():
# # # # # # # # # # #     st.title('Image Overlay API')

# # # # # # # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # # # # # # #     if uploaded_files:
# # # # # # # # # # #         image_data_list = []
# # # # # # # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # # # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # # # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # # # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # # # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # # # # # # #             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

# # # # # # # # # # #             image_data_list.append({
# # # # # # # # # # #                 'image_name': image_name,
# # # # # # # # # # #                 'font_size': font_size,
# # # # # # # # # # #                 'position': position,
# # # # # # # # # # #                 'text_color': text_color
# # # # # # # # # # #             })

# # # # # # # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # # # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # # # # # # #                 unique_key = f"resize_select_{i}"
# # # # # # # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # # # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # # # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # # # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # # # # # # #                     "2800x3920", "3025x3850"
# # # # # # # # # # #                 ), key=unique_key)

# # # # # # # # # # #                 if image_size == "Default":
# # # # # # # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # # # # # # #                     altered_size = "Default"
# # # # # # # # # # #                 else:
# # # # # # # # # # #                     width, height = image_size.split("x")
# # # # # # # # # # #                     width = int(width)
# # # # # # # # # # #                     height = int(height)
# # # # # # # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # # # # # # #                     altered_size = image_size

# # # # # # # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # # # # # # # #                 image_path = f"image_{i+1}.png"
# # # # # # # # # # #                 resized_image_with_overlay.save(image_path, 'PNG')
# # # # # # # # # # #                 st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
# # # # # # # # # # #                                    mime='image/png')

# # # # # # # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # # # # # # #         if st.button('Save'):
# # # # # # # # # # #             for i, image_data in enumerate(image_data_list):
# # # # # # # # # # #                 image_data['image'] = base64.b64encode(images[i]).decode('utf-8')
# # # # # # # # # # #                 save_to_history(image_data)
# # # # # # # # # # #             st.success('Data saved to history.json')

# # # # # # # # # # #         st.subheader('API Response')
# # # # # # # # # # #         st.json(image_data_list)

# # # # # # # # # # #         st.subheader('History Data')
# # # # # # # # # # #         history_data = load_json_data()
# # # # # # # # # # #         for data in history_data:
# # # # # # # # # # #             st.write(data)


# # # # # # # # # # # if __name__ == '__main__':
# # # # # # # # # # #     main()


# # # # # # # # # # # # import streamlit as st
# # # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # # import io
# # # # # # # # # # # # import json
# # # # # # # # # # # # import base64
# # # # # # # # # # # # from flask import Flask, jsonify, request

# # # # # # # # # # # # app = Flask(__name__)

# # # # # # # # # # # # def add_image_overlay(images, image_data_list):
# # # # # # # # # # # #     images_with_overlay = []

# # # # # # # # # # # #     for image, image_data in zip(images, image_data_list):
# # # # # # # # # # # #         img = Image.open(io.BytesIO(image))
# # # # # # # # # # # #         overlay = Image.new('RGBA', img.size)

# # # # # # # # # # # #         image_name = image_data['image_name']
# # # # # # # # # # # #         font_size = image_data['font_size']
# # # # # # # # # # # #         position = image_data['position']
# # # # # # # # # # # #         text_color = image_data['text_color']
# # # # # # # # # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # # # # # # # # #         if position == 'bottom-left':
# # # # # # # # # # # #             x = 10
# # # # # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # # # # #         elif position == 'bottom-right':
# # # # # # # # # # # #             text_width, _ = font.getsize(image_name)
# # # # # # # # # # # #             x = img.width - text_width - 10
# # # # # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # # # # #         else:
# # # # # # # # # # # #             x = 10
# # # # # # # # # # # #             y = 10

# # # # # # # # # # # #         draw = ImageDraw.Draw(overlay)
# # # # # # # # # # # #         draw.text((x, y), image_name, font=font, fill=text_color)

# # # # # # # # # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # # # # # # # # #         images_with_overlay.append(img_with_overlay)

# # # # # # # # # # # #     return images_with_overlay


# # # # # # # # # # # # def resize_image(image, size):
# # # # # # # # # # # #     width, height = size
# # # # # # # # # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # # # # # # # # def store_json_data(json_data):
# # # # # # # # # # # #     with open('history.json', 'a') as file:
# # # # # # # # # # # #         file.write(json_data + '\n')


# # # # # # # # # # # # def load_json_data():
# # # # # # # # # # # #     data = []
# # # # # # # # # # # #     with open('history.json', 'r') as file:
# # # # # # # # # # # #         for line in file:
# # # # # # # # # # # #             data.append(json.loads(line))
# # # # # # # # # # # #     return data


# # # # # # # # # # # # def save_to_history(data):
# # # # # # # # # # # #     image_name = data['image_name']
# # # # # # # # # # # #     font_size = data['font_size']
# # # # # # # # # # # #     position = data['position']
# # # # # # # # # # # #     text_color = data['text_color']
# # # # # # # # # # # #     altered_size = data.get('altered_size', None)

# # # # # # # # # # # #     image_data = {
# # # # # # # # # # # #         'image_name': image_name,
# # # # # # # # # # # #         'font_size': font_size,
# # # # # # # # # # # #         'position': position,
# # # # # # # # # # # #         'text_color': text_color,
# # # # # # # # # # # #         'altered_size': altered_size
# # # # # # # # # # # #     }

# # # # # # # # # # # #     store_json_data(json.dumps(image_data))
# # # # # # # # # # # #     return {"message": "Data saved to history.json"}


# # # # # # # # # # # # @app.route('/api/history', methods=['GET'])
# # # # # # # # # # # # def get_history():
# # # # # # # # # # # #     history_data = load_json_data()
# # # # # # # # # # # #     return jsonify(history_data)


# # # # # # # # # # # # @app.route('/api/image-overlay', methods=['POST'])
# # # # # # # # # # # # def process_image_overlay():
# # # # # # # # # # # #     uploaded_files = request.files.getlist('files')
# # # # # # # # # # # #     image_data_list = json.loads(request.form.get('data'))

# # # # # # # # # # # #     images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # # # # # # # # # # #     images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # # # # #     response_data = []

# # # # # # # # # # # #     for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # # # # #         resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
# # # # # # # # # # # #         image_path = f"image_{i+1}.png"
# # # # # # # # # # # #         resized_image_with_overlay.save(image_path, 'PNG')

# # # # # # # # # # # #         with open(image_path, 'rb') as file:
# # # # # # # # # # # #             image_data = file.read()

# # # # # # # # # # # #         image_base64 = base64.b64encode(image_data).decode('utf-8')

# # # # # # # # # # # #         response_data.append({
# # # # # # # # # # # #             'image_name': image_data_list[i]['image_name'],
# # # # # # # # # # # #             'image': image_base64
# # # # # # # # # # # #         })

# # # # # # # # # # # #     return jsonify(response_data)


# # # # # # # # # # # # def generate_html(history_data):
# # # # # # # # # # # #     html = """
# # # # # # # # # # # #     <html>
# # # # # # # # # # # #     <head>
# # # # # # # # # # # #     <style>
# # # # # # # # # # # #     table {
# # # # # # # # # # # #         border-collapse: collapse;
# # # # # # # # # # # #         width: 100%;
# # # # # # # # # # # #     }
    
# # # # # # # # # # # #     th, td {
# # # # # # # # # # # #         text-align: left;
# # # # # # # # # # # #         padding: 8px;
# # # # # # # # # # # #         border-bottom: 1px solid #ddd;
# # # # # # # # # # # #     }
# # # # # # # # # # # #     </style>
# # # # # # # # # # # #     </head>
# # # # # # # # # # # #     <body>
    
# # # # # # # # # # # #     <h2>History Data</h2>
    
# # # # # # # # # # # #     <table>
# # # # # # # # # # # #       <tr>
# # # # # # # # # # # #         <th>Image Name</th>
# # # # # # # # # # # #         <th>Font Size</th>
# # # # # # # # # # # #         <th>Position</th>
# # # # # # # # # # # #         <th>Text Color</th>
# # # # # # # # # # # #         <th>Altered Size</th>
# # # # # # # # # # # #       </tr>
# # # # # # # # # # # #     """

# # # # # # # # # # # #     for data in history_data:
# # # # # # # # # # # #         image_name = data['image_name']
# # # # # # # # # # # #         font_size = data['font_size']
# # # # # # # # # # # #         position = data['position']
# # # # # # # # # # # #         text_color = data['text_color']
# # # # # # # # # # # #         altered_size = data['altered_size']
        
# # # # # # # # # # # #         html += f"""
# # # # # # # # # # # #         <tr>
# # # # # # # # # # # #           <td>{image_name}</td>
# # # # # # # # # # # #           <td>{font_size}</td>
# # # # # # # # # # # #           <td>{position}</td>
# # # # # # # # # # # #           <td>{text_color}</td>
# # # # # # # # # # # #           <td>{altered_size}</td>
# # # # # # # # # # # #         </tr>
# # # # # # # # # # # #         """

# # # # # # # # # # # #     html += """
# # # # # # # # # # # #     </table>
    
# # # # # # # # # # # #     </body>
# # # # # # # # # # # #     </html>
# # # # # # # # # # # #     """
    
# # # # # # # # # # # #     return html


# # # # # # # # # # # # def main():
# # # # # # # # # # # #     st.title('Image Overlay API')

# # # # # # # # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # # # # # # # #     if uploaded_files:
# # # # # # # # # # # #         image_data_list = []
# # # # # # # # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # # # # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # # # # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # # # # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # # # # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # # # # # # # #             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

# # # # # # # # # # # #             image_data_list.append({
# # # # # # # # # # # #                 'image_name': image_name,
# # # # # # # # # # # #                 'font_size': font_size,
# # # # # # # # # # # #                 'position': position,
# # # # # # # # # # # #                 'text_color': text_color
# # # # # # # # # # # #             })

# # # # # # # # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # # # # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # # # # # # # #                 unique_key = f"resize_select_{i}"
# # # # # # # # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # # # # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # # # # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # # # # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # # # # # # # #                     "2800x3920", "3025x3850"
# # # # # # # # # # # #                 ), key=unique_key)

# # # # # # # # # # # #                 if image_size == "Default":
# # # # # # # # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # # # # # # # #                     altered_size = "Default"
# # # # # # # # # # # #                 else:
# # # # # # # # # # # #                     width, height = map(int, image_size.split("x"))
# # # # # # # # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # # # # # # # #                     altered_size = image_size

# # # # # # # # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # # # # # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # # # # # # # #         if st.button('Save to History'):
# # # # # # # # # # # #             for data in image_data_list:
# # # # # # # # # # # #                 save_to_history(data)
# # # # # # # # # # # #             st.success('Data saved to history.json')

# # # # # # # # # # # #     if st.button('View History'):
# # # # # # # # # # # #         history_data = load_json_data()
# # # # # # # # # # # #         history_html = generate_html(history_data)
# # # # # # # # # # # #         st.write(history_html, unsafe_allow_html=True)

# # # # # # # # # # # #     if st.button('Download History HTML'):
# # # # # # # # # # # #         history_data = load_json_data()
# # # # # # # # # # # #         history_html = generate_html(history_data)
# # # # # # # # # # # #         b64 = base64.b64encode(history_html.encode()).decode()
# # # # # # # # # # # #         href = f'<a href="data:file/html;base64,{b64}" download="history.html">Click here to download history.html</a>'
# # # # # # # # # # # #         st.markdown(href, unsafe_allow_html=True)


# # # # # # # # # # # # if __name__ == '__main__':
# # # # # # # # # # # #     main()

# # # # # # # # # # # import streamlit as st
# # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # import io
# # # # # # # # # # # import json
# # # # # # # # # # # import base64
# # # # # # # # # # # from flask import Flask, jsonify, request
# # # # # # # # # # # from pyngrok import ngrok

# # # # # # # # # # # app = Flask(__name__)

# # # # # # # # # # # def add_image_overlay(images, image_data_list):
# # # # # # # # # # #     images_with_overlay = []

# # # # # # # # # # #     for image, image_data in zip(images, image_data_list):
# # # # # # # # # # #         img = Image.open(io.BytesIO(image))
# # # # # # # # # # #         overlay = Image.new('RGBA', img.size)

# # # # # # # # # # #         image_name = image_data['image_name']
# # # # # # # # # # #         font_size = image_data['font_size']
# # # # # # # # # # #         position = image_data['position']
# # # # # # # # # # #         text_color = image_data['text_color']
# # # # # # # # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # # # # # # # #         if position == 'bottom-left':
# # # # # # # # # # #             x = 10
# # # # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # # # #         elif position == 'bottom-right':
# # # # # # # # # # #             text_width, _ = font.getsize(image_name)
# # # # # # # # # # #             x = img.width - text_width - 10
# # # # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # # # #         else:
# # # # # # # # # # #             x = 10
# # # # # # # # # # #             y = 10

# # # # # # # # # # #         draw = ImageDraw.Draw(overlay)
# # # # # # # # # # #         draw.text((x, y), image_name, font=font, fill=text_color)

# # # # # # # # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # # # # # # # #         images_with_overlay.append(img_with_overlay)

# # # # # # # # # # #     return images_with_overlay


# # # # # # # # # # # def resize_image(image, size):
# # # # # # # # # # #     width, height = size
# # # # # # # # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # # # # # # # def store_json_data(json_data):
# # # # # # # # # # #     with open('history.json', 'a') as file:
# # # # # # # # # # #         file.write(json_data + '\n')


# # # # # # # # # # # def load_json_data():
# # # # # # # # # # #     data = []
# # # # # # # # # # #     with open('history.json', 'r') as file:
# # # # # # # # # # #         for line in file:
# # # # # # # # # # #             data.append(json.loads(line))
# # # # # # # # # # #     return data


# # # # # # # # # # # def save_to_history(data):
# # # # # # # # # # #     image_name = data['image_name']
# # # # # # # # # # #     font_size = data['font_size']
# # # # # # # # # # #     position = data['position']
# # # # # # # # # # #     text_color = data['text_color']
# # # # # # # # # # #     altered_size = data.get('altered_size', None)

# # # # # # # # # # #     image_data = {
# # # # # # # # # # #         'image_name': image_name,
# # # # # # # # # # #         'font_size': font_size,
# # # # # # # # # # #         'position': position,
# # # # # # # # # # #         'text_color': text_color,
# # # # # # # # # # #         'altered_size': altered_size
# # # # # # # # # # #     }

# # # # # # # # # # #     store_json_data(json.dumps(image_data))
# # # # # # # # # # #     return {"message": "Data saved to history.json"}


# # # # # # # # # # # @app.route('/api/history', methods=['GET'])
# # # # # # # # # # # def get_history():
# # # # # # # # # # #     history_data = load_json_data()
# # # # # # # # # # #     return jsonify(history_data)


# # # # # # # # # # # @app.route('/api/image-overlay', methods=['POST'])
# # # # # # # # # # # def process_image_overlay():
# # # # # # # # # # #     uploaded_files = request.files.getlist('files')
# # # # # # # # # # #     image_data_list = json.loads(request.form.get('data'))

# # # # # # # # # # #     images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # # # # # # # # # #     images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # # # #     response_data = []

# # # # # # # # # # #     for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # # # #         resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
# # # # # # # # # # #         image_path = f"image_{i+1}.png"
# # # # # # # # # # #         resized_image_with_overlay.save(image_path, 'PNG')

# # # # # # # # # # #         with open(image_path, 'rb') as file:
# # # # # # # # # # #             image_data = file.read()

# # # # # # # # # # #         image_base64 = base64.b64encode(image_data).decode('utf-8')

# # # # # # # # # # #         response_data.append({
# # # # # # # # # # #             'image_name': image_data_list[i]['image_name'],
# # # # # # # # # # #             'image': image_base64
# # # # # # # # # # #         })

# # # # # # # # # # #     return jsonify(response_data)


# # # # # # # # # # # def generate_html(history_data):
# # # # # # # # # # #     html = """
# # # # # # # # # # #     <html>
# # # # # # # # # # #     <head>
# # # # # # # # # # #     <style>
# # # # # # # # # # #     table {
# # # # # # # # # # #         border-collapse: collapse;
# # # # # # # # # # #         width: 100%;
# # # # # # # # # # #     }
    
# # # # # # # # # # #     th, td {
# # # # # # # # # # #         text-align: left;
# # # # # # # # # # #         padding: 8px;
# # # # # # # # # # #         border-bottom: 1px solid #ddd;
# # # # # # # # # # #     }
# # # # # # # # # # #     </style>
# # # # # # # # # # #     </head>
# # # # # # # # # # #     <body>
    
# # # # # # # # # # #     <h2>History Data</h2>
    
# # # # # # # # # # #     <table>
# # # # # # # # # # #       <tr>
# # # # # # # # # # #         <th>Image Name</th>
# # # # # # # # # # #         <th>Font Size</th>
# # # # # # # # # # #         <th>Position</th>
# # # # # # # # # # #         <th>Text Color</th>
# # # # # # # # # # #         <th>Altered Size</th>
# # # # # # # # # # #       </tr>
# # # # # # # # # # #     """

# # # # # # # # # # #     for data in history_data:
# # # # # # # # # # #         image_name = data['image_name']
# # # # # # # # # # #         font_size = data['font_size']
# # # # # # # # # # #         position = data['position']
# # # # # # # # # # #         text_color = data['text_color']
# # # # # # # # # # #         altered_size = data['altered_size']
        
# # # # # # # # # # #         html += f"""
# # # # # # # # # # #         <tr>
# # # # # # # # # # #           <td>{image_name}</td>
# # # # # # # # # # #           <td>{font_size}</td>
# # # # # # # # # # #           <td>{position}</td>
# # # # # # # # # # #           <td>{text_color}</td>
# # # # # # # # # # #           <td>{altered_size}</td>
# # # # # # # # # # #         </tr>
# # # # # # # # # # #         """

# # # # # # # # # # #     html += """
# # # # # # # # # # #     </table>
    
# # # # # # # # # # #     </body>
# # # # # # # # # # #     </html>
# # # # # # # # # # #     """
    
# # # # # # # # # # #     return html


# # # # # # # # # # # def main():
# # # # # # # # # # #     st.title('Image Overlay API')

# # # # # # # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # # # # # # #     if uploaded_files:
# # # # # # # # # # #         image_data_list = []
# # # # # # # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # # # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # # # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # # # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # # # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # # # # # # #             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

# # # # # # # # # # #             image_data_list.append({
# # # # # # # # # # #                 'image_name': image_name,
# # # # # # # # # # #                 'font_size': font_size,
# # # # # # # # # # #                 'position': position,
# # # # # # # # # # #                 'text_color': text_color
# # # # # # # # # # #             })

# # # # # # # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # # # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # # # # # # #                 unique_key = f"resize_select_{i}"
# # # # # # # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # # # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # # # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # # # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # # # # # # #                     "2800x3920", "3025x3850"
# # # # # # # # # # #                 ), key=unique_key)

# # # # # # # # # # #                 if image_size == "Default":
# # # # # # # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # # # # # # #                     altered_size = "Default"
# # # # # # # # # # #                 else:
# # # # # # # # # # #                     width, height = map(int, image_size.split("x"))
# # # # # # # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # # # # # # #                     altered_size = image_size

# # # # # # # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # # # # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # # # # # # #         if st.button('Save to History'):
# # # # # # # # # # #             for data in image_data_list:
# # # # # # # # # # #                 save_to_history(data)
# # # # # # # # # # #             st.success('Data saved to history.json')

# # # # # # # # # # #     if st.button('View History'):
# # # # # # # # # # #         history_data = load_json_data()
# # # # # # # # # # #         history_html = generate_html(history_data)
# # # # # # # # # # #         st.write(history_html, unsafe_allow_html=True)

# # # # # # # # # # #     if st.button('Download History HTML'):
# # # # # # # # # # #         history_data = load_json_data()
# # # # # # # # # # #         history_html = generate_html(history_data)
# # # # # # # # # # #         b64 = base64.b64encode(history_html.encode()).decode()
# # # # # # # # # # #         href = f'<a href="data:file/html;base64,{b64}" download="history.html">Click here to download history.html</a>'
# # # # # # # # # # #         st.markdown(href, unsafe_allow_html=True)


# # # # # # # # # # # if __name__ == '__main__':
# # # # # # # # # # #     app.run()


# # # # # # # # # # import streamlit as st
# # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # import io
# # # # # # # # # # import json
# # # # # # # # # # import base64
# # # # # # # # # # from flask import Flask, jsonify, request

# # # # # # # # # # app = Flask(__name__)

# # # # # # # # # # def add_image_overlay(images, image_data_list):
# # # # # # # # # #     images_with_overlay = []

# # # # # # # # # #     for image, image_data in zip(images, image_data_list):
# # # # # # # # # #         img = Image.open(io.BytesIO(image))
# # # # # # # # # #         overlay = Image.new('RGBA', img.size)

# # # # # # # # # #         image_name = image_data['image_name']
# # # # # # # # # #         font_size = image_data['font_size']
# # # # # # # # # #         position = image_data['position']
# # # # # # # # # #         text_color = image_data['text_color']
# # # # # # # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # # # # # # #         if position == 'bottom-left':
# # # # # # # # # #             x = 10
# # # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # # #         elif position == 'bottom-right':
# # # # # # # # # #             text_width, _ = font.getsize(image_name)
# # # # # # # # # #             x = img.width - text_width - 10
# # # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # # #         else:
# # # # # # # # # #             x = 10
# # # # # # # # # #             y = 10

# # # # # # # # # #         draw = ImageDraw.Draw(overlay)
# # # # # # # # # #         draw.text((x, y), image_name, font=font, fill=text_color)

# # # # # # # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # # # # # # #         images_with_overlay.append(img_with_overlay)

# # # # # # # # # #     return images_with_overlay


# # # # # # # # # # def resize_image(image, size):
# # # # # # # # # #     width, height = size
# # # # # # # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # # # # # # def store_json_data(json_data):
# # # # # # # # # #     with open('history.json', 'a') as file:
# # # # # # # # # #         file.write(json_data + '\n')


# # # # # # # # # # def load_json_data():
# # # # # # # # # #     data = []
# # # # # # # # # #     with open('history.json', 'r') as file:
# # # # # # # # # #         for line in file:
# # # # # # # # # #             data.append(json.loads(line))
# # # # # # # # # #     return data


# # # # # # # # # # def save_to_history(data):
# # # # # # # # # #     image_name = data['image_name']
# # # # # # # # # #     font_size = data['font_size']
# # # # # # # # # #     position = data['position']
# # # # # # # # # #     text_color = data['text_color']
# # # # # # # # # #     altered_size = data.get('altered_size', None)

# # # # # # # # # #     image_data = {
# # # # # # # # # #         'image_name': image_name,
# # # # # # # # # #         'font_size': font_size,
# # # # # # # # # #         'position': position,
# # # # # # # # # #         'text_color': text_color,
# # # # # # # # # #         'altered_size': altered_size
# # # # # # # # # #     }

# # # # # # # # # #     store_json_data(json.dumps(image_data))
# # # # # # # # # #     return {"message": "Data saved to history.json"}


# # # # # # # # # # @app.route('/api/history', methods=['GET'])
# # # # # # # # # # def get_history():
# # # # # # # # # #     history_data = load_json_data()
# # # # # # # # # #     return jsonify(history_data)


# # # # # # # # # # @app.route('/api/image-overlay', methods=['POST'])
# # # # # # # # # # def process_image_overlay():
# # # # # # # # # #     uploaded_files = request.files.getlist('files')
# # # # # # # # # #     image_data_list = json.loads(request.form.get('data'))

# # # # # # # # # #     images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # # # # # # # # #     images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # # #     response_data = []

# # # # # # # # # #     for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # # #         resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
# # # # # # # # # #         image_path = f"image_{i+1}.png"
# # # # # # # # # #         resized_image_with_overlay.save(image_path, 'PNG')

# # # # # # # # # #         with open(image_path, 'rb') as file:
# # # # # # # # # #             image_data = file.read()

# # # # # # # # # #         image_base64 = base64.b64encode(image_data).decode('utf-8')

# # # # # # # # # #         response_data.append({
# # # # # # # # # #             'image_name': image_data_list[i]['image_name'],
# # # # # # # # # #             'image': image_base64
# # # # # # # # # #         })

# # # # # # # # # #     return jsonify(response_data)


# # # # # # # # # # def generate_html(history_data):
# # # # # # # # # #     html = """
# # # # # # # # # #     <html>
# # # # # # # # # #     <head>
# # # # # # # # # #     <style>
# # # # # # # # # #     table {
# # # # # # # # # #         border-collapse: collapse;
# # # # # # # # # #         width: 100%;
# # # # # # # # # #     }
    
# # # # # # # # # #     th, td {
# # # # # # # # # #         text-align: left;
# # # # # # # # # #         padding: 8px;
# # # # # # # # # #         border-bottom: 1px solid #ddd;
# # # # # # # # # #     }
# # # # # # # # # #     </style>
# # # # # # # # # #     </head>
# # # # # # # # # #     <body>
    
# # # # # # # # # #     <h2>History Data</h2>
    
# # # # # # # # # #     <table>
# # # # # # # # # #       <tr>
# # # # # # # # # #         <th>Image Name</th>
# # # # # # # # # #         <th>Font Size</th>
# # # # # # # # # #         <th>Position</th>
# # # # # # # # # #         <th>Text Color</th>
# # # # # # # # # #         <th>Altered Size</th>
# # # # # # # # # #       </tr>
# # # # # # # # # #     """

# # # # # # # # # #     for data in history_data:
# # # # # # # # # #         image_name = data['image_name']
# # # # # # # # # #         font_size = data['font_size']
# # # # # # # # # #         position = data['position']
# # # # # # # # # #         text_color = data['text_color']
# # # # # # # # # #         altered_size = data['altered_size']
        
# # # # # # # # # #         html += f"""
# # # # # # # # # #         <tr>
# # # # # # # # # #           <td>{image_name}</td>
# # # # # # # # # #           <td>{font_size}</td>
# # # # # # # # # #           <td>{position}</td>
# # # # # # # # # #           <td>{text_color}</td>
# # # # # # # # # #           <td>{altered_size}</td>
# # # # # # # # # #         </tr>
# # # # # # # # # #         """

# # # # # # # # # #     html += """
# # # # # # # # # #     </table>
    
# # # # # # # # # #     </body>
# # # # # # # # # #     </html>
# # # # # # # # # #     """
    
# # # # # # # # # #     return html


# # # # # # # # # # def main():
# # # # # # # # # #     st.title('Image Overlay API')

# # # # # # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # # # # # #     if uploaded_files:
# # # # # # # # # #         image_data_list = []
# # # # # # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # # # # # #             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

# # # # # # # # # #             image_data_list.append({
# # # # # # # # # #                 'image_name': image_name,
# # # # # # # # # #                 'font_size': font_size,
# # # # # # # # # #                 'position': position,
# # # # # # # # # #                 'text_color': text_color
# # # # # # # # # #             })

# # # # # # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # # # # # #                 unique_key = f"resize_select_{i}"
# # # # # # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # # # # # #                     "2800x3920", "3025x3850"
# # # # # # # # # #                 ), key=unique_key)

# # # # # # # # # #                 if image_size == "Default":
# # # # # # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # # # # # #                     altered_size = "Default"
# # # # # # # # # #                 else:
# # # # # # # # # #                     width, height = map(int, image_size.split("x"))
# # # # # # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # # # # # #                     altered_size = image_size

# # # # # # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # # # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # # # # # #         if st.button('Save to History'):
# # # # # # # # # #             for data in image_data_list:
# # # # # # # # # #                 save_to_history(data)
# # # # # # # # # #             st.success('Data saved to history.json')

# # # # # # # # # #     if st.button('View History'):
# # # # # # # # # #         history_data = load_json_data()
# # # # # # # # # #         history_html = generate_html(history_data)
# # # # # # # # # #         st.write(history_html, unsafe_allow_html=True)

# # # # # # # # # #     if st.button('Download History HTML'):
# # # # # # # # # #         history_data = load_json_data()
# # # # # # # # # #         history_html = generate_html(history_data)
# # # # # # # # # #         b64 = base64.b64encode(history_html.encode()).decode()
# # # # # # # # # #         href = f'<a href="data:file/html;base64,{b64}" download="history.html">Click here to download history.html</a>'
# # # # # # # # # #         st.markdown(href, unsafe_allow_html=True)


# # # # # # # # # # if __name__ == '__main__':
# # # # # # # # # #     main()


# # # # # # # # # import streamlit as st
# # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # import io
# # # # # # # # # import json
# # # # # # # # # import base64
# # # # # # # # # from flask import Flask, jsonify, request

# # # # # # # # # app = Flask(__name__)

# # # # # # # # # def add_image_overlay(images, image_data_list):
# # # # # # # # #     images_with_overlay = []

# # # # # # # # #     for image, image_data in zip(images, image_data_list):
# # # # # # # # #         img = Image.open(io.BytesIO(image))
# # # # # # # # #         overlay = Image.new('RGBA', img.size)

# # # # # # # # #         image_name = image_data['image_name']
# # # # # # # # #         font_size = image_data['font_size']
# # # # # # # # #         position = image_data['position']
# # # # # # # # #         font_color = image_data['font_color']
# # # # # # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # # # # # #         if position == 'bottom-left':
# # # # # # # # #             x = 10
# # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # #         elif position == 'bottom-right':
# # # # # # # # #             text_width, _ = font.getsize(image_name)
# # # # # # # # #             x = img.width - text_width - 10
# # # # # # # # #             y = img.height - font_size - 10
# # # # # # # # #         else:
# # # # # # # # #             x = 10
# # # # # # # # #             y = 10

# # # # # # # # #         draw = ImageDraw.Draw(overlay)
# # # # # # # # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # # # # # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # # # # # #         images_with_overlay.append(img_with_overlay)

# # # # # # # # #     return images_with_overlay


# # # # # # # # # def resize_image(image, size):
# # # # # # # # #     width, height = size
# # # # # # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # # # # # def store_json_data(json_data):
# # # # # # # # #     with open('history.json', 'a') as file:
# # # # # # # # #         file.write(json_data + '\n')


# # # # # # # # # def load_json_data():
# # # # # # # # #     data = []
# # # # # # # # #     with open('history.json', 'r') as file:
# # # # # # # # #         for line in file:
# # # # # # # # #             data.append(json.loads(line))
# # # # # # # # #     return data


# # # # # # # # # def save_to_history(data):
# # # # # # # # #     image_name = data['image_name']
# # # # # # # # #     font_size = data['font_size']
# # # # # # # # #     position = data['position']
# # # # # # # # #     font_color = data['font_color']
# # # # # # # # #     altered_size = data.get('altered_size', None)

# # # # # # # # #     image_data = {
# # # # # # # # #         'image_name': image_name,
# # # # # # # # #         'font_size': font_size,
# # # # # # # # #         'position': position,
# # # # # # # # #         'font_color': font_color,
# # # # # # # # #         'altered_size': altered_size
# # # # # # # # #     }

# # # # # # # # #     store_json_data(json.dumps(image_data))
# # # # # # # # #     return {"message": "Data saved to history.json"}


# # # # # # # # # @app.route('/api/history', methods=['GET'])
# # # # # # # # # def get_history():
# # # # # # # # #     history_data = load_json_data()
# # # # # # # # #     return jsonify(history_data)


# # # # # # # # # @app.route('/api/image-overlay', methods=['POST'])
# # # # # # # # # def process_image_overlay():
# # # # # # # # #     uploaded_files = request.files.getlist('files')
# # # # # # # # #     image_data_list = json.loads(request.form.get('data'))

# # # # # # # # #     images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # # # # # # # #     images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # #     response_data = []

# # # # # # # # #     for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # #         resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
# # # # # # # # #         image_path = f"image_{i+1}.png"
# # # # # # # # #         resized_image_with_overlay.save(image_path, 'PNG')

# # # # # # # # #         with open(image_path, 'rb') as file:
# # # # # # # # #             image_data = file.read()

# # # # # # # # #         image_base64 = base64.b64encode(image_data).decode('utf-8')

# # # # # # # # #         response_data.append({
# # # # # # # # #             'image_name': image_data_list[i]['image_name'],
# # # # # # # # #             'image': image_base64
# # # # # # # # #         })

# # # # # # # # #     return jsonify(response_data)


# # # # # # # # # def generate_html(history_data):
# # # # # # # # #     html = """
# # # # # # # # #     <html>
# # # # # # # # #     <head>
# # # # # # # # #     <style>
# # # # # # # # #     table {
# # # # # # # # #         border-collapse: collapse;
# # # # # # # # #         width: 100%;
# # # # # # # # #     }
    
# # # # # # # # #     th, td {
# # # # # # # # #         text-align: left;
# # # # # # # # #         padding: 8px;
# # # # # # # # #         border-bottom: 1px solid #ddd;
# # # # # # # # #     }
# # # # # # # # #     </style>
# # # # # # # # #     </head>
# # # # # # # # #     <body>
    
# # # # # # # # #     <h2>History Data</h2>
    
# # # # # # # # #     <table>
# # # # # # # # #       <tr>
# # # # # # # # #         <th>Image Name</th>
# # # # # # # # #         <th>Font Size</th>
# # # # # # # # #         <th>Position</th>
# # # # # # # # #         <th>Font Color</th>
# # # # # # # # #         <th>Altered Size</th>
# # # # # # # # #       </tr>
# # # # # # # # #     """

# # # # # # # # #     for data in history_data:
# # # # # # # # #         image_name = data['image_name']
# # # # # # # # #         font_size = data['font_size']
# # # # # # # # #         position = data['position']
# # # # # # # # #         font_color = data['font_color']
# # # # # # # # #         altered_size = data['altered_size']
        
# # # # # # # # #         html += f"""
# # # # # # # # #         <tr>
# # # # # # # # #           <td>{image_name}</td>
# # # # # # # # #           <td>{font_size}</td>
# # # # # # # # #           <td>{position}</td>
# # # # # # # # #           <td>{font_color}</td>
# # # # # # # # #           <td>{altered_size}</td>
# # # # # # # # #         </tr>
# # # # # # # # #         """

# # # # # # # # #     html += """
# # # # # # # # #     </table>
    
# # # # # # # # #     </body>
# # # # # # # # #     </html>
# # # # # # # # #     """
    
# # # # # # # # #     return html


# # # # # # # # # def main():
# # # # # # # # #     st.title('Image Overlay API')

# # # # # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # # # # #     if uploaded_files:
# # # # # # # # #         image_data_list = []
# # # # # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # # # # #             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# # # # # # # # #             image_data_list.append({
# # # # # # # # #                 'image_name': image_name,
# # # # # # # # #                 'font_size': font_size,
# # # # # # # # #                 'position': position,
# # # # # # # # #                 'font_color': font_color
# # # # # # # # #             })

# # # # # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # # # # #                 unique_key = f"resize_select_{i}"
# # # # # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # # # # #                     "2800x3920", "3025x3850"
# # # # # # # # #                 ), key=unique_key)

# # # # # # # # #                 if image_size == "Default":
# # # # # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # # # # #                     altered_size = "Default"
# # # # # # # # #                 else:
# # # # # # # # #                     width, height = map(int, image_size.split("x"))
# # # # # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # # # # #                     altered_size = image_size

# # # # # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # # # # #         if st.button('Save to History'):
# # # # # # # # #             for data in image_data_list:
# # # # # # # # #                 save_to_history(data)
# # # # # # # # #             st.success('Data saved to history.json')

# # # # # # # # #     if st.button('View History'):
# # # # # # # # #         history_data = load_json_data()
# # # # # # # # #         history_html = generate_html(history_data)
# # # # # # # # #         st.write(history_html, unsafe_allow_html=True)

# # # # # # # # #     if st.button('Download History HTML'):
# # # # # # # # #         history_data = load_json_data()
# # # # # # # # #         history_html = generate_html(history_data)
# # # # # # # # #         b64 = base64.b64encode(history_html.encode()).decode()
# # # # # # # # #         href = f'<a href="data:file/html;base64,{b64}" download="history.html">Click here to download history.html</a>'
# # # # # # # # #         st.markdown(href, unsafe_allow_html=True)


# # # # # # # # # if __name__ == '__main__':
# # # # # # # # #     main()



# # # # # # # # import streamlit as st
# # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # import io
# # # # # # # # import json
# # # # # # # # import base64
# # # # # # # # from flask import Flask, jsonify, request

# # # # # # # # app = Flask(__name__)

# # # # # # # # def add_image_overlay(images, image_data_list):
# # # # # # # #     images_with_overlay = []

# # # # # # # #     for image, image_data in zip(images, image_data_list):
# # # # # # # #         img = Image.open(io.BytesIO(image))
# # # # # # # #         overlay = Image.new('RGBA', img.size)

# # # # # # # #         image_name = image_data['image_name']
# # # # # # # #         font_size = image_data['font_size']
# # # # # # # #         position = image_data['position']
# # # # # # # #         font_color = image_data['font_color']
# # # # # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # # # # #         if position == 'bottom-left':
# # # # # # # #             x = 10
# # # # # # # #             y = img.height - font_size - 10
# # # # # # # #         elif position == 'bottom-right':
# # # # # # # #             text_width, _ = font.getsize(image_name)
# # # # # # # #             x = img.width - text_width - 10
# # # # # # # #             y = img.height - font_size - 10
# # # # # # # #         else:
# # # # # # # #             x = 10
# # # # # # # #             y = 10

# # # # # # # #         draw = ImageDraw.Draw(overlay)
# # # # # # # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # # # # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # # # # #         images_with_overlay.append(img_with_overlay)

# # # # # # # #     return images_with_overlay


# # # # # # # # def resize_image(image, size):
# # # # # # # #     width, height = size
# # # # # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # # # # def store_json_data(json_data):
# # # # # # # #     with open('history.json', 'a') as file:
# # # # # # # #         file.write(json_data + '\n')


# # # # # # # # def load_json_data():
# # # # # # # #     data = []
# # # # # # # #     with open('history.json', 'r') as file:
# # # # # # # #         for line in file:
# # # # # # # #             data.append(json.loads(line))
# # # # # # # #     return data


# # # # # # # # def save_to_history(data):
# # # # # # # #     image_name = data['image_name']
# # # # # # # #     font_size = data['font_size']
# # # # # # # #     position = data['position']
# # # # # # # #     font_color = data['font_color']
# # # # # # # #     altered_size = data.get('altered_size', None)

# # # # # # # #     image_data = {
# # # # # # # #         'image_name': image_name,
# # # # # # # #         'font_size': font_size,
# # # # # # # #         'position': position,
# # # # # # # #         'font_color': font_color,
# # # # # # # #         'altered_size': altered_size
# # # # # # # #     }

# # # # # # # #     store_json_data(json.dumps(image_data))
# # # # # # # #     return {"message": "Data saved to history.json"}


# # # # # # # # @app.route('/api/history', methods=['GET'])
# # # # # # # # def get_history():
# # # # # # # #     history_data = load_json_data()
# # # # # # # #     return jsonify(history_data)


# # # # # # # # @app.route('/api/image-overlay', methods=['POST'])
# # # # # # # # def process_image_overlay():
# # # # # # # #     uploaded_files = request.files.getlist('files')
# # # # # # # #     image_data_list = json.loads(request.form.get('data'))

# # # # # # # #     images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # # # # # # #     images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # #     response_data = []

# # # # # # # #     for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # #         resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
# # # # # # # #         image_path = f"image_{i+1}.png"
# # # # # # # #         resized_image_with_overlay.save(image_path, 'PNG')

# # # # # # # #         with open(image_path, 'rb') as file:
# # # # # # # #             image_data = file.read()

# # # # # # # #         image_base64 = base64.b64encode(image_data).decode('utf-8')

# # # # # # # #         response_data.append({
# # # # # # # #             'image_name': image_data_list[i]['image_name'],
# # # # # # # #             'image': image_base64
# # # # # # # #         })

# # # # # # # #     return jsonify(response_data)


# # # # # # # # def generate_html(history_data):
# # # # # # # #     html = """
# # # # # # # #     <html>
# # # # # # # #     <head>
# # # # # # # #     <style>
# # # # # # # #     table {
# # # # # # # #         border-collapse: collapse;
# # # # # # # #         width: 100%;
# # # # # # # #     }
    
# # # # # # # #     th, td {
# # # # # # # #         text-align: left;
# # # # # # # #         padding: 8px;
# # # # # # # #         border-bottom: 1px solid #ddd;
# # # # # # # #     }
# # # # # # # #     </style>
# # # # # # # #     </head>
# # # # # # # #     <body>
    
# # # # # # # #     <h2>History Data</h2>
    
# # # # # # # #     <table>
# # # # # # # #       <tr>
# # # # # # # #         <th>Image Name</th>
# # # # # # # #         <th>Font Size</th>
# # # # # # # #         <th>Position</th>
# # # # # # # #         <th>Font Color</th>
# # # # # # # #         <th>Altered Size</th>
# # # # # # # #       </tr>
# # # # # # # #     """

# # # # # # # #     for data in history_data:
# # # # # # # #         image_name = data['image_name']
# # # # # # # #         font_size = data['font_size']
# # # # # # # #         position = data['position']
# # # # # # # #         font_color = data['font_color']
# # # # # # # #         altered_size = data['altered_size']
        
# # # # # # # #         html += f"""
# # # # # # # #         <tr>
# # # # # # # #           <td>{image_name}</td>
# # # # # # # #           <td>{font_size}</td>
# # # # # # # #           <td>{position}</td>
# # # # # # # #           <td>{font_color}</td>
# # # # # # # #           <td>{altered_size}</td>
# # # # # # # #         </tr>
# # # # # # # #         """

# # # # # # # #     html += """
# # # # # # # #     </table>
    
# # # # # # # #     </body>
# # # # # # # #     </html>
# # # # # # # #     """
    
# # # # # # # #     return html


# # # # # # # # def main():
# # # # # # # #     st.title('Image Overlay API')

# # # # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # # # #     if uploaded_files:
# # # # # # # #         image_data_list = []
# # # # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # # # #             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# # # # # # # #             image_data_list.append({
# # # # # # # #                 'image_name': image_name,
# # # # # # # #                 'font_size': font_size,
# # # # # # # #                 'position': position,
# # # # # # # #                 'font_color': font_color
# # # # # # # #             })

# # # # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # # # #                 unique_key = f"resize_select_{i}"
# # # # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # # # #                     "2800x3920", "3025x3850"
# # # # # # # #                 ), key=unique_key)

# # # # # # # #                 if image_size == "Default":
# # # # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # # # #                     altered_size = "Default"
# # # # # # # #                 else:
# # # # # # # #                     width, height = map(int, image_size.split("x"))
# # # # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # # # #                     altered_size = image_size

# # # # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # # # #         save_data = st.button('Save Data to History')
# # # # # # # #         if save_data:
# # # # # # # #             for data in image_data_list:
# # # # # # # #                 save_to_history(data)

# # # # # # # #             st.success("Data saved to history.json")

# # # # # # # #     history_html = generate_html(load_json_data())
# # # # # # # #     st.components.v1.html(history_html, width=800, height=600, scrolling=True)


# # # # # # # # if __name__ == '__main__':
# # # # # # # #     main()


# # # # # # # def generate_html(history_data):
# # # # # # #     html = """
# # # # # # #     <html>
# # # # # # #     <head>
# # # # # # #     <style>
# # # # # # #     table {
# # # # # # #         border-collapse: collapse;
# # # # # # #         width: 100%;
# # # # # # #     }
    
# # # # # # #     th, td {
# # # # # # #         text-align: left;
# # # # # # #         padding: 8px;
# # # # # # #         border-bottom: 1px solid #ddd;
# # # # # # #     }
# # # # # # #     </style>
# # # # # # #     </head>
# # # # # # #     <body>
    
# # # # # # #     <h2>History Data</h2>
    
# # # # # # #     <table>
# # # # # # #       <tr>
# # # # # # #         <th>Image Name</th>
# # # # # # #         <th>Font Size</th>
# # # # # # #         <th>Position</th>
# # # # # # #         <th>Font Color</th>
# # # # # # #         <th>Altered Size</th>
# # # # # # #       </tr>
# # # # # # #     """

# # # # # # #     for data in history_data:
# # # # # # #         image_name = data['image_name']
# # # # # # #         font_size = data['font_size']
# # # # # # #         position = data['position']
# # # # # # #         font_color = data.get('font_color', '')  # Use get() to provide a default value if key is missing
# # # # # # #         altered_size = data.get('altered_size', '')

# # # # # # #         html += f"""
# # # # # # #         <tr>
# # # # # # #           <td>{image_name}</td>
# # # # # # #           <td>{font_size}</td>
# # # # # # #           <td>{position}</td>
# # # # # # #           <td>{font_color}</td>
# # # # # # #           <td>{altered_size}</td>
# # # # # # #         </tr>
# # # # # # #         """

# # # # # # #     html += """
# # # # # # #     </table>
    
# # # # # # #     </body>
# # # # # # #     </html>
# # # # # # #     """
    
# # # # # # #     return html


# # # # # # # def main():
# # # # # # #     st.title('Image Overlay API')

# # # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # # #     if uploaded_files:
# # # # # # #         image_data_list = []
# # # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # # #             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# # # # # # #             image_data_list.append({
# # # # # # #                 'image_name': image_name,
# # # # # # #                 'font_size': font_size,
# # # # # # #                 'position': position,
# # # # # # #                 'font_color': font_color
# # # # # # #             })

# # # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # # #                 unique_key = f"resize_select_{i}"
# # # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # # #                     "2800x3920", "3025x3850"
# # # # # # #                 ), key=unique_key)

# # # # # # #                 if image_size == "Default":
# # # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # # #                     altered_size = "Default"
# # # # # # #                 else:
# # # # # # #                     width, height = map(int, image_size.split("x"))
# # # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # # #                     altered_size = image_size

# # # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # # #         save_data = st.button('Save Data to History')
# # # # # # #         if save_data:
# # # # # # #             for data in image_data_list:
# # # # # # #                 save_to_history(data)

# # # # # # #             st.success("Data saved to history.json")

# # # # # # #     history_html = generate_html(load_json_data())
# # # # # # #     st.components.v1.html(history_html, width=800, height=600, scrolling=True)


# # # # # # # if __name__ == '__main__':
# # # # # # #     main()
# # # # # # # import streamlit as st
# # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # import io
# # # # # # # import json
# # # # # # # import base64
# # # # # # # from flask import Flask, jsonify, request

# # # # # # # app = Flask(__name__)

# # # # # # # def add_image_overlay(images, image_data_list):
# # # # # # #     images_with_overlay = []

# # # # # # #     for image, image_data in zip(images, image_data_list):
# # # # # # #         img = Image.open(io.BytesIO(image))
# # # # # # #         overlay = Image.new('RGBA', img.size)

# # # # # # #         image_name = image_data['image_name']
# # # # # # #         font_size = image_data['font_size']
# # # # # # #         position = image_data['position']
# # # # # # #         font_color = image_data['font_color']
# # # # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # # # #         if position == 'bottom-left':
# # # # # # #             x = 10
# # # # # # #             y = img.height - font_size - 10
# # # # # # #         elif position == 'bottom-right':
# # # # # # #             text_width, _ = font.getsize(image_name)
# # # # # # #             x = img.width - text_width - 10
# # # # # # #             y = img.height - font_size - 10
# # # # # # #         else:
# # # # # # #             x = 10
# # # # # # #             y = 10

# # # # # # #         draw = ImageDraw.Draw(overlay)
# # # # # # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # # # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # # # #         images_with_overlay.append(img_with_overlay)

# # # # # # #     return images_with_overlay


# # # # # # # def resize_image(image, size):
# # # # # # #     width, height = size
# # # # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # # # def store_json_data(json_data):
# # # # # # #     with open('history.json', 'a') as file:
# # # # # # #         file.write(json_data + '\n')


# # # # # # # def load_json_data():
# # # # # # #     data = []
# # # # # # #     with open('history.json', 'r') as file:
# # # # # # #         for line in file:
# # # # # # #             data.append(json.loads(line))
# # # # # # #     return data


# # # # # # # def save_to_history(data):
# # # # # # #     image_name = data['image_name']
# # # # # # #     font_size = data['font_size']
# # # # # # #     position = data['position']
# # # # # # #     font_color = data['font_color']
# # # # # # #     altered_size = data.get('altered_size', None)

# # # # # # #     image_data = {
# # # # # # #         'image_name': image_name,
# # # # # # #         'font_size': font_size,
# # # # # # #         'position': position,
# # # # # # #         'font_color': font_color,
# # # # # # #         'altered_size': altered_size
# # # # # # #     }

# # # # # # #     store_json_data(json.dumps(image_data))
# # # # # # #     return {"message": "Data saved to history.json"}


# # # # # # # @app.route('/api/history', methods=['GET'])
# # # # # # # def get_history():
# # # # # # #     history_data = load_json_data()
# # # # # # #     return jsonify(history_data)


# # # # # # # @app.route('/api/image-overlay', methods=['POST'])
# # # # # # # def process_image_overlay():
# # # # # # #     uploaded_files = request.files.getlist('files')
# # # # # # #     image_data_list = json.loads(request.form.get('data'))

# # # # # # #     images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # # # # # #     images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # #     response_data = []

# # # # # # #     for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # #         resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
# # # # # # #         image_path = f"image_{i+1}.png"
# # # # # # #         resized_image_with_overlay.save(image_path, 'PNG')

# # # # # # #         with open(image_path, 'rb') as file:
# # # # # # #             image_data = file.read()

# # # # # # #         image_base64 = base64.b64encode(image_data).decode('utf-8')

# # # # # # #         response_data.append({
# # # # # # #             'image_name': image_data_list[i]['image_name'],
# # # # # # #             'image': image_base64
# # # # # # #         })

# # # # # # #     return jsonify(response_data)


# # # # # # # def generate_html(history_data):
# # # # # # #     html = """
# # # # # # #     <html>
# # # # # # #     <head>
# # # # # # #     <style>
# # # # # # #     table {
# # # # # # #         border-collapse: collapse;
# # # # # # #         width: 100%;
# # # # # # #     }
    
# # # # # # #     th, td {
# # # # # # #         text-align: left;
# # # # # # #         padding: 8px;
# # # # # # #         border-bottom: 1px solid #ddd;
# # # # # # #     }
# # # # # # #     </style>
# # # # # # #     </head>
# # # # # # #     <body>
    
# # # # # # #     <h2>History Data</h2>
    
# # # # # # #     <table>
# # # # # # #       <tr>
# # # # # # #         <th>Image Name</th>
# # # # # # #         <th>Font Size</th>
# # # # # # #         <th>Position</th>
# # # # # # #         <th>Font Color</th>
# # # # # # #         <th>Altered Size</th>
# # # # # # #       </tr>
# # # # # # #     """

# # # # # # #     for data in history_data:
# # # # # # #         image_name = data['image_name']
# # # # # # #         font_size = data['font_size']
# # # # # # #         position = data['position']
# # # # # # #         font_color = data['font_color']
# # # # # # #         altered_size = data['altered_size']
        
# # # # # # #         html += f"""
# # # # # # #         <tr>
# # # # # # #           <td>{image_name}</td>
# # # # # # #           <td>{font_size}</td>
# # # # # # #           <td>{position}</td>
# # # # # # #           <td>{font_color}</td>
# # # # # # #           <td>{altered_size}</td>
# # # # # # #         </tr>
# # # # # # #         """

# # # # # # #     html += """
# # # # # # #     </table>
    
# # # # # # #     </body>
# # # # # # #     </html>
# # # # # # #     """
    
# # # # # # #     return html


# # # # # # # def main():
# # # # # # #     st.title('Image Overlay API')

# # # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # # #     if uploaded_files:
# # # # # # #         image_data_list = []
# # # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # # #             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# # # # # # #             image_data_list.append({
# # # # # # #                 'image_name': image_name,
# # # # # # #                 'font_size': font_size,
# # # # # # #                 'position': position,
# # # # # # #                 'font_color': font_color
# # # # # # #             })

# # # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # # #                 unique_key = f"resize_select_{i}"
# # # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # # #                     "2800x3920", "3025x3850"
# # # # # # #                 ), key=unique_key)

# # # # # # #                 if image_size == "Default":
# # # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # # #                     altered_size = "Default"
# # # # # # #                 else:
# # # # # # #                     width, height = map(int, image_size.split("x"))
# # # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # # #                     altered_size = image_size

# # # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # # #         save_data = st.button('Save Data to History')
# # # # # # #         if save_data:
# # # # # # #             for data in image_data_list:
# # # # # # #                 save_to_history(data)

# # # # # # #             st.success("Data saved to history.json")

# # # # # # #     history_html = generate_html(load_json_data())
# # # # # # #     st.components.v1.html(history_html, width=800, height=600, scrolling=True)


# # # # # # # if __name__ == '__main__':
# # # # # # #     main()



# # # # # # import streamlit as st
# # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # import io
# # # # # # import json
# # # # # # import base64
# # # # # # from flask import Flask, jsonify, request

# # # # # # app = Flask(__name__)

# # # # # # def add_image_overlay(images, image_data_list):
# # # # # #     images_with_overlay = []

# # # # # #     for image, image_data in zip(images, image_data_list):
# # # # # #         img = Image.open(io.BytesIO(image))
# # # # # #         overlay = Image.new('RGBA', img.size)

# # # # # #         image_name = image_data['image_name']
# # # # # #         font_size = image_data['font_size']
# # # # # #         position = image_data['position']
# # # # # #         font_color = image_data.get('font_color', '#FFFFFF')
# # # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # # #         if position == 'bottom-left':
# # # # # #             x = 10
# # # # # #             y = img.height - font_size - 10
# # # # # #         elif position == 'bottom-right':
# # # # # #             text_width, _ = font.getsize(image_name)
# # # # # #             x = img.width - text_width - 10
# # # # # #             y = img.height - font_size - 10
# # # # # #         else:
# # # # # #             x = 10
# # # # # #             y = 10

# # # # # #         draw = ImageDraw.Draw(overlay)
# # # # # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # # #         images_with_overlay.append(img_with_overlay)

# # # # # #     return images_with_overlay


# # # # # # def resize_image(image, size):
# # # # # #     width, height = size
# # # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # # def store_json_data(json_data):
# # # # # #     with open('history.json', 'a') as file:
# # # # # #         file.write(json_data + '\n')


# # # # # # def load_json_data():
# # # # # #     data = []
# # # # # #     with open('history.json', 'r') as file:
# # # # # #         for line in file:
# # # # # #             data.append(json.loads(line))
# # # # # #     return data


# # # # # # def save_to_history(data):
# # # # # #     image_name = data['image_name']
# # # # # #     font_size = data['font_size']
# # # # # #     position = data['position']
# # # # # #     font_color = data.get('font_color', '#FFFFFF')
# # # # # #     altered_size = data.get('altered_size', None)

# # # # # #     image_data = {
# # # # # #         'image_name': image_name,
# # # # # #         'font_size': font_size,
# # # # # #         'position': position,
# # # # # #         'font_color': font_color,
# # # # # #         'altered_size': altered_size
# # # # # #     }

# # # # # #     store_json_data(json.dumps(image_data))
# # # # # #     return {"message": "Data saved to history.json"}


# # # # # # @app.route('/api/history', methods=['GET'])
# # # # # # def get_history():
# # # # # #     history_data = load_json_data()
# # # # # #     return jsonify(history_data)


# # # # # # @app.route('/api/image-overlay', methods=['POST'])
# # # # # # def process_image_overlay():
# # # # # #     uploaded_files = request.files.getlist('files')
# # # # # #     image_data_list = json.loads(request.form.get('data'))

# # # # # #     images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # # # # #     images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # #     response_data = []

# # # # # #     for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # #         resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
# # # # # #         image_path = f"image_{i+1}.png"
# # # # # #         resized_image_with_overlay.save(image_path, 'PNG')

# # # # # #         with open(image_path, 'rb') as file:
# # # # # #             image_data = file.read()

# # # # # #         image_base64 = base64.b64encode(image_data).decode('utf-8')

# # # # # #         response_data.append({
# # # # # #             'image_name': image_data_list[i]['image_name'],
# # # # # #             'image': image_base64
# # # # # #         })

# # # # # #     return jsonify(response_data)


# # # # # # def generate_html(history_data):
# # # # # #     html = """
# # # # # #     <html>
# # # # # #     <head>
# # # # # #     <style>
# # # # # #     table {
# # # # # #         border-collapse: collapse;
# # # # # #         width: 100%;
# # # # # #     }
    
# # # # # #     th, td {
# # # # # #         text-align: left;
# # # # # #         padding: 8px;
# # # # # #         border-bottom: 1px solid #ddd;
# # # # # #     }
# # # # # #     </style>
# # # # # #     </head>
# # # # # #     <body>
    
# # # # # #     <h2>History Data</h2>
    
# # # # # #     <table>
# # # # # #       <tr>
# # # # # #         <th>Image Name</th>
# # # # # #         <th>Font Size</th>
# # # # # #         <th>Position</th>
# # # # # #         <th>Font Color</th>
# # # # # #         <th>Altered Size</th>
# # # # # #       </tr>
# # # # # #     """

# # # # # #     for data in history_data:
# # # # # #         image_name = data.get('image_name', '')
# # # # # #         font_size = data.get('font_size', '')
# # # # # #         position = data.get('position', '')
# # # # # #         font_color = data.get('font_color', '')
# # # # # #         altered_size = data.get('altered_size', '')
        
# # # # # #         html += f"""
# # # # # #         <tr>
# # # # # #           <td>{image_name}</td>
# # # # # #           <td>{font_size}</td>
# # # # # #           <td>{position}</td>
# # # # # #           <td>{font_color}</td>
# # # # # #           <td>{altered_size}</td>
# # # # # #         </tr>
# # # # # #         """

# # # # # #     html += """
# # # # # #     </table>
    
# # # # # #     </body>
# # # # # #     </html>
# # # # # #     """
    
# # # # # #     return html


# # # # # # def main():
# # # # # #     st.title('Image Overlay API')

# # # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # # #     if uploaded_files:
# # # # # #         image_data_list = []
# # # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # # #             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# # # # # #             image_data_list.append({
# # # # # #                 'image_name': image_name,
# # # # # #                 'font_size': font_size,
# # # # # #                 'position': position,
# # # # # #                 'font_color': font_color
# # # # # #             })

# # # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # # #                 unique_key = f"resize_select_{i}"
# # # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # # #                     "2800x3920", "3025x3850"
# # # # # #                 ), key=unique_key)

# # # # # #                 if image_size == "Default":
# # # # # #                     resized_image_with_overlay = image_with_overlay
# # # # # #                     altered_size = "Default"
# # # # # #                 else:
# # # # # #                     width, height = map(int, image_size.split("x"))
# # # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # # #                     altered_size = image_size

# # # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1} ({altered_size})", use_column_width=True)
# # # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # # #         if st.button('Save Data to History'):
# # # # # #             for data in image_data_list:
# # # # # #                 save_to_history(data)

# # # # # #             st.success('Data saved to history.json')

# # # # # #     if st.button('Show History'):
# # # # # #         history_data = load_json_data()
# # # # # #         st.write(history_data)
# # # # # #         st.markdown(_html(history_data), unsafe_allow_html=True)


# # # # # # if __name__ == '__main__':
# # # # # #     main()

# # # # # import streamlit as st
# # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # import io
# # # # # import json
# # # # # import base64
# # # # # import requests

# # # # # API_KEY = "rnd_xSW5VaQqrhpJnae5ac3eEg7VZrnu"
# # # # # API_URL = "https://api.render.com/v1/services?limit=20"

# # # # # def add_image_overlay(images, image_data_list):
# # # # #     images_with_overlay = []

# # # # #     for image, image_data in zip(images, image_data_list):
# # # # #         img = Image.open(io.BytesIO(image))
# # # # #         overlay = Image.new('RGBA', img.size)

# # # # #         image_name = image_data['image_name']
# # # # #         font_size = image_data['font_size']
# # # # #         position = image_data['position']
# # # # #         font_color = image_data['font_color']
# # # # #         font = ImageFont.truetype('./arial.ttf', font_size)

# # # # #         if position == 'bottom-left':
# # # # #             x = 10
# # # # #             y = img.height - font_size - 10
# # # # #         elif position == 'bottom-right':
# # # # #             text_width, _ = font.getsize(image_name)
# # # # #             x = img.width - text_width - 10
# # # # #             y = img.height - font_size - 10
# # # # #         else:
# # # # #             x = 10
# # # # #             y = 10

# # # # #         draw = ImageDraw.Draw(overlay)
# # # # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # # #         images_with_overlay.append(img_with_overlay)

# # # # #     return images_with_overlay


# # # # # def resize_image(image, size):
# # # # #     width, height = size
# # # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # # def store_json_data(json_data):
# # # # #     with open('history.json', 'a') as file:
# # # # #         file.write(json_data + '\n')


# # # # # def load_json_data():
# # # # #     data = []
# # # # #     with open('history.json', 'r') as file:
# # # # #         for line in file:
# # # # #             data.append(json.loads(line))
# # # # #     return data


# # # # # def save_to_history(data):
# # # # #     image_name = data['image_name']
# # # # #     font_size = data['font_size']
# # # # #     position = data['position']
# # # # #     font_color = data['font_color']
# # # # #     altered_size = data.get('altered_size', None)

# # # # #     image_data = {
# # # # #         'image_name': image_name,
# # # # #         'font_size': font_size,
# # # # #         'position': position,
# # # # #         'font_color': font_color,
# # # # #         'altered_size': altered_size
# # # # #     }

# # # # #     store_json_data(json.dumps(image_data))
# # # # #     return {"message": "Data saved to history.json"}


# # # # # def generate_html(history_data):
# # # # #     html = """
# # # # #     <html>
# # # # #     <head>
# # # # #     <style>
# # # # #     table {
# # # # #         border-collapse: collapse;
# # # # #         width: 100%;
# # # # #     }
    
# # # # #     th, td {
# # # # #         text-align: left;
# # # # #         padding: 8px;
# # # # #         border-bottom: 1px solid #ddd;
# # # # #     }
# # # # #     </style>
# # # # #     </head>
# # # # #     <body>
    
# # # # #     <h2>History Data</h2>
    
# # # # #     <table>
# # # # #       <tr>
# # # # #         <th>Image Name</th>
# # # # #         <th>Font Size</th>
# # # # #         <th>Position</th>
# # # # #         <th>Font Color</th>
# # # # #         <th>Altered Size</th>
# # # # #       </tr>
# # # # #     """

# # # # #     for data in history_data:
# # # # #         image_name = data['image_name']
# # # # #         font_size = data['font_size']
# # # # #         position = data['position']
# # # # #         font_color = data['font_color']
# # # # #         altered_size = data['altered_size']
        
# # # # #         html += f"""
# # # # #         <tr>
# # # # #           <td>{image_name}</td>
# # # # #           <td>{font_size}</td>
# # # # #           <td>{position}</td>
# # # # #           <td>{font_color}</td>
# # # # #           <td>{altered_size}</td>
# # # # #         </tr>
# # # # #         """

# # # # #     html += """
# # # # #     </table>
    
# # # # #     </body>
# # # # #     </html>
# # # # #     """
    
# # # # #     return html


# # # # # def main():
# # # # #     st.title('Image Overlay API')

# # # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # # #     if uploaded_files:
# # # # #         image_data_list = []
# # # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # # #             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# # # # #             image_data_list.append({
# # # # #                 'image_name': image_name,
# # # # #                 'font_size': font_size,
# # # # #                 'position': position,
# # # # #                 'font_color': font_color
# # # # #             })

# # # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # # #                 unique_key = f"resize_select_{i}"
# # # # #                 image_size = st.selectbox("Select Image Size", (
# # # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # # #                     "2800x3920", "3025x3850"
# # # # #                 ), key=unique_key)

# # # # #                 if image_size == "Default":
# # # # #                     resized_image_with_overlay = image_with_overlay
# # # # #                     altered_size = "Default"
# # # # #                 else:
# # # # #                     width, height = map(int, image_size.split("x"))
# # # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # # #                     altered_size = image_size

# # # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # # #                 image_data_list[i]['altered_size'] = altered_size

# # # # #         if st.button('Save to History'):
# # # # #             for data in image_data_list:
# # # # #                 save_to_history(data)
# # # # #             st.success('Data saved to history.json')

# # # # #     if st.button('View History'):
# # # # #         history_data = load_json_data()
# # # # #         history_html = generate_html(history_data)
# # # # #         st.write(history_html, unsafe_allow_html=True)

# # # # #     if st.button('Download History HTML'):
# # # # #         history_data = load_json_data()
# # # # #         history_html = generate_html(history_data)
# # # # #         b64 = base64.b64encode(history_html.encode()).decode()
# # # # #         href = f'<a href="data:file/html;base64,{b64}" download="history.html">Click here to download history.html</a>'
# # # # #         st.markdown(href, unsafe_allow_html=True)


# # # # # if __name__ == '__main__':
# # # # #     main()


# # # # # import requests

# # # # # api_key = "rnd_xSW5VaQqrhpJnae5ac3eEg7VZrnu"
# # # # # url = "https://api.render.com/v1/services?limit=20"
# # # # # headers = {
# # # # #     "Accept": "application/json",
# # # # #     "Authorization": f"Bearer {api_key}"
# # # # # }

# # # # # response = requests.get(url, headers=headers)
# # # # # data = response.json()

# # # # # print(data)
# # # # import streamlit as st
# # # # from PIL import Image, ImageDraw, ImageFont
# # # # import io
# # # # import json
# # # # import base64

# # # # def add_image_overlay(images, image_data_list):
# # # #     images_with_overlay = []

# # # #     for image, image_data in zip(images, image_data_list):
# # # #         img = Image.open(io.BytesIO(image))
# # # #         overlay = Image.new('RGBA', img.size)

# # # #         image_name = image_data['image_name']
# # # #         font_size = image_data['font_size']
# # # #         position = image_data['position']
# # # #         font_color = image_data.get('font_color', 'white')
# # # #         font = ImageFont.truetype('arial.ttf', font_size)

# # # #         if position == 'bottom-left':
# # # #             x = 10
# # # #             y = img.height - font_size - 10
# # # #         elif position == 'bottom-right':
# # # #             text_width, _ = font.getsize(image_name)
# # # #             x = img.width - text_width - 10
# # # #             y = img.height - font_size - 10
# # # #         else:
# # # #             x = 10
# # # #             y = 10

# # # #         draw = ImageDraw.Draw(overlay)
# # # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # # #         images_with_overlay.append(img_with_overlay)

# # # #     return images_with_overlay


# # # # def resize_image(image, size):
# # # #     width, height = size
# # # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # # def store_json_data(json_data):
# # # #     with open('history.json', 'a') as file:
# # # #         file.write(json_data + '\n')


# # # # def load_json_data():
# # # #     data = []
# # # #     with open('history.json', 'r') as file:
# # # #         for line in file:
# # # #             data.append(json.loads(line))
# # # #     return data


# # # # def save_to_history(data):
# # # #     image_name = data['image_name']
# # # #     font_size = data['font_size']
# # # #     position = data['position']
# # # #     font_color = data.get('font_color', 'white')
# # # #     altered_size = data.get('altered_size', None)

# # # #     image_data = {
# # # #         'image_name': image_name,
# # # #         'font_size': font_size,
# # # #         'position': position,
# # # #         'font_color': font_color,
# # # #         'altered_size': altered_size
# # # #     }

# # # #     store_json_data(json.dumps(image_data))
# # # #     return {"message": "Data saved to history.json"}


# # # # def generate_html(history_data):
# # # #     html = """
# # # #     <html>
# # # #     <head>
# # # #     <style>
# # # #     table {
# # # #         border-collapse: collapse;
# # # #         width: 100%;
# # # #     }
    
# # # #     th, td {
# # # #         text-align: left;
# # # #         padding: 8px;
# # # #         border-bottom: 1px solid #ddd;
# # # #     }
# # # #     </style>
# # # #     </head>
# # # #     <body>
    
# # # #     <h2>History Data</h2>
    
# # # #     <table>
# # # #       <tr>
# # # #         <th>Image Name</th>
# # # #         <th>Font Size</th>
# # # #         <th>Position</th>
# # # #         <th>Font Color</th>
# # # #         <th>Altered Size</th>
# # # #       </tr>
# # # #     """

# # # #     for data in history_data:
# # # #         image_name = data['image_name']
# # # #         font_size = data['font_size']
# # # #         position = data['position']
# # # #         font_color = data['font_color']
# # # #         altered_size = data['altered_size']
        
# # # #         html += f"""
# # # #         <tr>
# # # #           <td>{image_name}</td>
# # # #           <td>{font_size}</td>
# # # #           <td>{position}</td>
# # # #           <td>{font_color}</td>
# # # #           <td>{altered_size}</td>
# # # #         </tr>
# # # #         """

# # # #     html += """
# # # #     </table>
    
# # # #     </body>
# # # #     </html>
# # # #     """
    
# # # #     return html


# # # # def main():
# # # #     st.title('Image Overlay API')

# # # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # # #     if uploaded_files:
# # # #         image_data_list = []
# # # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # # #         for i, uploaded_file in enumerate(uploaded_files):
# # # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# # # #             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# # # #             image_data_list.append({
# # # #                 'image_name': image_name,
# # # #                 'font_size': font_size,
# # # #                 'position': position,
# # # #                 'font_color': font_color
# # # #             })

# # # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # # #             if st.checkbox(f"Resize Image {i+1}"):
# # # #                 unique_key = f"resize_select_{i}"
# # # #                 image_size = st.selectbox("Select Image Size", (
# # # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # # #                     "2800x3920", "3025x3850"
# # # #                 ), key=unique_key)

# # # #                 if image_size == "Default":
# # # #                     resized_image_with_overlay = image_with_overlay
# # # #                     altered_size = "Default"
# # # #                 else:
# # # #                     width, height = map(int, image_size.split("x"))
# # # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # # #                     altered_size = image_size

# # # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # # #                 image_data_list[i]['altered_size'] = altered_size

# # # #         if st.button('Save to History'):
# # # #             for data in image_data_list:
# # # #                 save_to_history(data)
# # # #             st.success('Data saved to history.json')

# # # #     if st.button('View History'):
# # # #         history_data = load_json_data()
# # # #         history_html = generate_html(history_data)
# # # #         st.write(history_html, unsafe_allow_html=True)

# # # #     if st.button('Download History HTML'):
# # # #         history_data = load_json_data()
# # # #         history_html = generate_html(history_data)
# # # #         b64 = base64.b64encode(history_html.encode()).decode()
# # # #         href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
# # # #         st.markdown(href, unsafe_allow_html=True)


# # # # if __name__ == '__main__':
# # # #     main()

# # # import streamlit as st
# # # from PIL import Image, ImageDraw, ImageFont
# # # import io
# # # import json
# # # import base64

# # # def add_image_overlay(images, image_data_list):
# # #     images_with_overlay = []

# # #     for image, image_data in zip(images, image_data_list):
# # #         img = Image.open(io.BytesIO(image))
# # #         overlay = Image.new('RGBA', img.size)

# # #         image_name = image_data['image_name']
# # #         font_size = image_data['font_size']
# # #         position = image_data['position']
# # #         font_color = image_data.get('font_color', 'white')
# # #         font = ImageFont.truetype('arial.ttf', font_size)

# # #         if position == 'bottom-left':
# # #             x = 10
# # #             y = img.height - font_size - 10
# # #         elif position == 'bottom-right':
# # #             text_width, _ = font.getsize(image_name)
# # #             x = img.width - text_width - 10
# # #             y = img.height - font_size - 10
# # #         else:
# # #             x = 10
# # #             y = 10

# # #         draw = ImageDraw.Draw(overlay)
# # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # #         images_with_overlay.append(img_with_overlay)

# # #     return images_with_overlay


# # # def resize_image(image, size):
# # #     width, height = size
# # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # def store_json_data(json_data):
# # #     with open('history.json', 'a') as file:
# # #         file.write(json_data + '\n')


# # # def load_json_data():
# # #     data = []
# # #     with open('history.json', 'r') as file:
# # #         for line in file:
# # #             data.append(json.loads(line))
# # #     return data


# # # def save_to_history(data):
# # #     image_name = data['image_name']
# # #     font_size = data['font_size']
# # #     position = data['position']
# # #     font_color = data.get('font_color', 'white')
# # #     altered_size = data.get('altered_size', None)

# # #     image_data = {
# # #         'image_name': image_name,
# # #         'font_size': font_size,
# # #         'position': position,
# # #         'font_color': font_color,
# # #         'altered_size': altered_size
# # #     }

# # #     store_json_data(json.dumps(image_data))
# # #     return {"message": "Data saved to history.json"}


# # # def generate_html(history_data):
# # #     html = """
# # #     <html>
# # #     <head>
# # #     <style>
# # #     table {
# # #         border-collapse: collapse;
# # #         width: 100%;
# # #     }
    
# # #     th, td {
# # #         text-align: left;
# # #         padding: 8px;
# # #         border-bottom: 1px solid #ddd;
# # #     }
# # #     </style>
# # #     </head>
# # #     <body>
    
# # #     <h2>History Data</h2>
    
# # #     <table>
# # #       <tr>
# # #         <th>Image Name</th>
# # #         <th>Font Size</th>
# # #         <th>Position</th>
# # #         <th>Font Color</th>
# # #         <th>Altered Size</th>
# # #       </tr>
# # #     """

# # #     for data in history_data:
# # #         image_name = data['image_name']
# # #         font_size = data['font_size']
# # #         position = data['position']
# # #         font_color = data.get('font_color', 'white')
# # #         altered_size = data['altered_size'] if 'altered_size' in data else 'Default'

# # #         html += f"""
# # #         <tr>
# # #           <td>{image_name}</td>
# # #           <td>{font_size}</td>
# # #           <td>{position}</td>
# # #           <td>{font_color}</td>
# # #           <td>{altered_size}</td>
# # #         </tr>
# # #         """

# # #     html += """
# # #     </table>
    
# # #     </body>
# # #     </html>
# # #     """
    
# # #     return html


# # # def main():
# # #     st.title('Image Overlay API')

# # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # #     if uploaded_files:
# # #         image_data_list = []
# # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # #         for i, uploaded_file in enumerate(uploaded_files):
# # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))

# # #             image_data_list.append({
# # #                 'image_name': image_name,
# # #                 'font_size': font_size,
# # #                 'position': position
# # #             })

# # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # #             if st.checkbox(f"Resize Image {i+1}"):
# # #                 unique_key = f"resize_select_{i}"
# # #                 image_size = st.selectbox("Select Image Size", (
# # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # #                     "2800x3920", "3025x3850"
# # #                 ), key=unique_key)

# # #                 if image_size == "Default":
# # #                     resized_image_with_overlay = image_with_overlay
# # #                     altered_size = "Default"
# # #                 else:
# # #                     width, height = map(int, image_size.split("x"))
# # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # #                     altered_size = image_size

# # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # #                 image_data_list[i]['altered_size'] = altered_size

# # #         if st.button('Save to History'):
# # #             for data in image_data_list:
# # #                 save_to_history(data)
# # #             st.success('Data saved to history.json')

# # #     if st.button('View History'):
# # #         history_data = load_json_data()
# # #         history_html = generate_html(history_data)
# # #         st.write(history_html, unsafe_allow_html=True)

# # #     if st.button('Download History HTML'):
# # #         history_data = load_json_data()
# # #         history_html = generate_html(history_data)
# # #         b64 = base64.b64encode(history_html.encode()).decode()
# # #         href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
# # #         st.markdown(href, unsafe_allow_html=True)


# # # if __name__ == '__main__':
# # #     main()


# # # import streamlit as st
# # # from flask import Flask, jsonify, request
# # # from flask_restful import Api, Resource
# # # from PIL import Image, ImageDraw, ImageFont
# # # import io
# # # import json
# # # import base64

# # # app = Flask(__name__)
# # # api = Api(app)

# # # class ImageOverlay(Resource):
# # #     def post(self):
# # #         uploaded_files = request.files.getlist('images')
# # #         image_data_list = []

# # #         for i, uploaded_file in enumerate(uploaded_files):
# # #             image_name = request.form.get(f'image_name_{i+1}')
# # #             font_size = int(request.form.get(f'font_size_{i+1}'))
# # #             position = request.form.get(f'position_{i+1}')

# # #             image_data_list.append({
# # #                 'image_name': image_name,
# # #                 'font_size': font_size,
# # #                 'position': position
# # #             })

# # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # #         response_data = []
# # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # #             img_byte_arr = io.BytesIO()
# # #             image_with_overlay.save(img_byte_arr, format='PNG')
# # #             img_byte_arr = img_byte_arr.getvalue()
# # #             img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
# # #             response_data.append({'image': img_base64})

# # #         return jsonify(response_data)

# # # class History(Resource):
# # #     def get(self):
# # #         history_data = load_json_data()
# # #         return jsonify(history_data)

# # #     def post(self):
# # #         data = request.get_json()
# # #         for item in data:
# # #             save_to_history(item)
# # #         return {'message': 'Data saved to history.json'}

# # # api.add_resource(ImageOverlay, '/overlay')
# # # api.add_resource(History, '/history')

# # # def add_image_overlay(images, image_data_list):
# # #     images_with_overlay = []

# # #     for image, image_data in zip(images, image_data_list):
# # #         img = Image.open(io.BytesIO(image))
# # #         overlay = Image.new('RGBA', img.size)

# # #         image_name = image_data['image_name']
# # #         font_size = image_data['font_size']
# # #         position = image_data['position']
# # #         font_color = image_data.get('font_color', 'white')
# # #         font = ImageFont.truetype('arial.ttf', font_size)

# # #         if position == 'bottom-left':
# # #             x = 10
# # #             y = img.height - font_size - 10
# # #         elif position == 'bottom-right':
# # #             text_width, _ = font.getsize(image_name)
# # #             x = img.width - text_width - 10
# # #             y = img.height - font_size - 10
# # #         else:
# # #             x = 10
# # #             y = 10

# # #         draw = ImageDraw.Draw(overlay)
# # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # #         images_with_overlay.append(img_with_overlay)

# # #     return images_with_overlay


# # # def resize_image(image, size):
# # #     width, height = size
# # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # def store_json_data(json_data):
# # #     with open('history.json', 'a') as file:
# # #         file.write(json_data + '\n')


# # # def load_json_data():
# # #     data = []
# # #     with open('history.json', 'r') as file:
# # #         for line in file:
# # #             data.append(json.loads(line))
# # #     return data


# # # def save_to_history(data):
# # #     image_name = data['image_name']
# # #     font_size = data['font_size']
# # #     position = data['position']
# # #     font_color = data.get('font_color', 'white')
# # #     altered_size = data.get('altered_size', None)

# # #     image_data = {
# # #         'image_name': image_name,
# # #         'font_size': font_size,
# # #         'position': position,
# # #         'font_color': font_color,
# # #         'altered_size': altered_size
# # #     }

# # #     store_json_data(json.dumps(image_data))
# # #     return {"message": "Data saved to history.json"}


# # # def generate_html(history_data):
# # #     html = """
# # #     <html>
# # #     <head>
# # #     <style>
# # #     table {
# # #         border-collapse: collapse;
# # #         width: 100%;
# # #     }
    
# # #     th, td {
# # #         text-align: left;
# # #         padding: 8px;
# # #         border-bottom: 1px solid #ddd;
# # #     }
# # #     </style>
# # #     </head>
# # #     <body>
    
# # #     <h2>History Data</h2>
    
# # #     <table>
# # #       <tr>
# # #         <th>Image Name</th>
# # #         <th>Font Size</th>
# # #         <th>Position</th>
# # #         <th>Font Color</th>
# # #         <th>Altered Size</th>
# # #       </tr>
# # #     """

# # #     for data in history_data:
# # #         image_name = data['image_name']
# # #         font_size = data['font_size']
# # #         position = data['position']
# # #         font_color = data.get('font_color', 'white')
# # #         altered_size = data['altered_size'] if 'altered_size' in data else 'Default'

# # #         html += f"""
# # #         <tr>
# # #           <td>{image_name}</td>
# # #           <td>{font_size}</td>
# # #           <td>{position}</td>
# # #           <td>{font_color}</td>
# # #           <td>{altered_size}</td>
# # #         </tr>
# # #         """

# # #     html += """
# # #     </table>
    
# # #     </body>
# # #     </html>
# # #     """
    
# # #     return html


# # # def main():
# # #     st.title('Image Overlay API')

# # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # #     if uploaded_files:
# # #         image_data_list = []
# # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # #         for i, uploaded_file in enumerate(uploaded_files):
# # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))

# # #             image_data_list.append({
# # #                 'image_name': image_name,
# # #                 'font_size': font_size,
# # #                 'position': position
# # #             })

# # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # #             if st.checkbox(f"Resize Image {i+1}"):
# # #                 unique_key = f"resize_select_{i}"
# # #                 image_size = st.selectbox("Select Image Size", (
# # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # #                     "2800x3920", "3025x3850"
# # #                 ), key=unique_key)

# # #                 if image_size == "Default":
# # #                     resized_image_with_overlay = image_with_overlay
# # #                     altered_size = "Default"
# # #                 else:
# # #                     width, height = map(int, image_size.split("x"))
# # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # #                     altered_size = image_size

# # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # #                 image_data_list[i]['altered_size'] = altered_size

# # #         if st.button('Save to History'):
# # #             for data in image_data_list:
# # #                 save_to_history(data)
# # #             st.success('Data saved to history.json')

# # #     if st.button('View History'):
# # #         history_data = load_json_data()
# # #         history_html = generate_html(history_data)
# # #         st.write(history_html, unsafe_allow_html=True)

# # #     if st.button('Download History HTML'):
# # #         history_data = load_json_data()
# # #         history_html = generate_html(history_data)
# # #         b64 = base64.b64encode(history_html.encode()).decode()
# # #         href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
# # #         st.markdown(href, unsafe_allow_html=True)

# # # if __name__ == '__main__':
# # #     main()

# # # import streamlit as st
# # # from flask import Flask, jsonify, request
# # # from flask_restful import Api, Resource
# # # from PIL import Image, ImageDraw, ImageFont
# # # import io
# # # import json
# # # import base64

# # # app = Flask(__name__)
# # # api = Api(app)

# # # class ImageOverlay(Resource):
# # #     def post(self):
# # #         uploaded_files = request.files.getlist('images')
# # #         image_data_list = []

# # #         for i, uploaded_file in enumerate(uploaded_files):
# # #             image_name = request.form.get(f'image_name_{i+1}')
# # #             font_size = int(request.form.get(f'font_size_{i+1}'))
# # #             position = request.form.get(f'position_{i+1}')

# # #             image_data_list.append({
# # #                 'image_name': image_name,
# # #                 'font_size': font_size,
# # #                 'position': position
# # #             })

# # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]
# # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # #         response_data = []
# # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # #             img_byte_arr = io.BytesIO()
# # #             image_with_overlay.save(img_byte_arr, format='PNG')
# # #             img_byte_arr = img_byte_arr.getvalue()
# # #             img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
# # #             response_data.append({'image': img_base64})

# # #         return jsonify(response_data)

# # # class History(Resource):
# # #     def get(self):
# # #         history_data = load_json_data()
# # #         return jsonify(history_data)

# # #     def post(self):
# # #         data = request.get_json()
# # #         for item in data:
# # #             save_to_history(item)
# # #         return {'message': 'Data saved to history.json'}

# # # api.add_resource(ImageOverlay, '/overlay')
# # # api.add_resource(History, '/history')

# # # def add_image_overlay(images, image_data_list):
# # #     images_with_overlay = []

# # #     for image, image_data in zip(images, image_data_list):
# # #         img = Image.open(io.BytesIO(image))
# # #         overlay = Image.new('RGBA', img.size)

# # #         image_name = image_data['image_name']
# # #         font_size = image_data['font_size']
# # #         position = image_data['position']
# # #         font_color = image_data.get('font_color', 'white')
# # #         font = ImageFont.truetype('arial.ttf', font_size)

# # #         if position == 'bottom-left':
# # #             x = 10
# # #             y = img.height - font_size - 10
# # #         elif position == 'bottom-right':
# # #             text_width, _ = font.getsize(image_name)
# # #             x = img.width - text_width - 10
# # #             y = img.height - font_size - 10
# # #         else:
# # #             x = 10
# # #             y = 10

# # #         draw = ImageDraw.Draw(overlay)
# # #         draw.text((x, y), image_name, font=font, fill=font_color)

# # #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# # #         images_with_overlay.append(img_with_overlay)

# # #     return images_with_overlay


# # # def resize_image(image, size):
# # #     width, height = size
# # #     return image.resize((width, height), resample=Image.LANCZOS)


# # # def store_json_data(json_data):
# # #     with open('history.json', 'a') as file:
# # #         file.write(json_data + '\n')


# # # def load_json_data():
# # #     data = []
# # #     with open('history.json', 'r') as file:
# # #         for line in file:
# # #             data.append(json.loads(line))
# # #     return data


# # # def save_to_history(data):
# # #     image_name = data['image_name']
# # #     font_size = data['font_size']
# # #     position = data['position']
# # #     font_color = data.get('font_color', 'white')
# # #     altered_size = data.get('altered_size', None)

# # #     image_data = {
# # #         'image_name': image_name,
# # #         'font_size': font_size,
# # #         'position': position,
# # #         'font_color': font_color,
# # #         'altered_size': altered_size
# # #     }

# # #     store_json_data(json.dumps(image_data))
# # #     return {"message": "Data saved to history.json"}


# # # def generate_html(history_data):
# # #     html = """
# # #     <html>
# # #     <head>
# # #     <style>
# # #     table {
# # #         border-collapse: collapse;
# # #         width: 100%;
# # #     }
    
# # #     th, td {
# # #         text-align: left;
# # #         padding: 8px;
# # #         border-bottom: 1px solid #ddd;
# # #     }
# # #     </style>
# # #     </head>
# # #     <body>
    
# # #     <h2>History Data</h2>
    
# # #     <table>
# # #       <tr>
# # #         <th>Image Name</th>
# # #         <th>Font Size</th>
# # #         <th>Position</th>
# # #         <th>Font Color</th>
# # #         <th>Altered Size</th>
# # #       </tr>
# # #     """

# # #     for data in history_data:
# # #         image_name = data['image_name']
# # #         font_size = data['font_size']
# # #         position = data['position']
# # #         font_color = data.get('font_color', 'white')
# # #         altered_size = data['altered_size'] if 'altered_size' in data else 'Default'

# # #         html += f"""
# # #         <tr>
# # #           <td>{image_name}</td>
# # #           <td>{font_size}</td>
# # #           <td>{position}</td>
# # #           <td>{font_color}</td>
# # #           <td>{altered_size}</td>
# # #         </tr>
# # #         """

# # #     html += """
# # #     </table>
    
# # #     </body>
# # #     </html>
# # #     """
    
# # #     return html

# # # def main():
# # #     st.title('Image Overlay API')

# # #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# # #     if uploaded_files:
# # #         image_data_list = []
# # #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# # #         for i, uploaded_file in enumerate(uploaded_files):
# # #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# # #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# # #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))

# # #             image_data_list.append({
# # #                 'image_name': image_name,
# # #                 'font_size': font_size,
# # #                 'position': position
# # #             })

# # #         images_with_overlay = add_image_overlay(images, image_data_list)

# # #         for i, image_with_overlay in enumerate(images_with_overlay):
# # #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# # #             if st.checkbox(f"Resize Image {i+1}"):
# # #                 unique_key = f"resize_select_{i}"
# # #                 image_size = st.selectbox("Select Image Size", (
# # #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# # #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# # #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# # #                     "2800x3920", "3025x3850"
# # #                 ), key=unique_key)

# # #                 if image_size == "Default":
# # #                     resized_image_with_overlay = image_with_overlay
# # #                     altered_size = "Default"
# # #                 else:
# # #                     width, height = map(int, image_size.split("x"))
# # #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# # #                     altered_size = image_size

# # #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# # #                 image_data_list[i]['altered_size'] = altered_size

# # #         if st.button('Save to History'):
# # #             for data in image_data_list:
# # #                 save_to_history(data)
# # #             st.success('Data saved to history.json')

# # #     if st.button('View History'):
# # #         history_data = load_json_data()
# # #         history_html = generate_html(history_data)
# # #         st.write(history_html, unsafe_allow_html=True)

# # #     if st.button('Download History HTML'):
# # #         history_data = load_json_data()
# # #         history_html = generate_html(history_data)
# # #         b64 = base64.b64encode(history_html.encode()).decode()
# # #         href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
# # #         st.markdown(href, unsafe_allow_html=True)

# # # if __name__ == '__main__':
# # #     main()

# # import streamlit as st
# # from flask import Flask, jsonify, request
# # from flask_restful import Api, Resource
# # from PIL import Image, ImageDraw, ImageFont
# # import io
# # import json
# # import base64

# # app = Flask(__name__)
# # api = Api(app)

# # class ImageOverlay(Resource):
# #     def post(self):
# #         uploaded_files = request.files.getlist('images')
# #         image_data_list = []

# #         for i, uploaded_file in enumerate(uploaded_files):
# #             image_name = request.form.get(f'image_name_{i+1}')
# #             font_size = int(request.form.get(f'font_size_{i+1}'))
# #             position = request.form.get(f'position_{i+1}')

# #             image_data_list.append({
# #                 'image_name': image_name,
# #                 'font_size': font_size,
# #                 'position': position
# #             })

# #         images = [uploaded_file.read() for uploaded_file in uploaded_files]
# #         images_with_overlay = add_image_overlay(images, image_data_list)

# #         response_data = []
# #         for i, image_with_overlay in enumerate(images_with_overlay):
# #             img_byte_arr = io.BytesIO()
# #             image_with_overlay.save(img_byte_arr, format='PNG')
# #             img_byte_arr = img_byte_arr.getvalue()
# #             img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
# #             response_data.append({'image': img_base64})

# #         return jsonify(response_data)

# # class History(Resource):
# #     def get(self):
# #         history_data = load_json_data()
# #         return jsonify(history_data)

# #     def post(self):
# #         data = request.get_json()
# #         for item in data:
# #             save_to_history(item)
# #         return {'message': 'Data saved to history.json'}

# # api.add_resource(ImageOverlay, '/overlay')
# # api.add_resource(History, '/history')

# # def add_image_overlay(images, image_data_list):
# #     images_with_overlay = []

# #     for image, image_data in zip(images, image_data_list):
# #         img = Image.open(io.BytesIO(image))
# #         overlay = Image.new('RGBA', img.size)

# #         image_name = image_data['image_name']
# #         font_size = image_data['font_size']
# #         position = image_data['position']
# #         font_color = image_data.get('font_color', 'white')
# #         font = ImageFont.truetype('arial.ttf', font_size)

# #         if position == 'bottom-left':
# #             x = 10
# #             y = img.height - font_size - 10
# #         elif position == 'bottom-right':
# #             text_width, _ = font.getsize(image_name)
# #             x = img.width - text_width - 10
# #             y = img.height - font_size - 10
# #         else:
# #             x = 10
# #             y = 10

# #         draw = ImageDraw.Draw(overlay)
# #         draw.text((x, y), image_name, font=font, fill=font_color)

# #         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
# #         images_with_overlay.append(img_with_overlay)

# #     return images_with_overlay


# # def resize_image(image, size):
# #     width, height = size
# #     return image.resize((width, height), resample=Image.LANCZOS)


# # def store_json_data(json_data):
# #     with open('history.json', 'a') as file:
# #         file.write(json_data + '\n')


# # def load_json_data():
# #     data = []
# #     with open('history.json', 'r') as file:
# #         for line in file:
# #             data.append(json.loads(line))
# #     return data


# # def save_to_history(data):
# #     image_name = data['image_name']
# #     font_size = data['font_size']
# #     position = data['position']
# #     font_color = data.get('font_color', 'white')
# #     altered_size = data.get('altered_size', None)

# #     image_data = {
# #         'image_name': image_name,
# #         'font_size': font_size,
# #         'position': position,
# #         'font_color': font_color,
# #         'altered_size': altered_size
# #     }

# #     store_json_data(json.dumps(image_data))
# #     return {"message": "Data saved to history.json"}


# # def generate_html(history_data):
# #     html = """
# #     <html>
# #     <head>
# #     <style>
# #     table {
# #         border-collapse: collapse;
# #         width: 100%;
# #     }
    
# #     th, td {
# #         text-align: left;
# #         padding: 8px;
# #         border-bottom: 1px solid #ddd;
# #     }
# #     </style>
# #     </head>
# #     <body>
    
# #     <h2>History Data</h2>
    
# #     <table>
# #       <tr>
# #         <th>Image Name</th>
# #         <th>Font Size</th>
# #         <th>Position</th>
# #         <th>Font Color</th>
# #         <th>Altered Size</th>
# #       </tr>
# #     """

# #     for data in history_data:
# #         image_name = data['image_name']
# #         font_size = data['font_size']
# #         position = data['position']
# #         font_color = data.get('font_color', 'white')
# #         altered_size = data['altered_size'] if 'altered_size' in data else 'Default'

# #         html += f"""
# #         <tr>
# #           <td>{image_name}</td>
# #           <td>{font_size}</td>
# #           <td>{position}</td>
# #           <td>{font_color}</td>
# #           <td>{altered_size}</td>
# #         </tr>
# #         """

# #     html += """
# #     </table>
    
# #     </body>
# #     </html>
# #     """
    
# #     return html

# # def main():
# #     st.title('Image Overlay API')

# #     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# #     if uploaded_files:
# #         image_data_list = []
# #         images = [uploaded_file.read() for uploaded_file in uploaded_files]

# #         for i, uploaded_file in enumerate(uploaded_files):
# #             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# #             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# #             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))

# #             image_data_list.append({
# #                 'image_name': image_name,
# #                 'font_size': font_size,
# #                 'position': position
# #             })

# #         images_with_overlay = add_image_overlay(images, image_data_list)

# #         for i, image_with_overlay in enumerate(images_with_overlay):
# #             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# #             if st.checkbox(f"Resize Image {i+1}"):
# #                 unique_key = f"resize_select_{i}"
# #                 image_size = st.selectbox("Select Image Size", (
# #                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# #                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# #                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# #                     "2800x3920", "3025x3850"
# #                 ), key=unique_key)

# #                 if image_size == "Default":
# #                     resized_image_with_overlay = image_with_overlay
# #                     altered_size = "Default"
# #                 else:
# #                     width, height = map(int, image_size.split("x"))
# #                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# #                     altered_size = image_size

# #                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# #                 image_data_list[i]['altered_size'] = altered_size

# #         if st.button('Save to History'):
# #             for data in image_data_list:
# #                 save_to_history(data)
# #             st.success('Data saved to history.json')

# #     if st.button('View History'):
# #         history_data = load_json_data()
# #         history_html = generate_html(history_data)
# #         st.write(history_html, unsafe_allow_html=True)

# #     if st.button('Download History HTML'):
# #         history_data = load_json_data()
# #         history_html = generate_html(history_data)
# #         b64 = base64.b64encode(history_html.encode()).decode()
# #         href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
# #         st.markdown(href, unsafe_allow_html=True)

# # if __name__ == '__main__':
# #     main()
# import streamlit as st
# import base64
# import json
# from PIL import Image
# from io import BytesIO

# def add_image_overlay(images, image_data_list):
#     images_with_overlay = []

#     for image, image_data in zip(images, image_data_list):
#         img = Image.open(BytesIO(image))

#         # Add overlay to image
#         overlay_text = f"Image Name: {image_data['image_name']}\nFont Size: {image_data['font_size']}\nPosition: {image_data['position']}"
#         draw = ImageDraw.Draw(img)
#         font = ImageFont.truetype("arial.ttf", image_data['font_size'])
#         text_width, text_height = draw.textsize(overlay_text, font=font)

#         if image_data['position'] == 'bottom-left':
#             position = (10, img.height - text_height - 10)
#         elif image_data['position'] == 'bottom-right':
#             position = (img.width - text_width - 10, img.height - text_height - 10)
#         elif image_data['position'] == 'top-left':
#             position = (10, 10)
#         elif image_data['position'] == 'top-right':
#             position = (img.width - text_width - 10, 10)

#         draw.rectangle((position[0] - 5, position[1] - 5, position[0] + text_width + 5, position[1] + text_height + 5), fill='black')
#         draw.text(position, overlay_text, font=font, fill=image_data.get('font_color', 'white'))

#         images_with_overlay.append(img)

#     return images_with_overlay

# def resize_image(image, size):
#     img = Image.open(BytesIO(image))
#     img_resized = img.resize(size)
#     return img_resized

# def load_json_data():
#     # Load history data from JSON file
#     try:
#         with open('history.json', 'r') as f:
#             history_data = json.load(f)
#     except FileNotFoundError:
#         history_data = []

#     return history_data

# def store_json_data(data):
#     # Store data in history JSON file
#     try:
#         with open('history.json', 'w') as f:
#             f.write(data)
#     except:
#         pass

# def save_to_history(data):
#     image_name = data['image_name']
#     font_size = data['font_size']
#     position = data['position']
#     font_color = data.get('font_color', 'white')
#     altered_size = data.get('altered_size', None)

#     image_data = {
#         'image_name': image_name,
#         'font_size': font_size,
#         'position': position,
#         'font_color': font_color,
#         'altered_size': altered_size
#     }

#     history_data = load_json_data()
#     history_data.append(image_data)

#     store_json_data(json.dumps(history_data))

# def generate_html(history_data):
#     html = """
#     <html>
#     <head>
#     <style>
#     table {
#         border-collapse: collapse;
#         width: 100%;
#     }
    
#     th, td {
#         text-align: left;
#         padding: 8px;
#         border-bottom: 1px solid #ddd;
#     }
#     </style>
#     </head>
#     <body>
    
#     <h2>History Data</h2>
    
#     <table>
#       <tr>
#         <th>Image Name</th>
#         <th>Font Size</th>
#         <th>Position</th>
#         <th>Font Color</th>
#         <th>Altered Size</th>
#       </tr>
#     """

#     for data in history_data:
#         image_name = data['image_name']
#         font_size = data['font_size']
#         position = data['position']
#         font_color = data['font_color']
#         altered_size = data['altered_size']

#         html += f"""
#         <tr>
#           <td>{image_name}</td>
#           <td>{font_size}</td>
#           <td>{position}</td>
#           <td>{font_color}</td>
#           <td>{altered_size}</td>
#         </tr>
#         """

#     html += """
#     </table>
    
#     </body>
#     </html>
#     """

#     return html

# def main():
#     st.title("Image Overlay API")

#     uploaded_images = st.file_uploader("Upload Images", accept_multiple_files=True)

#     font_size = st.number_input("Font Size", min_value=1, value=20)
#     position = st.selectbox("Position", ["bottom-left", "bottom-right", "top-left", "top-right"])
#     font_color = st.selectbox("Font Color", ["white", "black"])

#     image_data_list = []

#     if uploaded_images:
#         for i, image in enumerate(uploaded_images):
#             image_data = {
#                 'image_name': image.name,
#                 'font_size': font_size,
#                 'position': position,
#                 'font_color': font_color
#             }
#             image_data_list.append(image_data)

#             image_bytes = image.read()
#             image_with_overlay = add_image_overlay([image_bytes], [image_data])[0]

#             image_size = st.selectbox("Altered Size", ["Default"] + [
#                 "500x700", "700x1000", "900x1200", "1050x1500",
#                 "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
#                 "2800x3920", "3025x3850"
#             ], key=str(i))

#             if image_size == "Default":
#                 resized_image_with_overlay = image_with_overlay
#                 altered_size = "Default"
#             else:
#                 width, height = map(int, image_size.split("x"))
#                 resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                 altered_size = image_size

#             st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#             image_data_list[i]['altered_size'] = altered_size

#     if st.button('Save to History'):
#         for data in image_data_list:
#             save_to_history(data)
#         st.success('Data saved to history.json')

#     if st.button('View History'):
#         history_data = load_json_data()
#         history_html = generate_html(history_data)
#         st.write(history_html, unsafe_allow_html=True)

#     if st.button('Download History HTML'):
#         history_data = load_json_data()
#         history_html = generate_html(history_data)
#         b64 = base64.b64encode(history_html.encode()).decode()
#         href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
#         st.markdown(href, unsafe_allow_html=True)

# if __name__ == '__main__':
#     main()
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
import base64
from flask import Flask, jsonify, request

app = Flask(__name__)


def add_image_overlay(images, image_data_list):
    images_with_overlay = []

    for image, image_data in zip(images, image_data_list):
        img = Image.open(io.BytesIO(image))
        overlay = Image.new('RGBA', img.size)

        image_name = image_data['image_name']
        font_size = image_data['font_size']
        position = image_data['position']
        text_color = image_data['text_color']
        font = ImageFont.truetype('./arial.ttf', font_size)

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
        draw.text((x, y), image_name, font=font, fill=text_color)

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
    text_color = data['text_color']
    altered_size = data.get('altered_size', None)

    image_data = {
        'image_name': image_name,
        'font_size': font_size,
        'position': position,
        'text_color': text_color,
        'altered_size': altered_size
    }

    store_json_data(json.dumps(image_data))
    return {"message": "Data saved to history.json"}


@app.route('/api/history', methods=['GET'])
def get_history():
    history_data = load_json_data()
    return jsonify(history_data)


@app.route('/api/image-overlay', methods=['POST'])
def process_image_overlay():
    uploaded_files = request.files.getlist('files')
    image_data_list = json.loads(request.form.get('data'))

    images = [uploaded_file.read() for uploaded_file in uploaded_files]
    images_with_overlay = add_image_overlay(images, image_data_list)

    response_data = []

    for i, image_with_overlay in enumerate(images_with_overlay):
        resized_image_with_overlay = resize_image(image_with_overlay, (800, 600))
        image_path = f"image_{i+1}.png"
        resized_image_with_overlay.save(image_path, 'PNG')

        with open(image_path, 'rb') as file:
            image_data = file.read()

        image_base64 = base64.b64encode(image_data).decode('utf-8')

        response_data.append({
            'image_name': image_data_list[i]['image_name'],
            'image': image_base64
        })

    return jsonify(response_data)


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
        <th>Text Color</th>
        <th>Altered Size</th>
      </tr>
    """

    for data in history_data:
        image_name = data['image_name']
        font_size = data['font_size']
        position = data['position']
        text_color = data['text_color']
        altered_size = data['altered_size']
        
        html += f"""
        <tr>
          <td>{image_name}</td>
          <td>{font_size}</td>
          <td>{position}</td>
          <td>{text_color}</td>
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
            text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

            image_data_list.append({
                'image_name': image_name,
                'font_size': font_size,
                'position': position,
                'text_color': text_color
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
        href = f'<a href="data:file/html;base64,{b64}" download="history.html">Click here to download history.html</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':

    main()