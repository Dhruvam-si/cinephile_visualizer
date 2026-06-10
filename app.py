from  flask import Flask,redirect,url_for,render_template,session,request,flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "diewreview"
app.permanent_session_lifetime=timedelta(minutes=1)
@app.route("/")
def home():
    return render_template("newind.html")

@app.route("/review",methods=["GET","POST"])
def review():
    if request.method=="POST":
        user = request.form["firstname"]
        movie = request.form["movie"]
        ver = request.form["verdict"]
        session["lname"]=request.form["lastname"]
        session.permanent=True

        print(request.form)
        print("User:", user)
        print("Movie:", movie)
        print("rev: ",ver)
        print(url_for("user", usr=user, mov=movie,rev = ver))
        
        return redirect(url_for("user",usr=user,mov=movie,rev=ver) )
    else:
        return render_template("reviews.html")
       
@app.route("/<usr>/<mov>/<rev>")
def user(usr,mov,rev):
    if "lname" in session:
     lname = session["lname"]
     return render_template("user_review.html",movie=mov,name=usr,review=rev,lastname=lname)
    else:
        return render_template("reviews.html")

@app.route("/lname")
def lname():
      if "lname" in session:
       lname = session["lname"]
       return render_template("user_review.html",movie="mov",name="usr",review="rev",lastname=lname)
      else:
        return render_template("reviews.html")

@app.route("/logout")
def logout():
    if "lname" in session:
       lname = session["lname"]
       flash(f"{lname} have successfully Logged Out!","info")
       session.pop("lname",None)
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)

