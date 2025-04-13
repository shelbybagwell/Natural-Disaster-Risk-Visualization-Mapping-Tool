from werkzeug.security import generate_password_hash, check_password_hash
import re

class UserHelper:

    def is_valid_email(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    def is_valid_username(username):
        return re.match(r"^[a-zA-Z0-9_]{4,50}$", username)

    def is_valid_name(name):
        return re.match(r"^[A-Za-z-\s\']{1,50}$", name)

    def is_strong_password(password):
        # At least 8 characters consisting of uppercase, lowercase, digits, or special characters
        return re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$', password)

    def hash_password(password):
        return generate_password_hash(password)
    
    def sanitize_user_object(User):
                
        if "password" in User:
            del User["password"]  # remove password

        return User