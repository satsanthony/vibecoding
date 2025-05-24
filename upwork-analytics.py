#https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import re

# Set page configuration
st.set_page_config(page_title="Upwork Job Analytics", layout="wide")
st.title("Upwork Job Market Analysis Dashboard")

# Function to load and preprocess data
@st.cache_data
def load_and_process_data():
    # Load the data
    df = pd.read_csv('upwork-extract.csv')
    
    # Define a mapping of original column names to meaningful names
    column_map = {
        'text-light 2': 'posting_date',
        'air3-link': 'job_title',
        'air3-link href': 'job_url',
        'highlight': 'primary_skill',
        'air3-badge-tagline': 'payment_status',
        'sr-only 3': 'rating_label',
        'air3-rating-value-text': 'client_rating',
        'air3-popper-content': 'rating_details',
        'total_spent': 'client_spent',
        'air3-badge-tagline 3': 'spent_label',
        'air3-badge-tagline 4': 'client_country',
        'job-tile-info-list': 'payment_type',
        'job-tile-info-list 2': 'experience_level',
        'mr-1': 'estimated_time_label',
        'job-tile-info-list 3': 'project_duration',
        'mb-0': 'job_description',
        'highlight 2': 'skill_1_highlight',
        'air3-token': 'skill_1',
        'air3-token 2': 'skill_2',
        'air3-token 3': 'skill_3',
        'font-weight-light': 'proposals_label',
        'num_proposals': 'proposal_count',
        'air3-token 4': 'skill_4',
        'air3-token 5': 'skill_5',
        'highlight 3': 'skill_2_highlight',
        'highlight 4': 'skill_3_highlight',
        'highlight 5': 'skill_4_highlight',
        'highlight 6': 'skill_5_highlight',
        'highlight-color': 'highlight_color_1',
        'highlight-color 2': 'highlight_color_2',
        'air3-token 6': 'skill_6'
    }
    
    # Apply the column renaming
    renamed_df = df.rename(columns=column_map)
    
    # Extract hourly rate from payment_type
    def extract_hourly_rate(payment_type):
        if pd.isna(payment_type) or 'Hourly' not in str(payment_type):
            return np.nan
        
        pattern = r'\$(\d+\.\d+)\s*-\s*\$(\d+\.\d+)'
        match = re.search(pattern, str(payment_type))
        
        if match:
            min_rate = float(match.group(1))
            max_rate = float(match.group(2))
            return (min_rate + max_rate) / 2
        else:
            return np.nan
    
    renamed_df['hourly_rate'] = renamed_df['payment_type'].apply(extract_hourly_rate)
    
    # Extract fixed price budget
    def extract_fixed_price(payment_type):
        if pd.isna(payment_type) or 'Fixed' not in str(payment_type):
            return np.nan
        
        pattern = r'\$(\d+(?:,\d+)?(?:\.\d+)?)'
        match = re.search(pattern, str(payment_type))
        
        if match:
            budget_str = match.group(1).replace(',', '')
            return float(budget_str)
        else:
            return np.nan
    
    renamed_df['fixed_price'] = renamed_df['payment_type'].apply(extract_fixed_price)
    
    # Calculate estimated total pay (using project duration and hourly rate)
    def estimate_total_pay(row):
        # For hourly jobs
        if pd.notna(row['hourly_rate']):
            duration_text = str(row['project_duration']).lower() if pd.notna(row['project_duration']) else ""
            
            # Estimate hours per week
            if "30+ hrs/week" in duration_text:
                hours_per_week = 35  # Estimate for full-time
            elif "less than 30 hrs/week" in duration_text:
                hours_per_week = 20  # Estimate for part-time
            else:
                hours_per_week = 25  # Default
            
            # Estimate project length in weeks
            if "less than 1 month" in duration_text:
                weeks = 3
            elif "1 to 3 months" in duration_text:
                weeks = 8
            elif "3 to 6 months" in duration_text:
                weeks = 18
            elif "more than 6 months" in duration_text:
                weeks = 30
            else:
                weeks = 8  # Default
            
            return row['hourly_rate'] * hours_per_week * weeks
        
        # For fixed price jobs
        elif pd.notna(row['fixed_price']):
            return row['fixed_price']
        
        return np.nan
    
    renamed_df['estimated_total_pay'] = renamed_df.apply(estimate_total_pay, axis=1)
    
    # Clean client rating
    renamed_df['client_rating'] = pd.to_numeric(renamed_df['client_rating'], errors='coerce')
    
    # Clean experience level
    renamed_df['experience_level'] = renamed_df['experience_level'].apply(lambda x: str(x).strip())
    
    # Extract skills from columns
    def extract_skills(row):
        skills = []
        skill_columns = ['primary_skill', 'skill_1', 'skill_2', 'skill_3', 'skill_4', 'skill_5', 'skill_6']
        
        for col in skill_columns:
            if col in row.index and pd.notna(row[col]) and row[col] != '':
                skills.append(str(row[col]).strip())
        
        return list(set([skill for skill in skills if skill]))  # Remove duplicates and empty strings
    
    renamed_df['extracted_skills'] = renamed_df.apply(extract_skills, axis=1)
    
    # Create a column for payment type category
    renamed_df['payment_type_category'] = renamed_df['payment_type'].apply(
        lambda x: 'Hourly' if 'Hourly' in str(x) else ('Fixed' if 'Fixed' in str(x) else 'Unknown')
    )
    
    return renamed_df

