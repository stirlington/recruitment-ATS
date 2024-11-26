import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set up the page
st.set_page_config(page_title="Recruitment Dashboard", layout="wide")

# Title and description
st.title("Recruitment Dashboard")
st.markdown("### Overview of key recruitment metrics for the last 30 days")

# Data simulation (replace with real data from your database)
invoiced_amount = 50000  # Total invoiced amount (£)
offers_made = 30  # Total offers made
conversion_rate = 65  # Conversion rate in percentage
contacted_candidates = 32
slipping_candidates = 68
time_to_first_contact = 4  # Days
career_site_views = 1451
applied_candidates = 178

# Candidate source data
categories = ['Applied', 'Email', 'Sourced', 'Added manually']
days = np.arange(1, 31)
candidates_per_origin = np.random.randint(5, 30, (4, len(days)))

# Calendar and email breakdowns
calendar_labels = ['On-site interviews', 'Phone interviews', 'Meetings']
calendar_sizes = [40, 35, 25]
email_labels = ['Sent', 'Received']
email_sizes = [60, 40]

# Layout: Stats + Charts
col1, col2, col3 = st.columns([2, 2, 1])

# Column 1: Candidate Sources Chart
with col1:
    st.subheader("New Candidates per Origin (Last 30 Days)")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    for i, category in enumerate(categories):
        ax1.bar(days, candidates_per_origin[i], label=category, alpha=0.7)
    ax1.set_title("New Candidates per Origin (Last 30 Days)")
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Number of Candidates")
    ax1.legend()
    ax1.grid(axis='y')
    st.pyplot(fig1)

# Column 2: Invoice and Offer Summary Pie Chart
with col2:
    st.subheader("Invoice and Offer Summary")
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    labels = ['Invoiced (£)', 'Offers Made', 'Conversion Rate (%)']
    sizes = [invoiced_amount, offers_made * 1000, conversion_rate * 100]
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax2.axis('equal')  
    st.pyplot(fig2)

# Column 3: Key Metrics Summary
with col3:
    st.subheader("Key Metrics")
    st.metric(label="Contacted Candidates", value=contacted_candidates)
    st.metric(label="Candidates Slipping Away", value=slipping_candidates)
    st.metric(label="Avg. Time to First Contact (days)", value=time_to_first_contact)
    st.metric(label="Career Site Views", value=career_site_views)
    st.metric(label="Applied Candidates", value=applied_candidates)

# Row: Calendar Events and Emails Breakdown
st.subheader("Calendar Events and Email Breakdown")
col4, col5 = st.columns(2)

with col4:
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.pie(calendar_sizes, labels=calendar_labels, autopct='%1.1f%%', startangle=90)
    ax3.axis('equal')  
    ax3.set_title('Calendar Events Breakdown')
    st.pyplot(fig3)

with col5:
    fig4, ax4 = plt.subplots(figsize=(6, 6))
    ax4.pie(email_sizes, labels=email_labels, autopct='%1.1f%%', startangle=90)
    ax4.axis('equal')  
    ax4.set_title('Emails Sent vs Received')
    st.pyplot(fig4)

# Footer: Summary Text
st.markdown("---")
st.markdown(f"**Total Invoiced:** £{invoiced_amount:,}")
st.markdown(f"**Offers Made:** {offers_made}")
st.markdown(f"**Conversion Rate:** {conversion_rate}%")
