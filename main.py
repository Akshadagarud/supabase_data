import streamlit as st
from supabase import create_client, Client
import re

# Supabase configuration
url =st.secrets["SUPABASE_URL"]
key =st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Set up the form
st.title('User_Registration_Info')

with st.form(key="form1"):
    name = st.text_input(label="Name*")
    phone_number = st.text_input(label="Phone Number*")
    email_id = st.text_input(label="Email ID*")
    field = st.toggle("Field Engineer")
    location = st.text_input(label="Location")
    domain_option = ['IT','CS','AI']
    domain = st.selectbox(label="Domain", options=domain_option)
    submit = st.form_submit_button(label="Submit")

if submit:
    if not name or not phone_number or not email_id:
        st.warning("Please fill out the Name, Phone Number, and Email fields.")
    else:
        if not re.match(r"^[a-zA-Z ]+$", name):
            st.warning("Invalid name format. Please enter a name that only contains alphabets and spaces.")
        elif not phone_number.isdigit() or len(phone_number)!= 10 or not phone_number.startswith(("7", "8", "9")):
            st.warning("Invalid phone number. Phone number should be 10 digits, start with 7, 8, or 9, and only contain numbers.")
        elif not re.match(r"^[a-zA-Z0-9_+\-.]+@[a-zA-Z]+\.[a-zA-Z]+$", email_id):
            st.warning("Invalid email format. Please enter a valid email address.")
        elif not re.match(r"^[a-zA-Z ]+$", location):
            st.warning("Invalid location format. Please enter a name that only contains alphabets and spaces.")
        else:
            existing_email = supabase.table("User data").select("email_id").eq("email_id", email_id).execute()
            if existing_email.data:
                st.warning("Email already exists in the database. Please use a different email address.")
            else:
                data = {
                    "name": name,
                    "phone_number": phone_number,
                    "email_id": email_id,
                    "location": location,
                    "domain": domain,
                    "field": field
                }
                response = supabase.table("User data").insert([data]).execute()

                if response:
                    st.success("Data inserted successfully.")
                else:
                    st.error("Failed to insert data. Please try again.")

    
