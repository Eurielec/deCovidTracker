"""
Class for sending emails with a CSV attachment.
"""

import os

# Import smtplib for the actual sending function
import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:

    def __init__(self):
        """
        Create an instance of class Email.
        """
        self.user = os.environ.get("EMAIL_USER")
        self.password = os.environ.get("EMAIL_PASSWORD")
        self.support = os.environ.get("SUPPORT_EMAIL")
        self.smtp_host = os.environ.get("SMTP_HOST")
        self.smtp_port = os.environ.get("SMTP_PORT")

    def send_email(self, to: str, association_name: str, csv: str):
        """
        Send email.

        Arguments:
            - to (str): email address to send the email to.
            - association_name (str): name of the association for the email.
            - csv (str): file to attach to the email.
        """

        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = '[%s] Trazabilidad mensual' % (association_name)
        msg['From'] = self.user
        msg['To'] = to
        body = """
            Este es un correo automático. Por favor contacte con %s para
            cualquier problema.

            El código de este programa puede consultarse en
            https://github.com/Eurielec/deCovidTracker-backend .
               """ % self.support
        msg.attach(MIMEText(body, 'plain'))
        attachment = MIMEText(csv, _subtype="csv")
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename="%s.csv" % association_name)
        msg.attach(attachment)

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP_SSL(
                "%s:%s" % (self.smtp_host, self.smtp_port))
            print("Attempting mail send", self.smtp_host, self.smtp_port)
            # server.connect(self.smtp_host, int(self.smtp_port))
            print("B")
            # server.starttls()
            # server.ehlo()
            print("Attempting login", self.user, self.password)
            server.login(self.user, self.password)
            print("Attempting send", self.user, to, msg.as_string())
            server.sendmail(self.user, to, msg.as_string())
            # TODO: Send email here
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            try:
                server.quit()
            except Exception:
                print("Server wasnt created")
