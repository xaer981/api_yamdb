from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def create_code_and_send_email(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Добро пожаловать на проект YaMDb!',
        from_email='e-mail.com',
        recipient_list=(user.email,),
        message=confirmation_code,
        fail_silently=False
    )
