from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import author
from flask_app.models import book

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

@app.route("/save/author/<int:id>", methods=["POST"])
def save_author(id):
    book_i = book.Book.get_book(data={'id': id})
    author_i = author.Author.get_author_info(request.form)
    print(author_i, book_i)
    book_i.save_favorite(author_i)
    return redirect(f'/books/{id}')


