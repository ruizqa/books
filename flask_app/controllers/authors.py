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

@app.route("/")
@app.route("/authors")
def show_authors():
    authors = author.Author.get_all()
    return render_template("authors.html", authors=authors)

@app.route("/save_authors", methods=["POST"])
def save_dojo():
    author.Author.save(request.form)
    return redirect("/authors")

@app.route("/authors/<int:id>")
def show_author(id):
    author_e = author.Author.get_author_info({'id': id}).get_author_with_books()
    books = book.Book.get_all()
    faves = []
    print(author_e,author_e.favorites,books)
    if author_e.favorites:
        for fave in author_e.favorites:
            faves.append(fave.title)
    return render_template("a_favorites.html", author=author_e, books=books, faves=faves)

@app.route("/books/<int:id>")
def show_book(id):
    book_e = book.Book.get_book({'id': id}).get_book_favorites()
    authors = author.Author.get_all()
    faves = []
    if book_e.favorites:
        for fave in book_e.favorites:
            faves.append(fave.name)
    return render_template("b_favorites.html", book=book_e, authors=authors, faves=faves )

@app.route("/save/author/<int:id>", methods=["POST"])
def save_author(id):
    book_i = book.Book.get_book(data={'id': id})
    author_i = author.Author.get_author_info(request.form)
    print(author_i, book_i)
    book_i.save_favorite(author_i)
    return redirect(f'/books/{id}')

@app.route("/save/book/<int:id>", methods=["POST"])
def save_book(id):
    author_i= author.Author.get_author_info({'id': id})
    book_i = book.Book.get_book(request.form)
    print(author_i, book_i)
    author_i.save_favorite(book_i)
    return redirect(f'/authors/{id}')

