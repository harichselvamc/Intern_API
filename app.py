# import streamlit as st
# from PIL import Image, ImageDraw, ImageFont
# import io
# import json
# from fastapi import FastAPI
# import base64

# app = FastAPI()


# def add_image_overlay(images, image_data_list):
#     images_with_overlay = []
    
    

#     for image, image_data in zip(images, image_data_list):
#         img = Image.open(io.BytesIO(image))
#         overlay = Image.new('RGBA', img.size)

#         image_name = image_data['image_name']
#         font_size = image_data['font_size']
#         position = image_data['position']
#         text_color = image_data['text_color']
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
#         draw.text((x, y), image_name, font=font, fill=text_color)

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


# @app.get("/history")
# def get_history():
#     history_data = load_json_data()
#     return history_data


# @app.post("/save")
# def save_to_history(data: dict):
#     image = data.pop('image')
#     json_data = json.dumps(data)
#     store_json_data(json_data)
#     return {"message": "Data saved to history.json"}


# def main():
#     st.title('Image Overlay API')

#     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     if uploaded_files:
#         image_data_list = []
#         images = [uploaded_file.read() for uploaded_file in uploaded_files]

#         for i, uploaded_file in enumerate(uploaded_files):
#             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
#             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
#             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
#             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

#             image_data_list.append({
#                 'image_name': image_name,
#                 'font_size': font_size,
#                 'position': position,
#                 'text_color': text_color
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
#                     width, height = image_size.split("x")
#                     width = int(width)
#                     height = int(height)
#                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                     altered_size = image_size

#                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#                 image_path = f"image_{i+1}.png"
#                 resized_image_with_overlay.save(image_path, 'PNG')
#                 st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
#                                    mime='image/png')

#                 image_data_list[i]['altered_size'] = altered_size

#         if st.button('Save'):
#             for i, image_data in enumerate(image_data_list):
#                 image_data['image'] = base64.b64encode(images[i]).decode('utf-8')
#                 if 'altered_size' not in image_data:
#                     image_data['altered_size'] = "Default"
#                 save_to_history(image_data)
#             st.success('Data saved to history.json')

#         st.subheader('API Response')
#         st.json(image_data_list)

#         st.subheader('History Data')
#         history_data = load_json_data()
#         for data in history_data:
#             st.write(data)

#         current_url = st.experimental_get_query_params()
#         query_params = []
#         for key, value in current_url.items():
#             query_params.append(f"{key}={value[0]}")
#         query_string = "&".join(query_params)
#         sharable_link = f"[Sharable Link](?{query_string})"
#         st.markdown(sharable_link)


# if __name__ == '__main__':
#     main()


# import streamlit as st
# from PIL import Image, ImageDraw, ImageFont
# import io
# import json
# from fastapi import FastAPI
# import base64

# app = FastAPI()


# def add_image_overlay(images, image_data_list):
#     images_with_overlay = []

#     for image, image_data in zip(images, image_data_list):
#         img = Image.open(io.BytesIO(image))
#         overlay = Image.new('RGBA', img.size)

#         image_name = image_data['image_name']
#         font_size = image_data['font_size']
#         position = image_data['position']
#         text_color = image_data['text_color']
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
#         draw.text((x, y), image_name, font=font, fill=text_color)

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


# @app.get("/history")
# def get_history():
#     history_data = load_json_data()
#     return history_data


# @app.post("/save")
# def save_to_history(data: dict):
#     image_name = data['image_name']
#     font_size = data['font_size']
#     position = data['position']
#     text_color = data['text_color']
#     altered_size = data['altered_size']

#     image_data = {
#         'image_name': image_name,
#         'font_size': font_size,
#         'position': position,
#         'text_color': text_color,
#         'altered_size': altered_size
#     }

#     store_json_data(json.dumps(image_data))
#     return {"message": "Data saved to history.json"}


# def main():
#     st.title('Image Overlay API')

#     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     if uploaded_files:
#         image_data_list = []
#         images = [uploaded_file.read() for uploaded_file in uploaded_files]

#         for i, uploaded_file in enumerate(uploaded_files):
#             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
#             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
#             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
#             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

#             image_data_list.append({
#                 'image_name': image_name,
#                 'font_size': font_size,
#                 'position': position,
#                 'text_color': text_color
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
#                     width, height = image_size.split("x")
#                     width = int(width)
#                     height = int(height)
#                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                     altered_size = image_size

#                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#                 image_path = f"image_{i+1}.png"
#                 resized_image_with_overlay.save(image_path, 'PNG')
#                 st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
#                                    mime='image/png')

