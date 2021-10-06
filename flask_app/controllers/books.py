from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import author
from flask_app.models import book

@app.route("/books")
def form():
    books = book.Book.get_all()
    return render_template("books.html", books=books)

@app.route("/save_books", methods=["POST"])
def save_books():
    newbook = book.Book.save(request.form)
    if newbook:
        return redirect('/books')
    else:
        flash(f"There was an error saving the data {newbook}","error")

@app.route("/books/<int:id>")
def show_book(id):
    book_e = book.Book.get_book({'id': id}).get_book_favorites()
    authors = author.Author.get_all()
    faves = []
    if book_e.favorites:
        for fave in book_e.favorites:
            faves.append(fave.name)
    return render_template("b_favorites.html", book=book_e, authors=authors, faves=faves )

@app.route("/save/book/<int:id>", methods=["POST"])
def save_book(id):
    author_i= author.Author.get_author_info({'id': id})
    book_i = book.Book.get_book(request.form)
    print(author_i, book_i)
    author_i.save_favorite(book_i)
    return redirect(f'/authors/{id}')