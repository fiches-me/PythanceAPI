import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailHelper:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST")
        self.port = os.getenv("SMTP_PORT")
        self.sender = os.getenv("SMTP_USER")
        self.app_pass = os.getenv("SMTP_PASSWORD")

        # dev mode if any SMTP variable is missing
        self.dev_mode = not all([self.host, self.port, self.sender, self.app_pass])

        if self.dev_mode:
            print("[MailHelper] SMTP variables not defined → DEV MODE enabled (emails will be printed)")
        else:
            self.context = ssl.create_default_context()

    def verification_email(self, target, code):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Code de vérification"
        message["From"] = self.sender or "dev@localhost"
        message["To"] = target

        html = """\
        <html>
          <body>
            <p>Votre code :</p>
            <span style="font-weight: bold;">{code}</span>
          </body>
        </html>
        """.format(code=code)

        self.send_mail(html, message, target)

    def send_mail(self, html, message, target):
        message.attach(MIMEText(html, "html"))

        if self.dev_mode:
            print("📧 DEV EMAIL")
            print("To:", target)
            print("Subject:", message["Subject"])
            print("Body:")
            print(html)
            print("-" * 40)
            return

        with smtplib.SMTP_SSL(self.host, int(self.port), context=self.context) as server:
            server.login(self.sender, self.app_pass)
            server.sendmail(self.sender, target, message.as_string())
