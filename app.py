from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "studyplanner"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

# =========================
# USER DATABASE
# =========================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(100)
    )


# =========================
# NOTES DATABASE
# =========================

class Note(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100)
    )

    content = db.Column(
        db.Text
    )


# =========================
# HOME
# =========================

@app.route("/")

def home():

    return render_template(
        "index.html"
    )


# =========================
# REGISTER
# =========================

@app.route(
    "/register",
    methods=["GET", "POST"]
)

def register():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return "⚠ Username already exists"

        user = User(

            username=username,

            password=password
        )

        db.session.add(user)

        db.session.commit()

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# =========================
# LOGIN
# =========================

@app.route(
    "/login",
    methods=["GET", "POST"]
)

def login():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        user = User.query.filter_by(

            username=username,

            password=password

        ).first()

        if user:

            session["user"] = username

            return redirect(
                url_for("dashboard")
            )

        else:

            return "❌ Invalid Username or Password"

    return render_template(
        "login.html"
    )


# =========================
# FORGOT PASSWORD
# =========================

@app.route(
    "/forgot",
    methods=["GET", "POST"]
)

def forgot():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        new_password = request.form.get(
            "password"
        )

        user = User.query.filter_by(
            username=username
        ).first()

        if user:

            user.password = new_password

            db.session.commit()

            return redirect(
                url_for("login")
            )

        else:

            return "❌ Username not found"

    return render_template(
        "forgot.html"
    )


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")

def dashboard():

    if "user" in session:

        return render_template(

            "dashboard.html",

            username=session["user"]

        )

    return redirect(
        url_for("login")
    )


# =========================
# SMART AI TIMETABLE
# =========================

@app.route(
    "/timetable",
    methods=["GET", "POST"]
)

def timetable():

    day1_data = []

    day2_data = []

    holiday_message = ""

    if request.method == "POST":

        subjects = request.form.get(
            "subjects"
        )

        hard_input = request.form.get(
            "hard_subjects"
        )

        holiday = request.form.get(
            "holiday"
        )

        subject_list = [

            s.strip()

            for s in subjects.split(",")

            if s.strip()
        ]

        hard_subjects = [

            s.strip().lower()

            for s in hard_input.split(",")

            if s.strip()
        ]

        easy_morning_slot = "5:30 AM - 6:15 AM"

        hard_slots = [

            "6:30 AM - 8 AM",

            "8:15 AM - 9:45 AM"

        ]

        easy_evening_slots = [

            "6 PM - 6:45 PM",

            "7 PM - 7:45 PM",

            "8 PM - 8:45 PM",

            "9 PM - 9:45 PM"

        ]

        next_day_hard_slots = [

            "6:30 AM - 8 AM",

            "8:15 AM - 9:45 AM"

        ]

        next_day_easy_slots = [

            "6 PM - 6:45 PM",

            "7 PM - 7:45 PM",

            "8 PM - 8:45 PM",

            "9 PM - 9:45 PM"

        ]

        hard_count = 0

        easy_count = 0

        next_hard = 0

        next_easy = 0

        # =========================
        # EASY SUBJECTS
        # =========================

        for subject in subject_list:

            subject_name = subject.strip()

            if subject_name.lower() not in hard_subjects:

                duration = "45 Minutes"

                if easy_count < 5:

                    if easy_count == 0:

                        time_slot = easy_morning_slot

                    else:

                        time_slot = easy_evening_slots[
                            easy_count - 1
                        ]

                    easy_count += 1

                    day1_data.append({

                        "subject": subject_name,

                        "time": time_slot,

                        "hours": duration,

                        "break_time":
                        "15 Minutes Fresh Break ☕"

                    })

                else:

                    time_slot = next_day_easy_slots[
                        next_easy %
                        len(next_day_easy_slots)
                    ]

                    next_easy += 1

                    day2_data.append({

                        "subject": subject_name,

                        "time": time_slot,

                        "hours": duration,

                        "break_time":
                        "15 Minutes Fresh Break ☕"

                    })

        # =========================
        # HARD SUBJECTS
        # =========================

        for subject in subject_list:

            subject_name = subject.strip()

            if subject_name.lower() in hard_subjects:

                duration = "90 Minutes"

                if hard_count < 2:

                    time_slot = hard_slots[
                        hard_count
                    ]

                    hard_count += 1

                    day1_data.append({

                        "subject": subject_name,

                        "time": time_slot,

                        "hours": duration,

                        "break_time":
                        "15 Minutes Fresh Break ☕"

                    })

                else:

                    time_slot = next_day_hard_slots[
                        next_hard %
                        len(next_day_hard_slots)
                    ]

                    next_hard += 1

                    day2_data.append({

                        "subject": subject_name,

                        "time": time_slot,

                        "hours": duration,

                        "break_time":
                        "15 Minutes Fresh Break ☕"

                    })

        # =========================
        # HOLIDAY EXTRA STUDY
        # =========================

        if holiday == "Yes":

            holiday_message = (

                "📅 Today is a holiday 😄 "
                "You can study 2 extra hours "
                "for revision and weak subjects."
            )

            day1_data.append({

                "subject":
                "Revision + Weak Subject Practice + Writing + Chill & Enjoy",

                "time":
                "10 PM - 11 PM",

                "hours":
                "2 Hours Extra Study",

                "break_time":
                "15 Minutes Fresh Break ☕"

            })

    return render_template(

        "timetable.html",

        timetable=day1_data,

        nextday=day2_data,

        holiday_message=holiday_message
    )


# =========================
# USER NOTES
# =========================

@app.route(
    "/notes",
    methods=["GET", "POST"]
)

def notes():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    current_user = session["user"]

    if request.method == "POST":

        content = request.form.get(
            "content"
        )

        new_note = Note(

            username=current_user,

            content=content

        )

        db.session.add(
            new_note
        )

        db.session.commit()

    user_notes = Note.query.filter_by(

        username=current_user

    ).all()

    return render_template(

        "notes.html",

        notes=user_notes
    )


# =========================
# RESULT
# =========================

@app.route("/result")

def result():

    return render_template(
        "result.html"
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")

def logout():

    session.pop(
        "user",
        None
    )

    return redirect(
        url_for("login")
    )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(

        debug=True,

        host="0.0.0.0"
    )