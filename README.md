# Project 1

OVERVIEW:

Registration: • using FLASK-WTFORMS libraray for registration form. User can able to register with mandatory fields i.e. username, email and password • password is encrypted using passlib.hash-sha256_crypt library • index.html, forms.py, application.py • http://localhost:5000/

Login: • using FLASK-WTFORMS libaray for login form. User can able to login with mandatory fields i.e. username and password • index.html, forms.py, application.py • http://localhost:5000/

Logout: • after logged in, user can able to logout from navigation bar • application.py, layout.html • http://localhost:5000/home

Import: • using CSV libraray, import the books.csv file to the PostgreSQL database on heroku server • import.py

Search: • user can able to search books through title, author, year and ISBN. The result is shown on another page consisting list of all possible search results. • home.html, search.html, application.py • http://localhost:5000/home • http://localhost:5000/search_result

Book Page: • From the result of search, user can able to click on the tilte of book to see the book record on another page with book id (search_result/book.id) • search.html, bookrecord.html, application.py • http://localhost:5000/search_result/6

Review Submission: • On the book page, user can able to submit a review which can only be done at once. User can also able to see the multiple reviews of that book from different users as well. • Bookrecord.html, application.py • http://localhost:5000/search_result/6

Goodreads Review Data: • User can also able to see the average rating and number of reviews from Goodreads using REQUESTS library by accessing API in JSON format • Bookrecord.html, application.py • http://localhost:5000/search_result/6

API Access: • From the search result page, user can also able to request data by clicking the ISBN in JSON format by accessing it’s api. User can also get the data using url (api/isbn) • application.py • http://localhost:5000/search_result • http://localhost:5000/api/0375913750

Details: Developed a responsive Web application using Flask and Bootstrap. Using flask-wtforms and passlib.hash-sha256 libraries to make registration and login form more responsive and secure. In this way user get feedback if they are doing wrong entry. After the logged in, username can be shown throughout the website to display which user is active in the current session. Now user can easily search out the books using keyword to display all possible results. And then user can able to see the record of the books, see the multiple reviews from other users and provide the reviews. If user make a GET request to website using api/isbn where isbn is the isbn number of the book, website is returning the a JSON response containing the book’s record.
