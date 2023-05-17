# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# create message object instance
msg = MIMEMultipart()

message = "Thank you 2ыфв"

# setup the parameters of the message
password = "Abyrvalg44!"
msg['From'] = "robot_sp@hotmail.com"
msg['To'] = "mikhaillapov@gmail.com"
msg['Subject'] = "Subscription 12134"

# add in the message body
msg.attach(MIMEText(message, 'plain'))

# create server
server = smtplib.SMTP('smtp-mail.outlook.com: 587')

server.starttls()

# Login Credentials for sending the mail
server.login(msg['From'], password)

# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())

server.quit()

print ("successfully sent email to %s:" % (msg['To']))

#
# def send_email(host, subject, to_addr, from_addr, password, body_text):
#     """
#     Send an email
#     """
#     print(f"0successfully sent email to {to_addr}: {body_text}")
#     BODY = "\r\n".join((
#         "From: %s" % from_addr,
#         "To: %s" % to_addr,
#         "Subject: %s" % subject,
#         "",
#         body_text
#     ))
#
#     print(f"1successfully sent email to {to_addr}: {body_text}")
#     server = smtplib.SMTP(host)
#     server.starttls()
#     server.login(from_addr, password)
#     print(f"2successfully sent email to {to_addr}: {body_text}")
#     server.sendmail(from_addr, to_addr, BODY)
#     print(f"3successfully sent email to {to_addr}: {body_text}")
#     server.quit()
#     print(f"4successfully sent email to {to_addr}: {body_text}")
#
# # конфигурируем почту
# if __name__ == "__main__":
#     host_email = "smtp-mail.outlook.com: 587"
#     subject_email = "Subscription1"
#     to_addr_email = "mikhaillapov@gmail.com"
#     from_addr_email = "robot_sp@hotmail.com"
#     password_email = "Abyrvalg44!"
#     body_text_email = "None_2"
#     send_email(host_email, subject_email, to_addr_email,from_addr_email, password_email, body_text_email)
#
