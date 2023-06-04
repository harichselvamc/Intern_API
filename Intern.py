# # # # # import streamlit as st
# # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # import io
# # # # # import json
# # # # # import base64

# # # # # def add_image_overlay(images, image_data_list):
# # # # #     images_with_overlay = []

# # # # #     for image, image_data in zip(images, image_data_list):
# # # # #         img = Image.open(io.BytesIO(image))
# # # # #         overlay = Image.new('RGBA', img.size)

# # # # #         image_name = image_data['image_name']
# # # # #         font_size = image_data['font_size']
# # # # #         position = image_data['position']
# # # # #         font_color = image_data.get('font_color', 'white')
# # # # #         font = ImageFont.truetype('arial.ttf', font_size)

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
# # # # #     font_color = data.get('font_color', 'white')
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
# # # # #         font_color = data.get('font_color', 'white')
# # # # #         altered_size = data.get('altered_size', '')

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
# # # # #         href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
# # # # #         st.markdown(href, unsafe_allow_html=True)


# # # # # if __name__ == '__main__':
# # # # #     main()
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
# # # #         font_color = data.get('font_color', 'white')
# # # #         altered_size = data.get('altered_size', '')

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


# # # # def view_history():
# # # #     with open('history.html', 'r') as file:
# # # #         history_html = file.read()
# # # #     st.write(history_html, unsafe_allow_html=True)


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
# # # #         view_history()

# # # #     if st.button('Download History HTML'):
# # # #         history_data = load_json_data()
# # # #         history_html = generate_html(history_data)
# # # #         with open('history.html', 'w') as file:
# # # #             file.write(history_html)
# # # #         with open('history.html', 'r') as file:
# # # #             b64 = base64.b64encode(file.read().encode()).decode()
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
# # #         altered_size = data.get('altered_size', '')

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


# # # @st.cache(allow_output_mutation=True)
# # # def get_history_data():
# # #     return load_json_data()


# # # def view_history():
# # #     history_data = get_history_data()
# # #     history_html = generate_html(history_data)
# # #     st.write(history_html, unsafe_allow_html=True)


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
# # #             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# # #             image_data_list.append({
# # #                 'image_name': image_name,
# # #                 'font_size': font_size,
# # #                 'position': position,
# # #                 'font_color': font_color
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
# # #         view_history()

# # #     if st.button('Download History HTML'):
# # #         history_data = get_history_data()
# # #         history_html = generate_html(history_data)
# # #         with open('history.html', 'w') as file:
# # #             file.write(history_html)
# # #         with open('history.html', 'r') as file:
# # #             b64 = base64.b64encode(file.read().encode()).decode()
# # #         href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
# # #         st.markdown(href, unsafe_allow_html=True)


# # # if __name__ == '__main__':
# # #     main()



# # import streamlit as st
# # from PIL import Image, ImageDraw, ImageFont
# # import io
# # import json
# # import base64

# # # Function to add image overlay
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


# # # Function to resize image
# # def resize_image(image, size):
# #     width, height = size
# #     return image.resize((width, height), resample=Image.LANCZOS)


# # # Function to store JSON data
# # def store_json_data(json_data):
# #     with open('history.json', 'a') as file:
# #         file.write(json_data + '\n')


# # # Function to load JSON data
# # def load_json_data():
# #     data = []
# #     with open('history.json', 'r') as file:
# #         for line in file:
# #             data.append(json.loads(line))
# #     return data


# # # Function to save data to history
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


# # # Function to generate HTML for history
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
# #         <th>Actions</th>
# #       </tr>
# #     """

# #     for data in history_data:
# #         image_name = data['image_name']
# #         font_size = data['font_size']
# #         position = data['position']
# #         font_color = data.get('font_color', 'white')
# #         altered_size = data.get('altered_size', '')

# #         html += f"""
# #         <tr>
# #           <td>{image_name}</td>
# #           <td>{font_size}</td>
# #           <td>{position}</td>
# #           <td>{font_color}</td>
# #           <td>{altered_size}</td>
# #           <td>
# #             <a href="/api/delete/{image_name}" style="margin-right: 5px;">Delete</a>
# #             <a href="/api/edit/{image_name}">Edit</a>
# #           </td>
# #         </tr>
# #         """

