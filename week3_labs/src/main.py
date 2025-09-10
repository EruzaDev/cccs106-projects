import flet as ft
import mysql.connector
from db_connection import connect_db


def main(page: ft.Page):
    page.window.center()
    page.window.frameless = True

    page.title = "User Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.window.height = 350
    page.window.width = 400

    page.bgcolor = ft.Colors.AMBER_ACCENT

    page_title = ft.Text("User Login",
                         size=20,
                         text_align=ft.TextAlign.CENTER,
                         font_family='Arial',
                         weight=ft.FontWeight.BOLD
                         )

    user_name = ft.TextField(label="User Login",
                            hint_text="Enter your user name", 
                            helper_text="This is your unique identifier",
                            width=300,
                            autofocus=True,
                            icon=ft.Icon(name=ft.Icons.PERSON),
                            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
                            )
    password = ft.TextField(label="Password", 
                            hint_text="Enter your password",
                            helper_text="This is your secret key",
                            width=300,
                            password=True,
                            can_reveal_password=True,
                            icon=ft.Icon(name=ft.Icons.PASSWORD),
                            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
                            )
    
    async def login_click(e):
        success = ft.AlertDialog(
            modal=True,
            title = ft.Text("Login Successful"),
            content= ft.Text(f'Welcome, [username]'), # add username
            alignment=ft.alignment.center,
            actions = [
                ft.TextButton(
                    text="OK", on_click = lambda e: page.close(success), 
                )
            ]
        )

    page.add(page_title, user_name, password, login_click())

    

ft.app(main)