#                 image_data_list[i]['altered_size'] = altered_size

#         if st.button('Save'):
#             for i, image_data in enumerate(image_data_list):
#                 image_data['image'] = base64.b64encode(images[i]).decode('utf-8')
#                 if 'altered_size' not in image_data:
#                     image_data['altered_size'] = "Default"
#                 save_to_history(image_data)
#             st.success('Data saved to history.json')

#         st.subheader('API Response')
#         st.json(image_data_list)

#         st.subheader('History Data')
#         history_data = load_json_data()
#         for data in history_data:
#             st.write(data)

#         current_url = st.experimental_get_query_params()
#         query_params = []
#         for key, value in current_url.items():
#             query_params.append(f"{key}={value[0]}")
#         query_string = "&".join(query_params)
#         sharable_link = f"[Sharable Link](?{query_string})"
#         st.markdown(sharable_link)


# if __name__ == '__main__':
#     main()


# import streamlit as st
# from PIL import Image, ImageDraw, ImageFont
# import io
# import json
# from fastapi import FastAPI
# import base64

# app = FastAPI()


# def add_image_overlay(images, image_data_list):
#     images_with_overlay = []

#     for image, image_data in zip(images, image_data_list):
#         img = Image.open(io.BytesIO(image))
#         overlay = Image.new('RGBA', img.size)

#         image_name = image_data['image_name']
#         font_size = image_data['font_size']
#         position = image_data['position']
#         text_color = image_data['text_color']
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
#         draw.text((x, y), image_name, font=font, fill=text_color)

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


# @app.get("/history")
# def get_history():
#     history_data = load_json_data()
#     return history_data


# @app.post("/save")
# def save_to_history(data: dict):
#     image_name = data['image_name']
#     font_size = data['font_size']
#     position = data['position']
#     text_color = data['text_color']
#     altered_size = data.get('altered_size', None)

#     image_data = {
#         'image_name': image_name,
#         'font_size': font_size,
#         'position': position,
#         'text_color': text_color,
#         'altered_size': altered_size
#     }

#     store_json_data(json.dumps(image_data))
#     return {"message": "Data saved to history.json"}


# def main():
#     st.title('Image Overlay API')

#     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     if uploaded_files:
#         image_data_list = []
#         images = [uploaded_file.read() for uploaded_file in uploaded_files]

#         for i, uploaded_file in enumerate(uploaded_files):
#             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
#             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
#             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
#             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

#             image_data_list.append({
#                 'image_name': image_name,
#                 'font_size': font_size,
#                 'position': position,
#                 'text_color': text_color
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
#                     width, height = image_size.split("x")
#                     width = int(width)
#                     height = int(height)
#                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                     altered_size = image_size

#                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#                 image_path = f"image_{i+1}.png"
#                 resized_image_with_overlay.save(image_path, 'PNG')
#                 st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
#                                    mime='image/png')

#                 image_data_list[i]['altered_size'] = altered_size

#         if st.button('Save'):
#             for i, image_data in enumerate(image_data_list):
#                 image_data['image'] = base64.b64encode(images[i]).decode('utf-8')
#                 save_to_history(image_data)
#             st.success('Data saved to history.json')

#         st.subheader('API Response')
#         st.json(image_data_list)

#         st.subheader('History Data')
#         history_data = load_json_data()
#         for data in history_data:
#             st.write(data)

#         current_url = st.experimental_get_query_params()
#         query_params = []
#         for key, value in current_url.items():
#             query_params.append(f"{key}={value[0]}")
#         query_string = "&".join(query_params)
#         sharable_link = f"[Sharable Link](?{query_string})"
#         st.markdown(sharable_link)


# if __name__ == '__main__':
#     main()


# import streamlit as st
# from PIL import Image, ImageDraw, ImageFont
# import io
# import json
# from fastapi import FastAPI
# import base64

# app = FastAPI()


# def add_image_overlay(images, image_data_list):
#     images_with_overlay = []

#     for image, image_data in zip(images, image_data_list):
#         img = Image.open(io.BytesIO(image))
#         overlay = Image.new('RGBA', img.size)

#         image_name = image_data['image_name']
#         font_size = image_data['font_size']
#         position = image_data['position']
#         text_color = image_data['text_color']
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
#         draw.text((x, y), image_name, font=font, fill=text_color)

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


# @app.get("/history")
# def get_history():
#     history_data = load_json_data()
#     return history_data


# @app.post("/save")
# def save_to_history(data: dict):
#     image_name = data['image_name']
#     font_size = data['font_size']
#     position = data['position']
#     text_color = data['text_color']
#     altered_size = data.get('altered_size', None)

