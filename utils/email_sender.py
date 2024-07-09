import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2

import config


def send_email(
    recipients: list[str],
    *,
    mail_body: str,
    mail_subject: str,
    attachment: str = None,
) -> None:
    TOKEN_API = config.TOKEN_API
    USER = config.EMAIL_USER
    SMTP_SERVER = config.SMTP_SERVER

    msg = MIMEMultipart("alternative")
    msg["Subject"] = mail_subject
    msg["From"] = f"{USER} sent this email"
    msg["To"] = ", ".join(recipients)
    msg["Reply-To"] = USER
    msg["Return-Path"] = USER
    msg["X-Mailer"] = "decorator"

    if attachment:
        is_file_exists = os.path.exists(attachment)
        if not is_file_exists:
            print(f'file {attachment} doesn`t exist')
            raise ValueError(f'file {attachment} doesn`t exist')
        else:
            basename = os.path.basename(attachment)
            filesize = os.path.getsize(attachment)
            file = MIMEBase('application', f'octet-stream; name={basename}')
            file.set_payload(open(attachment, 'rb').read())
            file.add_header('Content-Description', attachment)
            file.add_header('Content-Description', f'attachment; filename={attachment}; size={filesize}')
            encoders.encode_base64(file)
            msg.attach(file)

    text_to_send = MIMEText(mail_body, "html")
    msg.attach(text_to_send)

    mail = smtplib.SMTP_SSL(SMTP_SERVER)
    mail.login(USER, TOKEN_API)
    mail.sendmail(USER, recipients, msg.as_string())
    mail.quit()


def create_welcome_letter(params: dict) -> str:
    template_loader = jinja2.FileSystemLoader(searchpath='./')
    template_env = jinja2.Environment(loader=template_loader)
    template_file = 'templates/welcome_letter.html'
    template = template_env.get_template(template_file)
    output = template.render(params)
    return output
