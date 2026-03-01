from openai import OpenAI
#from resume_reader import ResumeReader
#import os
from dotenv import load_dotenv
from streamlit import st

#load_dotenv()

API_KEY = st.secrets["API_KEY"]

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)

#path = "CV.pdf"
#cv = ResumeReader(path)

def enhance_cv(cv: str, target_role: str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Read the following CV:\n{cv} \n and rewrite the whole resume with specific sections of the resume for Section-wise enhancement, such as:\n 1. Professional Summary\n 2. Skills\n 3. Work Experience\n 4. Education\n 5. Projects\n 6. Certifications\n 7. Achievements\n 8. Hobbies and Interests \n don't add any new section if not available in the original CV. Also, enhance the content of each section with more details and make it more impactful and professional but keep the original structure intanct. Make the CV ATS friendly and use appropriate keywords for the role of {target_role}. Check for Grammars. If a section contains multiple items, always make that into a table format. Also, make sure to keep the content concise and avoid unnecessary details. Don't add any comments like what is formatted ot not, or any other comments just give the enhanced CV in markdown format. Don't write anything like or related to 'This resume is optimized for ATS parsing and highlights keywords relevant to software development, AI, and data‑driven roles.' in footer. Don't even add any footer, for godsake."},
                ]
            }
        ]
    )

    new_cv = response.choices[0].message.content


    response2 = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Read the following old CV:\n{cv} and new CV:\n{new_cv}\n evaluate them by \n 1.Clarity and effectiveness 2.Grammar and conciseness 3.Action-oriented language 4.Use of measurable outcomes 5.Readability 6.Relevance to job roles 7.ATS-friendliness 8.Overall impact and professionalism \n and give a score out of 10 for each cv and its evaluation and also give a % of improvement from old cv to new cv. Return the 3 scores and the % of improvement in a array format like this: old_cv_score, new_cv_score, improvement_percentage. Dont add []. Don't add any comments just give the output in the specified format."},
                ]
            }
        ]
    )

    evaluation = response2.choices[0].message.content
    return new_cv, evaluation

