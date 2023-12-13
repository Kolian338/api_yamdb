from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def send_code_to_email(code: str, recipient_list: list[str]):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код: {code}',
        from_email='from@example.com',
        recipient_list=recipient_list,
        fail_silently=False,
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
