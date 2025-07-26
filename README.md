# FinAI — Senior Project Flask Web App

**FinAI** is a web‐based financial assistant built with Flask and the OpenAI API. It lets users upload their own CSV financial datasets, ask natural-language questions, and receive data‐driven insights and reports instantly.

---

##  Background & Motivation

In the modern finance landscape, professionals and students often juggle large spreadsheets and manual analysis to answer routine questions (“What was my average monthly revenue last quarter?”, “How did my expenses trend year-over-year?”).  
**FinAI** automates that work:

- **Natural Language Interface**  
  No SQL or Excel formulas required. Simply type your question in everyday language.

- **AI-Powered Analysis**  
  Uses OpenAI to parse your CSV, run calculations, and generate narrative summaries.

- **Self-Serve Reporting**  
  Upload a file, click “Analyze,” and get a formatted report you can download or share.

---

##  Features

- **User Authentication**  
  Secure signup/login with email, password, and proficiency level.

- **CSV-Driven Q&A**  
  Upload your financial CSV, then chat with “FinAI” about any column or metric.

- **Automated Report Generator**  
  One-click summary of key KPIs, trends, and outliers.

- **Feedback Loop**  
  Submit feedback directly from the app to continually improve prompts.

- **Lightweight & Local-First**  
  Flask backend with SQLite; all logic runs on your machine or private server.

---

##  Architecture & Directory Structure

Below is the folder layout of the FinAI project. This shows where each component lives:

```text
FinAI_Project/
├── app/                  # Main Flask application package
│   ├── llm_tools/        # AI logic & OpenAI prompt templates
│   └── templates/        # Jinja2 HTML templates (views)
├── static/               # CSS, JavaScript, and image assets
├── instance/             # SQLite database (auto-created on first run)
├── run.py                # Application entrypoint (starts Flask server)
├── requirements.txt      # List of Python dependencies
├── .gitignore            # Files and folders ignored by Git
└── README.md             # Project documentation (this file)
```


---

##  Setup & Installation

1. **Clone the repo**  
 ```bash
  git clone https://github.com/abdulrahmanHalzubaidi/FinAI.git
  cd FinAI
 ```  
2. **Create & activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Configure your API key**
```bash 
OPENAI_API_KEY=sk-YOUR_API_KEY
```
5. **Initialize & run**
```bash
python run.py
```
---

##  Usage
1. Sign up with your email and set a finance proficiency level.

2. Log in and explore the dashboard.

3. Upload a CSV file under “FinAI Analyzer” to generate a KPI report.

4. Chat with FinAI under “Ask FinAI” for custom queries.

5. View & download your report or share feedback.
   
---

##  Tech Stack
- **Backend: Python, Flask, SQLAlchemy, SQLite**

- **AI Engine: OpenAI GPT-4 via openai Python SDK**

- **Frontend: Jinja2 templates, vanilla HTML/CSS/JS**

- **Deployment: Local machine or any WSGI-compatible host**

---
##  Future Improvements
-**Add chart visualizations (Plotly, Chart.js)**

-**Support Excel & other file formats**

-**Role-based access control & multi-user reports**

-**Deploy to Docker or serverless environments**

---

## Conclusion

FinAI makes financial analysis easy for everyone. Upload your CSV data, ask questions in plain English, and get clear insights instantly. No complex tools or formulas—just AI-powered answers to help you make smarter decisions.

*Thank you for exploring FinAI -- where finance meets AI!* :)
