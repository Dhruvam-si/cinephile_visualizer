from  flask import Flask,redirect,url_for,render_template,session,request,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "diewreview"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id= db.Column("id",db.Integer,primary_key=True)
    firstname = db.Column("firstname",db.String(30))
    lastname = db.Column("lastname",db.String(30))

    def __init__(self,firstname,lastname):
        self.firstname = firstname
        self.lastname=lastname





#time for session storing
app.permanent_session_lifetime=timedelta(minutes=5)

#homepage/login page
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        session["firstname"] = request.form["faname"]
        session["lastname"] = request.form["laname"]
        session.permanent = True

        return redirect(url_for("review"))

    # GET request
    if "firstname" in session and "lastname" in session:
        flash("You are already logged in !","info")
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

    # POST
    user = request.form["firstname"]
    session["lname"] = request.form["lastname"]
    movie = request.form["movie"]
    ver = request.form["verdict"]

    return redirect(
        url_for("user", usr=user, mov=movie, rev=ver)
    )
       
@app.route("/<usr>/<mov>/<rev>")
def user(usr,mov,rev):
    if "lname" in session:
     lname = session["lname"]
     return render_template("review_show.html",movie=mov,name=usr,review=rev,lastname=lname)
    else:
        return render_template("newind.html")

@app.route("/lname")
def lname():
      if "lname" in session:
       lname = session["lname"]
       return render_template("show_review.html",movie="mov",name="usr",review="rev",lastname=lname)
      else:
        return render_template("write_review.html")

@app.route("/logout")
def logout():
       popping = session["firstname"]
       flash(f"{popping} have successfully Logged Out!","info")
       session.pop("firstname", None)
       session.pop("lastname", None)
       return redirect(url_for("home"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


