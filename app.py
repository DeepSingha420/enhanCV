import io
import streamlit as st
from ai2 import enhance_cv
from resume_reader import ResumeReader
from markdown_pdf import MarkdownPdf, Section

st.set_page_config(
    page_title="enhanCV", page_icon="📄"
)

st.title("enhanCV")
st.subheader("AI-powered Resume Enhancer and Evaluator")

roles = [
    # --- Technology & Data ---
    "Software Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer",
    "Data Scientist", "Data Analyst", "Data Engineer", "Machine Learning Engineer",
    "DevOps Engineer", "Cloud Architect", "Cybersecurity Analyst", "Database Administrator",
    "QA Automation Engineer", "Mobile App Developer (iOS/Android)", "Blockchain Developer",
    
    # --- Product & Design ---
    "Product Manager", "Project Manager", "UI/UX Designer", "Product Designer",
    "Graphic Designer", "Creative Director", "Systems Architect",
    
    # --- Business, Marketing & Sales ---
    "Business Analyst", "Marketing Manager", "Digital Marketer", "SEO Specialist",
    "Social Media Manager", "Content Strategist", "Sales Executive", "Account Manager",
    "Business Development Manager", "Operations Manager", "Human Resources (HR) Specialist",
    "Recruiter", "Customer Success Manager", "Financial Analyst", "Accountant",
    
    # --- Healthcare & Science ---
    "Medical Doctor", "Nurse Practitioner", "Pharmacist", "Biomedical Researcher",
    "Healthcare Administrator", "Lab Technician", "Psychologist",
    
    # --- Education & Legal ---
    "Teacher / Educator", "Professor", "Instructional Designer", "Attorney / Lawyer",
    "Legal Assistant", "Para-legal",
    
    # --- Engineering & Trades ---
    "Mechanical Engineer", "Electrical Engineer", "Civil Engineer", "Structural Engineer",
    "Architect", "Manufacturing Engineer", "Electrician", "Technician",
    
    # --- Writing & Communication ---
    "Technical Writer", "Copywriter", "Editor", "Public Relations Specialist",
    
    # --- Catch-all ---
    "Other"
]

upload = st.file_uploader("Upload your CV (PDF/txt format)", type=["pdf", "txt"])

selected_role = st.selectbox(
    "Select the target job role for ATS optimization:",
    options=roles,
    index=None,
    placeholder="Type specific role or leave blank for better result..."
)

if selected_role == "Other":
    custom_role = st.text_input("Enter your specific job title:")
    target_role = custom_role
else:
    target_role = selected_role

if not target_role:
    target_role = "applicable job roles of the person"

if upload is not None:
    cv = ResumeReader(upload)
    with st.expander("Show Extracted CV Content"):
        st.markdown("### Original CV")
        st.markdown(cv)
    if st.button("Enhance and EvaluateCV"):
        with st.spinner("Enhancing and Evaluating your CV..."):
            enhanced_cv, evaluation = enhance_cv(cv, target_role)
            old_score, new_score, improvement_percentage = evaluation.split(",")
            with st.expander("Show Enhanced CV"):
                st.markdown("### Enhanced CV")
                st.markdown(enhanced_cv)
            
            pdf = MarkdownPdf(toc_level=0)
            pdf.add_section(Section(enhanced_cv))
            pdf_buffer = io.BytesIO()
            pdf.save_bytes(pdf_buffer)
            pdf_bytes = pdf_buffer.getvalue()
            #cv_pdf = pdf.save('enhanced_cv.pdf')

            st.download_button(
            label="Download Enhanced CV as PDF",
            data=pdf_bytes,
            file_name="enhanced_cv.pdf",
            mime="application/pdf"
            )
            st.markdown("### Evaluation Scores")
            st.markdown(f"**Original CV Score:** {old_score}/10")
            st.markdown(f"**Enhanced CV Score:** {new_score}/10")
            st.metric(label="Improvement Percentage:", value=f"{improvement_percentage}%", delta=None, delta_color="normal")

st.caption("Made with ❤️ by DeathWish. I am poor and free LLM can be stupid sometimes. So deal with it.")


