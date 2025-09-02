# Signal -> Bu Djangodagi modellarmi kuzatib turuvchi va uni o'zgartirishlari haqida habar beruvchi funksiya
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Comment, New, Subscribe


@receiver(post_save, sender=Comment)
def my_signal(sender, instance, created, **kwargs):
    if created:
        TOKEN = settings.TG_TOKEN
        users = [727652365, 2041703880, 7700273816, 5826168637, 660749508, 5654839817]
        for i in users:
            message = f"REKLAMA: Karochi, \nYangi comment: {instance.message}\nKimdan: " \
                      f"{instance.user}\nYangilik: {instance.new.title}"
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={i}&text={message}"
            requests.get(url)
        print("\n\n\nHammasi tugadi Signal ishi bo'ldi \n\n")


@receiver(post_save, sender=New)
def new_signals(sender, instance: New, created, **kwargs):
    if created:
        message = f"Yangilik: {instance.title}\nDescription: {instance.short_desc}"
        # message = f"REKLAMA: Karochi, \nYangi comment: {instance.message}\nKimdan: " \
        #               f"{instance.user}\nYangilik: {instance.new.title}"
        subs = [x.email for x in Subscribe.objects.filter(is_trash=False)]
        try:
            # subs = ['work.akcaunt@gmail.com', "saidvaleyvabdulaziz@gmail.com"]
            send_mail("Saytda Yangi Yangilik Qo'shildi", message, settings.EMAIL_HOST_USER, subs)
        except:
            pass






