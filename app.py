import time
import hashlib

from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lwpxktnemjbjbq:1e5f7178b6dc3de5821a0cd96beae0b0dbff29826d9d3a98edcfeca7ef3bebea@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/dciepftsq0l0s2'

app.config['SECRET_KEY'] = 'WHO_IS_YOUR_DADDY'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#####################################################################################
############################# DATABASE MODELS #######################################


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("index"))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    elif request.method == 'POST':
        print('Login request')
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        print(username, ',', password)
        user = User.query.filter_by(name=username).first()
        password = hashlib.sha256(password.encode()).hexdigest()
        print(user)

        if user is not None and password == user.pwd:
            user_is_logged_in = True
            login_user(user)
            return redirect(url_for("puzzle"))
        else:
            return redirect(url_for("index"))

    else:
        return "Backend FUCKED UP badly"


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
            answer = request.form.get("answer").strip()
            answer_lower = answer.lower()
            print('submitted answer: ', answer)

            current_puzzle_id = token[current_level]
            is_location = str(current_puzzle_id).islower()
            print("Current puzzle id: ", current_puzzle_id)
            print("is location: ", is_location)

            current_puzzle = Quiz.query.filter_by(
                id=current_puzzle_id).first()
            print("Current puzzle:")
            print(current_puzzle)
            puzzle_answers = current_puzzle.answer.split(',')

            answer_record = Answers(
                level_name=current_puzzle_id, team=current_user.name, answer=answer)
            db.session.add(answer_record)
            db.session.commit()

            is_correct = False
            # for location case is important
            if is_location:
                is_correct = answer == current_puzzle.answer.strip()
            else:
                for puzzle_answer in puzzle_answers:
                    if puzzle_answer.strip().lower() == answer_lower:
                        is_correct = True
                        break
            if is_correct:
                user = User.query.filter_by(name=current_user.name).first()
                new_level = user.level_completed + 1
                user.last_time = datetime.now()
                user.level_completed = new_level
                db.session.commit()

                user = User.query.filter_by(name=current_user.name).first()
            else:
                user = User.query.filter_by(name=current_user.name).first()

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
            # return render_template("puzzle.html", level=current_user.level_completed+1, image_link=image_link)
            return render_template("puzzle.html", level=level, image_link=image_link)

    else:
        return "You're not supposed to be here !"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/congrats")
@login_required
def congrats():
    TOTAL_QUIZ = len(current_user.token)
    if TOTAL_QUIZ == current_user.level_completed:
        return render_template("congrats.html")
    return redirect(url_for("puzzle"))


@app.route("/leaderboard")
@login_required
def leaderboard():
    # ordering the leaderboard by the user standings in a descending order
    user_list = User.query.filter_by(role="TEAM").order_by(
        User.level_completed.desc(), User.last_time.asc())
    return render_template("leaderboard.html", user_list=user_list)


@login_required
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template("admin_login.html")

    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        if username == "admin" and password == "WHO_IS_YOUR_DADDY":
            print('Trying to login admin')
            admin_user = User.query.filter_by(name=username).first()
            print(admin_user)
            login_user(admin_user)
            print(current_user)
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("admin"))

    else:
        return redirect(url_for("index"))


@login_required
@app.route("/team_reg", methods=['GET', 'POST'])
def team_reg():
    if current_user.name == "admin":
        if request.method == 'GET':
            return render_template("team_register.html")

        elif request.method == 'POST':
            teamname = request.form.get("teamname")
            password = request.form.get("password")
            token = request.form.get("token")

            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = User(name=teamname, pwd=password_hash, token=token)
            db.session.add(user)
            db.session.commit()

            return render_template("team_register.html")
        else:
            return "Backend fucked up badly !"
    else:
        return redirect(url_for("index"))

@login_required
@app.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    print('in admin dashboard')
    print(current_user.name == "admin")
    if current_user.name == "admin":
        print('user is admin')
        if request.method == 'GET':
            answer_list = Answers.query.order_by(Answers.level_name.asc())
            return render_template("answer_page.html", answer_list=answer_list)

        elif request.method == 'POST':
            teamname = request.form.get("teamname")
            level = request.form.get("level")

            if level == "" and teamname != "":
                answer_list = Answers.query.filter_by(team=teamname)
            elif teamname == "" and level != "":
                level_int = level
                answer_list = Answers.query.filter_by(level_name=level_int)
            elif level != "" and teamname != "":
                level_int = level
                answer_list = Answers.query.filter_by(
                    team=teamname, level_name=level_int)
            else:
                answer_list = Answers.query.order_by(Answers.level.asc())

            return render_template("answer_page.html", answer_list=answer_list)

        else:
            return "Backend fucked up badly !"
    else:
        return redirect(url_for("index"))

############################## ROUTE HANDLERS #######################################
#####################################################################################


if __name__ == "__main__":
    app.run(debug=True)
