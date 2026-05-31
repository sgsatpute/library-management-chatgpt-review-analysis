import hashlib as hash
import csv
from datetime import datetime, timedelta

class Book:                     # Class: A template or blueprint for creating objects
    def __init__(self, book_id, title, author, quantity, Cost,due_date=None,):     # Book is a class that defines attributes like title, author, and pages
        self.book_id = book_id  # self.book_id refers to the instance's attribute
        self.title = title
        self.author = author
        self.quantity = quantity
        self.Cost = Cost
        self.due_date = due_date
        self.reviews = []       # store reviews

    def add_review(self, review_text):
        self.reviews.append(review_text)

    def display_reviews(self):
        if self.reviews:
            print("\n  Reviews:")
            for review in self.reviews:
                print(f"    - {review}")
        else:
            print("\n  No reviews available.")

# Class to represent a Patron
class Patron:
    def __init__(self, patron_id, name, email, password, role='patron',):
        self.patron_id = patron_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

# Class to manage the Library system
class Library:
    def __init__(self):
        self.books = []
        self.patrons = []
        self.borrowed_books = {}
        self.current_patron = None
        self.load_books()
        self.load_patrons()
        self.load_borrowed_books()

    def load_books(self):
        try:
            with open('books.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book(
                        book_id=int(row['book_id']),
                        title=row['title'],
                        author=row['author'],
                        quantity=int(row['quantity']),
                        Cost=float(row['Cost']),
                        due_date=datetime.fromisoformat(row['due_date']) if row['due_date'] else None
                    )
                    book.reviews = row['reviews'].split('|') if row['reviews'] else []  # Load reviews
                    self.books.append(book)
        except FileNotFoundError:
            print("books.csv not found, starting with an empty book list.")
        except Exception as e:
            print(f"Error loading books: {e}")

    def save_books(self):
        try:
            with open('books.csv', mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['book_id', 'title', 'author', 'quantity','Cost','reviews','due_date'])
                writer.writeheader()
                for book in self.books:
                    writer.writerow({
                        'book_id': book.book_id,
                        'title': book.title,
                        'author': book.author,
                        'quantity': book.quantity,
                        'Cost': book.Cost,
                        'reviews': '|'.join(book.reviews),
                        'due_date': book.due_date.isoformat() if book.due_date else ''
                    })
        except Exception as e:
            print(f"Error saving books: {e}")

    def load_patrons(self):
        try:
            with open('patrons.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    patron = Patron(
                        patron_id=int(row['patron_id']),
                        name=row['name'],
                        email=row['email'],
                        password=row['password'],
                        role=row['role']
                    )
                    self.patrons.append(patron)
        except FileNotFoundError:
            print("patrons.csv not found, starting with an empty patron list.")
        except Exception as e:
            print(f"Error loading patrons: {e}")

    def save_patrons(self):
        try:
            with open('patrons.csv', mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['patron_id', 'name', 'email', 'password', 'role',])
                writer.writeheader()
                for patron in self.patrons:
                    writer.writerow({
                        'patron_id': patron.patron_id,
                        'name': patron.name,
                        'email': patron.email,
                        'password':patron.password,
                        'role': patron.role,
                    })
        except Exception as e:
            print(f"Error saving patrons: {e}")

    def load_borrowed_books(self):
        try:
            with open('borrowed_books.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    patron_id = int(row[0])
                    book_id = int(row[1])
                    due_date = datetime.fromisoformat(row[2]) if row[2] else None
                    book = next((b for b in self.books if b.book_id == book_id), None)
                    if book:
                        if patron_id in self.borrowed_books:
                            self.borrowed_books[patron_id].append(book)
                        else:
                            self.borrowed_books[patron_id] = [book]
                        book.due_date = due_date
        except FileNotFoundError:
            print("borrowed_books.csv not found, starting with an empty borrowed books list.")
        except Exception as e:
            print(f"Error loading borrowed books: {e}")

    def save_borrowed_books(self):
        try:
            with open('borrowed_books.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['patron_id', 'book_id', 'due_date'])
                for patron_id, books in self.borrowed_books.items():
                    for book in books:
                        writer.writerow([patron_id, book.book_id, book.due_date.isoformat() if book.due_date else ''])
        except Exception as e:
            print(f"Error saving borrowed books: {e}")

    def add_book(self, book):
        if any(b.book_id == book.book_id for b in self.books):
            print("Book ID already exists. Please use a unique ID.")
            return
        self.books.append(book)
        self.save_books()
        print("Book added successfully.")

    def view_books(self):
        print("\nBooks in Library:")
        for book in self.books:
            print(f"  \n(|ID: {book.book_id},  |Title: {book.title},  |Author: {book.author},  |Quantity: {book.quantity},  |Cost: {book.Cost})")
            book.display_reviews()

    def delete_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                self.save_books()
                print("Book deleted successfully.")
                return
        print("Book not found.")

    def search_books_by_title(self, search_query):      # where not able to get accurate results due upper lower case
        search_query_lower = search_query.lower()       # is used to convert a string (typically a user-provided search query) to lowercase
        found_books = [book for book in self.books if search_query_lower in book.title.lower()]
        if found_books:
            print("\nSearch Results:")
            for book in found_books:
                print(f"  |ID: {book.book_id},  |Title: {book.title},  |Author: {book.author},  |Cost: {book.Cost},  |Quantity: {book.quantity}")
        else:
            print("No books found with the given title.")

    def add_patron(self, patron):
        if any(p.patron_id == patron.patron_id for p in self.patrons):
            print("Patron ID already exists. Please use a unique ID.")
            return
        self.patrons.append(patron)
        self.save_patrons()
        print("Patron registered successfully.")

    def view_patrons(self):
        print("\nPatrons:")
        for patron in self.patrons:
            print(f"ID: {patron.patron_id}, Name: {patron.name}, Email: {patron.email}, Role: {patron.role}")

    def delete_patron(self, patron_id):
        for patron in self.patrons:
            if patron.patron_id == patron_id:
                self.patrons.remove(patron)
                self.save_patrons()
                print("Patron deleted successfully.")
                return
        print("Patron not found.")

    def borrow_book(self, book_id, patron_id):
        for book in self.books:
            if book.book_id == book_id:
                if book.quantity > 0:
                    if patron_id in self.borrowed_books:
                        self.borrowed_books[patron_id].append(book)
                    else:
                        self.borrowed_books[patron_id] = [book]
                    book.quantity -= 1
                    book.due_date = datetime.now() + timedelta(days=7)
                    self.save_books()
                    self.save_borrowed_books()
                    print("Book borrowed successfully.")
                    return
                else:
                    print("Book is out of stock.")
                    return
        print("Book not found.")

    def return_book(self, book_id, patron_id):
        if patron_id in self.borrowed_books:
            for book in self.borrowed_books[patron_id]:
                if book.book_id == book_id:
                    self.borrowed_books[patron_id].remove(book)
                    for library_book in self.books:
                        if library_book.book_id == book_id:
                            library_book.quantity += 1
                            library_book.due_date = None
                    self.save_books()
                    self.save_borrowed_books()
                    print("Book returned successfully.")
                    return
            print("You have not borrowed this book.")
        else:
            print("You have not borrowed any books.")

    def check_overdue_books(self):
        if self.current_patron.role == 'admin':
            print("\nOverdue Books:")
            for patron_id, books in self.borrowed_books.items():
                for book in books:
                    if book.due_date and book.due_date < datetime.now():
                        print(f" |Patron ID: {patron_id},  |Book ID: {book.book_id},  |Title: {book.title},  |Due Date: {book.due_date.strftime('%Y-%m-%d')}")
        else:
            patron_id = self.current_patron.patron_id
            print("\nYour Overdue Books:")
            if patron_id in self.borrowed_books:
                for book in self.borrowed_books[patron_id]:
                    if book.due_date and book.due_date < datetime.now():
                        days_overdue = (datetime.now() - book.due_date).days
                        fine = days_overdue * 100
                        print("You have received a fine.")
                        print(f" |Book ID: {book.book_id},  |Title: {book.title},  |Fine: {fine},  |Due Date: {book.due_date.strftime('%Y-%m-%d')}")
            else:
                print("No overdue books.")

    def register_patron(self):
        try:
            patron_id = int(input("Enter Patron ID: "))
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            hash_password = hash.sha256(password.encode()).hexdigest()     # converted into hash
            password=hash_password
            role = input("Enter Role (patron/admin): ").lower()            # lower case
            if role not in ['patron', 'admin']:
                print("Invalid role. Defaulting to 'patron'.")
                role = 'patron'
            patron = Patron(patron_id, name, email, password, role)
            self.add_patron(patron)
        except ValueError:
            print("Invalid input. Please enter valid details.")

    def login_patron(self):
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        hash_password= hash.sha256(password.encode()).hexdigest()              # again hashed
        password=hash_password
        for patron in self.patrons:
            if patron.email == email and patron.password == password:          #the hashed password
                self.current_patron = patron
                print(f"Welcome, {patron.name}!")
                if patron.role == 'patron':
                    self.display_borrowed_books(patron.patron_id)
                return True
        print("Invalid email or password.")
        return False

    def logout_patron(self):
        self.current_patron = None
        print("Logged out successfully.")

    def display_borrowed_books(self, patron_id):
        if patron_id in self.borrowed_books:
            print("\nBorrowed Books:")
            for book in self.borrowed_books[patron_id]:
                print(f" |ID: {book.book_id},  |Title: {book.title},  |Due Date: {book.due_date.strftime('%Y-%m-%d') if book.due_date else 'N/A'}")
        else:
            print("No borrowed books.")

    def review_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:             
                review_text = input(f"Enter your review for {book.title}: ")
                book.add_review(review_text)
                self.save_books()
                print("Review added successfully.")
                return
        print("Book not found.")

# Functions to display menus and handle choices
def display_initial_menu():
    print("\nLibrary Management System Menu:")
    print("1. Register Patron/Admin")
    print("2. Login")
    print("3. Exit")
    return input("Enter your choice: ")

def display_admin_menu():
    print("\nAdmin Menu:")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search a Book")
    print("4. Delet Book")
    print("5. Add Patron")
    print("6. View Patrons")
    print("7. Delet patron")
    print("8. Check overdue books")
    print("9. Logout")
    print("10. Exit")
    return input("Enter your choice: ")

def display_patron_menu():
    print("\nPatron Menu:")
    print("1. View Books")
    print("2. search a book")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Review Book")
    print("6. Check Overdue Books")
    print("7. Logout")
    print("8. Exit")
    return input("Enter your choice: ")

# Main function to run the library system

def main():
    library = Library()

    while True:
        if library.current_patron is None:
            choice = display_initial_menu()

            if choice == '1':
                library.register_patron()

            elif choice == '2':
                if library.login_patron():
                    continue

            elif choice == '3':
                print("Exiting program...")
                library.save_books()
                library.save_patrons()
                library.save_borrowed_books()
                break


            else:
                print("Invalid choice. Please enter a number from 1 to 3.")
# The admin menu==
        else:
            if library.current_patron.role == 'admin':
                while True:
                    choice = display_admin_menu()

                    if choice == '1':
                        book_id = int(input("Enter Book ID: "))
                        title = input("Enter Title: ")
                        author = input("Enter Author: ")
                        quantity = int(input("Enter Quantity: "))
                        Cost = int(input("enter the cost of the book"))
                        review = input("Enter review of the book (optional): ")
                        book = Book(book_id, title, author, quantity, Cost)
                        if review.strip():
                            book.add_review(review)
                        library.add_book(book)

                    elif choice == '2':
                        library.view_books()

                    elif choice == '3':
                        search_query = input("Enter the title to search: ")
                        library.search_books_by_title(search_query)

                    elif choice == '4':
                        book_id = int(input("Enter Book ID to delete: "))
                        library.delete_book(book_id)

                    elif choice == '5':
                        library.register_patron()

                    elif choice == '6':
                        library.view_patrons()

                    elif choice == '7':
                        patron_id = int(input("Enter Patron ID to delete: "))
                        library.delete_patron(patron_id)

                    elif choice == '8':
                        library.check_overdue_books()

                    elif choice == '9':
                        library.logout_patron()
                        break

                    elif choice == '10':
                        print("Exiting program...")
                        library.save_books()
                        library.save_patrons()
                        library.save_borrowed_books()
                        exit()

                    else:
                        print("Invalid choice. Please enter a number from 1 to 10.")

# the patron menu==
            else:
                while True:
                    choice = display_patron_menu()

                    if choice == '1':
                        library.view_books()

                    elif choice == '2':
                        search_query = input("enter title book to search:")
                        library.search_books_by_title(search_query)


                    elif choice == '3':
                        book_id = int(input("Enter Book ID to borrow: "))
                        patron_id = library.current_patron.patron_id
                        library.borrow_book(book_id, patron_id)          # line=201

                    elif choice == '4':
                        book_id = int(input("Enter Book ID to return: "))
                        patron_id = library.current_patron.patron_id
                        library.return_book(book_id, patron_id)          # line=220

                    elif choice == '5':
                        book_id = int(input("Enter Book ID to review: "))
                        library.review_book(book_id)                     

                    elif choice == '6':
                        library.check_overdue_books()                    # line=237

                    elif choice == '7':
                        library.logout_patron()                          # line=284
                        break

                    elif choice == '8':
                        print("Exiting program...")
                        library.save_books()
                        library.save_patrons()
                        library.save_borrowed_books()
                        exit()

                    else:
                        print("Invalid choice. Please enter a number from 1 to 8.")

if __name__ == "__main__":
    main()
#end of program
