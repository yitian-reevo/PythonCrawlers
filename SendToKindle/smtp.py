# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
 
def SendToKindle(mail_host, mail_user, mail_pass, receiver, fullpath, bookname):
    message = MIMEMultipart()
    message['From'] = Header("SentToKindle", 'utf-8')
    message['To'] =  receiver 
    message['Subject'] = Header('convert')

    att = MIMEText(open(fullpath, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=%s' % bookname
    message.attach(att)

    smtpObj = smtplib.SMTP(mail_host, 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(mail_user, [receiver], message.as_string())
    smtpObj.quit()

# Test
# SendToKindle("smtp.gmail.com", "huangyitian1105@gmail.com", "hyt901105",  'wfgydbu@163.com', 'C:\Users\ethan\Desktop\ui.py', 'ui.py')
