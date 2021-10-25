import re
from config import config


class Validator:

    def __init__(self):
        """
        Create Validator instance
        """
        self.config = config.Config()
        return

    def validate_nif_nie(self, nif_nie: str):
        """
        Returns if a provided DNI is valid or not.

        Arguments:
            nif_nie (str): the spanish id number to validate.
        """
        # Check the format
        nif_nie = re.sub("[-, ]", "", nif_nie).strip()
        if not re.match(
            "(^[X,Y,Z][-, ]?[0-9]{7}[-, ]?[A-Z]$)|(^[0-9]{8,8}[-, ]?[A-Za-z]$)",
                nif_nie):
            return False
        if nif_nie[0] in "XYZ":
            swap = {
                "X": "0", "Y": "1", "Z": "2"
            }
            nif_nie = swap[nif_nie[0]] + nif_nie[1:]
        # Check the letter
        _letter = 'TRWAGMYFPDXBNJZSQVHLCKE'[int(nif_nie[:-1]) % 23]
        if nif_nie[-1] != _letter:
            return False
        return True

    def validate_email(self, email: str):
        """
        Returns if the provided email is a valid UPM email account.

        Arguments:
            email (str): the email to validate.
        """
        if not re.match(".*@(?:alumnos.upm.es|upm.es|.*.upm.es)$", email):
            return False
        return True

    def validate_type(self, type: str):
        if not re.match("(:?access|exit)$", type):
            return False
        return True

    def validate_association(self, association: str):
        print(association)
        if self.config.get_association_config(association) is None:
            return False
        return True

    def validate_event(self, event):
        if (self.validate_email(event.email)
            and self.validate_type(event.type)
            and self.validate_nif_nie(event.nif_nie)
                and self.validate_association(event.association)):
            return True
        return False