# Load the data
with st.spinner('Loading and processing data...'):
    data = load_and_process_data()

# Create skills analytics data
def prepare_skills_data(data):
    # Extract all skills into a flat list
    all_skills = []
    for skills in data['extracted_skills']:
        if isinstance(skills, list):
            all_skills.extend(skills)
    
    # Count frequency of each skill
    skill_counts = pd.Series(all_skills).value_counts().reset_index()
    skill_counts.columns = ['skill', 'job_count']
    
    # Calculate average pay for each skill
    skill_pay = {}
    for skill in skill_counts['skill']:
        # Filter jobs that require this skill
        jobs_with_skill = data[data['extracted_skills'].apply(lambda x: skill in x if isinstance(x, list) else False)]
        avg_pay = jobs_with_skill['estimated_total_pay'].mean()
        skill_pay[skill] = avg_pay
    
    skill_counts['avg_pay'] = skill_counts['skill'].map(skill_pay)
    
    return skill_counts

skills_data = prepare_skills_data(data)
top_skills = skills_data.nlargest(15, 'job_count')

# VISUALIZATION 1: Metric Headers
st.subheader("Key Job Market Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Number of Jobs", 
        f"{len(data):,}"
    )

with col2:
    hourly_jobs = data[data['payment_type_category'] == 'Hourly']
    avg_hourly = hourly_jobs['hourly_rate'].mean()
    st.metric(
        "Avg Hourly Rate", 
        f"${avg_hourly:.2f}/hr" if not np.isnan(avg_hourly) else "N/A"
    )

with col3:
    fixed_jobs = data[data['payment_type_category'] == 'Fixed']
    avg_fixed = fixed_jobs['fixed_price'].mean()
    st.metric(
        "Avg Fixed Price", 
        f"${avg_fixed:.2f}" if not np.isnan(avg_fixed) else "N/A"
    )

with col4:
    avg_total = data['estimated_total_pay'].mean()
    st.metric(
        "Avg Est. Total Pay", 
        f"${avg_total:.2f}" if not np.isnan(avg_total) else "N/A"
    )

# VISUALIZATION 2: Top Skills by Popularity
st.subheader("Top Skills by Popularity")
fig_popularity = px.bar(
    top_skills,
    y='skill',
    x='job_count',
    orientation='h',
    title='Top 15 Skills by Number of Jobs',
    labels={'job_count': 'Number of Jobs', 'skill': 'Skill'},
    color='job_count',
    color_continuous_scale='Viridis'
)
fig_popularity.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig_popularity, use_container_width=True)

# VISUALIZATION 3: Top Skills by Average Pay
st.subheader("Top Skills by Estimated Average Pay")
fig_pay = px.bar(
    top_skills,
    y='skill',
    x='avg_pay',
    orientation='h',
    title='Top 15 Skills by Average Estimated Pay',
    labels={'avg_pay': 'Average Estimated Pay ($)', 'skill': 'Skill'},
    color='avg_pay',
    color_continuous_scale='Greens'
)
fig_pay.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig_pay, use_container_width=True)

# Add a footer with data source
st.markdown("---")
st.caption("Data Source: Upwork Job Postings Dataset 2024 (50K Records) from Kaggle")