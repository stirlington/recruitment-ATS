import streamlit as st
import pandas as pd
import requests  # Import requests to make API calls

# Function to fetch candidates data from ATS API
def fetch_candidates_data():
    # Replace with your actual ATS API endpoint for candidates
    response = requests.get("https://api.yourats.com/candidates")
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON data
    else:
        st.error("Failed to fetch candidates data from ATS")
        return None

# Fetch candidates data
candidates_data = fetch_candidates_data()

if candidates_data:
    # Convert the candidates data to a DataFrame for easier manipulation
    df = pd.DataFrame(candidates_data)

    # Search filters
    st.sidebar.header("Search Candidates")
    name_filter = st.sidebar.text_input("Search by Name")
    email_filter = st.sidebar.text_input("Search by Email")
    status_filter = st.sidebar.selectbox("Select Status", options=["All", "Applied", "Interviewing", "Hired", "Rejected"])
    position_filter = st.sidebar.text_input("Search by Position Applied For")
    source_filter = st.sidebar.text_input("Search by Source")

    # Apply filters
    if name_filter:
        df = df[df['name'].str.contains(name_filter, case=False)]
    if email_filter:
        df = df[df['email'].str.contains(email_filter, case=False)]
    if status_filter != "All":
        df = df[df['status'] == status_filter]
    if position_filter:
        df = df[df['position_applied_for'].str.contains(position_filter, case=False)]
    if source_filter:
        df = df[df['source'].str.contains(source_filter, case=False)]

    # Display the filtered candidates
    st.header("Candidates List")
    st.dataframe(df)

else:
    st.warning("No candidates data available.") 
