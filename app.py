import streamlit as st
import psycopg2

# Create a singleton object for the database connection
@st.experimental_singleton
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
    name = st.text_input("Name")
    email = st.text_input("Email")
    submit = st.form_submit_button("Submit")

# If the submit button is clicked, write the data to the database
if submit:
    cursor = get_database_connection().cursor()
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(query, (name, email))
    get_database_connection().commit()

# Display a message
st.write("Data saved to database!")
