from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author
# model the class after the friend table from our database
class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites =[]
# Now we use class methods to query our database
    @classmethod
    def get_all(cls): #not a useful method for this assignment, but leaving it here just in case
        query = "SELECT * FROM books;"
        results = connectToMySQL('books').query_db(query)
        books = []
        if len(results)<1:
            return False
        else:
            for book in results:
                books.append( cls(book) )
            return books
    @classmethod
    def get_book(cls,data): 
        query = "SELECT * FROM books WHERE id = %(id)s ;"
        results = connectToMySQL('books').query_db(query,data)
        if not results or len(results)<1:
            return False
        else:
            return(cls(results[0]))   
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO books ( title , num_of_pages , created_at, updated_at ) VALUES ( %(title)s , %(num_of_pages)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('books').query_db( query, data )
    @classmethod
    def update(cls, data ):
        query = "UPDATE books SET title = %(title)s , num_of_pages = %(num_of_pages)s, updated_at = NOW() WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('books').query_db( query, data )
    @classmethod
    def remove(cls, data ):
        # query = "SET SQL_SAFE_UPDATES = 0;"
        query = "DELETE FROM books WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('books').query_db( query, data )
    def get_book_favorites(self):
        query = "SELECT authors.id FROM books LEFT JOIN favorites ON books.id = favorites.book_id\
            LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s\
            HAVING authors.id IS NOT NULL;"
        data={'id':self.id}
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('books').query_db(query,data)
        if not results:
            return self
        else:
            for favorite in results:
                self.favorites.append(author.Author.get_author_info(favorite))
            return self
    def save_favorite(self,author):
        query= "INSERT INTO favorites (book_id, author_id)\
            VALUES ( %(book_id)s , %(author_id)s);"
        data = {'book_id': self.id, 'author_id': author.id}
        
        return connectToMySQL('books').query_db(query,data)