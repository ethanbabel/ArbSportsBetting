import update_database
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import smtplib

USERNAME_SMTP = 'AKIA3FLDXAQIIB6TPL7G'
PASSWORD_SMTP = 'BHXSEcbqlokVc73A5qx4HdUuyQGr8XI6XTNl/nQpozsr'
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


if __name__ == "__main__":
    send_arbs()