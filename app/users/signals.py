from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args,
                                 **kwargs):
    message = f"Hi,\n\tSomeone requested a new password for your account. " \
              f"If You didn't make this request then you can safely ignore " \
              f"this. \n\tOtherwise you can reset password using following " \
              f"link \n\t{settings.PASSWORD_RESET_URL}/reset-password/?" \
              f"token={reset_password_token.key}\n\tThanks"
    send_mail(
        "Password Reset for {title}".format(
            title="Shopping Insight Technology"),
        message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )
