# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact, update_list
from week4_labs.contact_book_app.src.utils import country_prefixes


def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT

    db_conn = init_db()

    name_input = ft.TextField(label="Name", width=350, icon=ft.Icons.PERSON_2_ROUNDED)
    phone_input = ft.TextField(label="Phone", width=170,hint_text="###-####-###", keyboard_type=ft.KeyboardType.NUMBER)
    email_input = ft.TextField(label="Email", width=350, keyboard_type=ft.KeyboardType.EMAIL, on_change= lambda e: email_domain(e.control.value), icon=ft.Icons.EMAIL)

    country_drop = ft.DropdownM2(
        label="Country",
        options=[ft.dropdownm2.Option(c) for c in country_prefixes.keys()],
        icon=ft.Icons.PHONE,
        value="PHL (+63)",
        width=170,
    )

    inputs = (name_input, phone_input, email_input)

    search_box = ft.TextField(label="Search contacts", on_change=lambda e: displaying_contacts(e.control.value), prefix_icon=ft.Icons.SEARCH)

    contacts_list_view = ft.ListView(expand=1, spacing=10)

    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn, country_drop)
    )

    page.add(
        ft.Column(
            [
                ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                ft.Row([country_drop, phone_input],  alignment=ft.MainAxisAlignment.CENTER, wrap=True),
                email_input,
                add_button,
                ft.Divider(),
                search_box,
                ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content = contacts_list_view,
                    expand = True
                )
            ],
            expand = True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    def displaying_contacts(term):
        if term:
            update_list(page, contacts_list_view, db_conn, term)
        else:
            display_contacts(page, contacts_list_view, db_conn)

    def email_domain(term):
        if "@" in term:
            email_input.suffix_text = None
        else:
            email_input.suffix_text = "@gmail.com"
        page.update()

    email_domain("")
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)