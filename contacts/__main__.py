from database import Database
from tui import ContactsApp

def main():
    app = ContactsApp(db=Database())
    app.run()


if __name__ == "__main__":
    main()