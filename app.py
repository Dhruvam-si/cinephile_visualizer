from flask import Flask, redirect, url_for, render_template, session, request, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "diewreview"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.sqlite3"  # fixed: 3 slashes
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    firstname = db.Column("firstname", db.String(30))
    lastname = db.Column("lastname", db.String(30))

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        fname = request.form["faname"]
        lname = request.form["laname"]

        session["firstname"] = fname
        session["lastname"] = lname
        session.permanent = True

        # save to DB if user doesn't already exist
        existing = users.query.filter_by(firstname=fname, lastname=lname).first()
        if not existing:
            new_user = users(fname, lname)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for("review"))

    if "firstname" in session and "lastname" in session:
        flash("You are already logged in !", "info")
        return render_template(
            "newind.html",
            faname=session["firstname"],
            laname=session["lastname"]
        )

    return render_template("newind.html")


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
        return render_template(
            "write_review.html",
            firstname=session["firstname"],
            lastname=session["lastname"]
        )

    user = request.form["firstname"]
    session["lname"] = request.form["lastname"]
    movie = request.form["movie"]
    ver = request.form["verdict"]

    return redirect(url_for("user", usr=user, mov=movie, rev=ver))


@app.route("/<usr>/<mov>/<rev>")
def user(usr, mov, rev):
    if "firstname" not in session or "lastname" not in session:
     return redirect(url_for("home"))
    if "lname" in session:
        lname = session["lname"]
        return render_template("review_show.html", movie=mov, name=usr, review=rev, lastname=lname)
    else:
        return render_template("newind.html")


@app.route("/lname")
def lname():
    if "lname" in session:
        lname = session["lname"]
        return render_template("show_review.html", movie="mov", name="usr", review="rev", lastname=lname)
    else:
        return render_template("write_review.html")


@app.route("/logout")
def logout():
    if "firstname" in session:
     popping = session["firstname"]
     flash(f"{popping} have successfully Logged Out!", "info")
     session.pop("firstname", None)
     session.pop("lastname", None)
     return redirect(url_for("home"))


if __name__ == '__main__':
    with app.app_context():  # fixed: no argument
        db.create_all()
    app.run(debug=True)


