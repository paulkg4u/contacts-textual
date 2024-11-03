from textual.app import App, on
from textual.widgets import (
    Footer, Header, Button, Label,
    DataTable, Static, Input
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

    @on(Button.Pressed, "#add")
    def action_add(self):
        def check_contact(contact_data):
            if contact_data:
                self.db.add_contact(contact_data)
                id, *contact = self.db.get_last_contact()
                self.query_one(DataTable).add_row(
                    *contact, key=id
                )

        self.push_screen(InputDialog(), check_contact)

    @on(Button.Pressed, "#delete")
    def action_delete(self):
        contacts_list = self.query_one(DataTable)
        row_key, _ = contacts_list.coordinate_to_cell_key(
            contacts_list.cursor_coordinate
        )

        def check_answer(accepted):
            if accepted and row_key:
                self.db.delete_contact(contact_id=row_key.value)
                contacts_list.remove_row(row_key)

        name = contacts_list.get_row(row_key)[0]

        self.push_screen(
            QuestionDialog(
                f"Are you sure you want to delete {name}?",
            ),
            check_answer
        )

    @on(Button.Pressed, "#clear")
    def action_clear(self):
        def check_answer(accepted):
            if accepted:
                self.db.clear_contacts()
                self.query_one(DataTable).clear()

        self.push_screen(
            QuestionDialog(
                "Are you sure you want to clear all contacts?",
            ),
            check_answer
        )

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


class InputDialog(Screen):

    def compose(self):
        yield Grid(
            Label("Add a new contact", id="title"),
            Label("Name", classes="label"),
            Input(
                placeholder="Contact Name",
                classes="input",
                id="name"
            ),
            Label("Email", classes="label"),
            Input(
                placeholder="Contact Email",
                classes="input",
                id="email"
            ),
            Label("Phone", classes="label"),
            Input(
                placeholder="Contact Phone",
                classes="input",
                id="phone"
            ),
            Static(),

            Button("Save", variant="success", id="save"),
            Button("Cancel", variant="warning", id="cancel"),
            id="input-dialog"
        )

    def on_button_pressed(self, event):
        if event.button.id == "save":
            self.dismiss((
                self.query_one("#name", Input).value,
                self.query_one("#email", Input).value,
                self.query_one("#phone", Input).value
            ))
        elif event.button.id == "cancel":
            self.dismiss()
