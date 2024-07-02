import streamlit as st
from supabase import create_client, Client

# Supabase configuration
url =st.secrets["SUPABASE_URL"]
key =st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Set up the form
st.title('User_Registration_Info')

with st.form(key='user_form'):
    name = st.text_input("Name")
    if not name.isalpha():
        st.warning('Please enter a valid name containing only alphabetic characters.')
    
    phone_number = st.text_input("Phone Number")
    if not (phone_number.isdigit() and len(phone_number) == 10):
        st.warning('Please enter a valid 10-digit phone number.')

    email_id = st.text_input('Email ID')

    if not (email_id.strip().endswith("@gmail.com") and "@" in email_id):
        st.warning('Please enter a valid Gmail email address.')

    field = st.checkbox('Field')
    location = st.text_input('Location')
    domain = st.selectbox("Domain", ["ML", "DS", "AI", "DL", "Other"])
    
    
 # Submit button
    submit_button = st.form_submit_button(label="Submit")

# Display the submitted form data and store it in Supabase
if submit_button:
    phone_valid = phone_number.isdigit() and len(phone_number) == 10
    email_valid = email_id.strip().endswith("@gmail.com") and "@" in email_id
    name_valid = name.isalpha()

    if phone_valid and email_valid and name_valid:
        try:
            # Check if the user with the same email already exists
            response = supabase.table("User data").select("*").eq("email_id", email_id).execute()

            if response.status_code == 400:
                st.error(f"Error fetching data from Supabase: {response.content}")

            else:
                data = response.get("data")

                if data:
                    st.error("A record with this Email ID already exists.")
                else:
                    # Insert data into Supabase
                    data_to_insert = {
                        "name": name,
                        "phone_number": phone_number,
                        "email_id": email_id,
                        "field": field,
                        "location": location,
                        "domain": domain
                    }

                    # Insert data into a table
                    insert_response = supabase.table('User data').insert(data_to_insert).execute()

                    if insert_response.status_code == 201:
                        st.success("Form submitted successfully")
                    else:
                        st.error(f"Insertion failed: {insert_response.content}")

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please correct the highlighted fields and submit again.")
