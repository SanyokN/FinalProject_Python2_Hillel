from utils.email_sender import create_welcome_letter, send_email


def confirm_registration(created_user, base_url):
    email_body = create_welcome_letter(
        {
            'name': created_user.name,
            'surname': created_user.surname,
            'link': f'{base_url}api/users/verify/{created_user.user_uuid}'
        }
    )
    send_email([created_user.email], mail_body=email_body, mail_subject='Verification')
