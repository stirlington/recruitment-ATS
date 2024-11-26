import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests  # Import requests to make API calls

# Function to fetch data from ATS API
def fetch_ats_data():
    # Replace with your actual ATS API endpoint
    response = requests.get("https://api.yourats.com/data")
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON data
    else:
        st.error("Failed to fetch data from ATS")
        return None

# Fetch data from ATS
ats_data = fetch_ats_data()

if ats_data:
    # Extract relevant data from the fetched data
    invoiced_amount = ats_data['invoiced_amount']
    offers_made = ats_data['offers_made']
    conversion_rate = ats_data['conversion_rate']
    contacted_candidates = ats_data['contacted_candidates']
    slipping_candidates = ats_data['slipping_candidates']
    time_to_first_contact = ats_data['time_to_first_contact']
    career_site_views = ats_data['career_site_views']
    applied_candidates = ats_data['applied_candidates']
    
    # Candidate sources over time (bar chart)
    categories = ['Applied', 'Email', 'Sourced', 'Added manually']
    days = np.arange(1, 31)
    candidates_per_origin = np.random.randint(5, 30, (4, len(days)))  # Replace with actual data if available

    # Calendar and email breakdowns (pie charts)
    calendar_labels = ['On-site interviews', 'Phone interviews', 'Meetings']
    calendar_sizes = [40, 35, 25]
    email_labels = ['Sent', 'Received']
    email_sizes = [60, 40]

    # Drop-off and proceed rates (progress bars)
    drop_off_rate = 93 / 185
    proceed_rate = 59 / 185

    # Layout: Last 30 Days Section
    st.markdown("#### Last 30 Days")
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.subheader("New Candidates per Origin")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        for i, category in enumerate(categories):
            ax1.bar(days, candidates_per_origin[i], label=category, alpha=0.7)
        ax1.set_title("New Candidates per Origin")
        ax1.set_xlabel("Days")
        ax1.set_ylabel("Number of Candidates")
        ax1.legend()
        ax1.grid(axis='y')
        st.pyplot(fig1)

    with col2:
        st.subheader("Avg. Evaluation Score")
        st.markdown(f"### {conversion_rate}%")
        st.progress(conversion_rate / 100)

    with col3:
        st.subheader("Key Metrics")
        st.metric(label="Contacted Candidates", value=contacted_candidates)
        st.metric(label="Candidates Slipping Away", value=slipping_candidates)
        st.metric(label="Avg. Time to First Contact (days)", value=time_to_first_contact)
        st.metric(label="Career Site Views", value=career_site_views)
        st.metric(label="Applied Candidates", value=applied_candidates)

    # Calendar Events and Emails Breakdown Section
    st.markdown("---")
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Calendar Events Breakdown")
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(calendar_sizes, labels=calendar_labels, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

    with col5:
        st.subheader("Emails Sent vs Received")
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        ax3.pie(email_sizes, labels=email_labels, autopct='%1.1f%%', startangle=90)
        ax3.axis('equal')
        st.pyplot(fig3)

    # Drop-off and Proceed Rates Section
    st.markdown("---")
    st.subheader("All Time Metrics")

    col6, col7 = st.columns(2)

    with col6:
        st.write("**Drop-off Rate**")
        st.progress(drop_off_rate)
        st.write(f"{int(drop_off_rate * 185)} out of 185 candidates were disqualified.")

    with col7:
        st.write("**Proceed Rate**")
        st.progress(proceed_rate)
        st.write(f"{int(proceed_rate * 185)} out of 185 candidates were proceeded further in the pipeline.")
