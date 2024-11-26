import streamlit as st
import sqlite3
import os
from datetime import datetime

# Database setup
DB_FILE = "recruitment.db"
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            linkedin TEXT,
            resume_path TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT,
            status TEXT DEFAULT 'Open'
        )
    """)
    conn.commit()
    conn.close()

# Helper functions
def add_candidate(name, email, phone, linkedin, resume_path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO candidates (name, email, phone, linkedin, resume_path)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, linkedin, resume_path))
    conn.commit()
    conn.close()

def get_candidates():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_job(title, description, location):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jobs (title, description, location)
        VALUES (?, ?, ?)
    """, (title, description, location))
    conn.commit()
    conn.close()

def get_jobs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Streamlit UI
st.set_page_config(page_title="Recruitment CRM/ATS", layout="wide")

st.sidebar.title("Navigation")
pages = ["Dashboard", "Manage Candidates", "Manage Jobs", "Settings"]
selected_page = st.sidebar.radio("Go to", pages)

if selected_page == "Dashboard":
    st.title("Dashboard")
    
    candidates_count = len(get_candidates())
    jobs_count = len(get_jobs())
    
    st.metric("Total Candidates", candidates_count)
    st.metric("Total Job Postings", jobs_count)

elif selected_page == "Manage Candidates":
    st.title("Manage Candidates")
    
    with st.form("add_candidate_form"):
        st.subheader("Add New Candidate")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn Profile")
        resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
        
        if st.form_submit_button("Add Candidate"):
            if resume_file:
                resume_path = os.path.join("uploads", resume_file.name)
                with open(resume_path, "wb") as f:
                    f.write(resume_file.read())
                add_candidate(name, email, phone, linkedin, resume_path)
                st.success(f"Candidate {name} added successfully!")
    
    st.subheader("Candidate List")
    candidates = get_candidates()
    
    for candidate in candidates:
        st.write(f"**Name**: {candidate[1]}")
        st.write(f"**Email**: {candidate[2]}")
        st.write(f"**Phone**: {candidate[3]}")
        st.write(f"**LinkedIn**: {candidate[4]}")
        if candidate[5]:
            st.write(f"[Download Resume](./{candidate[5]})")

elif selected_page == "Manage Jobs":
    st.title("Manage Jobs")
    
    with st.form("add_job_form"):
        st.subheader("Add New Job Posting")
        title = st.text_input("Job Title")
        description = st.text_area("Job Description")
        location = st.text_input("Location")
        
        if st.form_submit_button("Add Job"):
            add_job(title, description, location)
            st.success(f"Job '{title}' added successfully!")
    
    st.subheader("Job List")
    
    jobs = get_jobs()
    
    for job in jobs:
        st.write(f"**Title**: {job[1]}")
        st.write(f"**Description**: {job[2]}")
        st.write(f"**Location**: {job[3]}")
        st.write("---")

elif selected_page == "Settings":
    st.title("Settings")
    
    with st.form("settings_form"):
        company_name = st.text_input("Company Name", value="Your Company Name")
        tagline = st.text_input("Tagline", value="Your Tagline Here")
        
        logo_file = st.file_uploader("Upload Logo", type=["png", "jpg"])
        
        if logo_file:
            logo_path = os.path.join("uploads", logo_file.name)
            with open(logo_path, "wb") as f:
                f.write(logo_file.read())
        
        if st.form_submit_button("Save Settings"):
            # Save settings logic here (e.g., update database or config file)
            st.success("Settings updated successfully!")
