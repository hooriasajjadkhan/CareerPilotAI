from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from dotenv import load_dotenv
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
import os
from services.pdf_generator import (
    create_resume_pdf,
    create_roadmap_pdf
)

from config import Config
from models.database import db, login_manager
from models.user import User
from utils.auth import bcrypt

from services.interview_ai import ask_ai
from services.resume_ai import analyze_resume
from services.roadmap_ai import generate_roadmap

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# ==========================
# Initialize Extensions
# ==========================
db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)

# ==========================
# Create Database
# ==========================
with app.app_context():
    db.create_all()

# ==========================
# Dashboard
# ==========================
@app.route("/")
@login_required
def dashboard():
    return render_template("index.html")
# ==========================
# AI Mock Interview
# ==========================
@app.route("/interview")
@login_required
def interview():
    return render_template("interview.html")


@app.route("/chat", methods=["POST"])
@login_required
def chat():

    data = request.get_json()

    user_message = data.get("message")

    reply = ask_ai(user_message)

    return jsonify({
        "reply": reply
    })


# ==========================
# Resume Analyzer
# ==========================
@app.route("/resume", methods=["GET", "POST"])
@login_required
def resume():

    if request.method == "POST":

        if "resume" not in request.files:

            flash("Please upload a resume.")

            return redirect(url_for("resume"))

        file = request.files["resume"]

        if file.filename == "":

            flash("Please select a file.")

            return redirect(url_for("resume"))

        upload_folder = os.path.join("static", "uploads")

        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(
            upload_folder,
            file.filename
        )

        file.save(filepath)

        result = analyze_resume(filepath)

        pdf_path = create_resume_pdf(result)

        return render_template(
            "resume.html",
            result=result,
            pdf_path=pdf_path
        )

    return render_template("resume.html")


# ==========================
# Career Roadmap
# ==========================
@app.route("/roadmap", methods=["GET", "POST"])
@login_required
def roadmap():

    if request.method == "POST":

        career = request.form["career"]

        skills = request.form["skills"]

        level = request.form["level"]

        result = generate_roadmap(
            career,
            skills,
            level
        )

        pdf_path = create_roadmap_pdf(result)

        return render_template(
            "roadmap.html",
            result=result,
            pdf_path=pdf_path
        )

    return render_template("roadmap.html")

       


# ==========================
# Settings
# ==========================
@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")


# ==========================
# Register
# ==========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists.")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")

        return redirect(url_for("login"))

    return render_template("register.html")


# ==========================
# Login
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)

            flash(f"Welcome back, {user.username}!")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html")


# ==========================
# Logout
# ==========================
@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.")

    return redirect(url_for("login"))


# ==========================
# Run App
# ==========================
if __name__ == "__main__":
    app.run(debug=True)