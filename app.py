import streamlit as st
import psycopg2
import pandas as pd
import random
from typing import List, Tuple

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# CSV_URL = "https://raw.githubusercontent.com/shkkonda/imageEloCalc/main/nokiamon_image.csv"
# final_df = pd.read_csv(CSV_URL)

# def get_random_image_pair(df) -> Tuple[str, str]:
#     left_image = random.choice(df['image_link'])
#     right_image = random.choice(df['image_link'])

#     while left_image == right_image:
#         right_image = random.choice(df['image_link'])

#     return left_image, right_image

# left_image, right_image = get_random_image_pair(final_df)

@st.cache_resource
def get_database_connection():
    conn = psycopg2.connect(
        host="database-1.cv9g4hhrgmvg.us-east-1.rds.amazonaws.com",
        user="postgres",
        password="eRYebFlJePOFRZeVVuQT",
        database=""
    )
    return conn

@st.cache  # Cache the DataFrame
def fetch_table_as_dataframe():
    conn = get_database_connection()
    cursor = conn.cursor()

    # Execute the query to fetch the table
    cursor.execute("SELECT * FROM noki_combos")

    # Fetch all the rows
    rows = cursor.fetchall()

    # Get the column names
    columns = [desc[0] for desc in cursor.description]

    # Create a DataFrame with the fetched data
    df = pd.DataFrame(rows, columns=columns)

    return df

# Usage
noki_combos_df = fetch_table_as_dataframe()

def get_random_images(df):
    # Get a random row from the DataFrame
    random_row = df.sample(n=1, random_state=random.seed())

    # Extract the values from the 'noki_1' and 'noki_2' columns
    left_image = random_row['noki_1'].values[0]
    right_image = random_row['noki_2'].values[0]

    # Return the left_image and right_image
    return left_image, right_image

left_image, right_image = get_random_images(noki_combos_df)

wallet_address = st.text_input('Enter Wallet Address')  # New Field for Wallet Address

# Create a grid layout with two columns
col1, col2 = st.columns(2)

# Form 1 in the first column
with col1.form("my_form"):
    image_link = st.empty()
    image_link.image(left_image, use_column_width=True)
    submit = st.form_submit_button("Submit")

# Form 2 in the second column
with col2.form("my_form_2"):
    image_link_2 = st.empty()
    image_link_2.image(right_image, use_column_width=True)
    submit_2 = st.form_submit_button("Submit")

# If the submit button of Form 1 is clicked, write the data to the database
if submit:
    cursor = get_database_connection().cursor()
    query = "INSERT INTO images_wallet (left_image_link, right_image_link, selected_image_link, wallet_address) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (image_link.url, image_link_2.url, image_link.url, wallet_address))
    get_database_connection().commit()

# If the submit button of Form 2 is clicked, write the data to the database
if submit_2:
    cursor = get_database_connection().cursor()
    query = "INSERT INTO images_wallet (left_image_link, right_image_link, selected_image_link, wallet_address) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (image_link.url, image_link_2.url, image_link_2.url, wallet_address))
    get_database_connection().commit()

# Display a message
st.write("Data saved to database!")
