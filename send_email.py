import update_database
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME_SMTP = os.getenv('USERNAME_SMTP')
PASSWORD_SMTP = os.getenv('PASSWORD_SMTP')
SENDER = 'ethanbabelarbitragebetting@gmail.com'
SENDERNAME = "Ethan Babel Arbitrage Betting"

def send_arbs():
    smtp = smtplib.SMTP('email-smtp.us-west-1.amazonaws.com', 587) 
    smtp.ehlo() 
    smtp.starttls() 
    smtp.ehlo()
    smtp.login(USERNAME_SMTP, PASSWORD_SMTP) 

    subject = 'Arbing Opportunity'
    text = update_database.get_arbitrage()
    msg = MIMEMultipart()
    msg['Subject'] = subject 
    msg['From'] = formataddr((SENDERNAME, SENDER))
    msg.attach(MIMEText(text)) 
    to = ["babelethan@gmail.com"]
    smtp.sendmail(from_addr=SENDER, to_addrs=to, msg=msg.as_string())

    smtp.close()

def send_error(error: str):
    smtp = smtplib.SMTP('email-smtp.us-west-1.amazonaws.com', 587) 
    smtp.ehlo() 
    smtp.starttls() 
    smtp.ehlo()
    smtp.login(USERNAME_SMTP, PASSWORD_SMTP) 

    subject = 'ERROR'
    msg = MIMEMultipart()
    msg['Subject'] = subject 
    msg['From'] = formataddr((SENDERNAME, SENDER))
    msg.attach(MIMEText(error)) 
    to = ["babelethan@gmail.com"]
    smtp.sendmail(from_addr=SENDER, to_addrs=to, msg=msg.as_string())

    smtp.close()