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

    page.theme_mode = ft.ThemeMode.LIGHT

    
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
        success_dialog = ft.AlertDialog(
            icon=ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
            modal=True,
            title = ft.Text("Login Successful", text_align=ft.TextAlign.CENTER),
            content= ft.Text(f'Welcome, {user_name.value}'), # add username
            actions = [
                ft.TextButton(
                    text="OK", on_click = lambda e: page.close(success_dialog), 
                )
            ]
        )
        
        failure_dialog = ft.AlertDialog(
            icon = ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.RED),
            modal = True,
            title = ft.Text("Login Failed", text_align=ft.TextAlign.CENTER),
            content = ft.Text("Invalid username or password"),
            actions = [
                ft.TextButton(
                    text="OK", on_click = lambda e: page.close(failure_dialog), 
                )
            ]
        )

        invalid_input_dialog = ft.AlertDialog(
            icon=ft.Icon(name=ft.Icons.INFO, color=ft.Colors.BLUE),
            modal = True,
            title = ft.Text("Input Error", text_align=ft.TextAlign.CENTER),
            content = ft.Text("Please enter username or password"),
            actions = [
                ft.TextButton(
                    text = "OK", on_click = lambda e: page.close(invalid_input_dialog)
                )
            ]
        )

        database_error_dialog  = ft.AlertDialog(
            modal = True,
            title = ft.Text("Database Error"),
            content = ft.Text("An error occured while connecting to the database"), 
            alignment = ft.alignment.center,
            actions = [ft.TextButton(
                text="OK", on_click = lambda e: page.close(database_error_dialog)
            )]
        )

        if user_name.value and password.value:
            try:
                db = connect_db()
                cursor = db.cursor()

                query = "SELECT * FROM users WHERE username = %s AND password = %s"

                cursor.execute(query, (user_name.value, password.value))

                result = cursor.fetchone()

                if result:
                    page.open(success_dialog)
                else:
                    page.open(failure_dialog)
                page.update()
            except mysql.connector.Error:
                page.open(database_error_dialog)
            finally:
                if cursor:
                    cursor.close()
                if db:
                    db.close()
        else:
            page.open(invalid_input_dialog)
    
    login_button = ft.ElevatedButton(text="Login", width=100, icon=ft.Icons.LOGIN,on_click=login_click)

    page.add(page_title, 
            ft.Container(
                content=ft.Column([user_name, password],
                spacing = 20
                )
            ), 
            ft.Container(
                content = login_button,
                margin = ft.Margin(0, 20, 40, 0),
                alignment = ft.alignment.top_right
            )
        )
    page.update()

    

ft.app(target=main)
