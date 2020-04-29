import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://cjzalftyeobeti:8bdef532d3b7e3e2bc817ad874116bb878f192e0e20ab43bc85f9bbbedebeb05@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d1u5irucd38qh1')
db = scoped_session(sessionmaker(bind=engine))


def main():
    #Get Data from CSV file
    f = open("books.csv")
    reader = csv.reader(f)

    #Insert the CSV Data into Database
    books = db.execute("Select * from books").fetchall()

    #Check if Database is empty then insert the CSV data
    if not books:
        for isbn, title, author, year in reader:
                db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                                                {"isbn":isbn, "title":title, "author":author, "year":year})
                db.commit()

if __name__ == "__main__":
    main()
