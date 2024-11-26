import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Recruitment Dashboard", layout="wide")

st.title("Recruitment Dashboard")
st.markdown("### Overview of key recruitment metrics for the last 30 days")

# Simulated data (replace with real data from your database)
invoiced_amount = 50000
offers_made = 30
conversion_rate = 75
contacted_candidates = 32
slipping_candidates = 68
time_to_first_contact = 4
career_site_views = 1451
applied_candidates = 178

categories = ['Applied', 'Email', 'Sourced', 'Added manually']
days = np.arange(1, 31)
candidates_per_origin = np.random.randint(5, 30, (4, len(days)))

calendar_labels = ['On-site interviews', 'Phone interviews', 'Meetings']
calendar_sizes = [40, 35, 25]
email_labels = ['Sent', 'Received']
email_sizes = [60, 40]

drop_off_rate = 93 / 185
proceed_rate = 59 / 185

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
