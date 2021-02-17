import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
class SendMail:
    def __init__(self, m='phill81@bk.ru', s='тест', b='тестовое письмо'):
        email_send = m  #'www.phill.999@gmail.com'
        subject = s  #'testing letter'
        body = b  # 'привет, мое первое тестовое письмо'

    #Настройки аккаунта сервера рассылки
        email_user = 'phill81@bk.ru'
        email_password = 'alskdj1379'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        #вложение
        # filename = 'README.md'
        # attachment = open(filename, 'rb')

        # part = MIMEBase('application', 'octet-stream')
        # part.set_payload((attachment).read())
        # encoders.encode_base64(part)
        # part.add_header('Content-Disposition', "attachment; filename= "+filename)
        # msg.attach(part)

        text = msg.as_string()
        try:
            # server = smtplib.SMTP('smtp.mail.ru', 465)
            server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
            # server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()
        except BaseException as e:
            print(e)


