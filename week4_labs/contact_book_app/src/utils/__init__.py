import re

EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def validate(name, phone, email, page):
    if name.value.strip() == "":
        name.error_text = "Name cannot be empty!"
    else:
        name.error_text = None
    if phone.value.strip() == "":
        phone.error_text = "Phone cannot be empty!"
    elif not phone.value.isdigit():
        phone.error_text = "Phone must be a valid number!"
    else:
        phone.error_text = None
    if email.value.strip() == "":
        email.error_text = "Email cannot be empty!"
    elif not bool(EMAIL_PATTERN.match(email.value.strip())):
        email.error_text = "Invalid email address"
    else:
        email.error_text = None

    print(phone.error_text)
    print(name.error_text)
    print(email.error_text)


    if not email.error_text and not phone.error_text and not  name.error_text:
        return True
    else:
        return False