# #     html += """
# #     </table>
    
# #     </body>
# #     </html>
# #     """
    
# #     return html


# # # Function to view history
# # def view_history():
# #     with open('history.html', 'r') as file:
# #         history_html = file.read()
# #     st.write(history_html, unsafe_allow_html=True)


# # # Function to delete an entry from history
# # def delete_entry(image_name):
# #     data = load_json_data()
# #     updated_data = [entry for entry in data if entry['image_name'] != image_name]
# #     with open('history.json', 'w') as file:
# #         for entry in updated_data:
# #             file.write(json.dumps(entry) + '\n')
# #     return {"message": f"Entry with image name '{image_name}' deleted from history.json"}


# # # Function to edit an entry from history
# # def edit_entry(image_name, new_data):
# #     data = load_json_data()
# #     updated_data = [entry if entry['image_name'] != image_name else new_data for entry in data]
# #     with open('history.json', 'w') as file:
# #         for entry in updated_data:
# #             file.write(json.dumps(entry) + '\n')
# #     return {"message": f"Entry with image name '{image_name}' updated in history.json"}


# # # Main function
# # def main():
# #     st.title('Image Overlay API')

# #     # API routes
# #     if st.sidebar.checkbox("Show API routes"):
# #         st.sidebar.markdown("### API Routes")
# #         st.sidebar.markdown("- POST /api/overlay: Add image overlay")
# #         st.sidebar.markdown("- GET /api/history: View history")
# #         st.sidebar.markdown("- DELETE /api/delete/{image_name}: Delete entry from history")
# #         st.sidebar.markdown("- PUT /api/edit/{image_name}: Edit entry in history")

# #     # Create image overlay
# #     if st.sidebar.checkbox("Add Image Overlay"):
# #         uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
# #         if uploaded_files:
# #             image_data_list = []
# #             images = [uploaded_file.read() for uploaded_file in uploaded_files]

# #             for i, uploaded_file in enumerate(uploaded_files):
# #                 image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
# #                 font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
# #                 position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
# #                 font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

# #                 image_data_list.append({
# #                     'image_name': image_name,
# #                     'font_size': font_size,
# #                     'position': position,
# #                     'font_color': font_color
# #                 })

# #             images_with_overlay = add_image_overlay(images, image_data_list)

# #             for i, image_with_overlay in enumerate(images_with_overlay):
# #                 st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

# #                 if st.checkbox(f"Resize Image {i+1}"):
# #                     unique_key = f"resize_select_{i}"
# #                     image_size = st.selectbox("Select Image Size", (
# #                         "Default", "1920x1080", "630x900", "720x1080", "900x1260",
# #                         "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
# #                         "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
# #                         "2800x3920", "3025x3850"
# #                     ), key=unique_key)

# #                     if image_size == "Default":
# #                         resized_image_with_overlay = image_with_overlay
# #                         altered_size = "Default"
# #                     else:
# #                         width, height = map(int, image_size.split("x"))
# #                         resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
# #                         altered_size = image_size

# #                     st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

# #                     image_data_list[i]['altered_size'] = altered_size

# #             if st.button('Save to History'):
# #                 for data in image_data_list:
# #                     save_to_history(data)
# #                 st.success('Data saved to history.json')

# #     # View history
# #     if st.sidebar.button('View History'):
# #         view_history()

# #     # Delete entry from history
# #     delete_route = st.sidebar.text_input("Enter image name to delete from history")
# #     if st.sidebar.button('Delete Entry'):
# #         if delete_route:
# #             delete_entry(delete_route)
# #             st.success(f"Entry with image name '{delete_route}' deleted from history.json")
# #         else:
# #             st.warning("Please enter an image name to delete from history")

