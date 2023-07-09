import streamlit as st
import psycopg2
import pandas as pd
import random
from typing import List, Tuple
from streamlit_option_menu import option_menu

st.title("NokiRank: Unleash Your Inner Nokiamon Judge!")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add the menu links to the sidebar
menu_selection = option_menu(None, ["Choose", "Ranks"],
                             icons=['image', "table"],
                             menu_icon="cast", default_index=0, orientation="horizontal")

@st.cache_resource
def get_database_connection():
    conn = psycopg2.connect(**st.secrets["postgres"])
    return conn

def display_thank_you_note():
    st.write("Thank you for your submissions! You've been a great Nokiamon judge!")
    continue_button = st.button("Continue rating more")
    if continue_button:
        st.session_state.submission_counter = 0
        st.session_state.left_image = None
        st.session_state.right_image = None
        st.experimental_rerun()
    

# Counter to keep track of submissions
if "submission_counter" not in st.session_state:
    st.session_state.submission_counter = 0

if menu_selection == "Ranks":
    # Add your code for the second page here
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM noki_selections")

    # Fetch all the rows
    rows = cursor.fetchall()
    
    # Get the column names
    columns = [desc[0] for desc in cursor.description]
    
    # Create a DataFrame with the fetched data
    df = pd.DataFrame(rows, columns=columns)
    
    import math
    import pandas as pd
    
    def calculate_elo_rating(games_df, k_factor=32):
        # Create a dictionary to store the ratings and game counts for each contender
        ratings = {}
    
        # Iterate over each row in the games DataFrame
        for _, row in games_df.iterrows():
            contender_1 = row['left_image_link']
            contender_2 = row['right_image_link']
            winner = row['selected_image_link']
    
            # Initialize ratings for new contenders
            if contender_1 not in ratings:
                ratings[contender_1] = {'rating': 1000, 'games': 0}
            if contender_2 not in ratings:
                ratings[contender_2] = {'rating': 1000, 'games': 0}
    
            # Update game counts for contenders
            ratings[contender_1]['games'] += 1
            ratings[contender_2]['games'] += 1
    
            # Calculate expected scores
            expected_score_contender_1 = 1 / (1 + math.pow(10, (ratings[contender_2]['rating'] - ratings[contender_1]['rating']) / 400))
            expected_score_contender_2 = 1 / (1 + math.pow(10, (ratings[contender_1]['rating'] - ratings[contender_2]['rating']) / 400))
    
            # Update ratings based on the outcome
            if winner == contender_1:
                ratings[contender_1]['rating'] += k_factor * (1 - expected_score_contender_1)
                ratings[contender_2]['rating'] += k_factor * (0 - expected_score_contender_2)
            elif winner == contender_2:
                ratings[contender_1]['rating'] += k_factor * (0 - expected_score_contender_1)
                ratings[contender_2]['rating'] += k_factor * (1 - expected_score_contender_2)
    
        return ratings
    
    
    # Calculate Elo ratings
    ratings = calculate_elo_rating(df)
    
    # Convert ratings dictionary to a DataFrame
    ratings_df = pd.DataFrame(ratings.items(), columns=['nokiamon', 'rating'])
    ratings_df['Matches Featured In'] = ratings_df['nokiamon'].map(lambda x: ratings[x]['games'])
    ratings_df['elo_rating'] = ratings_df['nokiamon'].map(lambda x: ratings[x]['rating'])
    
    ratings_df = ratings_df.sort_values(by='elo_rating', ascending=False)[['nokiamon', 'elo_rating', 'Matches Featured In']]
    styled_df = ratings_df.style.set_properties(**{'text-align': 'center'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])

    # Display ratings_df as a table with images
    st.dataframe(styled_df, height=500, hide_index=True, column_config={
        "nokiamon": st.column_config.ImageColumn(
            "Nokiamon", help="Image"
        ),
        "elo_rating": st.column_config.NumberColumn("Likability Score", format='%.0f')
    }, use_container_width=True)

    
else:
    if st.session_state.submission_counter >= 10:
        display_thank_you_note()
    else:
        messages = [
            "Great choice!",
            "Well done!",
            "Fantastic!",
            "Awesome selection!",
            "You've got good taste!",
            "Impressive choice!",
            "You're on a roll!",
            "Excellent decision!",
            "Way to go!",
            "You're a Nokiamon master!",
            "Outstanding selection!",
            "That's a winner!",
            "You know your Nokiamon!",
            "Amazing pick!",
            "That's a rare Nokiamon!"
        ]
    
        @st.cache_data  # Cache the DataFrame
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
    
        if 'left_image' not in st.session_state:
            st.session_state.left_image = left_image
        if 'right_image' not in st.session_state:
            st.session_state.right_image = right_image
    
        if "wallet_address" not in st.session_state:
            st.session_state.wallet_address = ' '
        
        wallet_address = st.text_input('Enter Wallet Address (Optional - Add if you want to be considered for free Noki airdrops)', value=st.session_state.wallet_address)
        st.session_state.wallet_address = wallet_address

    
        # Create a grid layout with two columns
        col1, col2 = st.columns(2)
    
        # Form 1 in the first column
        with col1.form("my_form"):
            image_link = st.empty()
            image_link.image(left_image, use_column_width=True)
            form_submit = st.form_submit_button("Submit")
    
        # Form 2 in the second column
        with col2.form("my_form_2"):
            image_link_2 = st.empty()
            image_link_2.image(right_image, use_column_width=True)
            form_submit_2 = st.form_submit_button("Submit")
    
        # If the submit button of Form 1 is clicked, write the data to the database
        if form_submit:
            cursor = get_database_connection().cursor()
            query = "INSERT INTO noki_selections_dev (left_image_link, right_image_link, selected_image_link, wallet_address) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (st.session_state.left_image, st.session_state.right_image, st.session_state.left_image, wallet_address))
            get_database_connection().commit()
            st.session_state.left_image = left_image
            st.session_state.right_image = right_image
            # Increment the submission counter after each submission
            st.session_state.submission_counter += 1
            # Display a randomly selected success message
            success_message = random.choice(messages)
            st.write(success_message)
    
        # If the submit button of Form 2 is clicked, write the data to the database
        if form_submit_2:
            cursor = get_database_connection().cursor()
            query = "INSERT INTO noki_selections_dev (left_image_link, right_image_link, selected_image_link, wallet_address) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (st.session_state.left_image, st.session_state.right_image, st.session_state.right_image, wallet_address))
            get_database_connection().commit()
            st.session_state.left_image = left_image
            st.session_state.right_image = right_image
            # Increment the submission counter after each submission
            st.session_state.submission_counter += 1
            # Display a randomly selected success message
            success_message = random.choice(messages)
            st.write(success_message)
    
        # Update session state variables on any non-submit interaction
        if not form_submit and not form_submit_2:
            st.session_state.left_image = left_image
            st.session_state.right_image = right_image

        st.write(st.session_state.submission_counter)


