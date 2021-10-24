import secrets

from config import config


class HTTPSecurity:

    def __init__(self):
        c = config.Config()
        self.a_configs = c.get_associations_configs()

    def validate_admin(self, association, username: str = "",
                       password: str = ""):
        correct_username = secrets.compare_digest(
            username, self.a_configs[association]["admin_username"])
        correct_password = secrets.compare_digest(
            password, self.a_configs[association]["admin_password"])
        if not (correct_username and correct_password):
            return False
        return True