# #     # Edit entry in history
# #     edit_route = st.sidebar.text_input("Enter image name to edit in history")
# #     if st.sidebar.button('Edit Entry'):
# #         if edit_route:
# #             uploaded_files = st.file_uploader('Upload new image', type=['png', 'jpg', 'jpeg'])
# #             if uploaded_files:
# #                 image_data = {
# #                     'image_name': uploaded_files[0].name,
# #                     'font_size': st.number_input('Overlay font size', min_value=1, value=20),
# #                     'position': st.selectbox('Overlay position', ('bottom-left', 'bottom-right', 'top-left', 'top-right')),
# #                     'font_color': st.color_picker('Font color', '#FFFFFF')
# #                 }
# #                 edit_entry(edit_route, image_data)
# #                 st.success(f"Entry with image name '{edit_route}' updated in history.json")
# #         else:
# #             st.warning("Please enter an image name to edit in history")


# # if __name__ == '__main__':
# #     main()

# import streamlit as st
# from PIL import Image, ImageDraw, ImageFont
# import io
# import json
# import base64

# def add_image_overlay(images, image_data_list):
#     images_with_overlay = []

#     for image, image_data in zip(images, image_data_list):
#         img = Image.open(io.BytesIO(image))
#         overlay = Image.new('RGBA', img.size)

#         image_name = image_data['image_name']
#         font_size = image_data['font_size']
#         position = image_data['position']
#         font_color = image_data.get('font_color', 'white')
#         font = ImageFont.truetype('arial.ttf', font_size)

#         if position == 'bottom-left':
#             x = 10
#             y = img.height - font_size - 10
#         elif position == 'bottom-right':
#             text_width, _ = font.getsize(image_name)
#             x = img.width - text_width - 10
#             y = img.height - font_size - 10
#         else:
#             x = 10
#             y = 10

#         draw = ImageDraw.Draw(overlay)
#         draw.text((x, y), image_name, font=font, fill=font_color)

#         img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay)
#         images_with_overlay.append(img_with_overlay)

#     return images_with_overlay


# def resize_image(image, size):
#     width, height = size
#     return image.resize((width, height), resample=Image.LANCZOS)


# def store_json_data(json_data):
#     with open('history.json', 'a') as file:
#         file.write(json_data + '\n')


# def load_json_data():
#     data = []
#     with open('history.json', 'r') as file:
#         for line in file:
#             data.append(json.loads(line))
#     return data


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

#     store_json_data(json.dumps(image_data))
#     return {"message": "Data saved to history.json"}


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
#         <th>Actions</th>
#       </tr>
#     """

#     for data in history_data:
#         image_name = data['image_name']
#         font_size = data['font_size']
#         position = data['position']
#         font_color = data.get('font_color', 'white')
#         altered_size = data.get('altered_size', '')

#         html += f"""
#         <tr>
#           <td>{image_name}</td>
#           <td>{font_size}</td>
#           <td>{position}</td>
#           <td>{font_color}</td>
#           <td>{altered_size}</td>
#           <td>
#             <a href="/api/history/{image_name}" target="_blank">View</a> |
#             <a href="/api/history/{image_name}/edit" target="_blank">Edit</a> |
#             <a href="/api/history/{image_name}/delete" target="_blank">Delete</a>
#           </td>
#         </tr>
#         """

#     html += """
#     </table>
    
#     </body>
#     </html>
#     """
    
#     return html


# def view_history():
#     history_data = load_json_data()
#     history_html = generate_html(history_data)
#     with open('history.html', 'w') as file:
#         file.write(history_html)
#     with open('history.html', 'r') as file:
#         history_html = file.read()
#     st.write(history_html, unsafe_allow_html=True)


# def create_image_overlay():
#     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     if uploaded_files:
#         image_data_list = []
#         images = [uploaded_file.read() for uploaded_file in uploaded_files]

#         for i, uploaded_file in enumerate(uploaded_files):
#             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
#             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
#             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
#             font_color = st.color_picker(f'Font color for Image {i+1}', '#FFFFFF')

#             image_data_list.append({
#                 'image_name': image_name,
#                 'font_size': font_size,
#                 'position': position,
#                 'font_color': font_color
#             })

