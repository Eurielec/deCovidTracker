import os
import secrets


ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


class HTTPSecurity:

    def __init__(self):
        self.username = ADMIN_USER
        self.password = ADMIN_PASSWORD

    def validate_admin(self, username: str = "", password: str = ""):
        correct_username = secrets.compare_digest(
            username, self.username)
        correct_password = secrets.compare_digest(
            password, self.password)
        if not (correct_username and correct_password):
            return False
        return True
