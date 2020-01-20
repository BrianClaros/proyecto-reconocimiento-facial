from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from datetime import timedelta

import smtplib
import os

class ServerEmail():



    def __init__(self, server,port,email,password):
        self.server = server
        self.port = port
        self.email = email
        self.password = password
        self.fromEmail = self.email
        self.to = ""
        self.subject = ""
        self.photo = ""
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

    def sendMsjImage(self,emailDestinatary,subject,photo):
        msg = MIMEMultipart()
        img_data = open(photo, 'rb').read()
        date = self.formatTime()
        msg.attach(MIMEText('Se ha reconocido el rostro de la persona que ingreso al lugar en la fecha '+date , 'plain'))
        image = MIMEImage(img_data, name=os.path.basename(photo))
        msg.attach(image)
        msg['From'] = self.fromEmail
        msg['To'] = emailDestinatary
        msg['Subject'] = subject
        self.server.sendmail(msg['From'], msg['To'], msg.as_string())

    def stopServerEmail(self):
        self.server.quit()

    def formatTime(self):
        date = datetime.now()
        months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        day = date.day
        month = months[date.month - 1]
        year = date.year
        hour = date.hour
        min = date.minute
        message = "{} de {} del {} a las {} horas con {} minutos".format(day, month, year, hour, min)

        return message
