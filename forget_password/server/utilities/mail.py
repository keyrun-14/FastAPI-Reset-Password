
import smtplib
from email.mime.text import MIMEText
from server.utilities import settings 


def send_mail(Email, mail_body):
    msg = MIMEText(mail_body)
    msg['Subject'] = 'OTP for password change'
    msg['From'] = settings.email
    msg['To'] = Email

    with smtplib.SMTP_SSL('smtp.gmail.com') as smtp: #Added Gmails SMTP Server
        smtp.login(settings.email, settings.password) #This command Login SMTP Library using your GMAIL
        #This Sends the message
        smtp.sendmail(settings.email,Email,msg.as_string())
        return msg