from django.core.mail import send_mail
from django.conf import settings
import threading


def send_email_async(subject, message, reciptient_list):
    def send():
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            reciptient_list,
            fail_silently=False,
        )
    threading.Thread(target=send).start()
    
    
    
    
    