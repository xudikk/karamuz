import random

import requests
from django.conf import settings
from django.contrib.auth import login as lin, logout as lout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from core.auth_models import User, Otp
from base.helper import generate_key, code_decoder

def regis(request):
    ctx = {}
    if request.POST:
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        pas = request.POST.get('pass')
        pas_c = request.POST.get('pass_conf')

        if None in [username, pas, pas_c, phone]:
            ctx['error'] = "TO'ldir"
            return render(request, "auth/register.html", ctx)

        # shu yerda password tuzulishi uzunligi yoki nimadirlarni tekshirish mumkin!

        if pas != pas_c:
            ctx['error'] = "Parollarni bir xil qil"
            return render(request, "auth/register.html", ctx)

        user = User.objects.filter(Q(username=username) | Q(phone=phone)).first()
        if user:
            ctx['error'] = "username yoki phone allaqachon ro'yxatdan o'tgan!"
            return render(request, "auth/register.html", ctx)

        # ertaga shu yerda OTP tekshiramizz
        code = random.randint(100_000, 999_999)
        message = f"OTP code: {code}"
        url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={727652365}&text={message}"
        requests.get(url)


        # shu yerda sms bo'p chiqib ketadi!
        shifr = f"{generate_key(25)}&{code}&{generate_key(25)}"
        total = code_decoder(shifr, l=2)

        otp = Otp.objects.create(
            key=total,
            mobile=phone,
            next_step='regis',
            extra_fields={
                "username": username,
                "password": pas,
                "phone": phone
            }
        )
        request.session['otp_token'] = otp.key

        return redirect('step-one')

    return render(request, "auth/register.html")


def login(request):
    ctx = {}
    if request.POST:
        phone = request.POST.get('phone')
        pas = request.POST.get('pass')
        if None in [pas, phone]:
            ctx['error'] = "TO'ldir"
            return render(request, "auth/login.html")

        user = User.objects.filter(phone=phone).first()
        if not user:
            ctx['error'] = "parol yoki phone xato!"
            return render(request, "auth/login.html")

        if not user.check_password(str(pas)):
            ctx['error'] = "parol yoki phone xato!"
            return render(request, "auth/login.html")

        # shu yerdaa otp tekshiramizz!!!
        lin(request, user)
        return redirect("home")

    return render(request, "auth/login.html")


@login_required(login_url='login')
def logout(request):
    lout(request)
    return redirect('login')


def step_one(request):
    if not request.session.get("otp_token"):
        return redirect('login')

    if request.POST:
        otp = ""
        for i in request.POST:
            if "otp" in i:
                otp += request.POST[i]
        token = request.session['otp_token']
        original = Otp.objects.filter(key=token).first()
        if not original:
            try:
                del request.session['otp_token']
            except: pass
            return redirect('login')

        if original.is_expired or original.is_confirmed:
            ctx = {
                "error": "Token Allaqachon eskirgan"
            }
            render(request, 'auth/otp.html', ctx)
        if not original.check_time():
            original.is_expired = True
            original.save()
            ctx = {"error": "Tokenga ajratilgan vaqt tugadi"}
            return render(request, 'auth/otp.html', ctx)

        # shifrdan ochish
        shifr = code_decoder(original.key, decode=True, l=2)
        original_otp = shifr.split("&")[1]
        if str(otp) != str(original_otp):
            original.tries += 1
            original.save()
            ctx = {"error": "Xato Kod"}
            return render(request, 'auth/otp.html', ctx)

        try:
            del request.session['otp_token']
        except: pass
        original.is_confirmed = True
        original.is_expired = True
        original.save()

        if original.next_step == 'regis':
            user = User.objects.create_user(**original.extra_fields)
            lin(request, user)
            authenticate(request)

            return redirect("home")
        elif original.next_step == 'login':
            user = User.objects.get(id=int(original.extra_fields['user_id']))
            lin(request, user)
            return redirect("home")
        else:
            ctx = {"error": "nimadir xato"}
            return redirect("login")


    return render(request, 'auth/otp.html', )