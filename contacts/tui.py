from textual.app import App
from textual.widgets import Footer, Header, Button, Label
from textual.containers import Grid
from textual.screen import Screen


class ContactsApp(App):

    CSS_PATH = "contacts.tcss"
    BINDINGS = [
        ("m", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
    ]
    def compose(self):
        yield Header()
        yield Footer()
    
    def on_mount(self):
        self.title = "Contacts"
        self.sub_title = "A contacts book app with textual and python"
    
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
