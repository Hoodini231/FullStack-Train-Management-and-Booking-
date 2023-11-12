import re
import dns.resolver
from email.message import EmailMessage
import ssl
import smtplib

class Email:
    def __init__(self, email_name):
        self.name = email_name
        self.get_email_provider()

    def get_email_provider(self):
        try:
            temp = self.name.split("@")
            self.email_provider = temp[1]
            print(self.email_provider)
        except:
            self.email_provider = ""

    def check_valid_syntax(self):
        try:
            match = re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", self.name)
            if match == None:
                return False
            return True
        except:
            return False

    def check_valid_address(self):
        try:
            records = dns.resolver.resolve(self.email_provider, 'MX')
            return True
        except:
            return False

class Send_Email:
    def __init__(self, email_name, subject_name, bodytext):
        reciever = email_name
        sender = "INSERTCOMPANYEMAIL@gmail.com"
        pswd = "PASSWORD"
        em = EmailMessage()
        em['From'] = sender
        em['To'] = reciever
        em['Subject'] = subject_name
        em.set_content(bodytext)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
            smtp.login(sender, pswd)
            smtp.sendmail(sender, reciever, em.as_string())






