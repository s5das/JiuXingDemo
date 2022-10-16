# from util.scheduleTask import MailSender
import os
import sys
import threading

import yagmail


class MailSender:
    def __init__(self, mail_name, mail_password, mail_host, mail_port, receiver):
        self.mail_name = mail_name
        self.mail_password = mail_password
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.receiver = receiver

    def send(self, receiver, subject, content):
        yag = yagmail.SMTP(user=self.mail_name, password=self.mail_password, host=self.mail_host, port=self.mail_port)
        yag.send(to=receiver, subject=subject, contents=content)

    def sendAsync(self, receiver, subject, content):
        t = threading.Thread(target=self.send, args=(receiver, subject, content))
        t.start()
        self.create_task()

    def create_task(self):
        subject = "日志"
        with open("logfile.log", "r") as f:
            content = f.readlines()[-5:]
        t = threading.Timer(1, self.sendAsync, [self.receiver, subject, content])
        t.start()


sys.path.append("../..")

if os.getenv("MAIL_NAME"):
    mail_name = os.getenv("MAIL_NAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_host = os.getenv("MAIL_HOST")
    mail_port = os.getenv("MAIL_PORT")
    receiver = os.getenv("MAIL_RECEIVER")
    mailSender = MailSender(mail_name, mail_password, mail_host, mail_port, receiver)
    mailSender.create_task()

    mailSender.sendAsync(mailSender.receiver, "test", "test")
