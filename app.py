from flask import Flask, redirect, url_for, render_template, session, request, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from insights import generate_unhinged_insight
from serper_discourse import get_discourse
app = Flask(__name__)
app.secret_key = "diewreview"
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "users.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column("user_name", db.String(30))
    user_email = db.Column("user_email", db.String(30))

    def __init__(self, user_name, user_email):
        self.user_name = user_name
        self.user_email = user_email

class reviews(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    user_id=db.Column("user_id",db.Integer,db.ForeignKey("users.id"))
    user_movie=db.Column("user_movie",db.String(50))
    user_review=db.Column("user_review",db.String(2000))
    
    def __init__(self,user_id,user_movie,user_review,):
        self.user_id=user_id
        self.user_movie=user_movie
        self.user_review=user_review
        

app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_email = request.form["user_email"]

        session["user_name"] = user_name
        session["user_email"] = user_email
        session.permanent = True

        # save to DB if user doesn't already exist
        exists = users.query.filter_by(user_name=user_name, user_email=user_email).first()
        if not exists:
            new_user = users(user_name, user_email)
            db.session.add(new_user)
            db.session.commit()
            session["user_id"]=new_user._id
        else:
         session["user_id"]=exists._id

        return redirect(url_for("review"))

    if "user_name" in session and "user_email" in session:
        flash("You are already logged in !", "info")
        return render_template(
            "newind.html",
            user_name=session["user_name"],
            user_email=session["user_email"]
        )

    return render_template("newind.html")


@app.route("/review", methods=["GET", "POST"])
def review():
    # fix: bail out early if session data doesn't exist yet,
    # instead of crashing with a KeyError
    if "user_name" not in session or "user_email" not in session:
        flash("Please enter your name and email first.", "info")
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template(
            "write_review.html",
            user_name=session["user_name"],
            user_email=session["user_email"]
        )

    # POST: user submitted the review form
    movie = request.form["movie"]
    ver = request.form["verdict"]

    new_review = reviews(session["user_id"], movie, ver)
    db.session.add(new_review)
    db.session.commit()

    flash(f"Review for '{movie}' saved!", "info")
    return redirect(url_for("review"))



@app.route("/user_reviews")
def user_reviews():
    if "user_id" not in session:
        return redirect(url_for("home"))
    else:
        user_reviews_list=reviews.query.filter_by(user_id=session["user_id"]).all()
        return render_template("user_reviews.html",values=user_reviews_list)

@app.route("/insights")
def insights():
    if "user_id" not in session:
        flash("Please login first", "info")
        return redirect(url_for("home"))
    
    user_review = reviews.query.filter_by(user_id=session["user_id"]).first()
    
    if not user_review:
        flash("Write a review first to get your insight!", "info")
        return redirect(url_for("review"))
    
    keys = get_discourse(user_review.user_movie)
    ispot = generate_unhinged_insight(user_review.user_movie, user_review.user_review, keys, session["user_name"])
    return render_template("insights.html", ispot=ispot)

@app.route("/delete_reviews", methods=["GET", "POST"])
def delete_reviews():
    if request.method == "GET":
        user_reviews = reviews.query.filter_by(user_id=session["user_id"]).all()
        return render_template("delete_reviews.html", values=user_reviews)
    
    # POST
    selected_ids = request.form.getlist("review_ids")
    for id in selected_ids:
        review = reviews.query.filter_by(_id=id, user_id=session["user_id"]).first()
        db.session.delete(review)
    db.session.commit()
    return redirect(url_for("user_reviews"))


@app.route("/logout")
def logout():
    if "user_name" in session:
        popping = session["user_name"]
        flash(f"{popping} have successfully Logged Out!", "info")
        session.pop("user_name", None)
        session.pop("user_email", None)
    return redirect(url_for("home"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


