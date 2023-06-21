import streamlit as st
import psycopg2
import pandas as pd
import random

CSV_URL = "https://raw.githubusercontent.com/shkkonda/imageEloCalc/main/nokiamon_image.csv"
final_df = pd.read_csv(CSV_URL)

def get_random_image(df) -> str:
    left_image = random.choice(df['image_link'])
    return left_image

@st.cache_resource
def get_database_connection():
    conn = psycopg2.connect(
        host="database-1.cv9g4hhrgmvg.us-east-1.rds.amazonaws.com",
        user="postgres",
        password="eRYebFlJePOFRZeVVuQT",
        database=""
    )
    return conn

# Create a grid layout with two columns
col1, col2 = st.columns(2)

# Form 1 in the first column
with col1.form("my_form"):
    random_image = get_random_image(final_df)
    image_link = st.empty()
    image_link.image(random_image)
    submit = st.form_submit_button("Submit")

# Form 2 in the second column
with col2.form("my_form_2"):
    random_image_2 = get_random_image(final_df)
    image_link_2 = st.empty()
    image_link_2.image(random_image_2)
    submit_2 = st.form_submit_button("Submit")

# If the submit button of Form 1 is clicked, write the data to the database
if submit:
    cursor = get_database_connection().cursor()
    query = "INSERT INTO images (image_link) VALUES (%s)"
    cursor.execute(query, (random_image,))
    get_database_connection().commit()

# If the submit button of Form 2 is clicked, write the data to the database
if submit_2:
    cursor = get_database_connection().cursor()
    query = "INSERT INTO images (image_link) VALUES (%s)"
    cursor.execute(query, (random_image_2,))
    get_database_connection().commit()

# Display a message
st.write("Data saved to database!")
