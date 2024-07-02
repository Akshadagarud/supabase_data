import streamlit as st
from supabase import create_client, Client

# Supabase configuration
url =st.secrets["SUPABASE_URL"]
key =st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Set up the form
st.title('User_Registration_Info')

with st.form(key='user_form'):
    name = st.text_input('Name')
    phone_number = st.text_input("Phone Number")
    if not (phone_number.isdigit() and len(phone_number) == 10):
        st.warning('Please enter a valid 10-digit phone number.')
    email_id = st.text_input('Email ID')
    if not (email_id.strip().endswith('@gmail.com') and '@' in email_id):
        st.warning('Please enter a valid Gmail email address.')
    field = st.checkbox('Field')
    location = st.text_input('Location')
    domain = st.selectbox('Domain', ['ML', 'DS', 'AI', 'DL', 'Other'])
    
    
    # Submit button
    submit_button = st.form_submit_button(label='Submit')

# Display the submitted form data and store it in Supabase
    if submit_button:
        phone_valid = phone_number.isdigit() and len(phone_number) == 10
        email_valid = email_id.strip().endswith('@gmail.com') and '@' in email_id
     
        if phone_valid and email_valid:
            # Check for existing records with the same email_id
            response = supabase.table("User data").select("*").eq("email_id", email_id).execute()

        if response.data:
                st.error("A record with this Email ID already exists.")
        else:
                st.write('Form submitted successfully!')
                
            
    
    # Insert data into Supabase
    data = {
        'name': name,
        'phone_number': phone_number,
        'email_id': email_id,
        'field': field,
        'location': location,
        'domain': domain
    }
    
    try:
    # Insert data into a table
        response = supabase.table('User data').insert(data).execute()

    # Check for successful insertion (Supabase may not return status_code)
        if response.status == 201:
           print("Insertion successful:", response.get('data'))
        else:
           print("Insertion failed:", response.get('status'), response.get('error'))

    except Exception as e:
        print("Error:", e)