#         images_with_overlay = add_image_overlay(images, image_data_list)

#         for i, image_with_overlay in enumerate(images_with_overlay):
#             st.image(image_with_overlay, caption=f'Image {i+1} with Overlay', use_column_width=True)

#             if st.checkbox(f"Resize Image {i+1}"):
#                 unique_key = f"resize_select_{i}"
#                 image_size = st.selectbox("Select Image Size", (
#                     "Default", "1920x1080", "630x900", "720x1080", "900x1260",
#                     "1080x1440", "1440x1800", "1530x1980", "1800x2520", "1050x1500",
#                     "1200x1800", "1500x2100", "1800x2400", "2400x3000", "2550x3300",
#                     "2800x3920", "3025x3850"
#                 ), key=unique_key)

#                 if image_size == "Default":
#                     resized_image_with_overlay = image_with_overlay
#                     altered_size = "Default"
#                 else:
#                     width, height = map(int, image_size.split("x"))
#                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                     altered_size = image_size

#                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#                 image_data_list[i]['altered_size'] = altered_size

#         if st.button('Save to History'):
#             for data in image_data_list:
#                 save_to_history(data)
#             st.success('Data saved to history.json')


# def edit_image_overlay(image_name):
#     history_data = load_json_data()
#     image_data = None
#     for data in history_data:
#         if data['image_name'] == image_name:
#             image_data = data
#             break

#     if image_data is None:
#         st.error(f"No history data found for image: {image_name}")
#         return

#     st.header(f"Edit Image Overlay - {image_name}")

#     font_size = st.number_input("Overlay font size", min_value=1, value=image_data['font_size'])
#     position = st.selectbox("Overlay position", ('bottom-left', 'bottom-right', 'top-left', 'top-right'), index=['bottom-left', 'bottom-right', 'top-left', 'top-right'].index(image_data['position']))
#     font_color = st.color_picker("Font color", image_data['font_color'])

#     image_data['font_size'] = font_size
#     image_data['position'] = position
#     image_data['font_color'] = font_color

#     if st.button('Update Overlay'):
#         history_data = [data if data['image_name'] != image_name else image_data for data in history_data]
#         with open('history.json', 'w') as file:
#             for data in history_data:
#                 file.write(json.dumps(data) + '\n')
#         st.success(f"Overlay updated for image: {image_name}")


# def delete_image_overlay(image_name):
#     history_data = load_json_data()
#     updated_history_data = [data for data in history_data if data['image_name'] != image_name]
#     with open('history.json', 'w') as file:
#         for data in updated_history_data:
#             file.write(json.dumps(data) + '\n')
#     st.success(f"Overlay deleted for image: {image_name}")


# def main():
#     st.title('Image Overlay API')

#     page = st.sidebar.selectbox("Select Page", ('Create Overlay', 'View History'))
    
#     if page == 'Create Overlay':
#         create_image_overlay()
#     elif page == 'View History':
#         view_history()


# if __name__ == '__main__':
#     main()



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


def view_history():
    history_data = load_json_data()
    if not history_data:
        st.warning("No history data found.")
        return

    st.header("History Data")
    for data in history_data:
        st.subheader(data['image_name'])
        st.write("Font Size:", data['font_size'])
        st.write("Position:", data['position'])
        st.write("Font Color:", data['font_color'])
        st.write("Altered Size:", data.get('altered_size', "Default"))
        st.write("---")

    if st.button('Download History JSON'):
        with open('history.json', 'r') as file:
            b64 = base64.b64encode(file.read().encode()).decode()
        href = f'<a href="data:application/json;base64,{b64}" download="history.json">Download history.json File</a>'
        st.markdown(href, unsafe_allow_html=True)

    if st.button('Download History HTML'):
        history_html = generate_html(history_data)
        with open('history.html', 'w') as file:
            file.write(history_html)
        with open('history.html', 'r') as file:
            b64 = base64.b64encode(file.read().encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="history.html">Download history.html File</a>'
        st.markdown(href, unsafe_allow_html=True)


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
        view_history()


if __name__ == '__main__':
    main()
