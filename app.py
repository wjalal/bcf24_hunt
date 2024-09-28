import time
import hashlib
from dotenv import load_dotenv
import os
from flask import Flask, request, redirect, url_for, send_from_directory, abort
from flask import render_template
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONN_STR')
app.config['SECRET_KEY'] = os.getenv("SECRET")

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#####################################################################################
############################# DATABASE MODELS #######################################


class User(UserMixin, db.Model):
    id = db.Column(db.String(40), primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    pwd = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(30), nullable=False)
    level_completed = db.Column(db.Integer, default=0)
    last_time = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(10), default="TEAM")

    def __repr__(self):
        return "ID: %r" % self.id + " Name: " + self.name + " Pass: " + self.pwd


class Quiz(db.Model):
    id = db.Column(db.String(1), primary_key=True)
    link = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "ID: " + str(self.id) + " Answer: " + self.answer


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(40), nullable=False)
    team = db.Column(db.String(40), nullable=False)
    answer = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "Level: " + self.level + " Team: " + self.team + " Answer: " + self.answer


############################# DATABASE MODELS #######################################
#####################################################################################

#####################################################################################
############################## ROUTE HANDLERS #######################################


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("index"))

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for("puzzle"))
        else:
            return render_template("index.html")

    elif request.method == 'POST':
        print('Login request')
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        print(username, ',', password)
        user = User.query.filter_by(id=username).first()
        password = hashlib.sha256(password.encode()).hexdigest()
        print(user)

        if user is not None and password == user.pwd:
            login_user(user)
            return redirect(url_for("puzzle"))
        else:
            return redirect(url_for("index"))

    else:
        return "Backend FUCKED UP badly"


@app.route('/puzzle_image')
@login_required
def puzzle_image():
    # Only allow access if the user meets the conditions (e.g., logged in, etc.)
    token = current_user.token
    TOTAL_QUIZ = len(token)
    print(TOTAL_QUIZ)
    current_level = current_user.level_completed 
    print(current_level)
    
    if current_level >= TOTAL_QUIZ:
        abort(404)
    else:
        current_puzzle_id = token[current_level]
        print(current_puzzle_id)
        try:
            # return send_from_directory('puzzles', f"{current_puzzle_id}.png")
            return send_from_directory('static', "doge.jpg")
        except FileNotFoundError:
            abort(404)  


@app.route("/puzzle", methods=['GET', 'POST'])
@login_required
def puzzle():
    # TOTAL_QUIZ = len(Quiz.query.all())
    # print(TOTAL_QUIZ)

    token = current_user.token
    TOTAL_QUIZ = len(token)
    print(TOTAL_QUIZ)
    current_level = current_user.level_completed 
    print(current_level)


    if request.method == 'POST':
        print("POST")

        if current_level >= TOTAL_QUIZ:
            print("POST + CURRENT_LEVEL == TOTAL_QUIZ")
            return redirect(url_for("congrats"))

        else:
            print("POST + ")
            answer = request.form.get("answer").strip().replace(' ', '')
            answer = answer.lower()
            print('submitted answer: ', answer)

            try:
                # Directly execute the stored procedure without `db.session.begin()`
                db.session.execute(text("CALL update_user_level (:user_id, :answer)"), 
                                    {"user_id": current_user.id, "answer": answer})
                
                # Commit the session after calling the procedure
                db.session.commit()
                user = User.query.filter_by(name=current_user.id).first()
                return redirect(url_for("puzzle"))

            except Exception as e:
                # Rollback the session in case of errors
                db.session.rollback()
                print("Error occurred:", e)
                return redirect(url_for("puzzle"))

    elif request.method == 'GET':

        if current_user.level_completed >= TOTAL_QUIZ:
            print("GET + CURRENT_LEVEL == TOTAL_QUIZ")
            return redirect(url_for("congrats"))
        else:
            print("GET ELSE")
            print("Current User Level Completed: ", current_user.level_completed)

            current_puzzle_id = token[current_level]
            print("Current puzzle id:", current_puzzle_id)

            current_puzzle = Quiz.query.filter_by(
                id=current_puzzle_id).first()

            print("Current puzzle:")
            print(current_puzzle)
            image_link = current_puzzle.link
            level = int(current_user.level_completed) + 1
            return render_template("puzzle.html", level=level, image_link=image_link)
            # return render_template("puzzle.html", level=level)

    else:
        return "You're not supposed to be here !"


@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        role = current_user.role
    else:
        role = None
    logout_user()

    if role == 'ADMIN':
        return redirect(url_for("admin"))
    return redirect(url_for("index"))


@app.route("/congrats")
@login_required
def congrats():
    TOTAL_QUIZ = len(current_user.token)
    if TOTAL_QUIZ == current_user.level_completed:
        f_link = Quiz.query.filter_by(id='Z').first().link
        return render_template("congrats.html", image_link=f_link)
    return redirect(url_for("puzzle_image"))


@app.route("/leaderboard")
@login_required
def leaderboard():
    # ordering the leaderboard by the user standings in a descending order
    user_list = User.query.filter_by(role="TEAM").order_by(
        User.level_completed.desc(), User.last_time.asc())
    return render_template("leaderboard.html", user_list=user_list)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html")
    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        user = User.query.filter_by(id=username).first()
        password = hashlib.sha256(password.encode()).hexdigest()
        print(user)
        if user is not None and password == user.pwd and user.role=='ADMIN':
            login_user(user)
            print (user)
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("admin"))
    else:
        return redirect(url_for("index"))


@login_required
@app.route("/team_reg", methods=['GET', 'POST'])
def team_reg():
    if current_user.is_authenticated and current_user.role == "ADMIN":
        if request.method == 'GET':
            return render_template("team_register.html")
        elif request.method == 'POST':
            teamid = request.form.get("teamid")
            teamname = request.form.get("teamname")
            password = request.form.get("password")
            token = request.form.get("token")

            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = User(id=teamid, name=teamname, pwd=password_hash, token=token, role='TEAM')
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("leaderboard"))
        else:
            return "Backend fucked up badly !"
    else:
        return redirect(url_for("index"))

@login_required
@app.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    print('in admin dashboard')
    if current_user.is_authenticated and current_user.role == "ADMIN":
        print(current_user.id )
        print('user is admin')
        if request.method == 'GET':
            answer_list = Answers.query.order_by(Answers.id.desc())
            return render_template("answer_page.html", answer_list=answer_list)

        elif request.method == 'POST':
            teamname = request.form.get("teamname")
            level = request.form.get("level")

            if level == "" and teamname != "":
                answer_list = Answers.query.filter_by(team=teamname).order_by(Answers.id.desc())
            elif teamname == "" and level != "":
                level_int = level
                answer_list = Answers.query.filter_by(level_name=level_int).order_by(Answers.id.desc())
            elif level != "" and teamname != "":
                level_int = level
                answer_list = Answers.query.filter_by(
                    team=teamname, level_name=level_int).order_by(Answers.id.desc())
            else:
                answer_list = Answers.query.order_by(Answers.id.desc())

            return render_template("answer_page.html", answer_list=answer_list)

        else:
            return "Backend fucked up badly !"
    else:
        return redirect(url_for("index"))

############################## ROUTE HANDLERS #######################################
#####################################################################################


if __name__ == "__main__":
    app.run(debug=True)