#     image_data = {
#         'image_name': image_name,
#         'font_size': font_size,
#         'position': position,
#         'text_color': text_color,
#         'altered_size': altered_size
#     }

#     store_json_data(json.dumps(image_data))
#     return {"message": "Data saved to history.json"}


# def main():
#     st.title('Image Overlay API')

#     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     if uploaded_files:
#         image_data_list = []
#         images = [uploaded_file.read() for uploaded_file in uploaded_files]

#         for i, uploaded_file in enumerate(uploaded_files):
#             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
#             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
#             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
#             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

#             image_data_list.append({
#                 'image_name': image_name,
#                 'font_size': font_size,
#                 'position': position,
#                 'text_color': text_color
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
#                     width, height = image_size.split("x")
#                     width = int(width)
#                     height = int(height)
#                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                     altered_size = image_size

#                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#                 image_path = f"image_{i+1}.png"
#                 resized_image_with_overlay.save(image_path, 'PNG')
#                 st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
#                                    mime='image/png')

#                 image_data_list[i]['altered_size'] = altered_size

#         if st.button('Save'):
#             for i, image_data in enumerate(image_data_list):
#                 image_data['image'] = base64.b64encode(images[i]).decode('utf-8')
#                 save_to_history(image_data)
#             st.success('Data saved to history.json')

#         st.subheader('API Response')
#         st.json(image_data_list)

#         st.subheader('History Data')
#         history_data = load_json_data()
#         for data in history_data:
#             st.write(data)

#         current_url = st.experimental_get_query_params()
#         query_params = []
#         for key, value in current_url.items():
#             query_params.append(f"{key}={value[0]}")
#         query_string = "&".join(query_params)
#         sharable_link = f"[Sharable Link](?{query_string})"
#         st.markdown(sharable_link)


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
#         text_color = image_data['text_color']
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
#         draw.text((x, y), image_name, font=font, fill=text_color)

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
#     text_color = data['text_color']
#     altered_size = data.get('altered_size', None)

#     image_data = {
#         'image_name': image_name,
#         'font_size': font_size,
#         'position': position,
#         'text_color': text_color,
#         'altered_size': altered_size
#     }

#     store_json_data(json.dumps(image_data))
#     return {"message": "Data saved to history.json"}


# def main():
#     st.title('Image Overlay API')

#     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     if uploaded_files:
#         image_data_list = []
#         images = [uploaded_file.read() for uploaded_file in uploaded_files]

#         for i, uploaded_file in enumerate(uploaded_files):
#             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
#             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
#             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
#             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

#             image_data_list.append({
#                 'image_name': image_name,
#                 'font_size': font_size,
#                 'position': position,
#                 'text_color': text_color
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
#                     width, height = image_size.split("x")
#                     width = int(width)
#                     height = int(height)
#                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                     altered_size = image_size

#                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#                 image_path = f"image_{i+1}.png"
#                 resized_image_with_overlay.save(image_path, 'PNG')
#                 st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
#                                    mime='image/png')

#                 image_data_list[i]['altered_size'] = altered_size

#         if st.button('Save'):
#             for i, image_data in enumerate(image_data_list):
#                 image_data['image'] = base64.b64encode(images[i]).decode('utf-8')
#                 save_to_history(image_data)
#             st.success('Data saved to history.json')

#         st.subheader('API Response')
#         st.json(image_data_list)

#         st.subheader('History Data')
#         history_data = load_json_data()
#         for data in history_data:
#             st.write(data)

#         sharable_link = st.markdown("To run on remote hosting, deploy the Streamlit app.")
#         st.markdown("Example hosting platforms: Heroku, Streamlit Sharing, etc.")

# if __name__ == '__main__':
#     main()
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
#         text_color = image_data['text_color']
#         font = ImageFont.truetype('./arial.ttf', font_size)

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
#         draw.text((x, y), image_name, font=font, fill=text_color)

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
#     text_color = data['text_color']
#     altered_size = data.get('altered_size', None)

#     image_data = {
#         'image_name': image_name,
#         'font_size': font_size,
#         'position': position,
#         'text_color': text_color,
#         'altered_size': altered_size
#     }

#     store_json_data(json.dumps(image_data))
#     return {"message": "Data saved to history.json"}


# def main():
#     st.title('Image Overlay API')

#     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     if uploaded_files:
#         image_data_list = []
#         images = [uploaded_file.read() for uploaded_file in uploaded_files]

#         for i, uploaded_file in enumerate(uploaded_files):
#             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
#             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
#             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
#             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

