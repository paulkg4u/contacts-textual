from textual.app import App
from textual.widgets import (
    Footer, Header, Button, Label,
    DataTable, Static
)
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import Screen


class ContactsApp(App):

    CSS_PATH = "contacts.tcss"
    BINDINGS = [
        ("m", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
        ("a", "add", "Add"),
        ("d", "delete", "Delete"),
        ("c", "clear", "Clear All"),
    ]

    def __init__(self, db):
        super().__init__()
        self.db = db


    def compose(self):
        yield Header()
        contacts_list = DataTable(classes="contacts-list")
        contacts_list.focus()
        contacts_list.add_columns("Name", "Email", "Phone")
        contacts_list.cursor_type = "row"
        contacts_list.zebra_stripes = True
        add_button = Button("Add", variant="success", id="add")
        add_button.focus()
        buttons_panel = Vertical(
            add_button,
            Button("Delete", variant="error", id="delete"),
            Static(classes="separator"),
            Button("Clear All", variant="warning", id="clear"),
            classes="buttons-panel"
        )
        yield Horizontal(contacts_list, buttons_panel)
        yield Footer()
    
    def on_mount(self):
        self.title = "Contacts"
        self.sub_title = "A contacts book app with textual and python"
        self._load_contacts()


    def _load_contacts(self):
        contacts_list = self.query_one(DataTable)
        for contact_data in self.db.get_all_contacts():
            id, *contact = contact_data
            contacts_list.add_row(
                *contact, key=id
            )
    
    def action_toggle_dark(self):
        self.dark = not self.dark

    def action_request_quit(self):
        def check_answer(accepted):
            if accepted:
                self.exit()

        self.push_screen(
            QuestionDialog(
                "Are you sure you want to quit?",
            ),
            check_answer
        )


class QuestionDialog(Screen):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def compose(self):
        no_button = Button("No", variant="primary", id="no")
        no_button.focus()

        yield Grid(
            Label(self.message, id="question"),
            Button("Yes", variant="error", id="yes"),
            no_button,
            id="question-dialog"
        )

    def on_button_pressed(self, event):
        if event.button.id == "yes":
            self.dismiss(True)
        elif event.button.id == "no":
            self.dismiss(False)
