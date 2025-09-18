# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db, search_contacts
from utils import *


def update_list(page, contacts_list_view, db_conn, term):
    contacts_list_view.controls.clear()
    for contact in search_contacts(term):
        if contact:
            contact_id, name, phone, email = contact
            contacts_list_view.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    title=ft.Row([ft.Icon(ft.Icons.PERSON_2_OUTLINED), ft.Text(name)]),
                                    subtitle=ft.Row(
                                        [ft.Row([ft.Icon(ft.Icons.PHONE, size=15), ft.Text(f"Phone: {phone}")],
                                                expand=True, wrap=True), ft.Text("|"),
                                         ft.Row([ft.Icon(ft.Icons.EMAIL, size=15), ft.Text(f" Email: {email}")],
                                                expand=True, wrap=True)], spacing=5),
                                    trailing=ft.PopupMenuButton(
                                        icon=ft.Icons.MORE_VERT,
                                        items=[
                                            ft.PopupMenuItem(
                                                text="Edit",
                                                icon=ft.Icons.EDIT,
                                                on_click=lambda _, c=contact: open_edit_dialog(page, c,
                                                                                               db_conn,
                                                                                               contacts_list_view)
                                            ),
                                            ft.PopupMenuItem(),
                                            ft.PopupMenuItem(
                                                text="Delete",
                                                icon=ft.Icons.DELETE,
                                                on_click=lambda _, cid=contact_id: delete_contact(page,
                                                                                                  cid, db_conn,
                                                                                                  contacts_list_view)
                                            ),
                                        ],
                                    ),
                                )
                            ]
                        )
                    ),
                    shape=ft.RoundedRectangleBorder(radius=5)
                )
            )
        else:
            contacts_list_view.controls.append(
                ft.ListTile(
                    title = ft.Text("Not Found"),
                    subtitle = ft.Text(f"{term} not found"),
                    title_alignment=ft.alignment.center
                )
            )
    page.update()

def display_contacts(page, contacts_list_view, db_conn):
    """Fetches and displays all contacts in the ListView."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn)

    for contact in contacts:
        contact_id, name, phone, email = contact

        contacts_list_view.controls.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Row([ft.Icon(ft.Icons.PERSON_2_OUTLINED), ft.Text(name)]),
                                subtitle=ft.Row([ft.Row([ft.Icon(ft.Icons.PHONE, size=15), ft.Text(f"Phone: {phone}")], expand=True, wrap=True), ft.Text("|"),ft.Row([ft.Icon(ft.Icons.EMAIL, size=15) ,ft.Text(f" Email: {email}")], expand=True, wrap=True)], spacing=5),
                                trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(
                                        text="Edit",
                                        icon=ft.Icons.EDIT,
                                        on_click=lambda _, c=contact: open_edit_dialog(page, c,
                                                                                       db_conn, contacts_list_view)
                                    ),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(
                                        text="Delete",
                                        icon=ft.Icons.DELETE,
                                        on_click=lambda _, cid=contact_id: delete_contact(page,
                                                                                          cid, db_conn,
                                                                                          contacts_list_view)
                                    ),
                                ],
                                ),
                            )
                        ]
                    )
                ),
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )
    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn, prefix_num):
    """Adds a new contact and refreshes the list."""
    name_input, phone_input, email_input = inputs
    if validate(name_input, phone_input, email_input, page):
        email_input.value += "@gmail.com"
        phone_input.value = f"{country_prefixes[prefix_num.value]}{phone_input.value.lstrip('0')}"
        add_contact_db(db_conn, name_input.value.strip().title(), phone_input.value, email_input.value)
        for field in inputs:
            field.value = ""

    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Deletes a contact and refreshes the list."""

    def confirmed_delete(e):
        delete_contact_db(db_conn, contact_id)
        display_contacts(page, contacts_list_view, db_conn)
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal = True,
        title = ft.Text("Confirm Deletion"),
        content = ft.Text("Are you sure you want to delete this contact?"),
        actions = [
            ft.TextButton(text="Yes", on_click=confirmed_delete),
            ft.TextButton(text="No", on_click=lambda e: page.close(dialog)),
        ]
    )

    page.open(dialog)

def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    country_drop = ft.DropdownM2(
        label="Country",
        options=[ft.dropdownm2.Option(c) for c in country_prefixes.keys()],
        icon=ft.Icons.PHONE,
        value="PHL (+63)",
        width=170,
    )

    edit_name = ft.TextField(label="Name", width=350, icon=ft.Icons.PERSON_2_ROUNDED, value=name)
    edit_phone = ft.TextField(label="Phone", width=350,hint_text="###-####-###", keyboard_type=ft.KeyboardType.NUMBER, icon=ft.Icons.PHONE, value=phone, expand = True)
    edit_email = ft.TextField(label="Email", width=350, keyboard_type=ft.KeyboardType.EMAIL, on_change= lambda e: email_domain(edit_email, e.control.value, page), icon=ft.Icons.EMAIL, value=email)

    def save_and_close(e):
        if validate(edit_name, edit_phone, edit_email, page):
            update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value,
                              edit_email.value)
            dialog.open = False
            page.update()
        display_contacts(page, contacts_list_view, db_conn)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, ft.Column([edit_phone, edit_email])], alignment=ft.MainAxisAlignment.START),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)
                                                       or page.update()),
            ft.TextButton("Save", on_click=save_and_close),
        ],
        alignment=ft.alignment.top_center,
    )

    page.open(dialog)

