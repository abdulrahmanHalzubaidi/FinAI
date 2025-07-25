from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pandas as pd
import app
from app.llm_tools.finai_llm import generate_report, answer_finai
from markdown2 import markdown
import traceback
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import re


app = Flask(
    'WebApp',
    template_folder="app/templates",
)

app.secret_key = "your_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FinAI.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

#Define the UserDemographics model
class UserDemographics(db.Model):
    __tablename__ = 'user_demographics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    D_O_B = db.Column(db.Date, nullable=False)
    finance_proficiency_level = db.Column(db.String(50), nullable=False)

    # Define the Feedback model
class Feedback(db.Model): 
    __tablename__ = 'feedback'

    request_type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    status = db.Column(db.String(100), nullable=False, default='In progress')  # default added here
    time_of_creation = db.Column(db.Date, nullable=False)
    request_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_demographics.id'), nullable=False)



# Route: Main Page
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# Route: Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        app.logger.info(f"Login attempt with email: {email}")

        user = UserDemographics.query.filter_by(email=email).first()

        if user and user.password == password:
            app.logger.info(f"User {user.first_name} logged in successfully.")
            session["email"] = user.email
            session["username"] = user.first_name
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))
        else:
            app.logger.warning("Invalid email or password.")
            flash("Invalid login!")

    return render_template("login.html")


# Route: Sign Up
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")  # Optional
        email = request.form.get("email")
        password = request.form.get("password")
        dob_str = request.form.get("dob")  # Expected format: YYYY-MM-DD
        proficiency_level = request.form.get("finance_proficiency_level")

        # Basic input validation
        if not first_name or first_name.strip() == "":
            flash("First name is required.")
            return render_template("signup.html")

        if not email or email.strip() == "":
            flash("Email is required.")
            return render_template("signup.html")

        # Validate email format
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            flash("Invalid email.")
            return render_template("signup.html")

        if not password or password.strip() == "":
            flash("Password is required.")
            return render_template("signup.html")

        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date of birth format. Please use YYYY-MM-DD.", "danger")
            return render_template("signup.html")

        # Check if the email is already registered
        existing_user = UserDemographics.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return render_template("signup.html")

        # Try to create and save the new user
        new_user = UserDemographics(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            D_O_B=dob,
            finance_proficiency_level=proficiency_level
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created! Please log in.")
            return redirect(url_for("login"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error creating account. Please try again later.")
            print(f"Database error: {e}")  # Optional for debugging

    return render_template("signup.html")

# Route: Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

# Route: Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

# Route: About
@app.route("/about")
def about():
    return render_template("about.html")

# Route: Feedback
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if "username" not in session:
        return redirect(url_for("login"))
    user_id = session.get("user_id")

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        request_type = request.form["request_type"]

        feedback_entry = Feedback(
            title=title,
            description=description,
            request_type=request_type,
            status="In progress",
            time_of_creation=datetime.today().date(),
            user_id=user_id
        )

        try:
            db.session.add(feedback_entry)
            db.session.commit()
            flash("Your feedback has been submitted successfully!", "success")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("There was an issue submitting your feedback. Please try again later.", "danger")
            app.logger.error(f"Database error: {str(e)}")

        return redirect(url_for("feedback"))

    return render_template("feedback.html")



# Route: FinaAI Calculator
@app.route("/finai_calculator")
def finai_calculator():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("finai_calculator.html")

# Route: Ask FinAI
@app.route("/ask_finai")
def ask_finai():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("ask_finai.html")

@app.route("/chat", methods=["POST"])
def chat():
    df = None
    file = request.files.get("file")
    query = request.form.get("query")

    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Please upload a valid CSV file."})
    else:
        df = pd.read_csv(file)

    if df is None:
        return jsonify({"error": "No CSV file uploaded yet."})

    if not query:
        return jsonify({"error": "No query provided."})

    response = markdown(answer_finai(df=df, query=query))
    return jsonify({"response": response})


# Route: FinAI Analyzer
@app.route("/finai_analyzer", methods=["POST"])
def finai_analyzer():
    if "username" not in session:
        return redirect(url_for("login"))

    if "file" not in request.files:
        flash("No file uploaded!")
        return redirect(url_for("dashboard"))

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected!")
        return redirect(url_for("dashboard"))

    # Process the file (example: read CSV)
    try:
        if file.filename.endswith(".csv"):
            file.seek(0)
            df = pd.read_csv(file)
        else:
            flash("Unsupported file format! Please upload a CSV file.")
            return redirect(url_for("dashboard"))
        file.seek(0)
        summary = generate_report(file)
        return render_template("finai_report.html", summary=summary)

    except Exception as e:
        flash(f"Error processing file: {str(e)}")
        traceback.print_exc()
        return redirect(url_for("dashboard"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()