from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class ServerEmail():
    def __init__(self, server,port,email,password):
        self.server = server
        self.port = port
        self.email = email
        self.password = password
        self.fromEmail = self.email
        self.to = ""
        self.subject = ""
        self.photos = ""
        self.server = smtplib.SMTP(self.server+':'+self.port)
        self.server.starttls()
        self.server.login(self.email,self.password)

    def setEmail(self,email,password):
        self.email = email
        self.password = password

    def sendMsj(self,emailDestinatary, subject):
        msg = MIMEMultipart()
        msg.attach(MIMEText('Se ha detectado que una persona ingreso al lugar', 'plain'))
        msg['From'] = self.fromEmail
        msg['To'] = emailDestinatary
        msg['Subject'] = subject
        self.server.sendmail(msg['From'], msg['To'], msg.as_string())

    def stopServerEmail(self):
        self.server.quit()