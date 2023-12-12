from django.core.mail import send_mail


def send_code_to_email(code: str, recipient_list: list[str]):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код: {code}',
        from_email='from@example.com',
        recipient_list=recipient_list,
        fail_silently=False,
    )
