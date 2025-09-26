import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailHelper:
    def __init__(self):
        self.host = os.environ["SMTP_HOST"]
        self.port = os.environ["SMTP_PORT"]
        self.sender = os.environ["SMTP_USER"]
        self.app_pass = os.environ['SMTP_PASSWORD']
        self.context = ssl.create_default_context()

    def verification_email(self, target, code):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Code de vérification"
        message["From"] = self.sender
        message["To"] = target

        html = """\
        <html>
          <body>
            <span style="font-weight: bold;">{code}</span>
            </p>
          </body>
        </html>
        """
        html = html.format(code=code)
        self.send_mail(html, message, target)

    def send_mail(self, html, message, target):
        message.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL(self.host, self.port, context=self.context) as server:
            server.login(self.sender, self.app_pass)
            server.sendmail(self.sender, target, message.as_string())


