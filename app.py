import streamlit as st
import psycopg2
import pandas as pd
import random
from typing import Tuple

CSV_URL = "https://raw.githubusercontent.com/shkkonda/imageEloCalc/main/nokiamon_image.csv"
final_df = pd.read_csv(CSV_URL)

def get_random_image(df) -> Tuple[str, str]:
    row = random.choice(df.index)
    left_image = df.loc[row, 'image_link']
    name = df.loc[row, 'name']
    return left_image, name

@st.cache_resource
def get_database_connection():
    conn = psycopg2.connect(
        host="database-1.cv9g4hhrgmvg.us-east-1.rds.amazonaws.com",
        user="postgres",
        password="eRYebFlJePOFRZeVVuQT",
        database=""
    )
    return conn

# Create a form
with st.form("my_form"):
    random_image, name = get_random_image(final_df)
    image_link = st.empty()
    image_link.image(random_image)
    submit = st.form_submit_button(name)

# If the submit button is clicked, write the data to the database
if submit:
    cursor = get_database_connection().cursor()
    query = "INSERT INTO images (image_link) VALUES (%s)"
    cursor.execute(query, (random_image,))
    get_database_connection().commit()

# Display a message
st.write("Data saved to database!")
