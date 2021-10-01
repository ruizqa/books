from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book
# model the class after the friend table from our database
class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites=[]
# Now we use class methods to query our database
    def get_author_with_books(self):
        query= "SELECT books.id FROM authors\
                LEFT JOIN favorites ON favorites.author_id = authors.id\
                LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s HAVING books.id IS NOT NULL;"
        results = connectToMySQL('books').query_db( query , data={'id': self.id} )
        if not results:
            return self
        else:
            for row in results:
                self.favorites.append(book.Book.get_book(row))
            return self
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('books').query_db(query)
        # Create an empty list to append our instances of friends
        authors = []
        # Iterate over the db results and create instances of friends with cls.
        if len(results)<1:
            return False
        else:        
            for author in results:
                authors.append( cls(author) )
            return authors
    @classmethod
    def get_author_info(cls,data):
        query = "SELECT * FROM authors WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('books').query_db(query,data)
        if len(result)<1:
            return False
        else:
            return cls(result[0])
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO authors (name, created_at, updated_at) VALUES ( %(name)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('books').query_db( query, data )
    def save_favorite(self,book):
        query= "INSERT INTO favorites (book_id, author_id)\
            VALUES ( %(book_id)s , %(author_id)s);"
        data = {'book_id': book.id, 'author_id': self.id}
        
        return connectToMySQL('books').query_db(query,data)