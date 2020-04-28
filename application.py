import os
import requests

from flask import Flask, session, render_template, flash, redirect, url_for, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import *
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Check for environment variable
if not 'postgres://cjzalftyeobeti:8bdef532d3b7e3e2bc817ad874116bb878f192e0e20ab43bc85f9bbbedebeb05@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d1u5irucd38qh1':
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = '100df5f6f1d622b02af56f1b765bef66'
Session(app)

# Set up database
engine = create_engine('postgres://cjzalftyeobeti:8bdef532d3b7e3e2bc817ad874116bb878f192e0e20ab43bc85f9bbbedebeb05@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d1u5irucd38qh1')
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET', 'POST'])
def index():
    #receiving RegistrationForm and LoginForm from Form.py
    form = RegistrationForm()
    form1 = LoginForm()
    if form1.submit_login.data and form1.validate_on_submit():                                #IF user submitted the form, check IF all the credentials are verified THEN flash the msg and redirect to homepage OTHERWISE flash the invalid msg
        users = db.execute("SELECT * FROM users WHERE username = :username", {"username": form1.username1.data}).fetchone()
        if not users:                #check user enter in the fields
            flash('Login Unsuccessful, Please check your username & password.', 'danger')
            return redirect(url_for('index'))
        elif form1.username1.data == users.username and sha256_crypt.verify(form1.password1.data, users.password):           #matching the login credentials with database
            session["user"] = form1.username1.data            #create session using username
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check your username & password.', 'danger')
            return redirect(url_for('index'))

    elif form.submit.data and form.validate_on_submit():         #IF user submitted the form THEN save the credentials in db
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))            #encrypt the password using passlib
        db.execute("INSERT INTO users (first_name, last_name, username, email, password) VALUES (:first_name, :last_name, :username, :email, :password)", {"first_name":first_name, "last_name":last_name, "username":username, "email":email, "password":password})
        db.commit()
        flash('Account created', 'success')            #flash the msg and redirect to homepage
        return redirect(url_for('index'))

    elif "user" in session:
        return redirect(url_for("home"))
    return render_template("index.html", form = form, form1 = form1)


#Route for Home Page after logged in, where user will gonna seaarch the book
@app.route("/home")
def home():
    if "user" in session:                               #if user is signed in then give access to the home page otherwise log-in page
        user = session["user"]
        return render_template("home.html", title = 'Home', user = user)
    return redirect(url_for("index"))


#Route for Search Results
@app.route("/search_result", methods=['GET', 'POST'])
def search():
    if "user" in session:
        search = request.form.get("search_text")               #retrieving search text from form
        book_id = request.form.get("mycheckbox")               #retrieving CHECK BOX option from form
        if request.method == 'POST':
            if book_id == "1":                 #TITLE
                searches = db.execute("SELECT * FROM books WHERE title ILIKE '%' || :search || '%'",{"search": search}).fetchall()                #used "ILIKE" command for matching string under every case i.e lower,upper,keyword
                if not searches:
                    flash('No record found, try again!', 'danger')
                    return redirect(url_for('home'))
                return render_template("search.html",title = 'Search', searches = searches, search = search, choice = 'Title', user = session["user"])

            elif book_id == "2":              #AUTHOR
                searches = db.execute("SELECT * from books where author ILIKE '%' || :search || '%'", {"search": search}).fetchall()
                if not searches:
                    flash('No record found, try again!', 'danger')
                    return redirect(url_for('home'))
                return render_template("search.html",title = 'Search', searches = searches, search = search, choice = 'Author', user = session["user"])

            elif book_id == "3":             #YEAR
                if search.isdigit():                        #user can insert digits only for year
                    searches = db.execute("SELECT * from books where year = :year", {"year": search}).fetchall()
                    if not searches:
                        flash('No record found, try again!', 'danger')
                        return redirect(url_for('home'))
                    return render_template("search.html",title = 'Search', searches = searches, search = search, choice = 'Year', user = session["user"])
                flash('Enter Year in digits', 'warning')
                return redirect(url_for('home'))

            elif book_id == "4":             #ISBN NUMBERS
                searches = db.execute("SELECT * from books where isbn LIKE '%' || :search || '%'", {"search": search}).fetchall()
                if not searches:
                    flash('No record found, try again!', 'danger')
                    return redirect(url_for('home'))
                return render_template("search.html",title = 'Search', searches = searches, search = search, choice = 'ISBN Number', user = session["user"])

            else:
                flash('Choose the option and fill the search field', 'warning')
                return redirect(url_for('home'))

    return redirect(url_for("index"))


