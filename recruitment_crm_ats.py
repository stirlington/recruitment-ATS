# recruitment_crm_ats.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recruitment.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

# Database Models
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    linkedin = db.Column(db.String(200))
    resume = db.Column(db.String(200))  # Path to uploaded CV

class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default="Open")  # Open/Closed

class CompanySettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo_path = db.Column(db.String(200))
    company_name = db.Column(db.String(100))
    tagline = db.Column(db.String(200))

# Routes
@app.route('/')
def dashboard():
    candidates_count = Candidate.query.count()
    jobs_count = JobPosting.query.count()
    return render_template('dashboard.html', candidates_count=candidates_count, jobs_count=jobs_count)

@app.route('/candidates', methods=['GET', 'POST'])
def manage_candidates():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        linkedin = request.form['linkedin']
        resume_file = request.files['resume']
        
        if resume_file:
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(resume_path)
        else:
            resume_path = None
        
        candidate = Candidate(name=name, email=email, phone=phone, linkedin=linkedin, resume=resume_path)
        db.session.add(candidate)
        db.session.commit()
        flash('Candidate added successfully!', 'success')
        return redirect(url_for('manage_candidates'))
    
    candidates = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates)

@app.route('/jobs', methods=['GET', 'POST'])
def manage_jobs():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        
        job_posting = JobPosting(title=title, description=description, location=location)
        db.session.add(job_posting)
        db.session.commit()
        flash('Job posting created successfully!', 'success')
        return redirect(url_for('manage_jobs'))
    
    jobs = JobPosting.query.all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    settings_data = CompanySettings.query.first()
    
    if request.method == 'POST':
        company_name = request.form['company_name']
        tagline = request.form['tagline']
        logo_file = request.files['logo']
        
        if logo_file:
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_file.filename)
            logo_file.save(logo_path)
            
            if settings_data:
                settings_data.logo_path = logo_path
            else:
                settings_data = CompanySettings(logo_path=logo_path)
        
        if settings_data:
            settings_data.company_name = company_name
            settings_data.tagline = tagline
            db.session.commit()
        else:
            new_settings = CompanySettings(company_name=company_name, tagline=tagline)
            db.session.add(new_settings)
            db.session.commit()
        
        flash('Settings updated successfully!', 'success')
    
    return render_template('settings.html', settings=settings_data)

# Utility function to initialize database
@app.before_first_request
def create_tables():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure upload directory exists
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