#             image_data_list.append({
#                 'image_name': image_name,
#                 'font_size': font_size,
#                 'position': position,
#                 'text_color': text_color
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
#                     width, height = image_size.split("x")
#                     width = int(width)
#                     height = int(height)
#                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                     altered_size = image_size

#                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#                 image_path = f"image_{i+1}.png"
#                 resized_image_with_overlay.save(image_path, 'PNG')
#                 st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
#                                    mime='image/png')

#                 image_data_list[i]['altered_size'] = altered_size

#         if st.button('Save'):
#             for i, image_data in enumerate(image_data_list):
#                 image_data['image'] = base64.b64encode(images[i]).decode('utf-8')
#                 save_to_history(image_data)
#             st.success('Data saved to history.json')

#         st.subheader('API Response')
#         st.json(image_data_list)

#         st.subheader('History Data')
#         history_data = load_json_data()
#         for data in history_data:
#             st.write(data)

        

# if __name__ == '__main__':
#     main()

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
#         text_color = image_data['text_color']
#         font = ImageFont.truetype('./arial.ttf', font_size)

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
#         draw.text((x, y), image_name, font=font, fill=text_color)

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
#     text_color = data['text_color']
#     altered_size = data.get('altered_size', None)

#     image_data = {
#         'image_name': image_name,
#         'font_size': font_size,
#         'position': position,
#         'text_color': text_color,
#         'altered_size': altered_size
#     }

#     store_json_data(json.dumps(image_data))
#     return {"message": "Data saved to history.json"}


# def main():
#     st.title('Image Overlay API')

#     uploaded_files = st.file_uploader('Upload images', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     if uploaded_files:
#         image_data_list = []
#         images = [uploaded_file.read() for uploaded_file in uploaded_files]

#         for i, uploaded_file in enumerate(uploaded_files):
#             image_name = st.text_input(f'Enter image name for Image {i+1}', value=uploaded_file.name)
#             font_size = st.number_input(f'Overlay font size for Image {i+1}', min_value=1, value=20)
#             position = st.selectbox(f'Overlay position for Image {i+1}', ('bottom-left', 'bottom-right', 'top-left', 'top-right'))
#             text_color = st.color_picker(f'Text color for Image {i+1}', '#FFFFFF')

#             image_data_list.append({
#                 'image_name': image_name,
#                 'font_size': font_size,
#                 'position': position,
#                 'text_color': text_color
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
#                     width, height = image_size.split("x")
#                     width = int(width)
#                     height = int(height)
#                     resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
#                     altered_size = image_size

#                 st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

#                 image_path = f"image_{i+1}.png"
#                 resized_image_with_overlay.save(image_path, 'PNG')
#                 st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
#                                    mime='image/png')

#                 image_data_list[i]['altered_size'] = altered_size

#         if st.button('Save'):
#             for i, image_data in enumerate(image_data_list):
#                 save_to_history(image_data)
#             st.success('Data saved to history.json')

#         st.subheader('API Response')
#         formatted_response = []
#         for image_data in image_data_list:
#             formatted_response.append({
#                 'image_name': image_data['image_name'],
#                 'font_size': image_data['font_size'],
#                 'position': image_data['position'],
#                 'text_color': image_data['text_color'],
#                 'altered_size': image_data.get('altered_size', 'Default')
#             })
#         st.json(formatted_response)

#         st.subheader('History Data')
#         history_data = load_json_data()
#         for data in history_data:
#             st.write(data)

# if __name__ == '__main__':
#     main()

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
import base64

from flask import Flask, jsonify

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
                    width, height = image_size.split("x")
                    width = int(width)
                    height = int(height)
                    resized_image_with_overlay = resize_image(image_with_overlay, (width, height))
                    altered_size = image_size

                st.image(resized_image_with_overlay, caption=f"Resized Image {i+1}", use_column_width=True)

                image_path = f"image_{i+1}.png"
                resized_image_with_overlay.save(image_path, 'PNG')
                st.download_button(label=f'Download Image {i+1}', data=open(image_path, 'rb'), file_name=image_path,
                                   mime='image/png')

                image_data_list[i]['altered_size'] = altered_size

        if st.button('Save'):
            for i, image_data in enumerate(image_data_list):
                image_data['image'] = base64.b64encode(images[i]).decode('utf-8')
                save_to_history(image_data)
            st.success('Data saved to history.json')

        st.subheader('API Response')
        st.json(image_data_list)

        st.subheader('History Data')
        history_data = load_json_data()
        for data in history_data:
            st.write(data)


if __name__ == '__main__':
    main()
