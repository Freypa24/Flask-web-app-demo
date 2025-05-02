import re


def validate_password(password):
    strength = 0

    if len(password) >= 8:
        strength += 1

    if re.search(r'[A-Z]', password):
        strength += 1

        # Check if the password contains at least one lowercase letter
    if re.search(r'[a-z]', password):
        strength += 1

        # Check if the password contains at least one digit
    if re.search(r'\d', password):
        strength += 1

        # Check if the password contains at least one special character
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength += 1

        # If the conditions are met, the password is valid
    if strength >= 4:
        return True
    else:
        return False