#Route for book records
@app.route("/search_result/<int:search_id>", methods=['Get', 'Post'])
def BookRecord(search_id):

    if "user" in session:
        books = db.execute("SELECT * from books where id = :id", {"id":search_id}).fetchall()
        if not books:
            flash('Unavalaible: Provide another ID', 'danger')
            return redirect(url_for('search'))

        for book in books:
            bookisbn = book.isbn
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "iP3cnf8AFDBdS8AZrL1Bg", "isbns": bookisbn})
        data = res.json()
        avg_rating = data["books"][0]["average_rating"]
        reviews_count = data["books"][0]["work_reviews_count"]

        reviews = db.execute("SELECT username, feedback, rating FROM users INNER JOIN reviews ON reviews.user_id = users.id WHERE book_id = :book_id", {"book_id":search_id}).fetchall()    #retrieving the reviews from db

        feedback = request.form.get('feedback')        #retrieving the information from form
        rating = request.form.get('mycheckbox')
        userdata = db.execute("SELECT * from users where username = :username", {"username":session["user"]}).fetchall()     #retrieving the user data from db
        for user in userdata:
            userid = user.id
        if request.method == 'POST':
            if feedback and rating:            #make sure user checked the rating box and provide the feedback
                if not db.execute("SELECT * from reviews where book_id = :book_id and user_id = :user_id", {"book_id":search_id, "user_id":userid}).fetchall():         #check if user already provided the review
                    db.execute("INSERT INTO reviews (feedback, book_id, user_id, rating) VALUES (:feedback, :book_id, :user_id, :rating)",{"feedback":feedback, "book_id": search_id, "user_id": userid, "rating":rating})
                    db.commit()
                    flash('Successfully submitted the review', 'success')
                    return redirect(url_for("BookRecord", search_id = search_id))
                else:
                    flash('You have already provided the review', 'danger')
                    return redirect(url_for("BookRecord", search_id = search_id))

            else:
                 flash('Please provide review', 'warning')
                 return redirect(url_for("BookRecord", search_id = search_id))

        return render_template('bookrecord.html', title = 'Books', books = books, avg_rating = avg_rating, review_count = reviews_count, reviews = reviews, user = session["user"])
    return redirect(url_for('index'))

#route for api
@app.route("/api/<isbn>", methods=["GET"])
def bookapi(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "iP3cnf8AFDBdS8AZrL1Bg", "isbns": isbn})
    if res:
        data = res.json()
        avg_rating = data["books"][0]["average_rating"]
        reviews_count = data["books"][0]["work_reviews_count"]
        book = db.execute("SELECT * FROM books where isbn = :isbn", {"isbn":isbn}).fetchone()
        if not book:
            return jsonify({"error": "Invalid isbn number"}), 422
        return jsonify({"title": book.title, "author": book.author, "year": book.year, "isbn": book.isbn, "average_rating": avg_rating, "reviews_count": reviews_count})

    return jsonify({"error": "Invalid isbn number"}), 422


#Route for Log Out
@app.route("/logout")
def logout():
    if session.pop("user", None):
        return redirect(url_for("index"))

#DEBUG mode for flask app
if __name__ == "__main__":
    app.run(debug=True)
