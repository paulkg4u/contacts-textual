from textual.app import App
from textual.widgets import Footer, Header

class ContactsApp(App):
    def compose(self):
        yield Header()
        yield Footer()
    
    def on_mount(self):
        self.title = "Contacts"
        self.sub_title = "A contacts book app with textual and python"
    