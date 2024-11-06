import streamlit as st 
import google.generativeai as genai 
import os 
from dotenv import load_dotenv
from PIL import Image 


load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_responce(image,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt,image[0]])
    return response.text 

def input_image_setup(uploaded_image):
    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        
        image_parts= [
            {
                'mime_type' : uploaded_image.type, 
                'data' : bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No image uploaded')
    

### Streamli app 
st.set_page_config(page_title="Food Advisor APP")
st.header("Food Advisor APP")
uploaded_image = st.file_uploader("Choose an image...",type=['jpeg', 'png', 'jpg'])
image =''

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image,'Uploaded Image',use_column_width=True)

submit = st.button("Tell me about the food")


Advisor_prompt = '''
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               you can also mention whether the food is healthy or not, and also mention the 
               percentage split of the ratio of carbohydrates, fats, fibers, sugar and protein in the food,
               if the food is not healthy then mention the possible ways to make it healthy and which excercies
               are good for this kind of food.

'''

if submit: 
    image_data = input_image_setup(uploaded_image)
    response = get_gemini_responce(image_data,Advisor_prompt)
    st.subheader("The Response is:")
    st.write(response)
