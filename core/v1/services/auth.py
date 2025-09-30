import uuid

from methodism import generate_key, code_decoder
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from base.helper import BearerAuth
from core.auth_models import User, Otp
from rest_framework.status import HTTP_400_BAD_REQUEST
import random
# GenericAPIView -> model kerak bo'lsa
# APIView -> model muhim rol o'ynamaganida
import requests

# bular settingsga qo'shib qo'yiladi!!!!
bot_token = "1998469854:AAE8DgBdtWguqGOas0BKOB8qlYQgk8sF1vw"
user_id = 727652365


class StepOne(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile = request.data.get("phone")
        if not mobile:
            return Response({"error": "Phone required"}, status=HTTP_400_BAD_REQUEST)
        # if  len(mobile) != 12:
        #     return Response()

        code = random.randint(100_000, 999_999)  # hech kim bilmasligi kerak!!
        # shu yerda srzi sms bo'p chiqib ketadi
        message = f"Otp kod: {code}\n bu kodni hech kimga bermang"
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={user_id}&text={message}&parse_mode=HTML'
        requests.get(url)
        # davom etadi

        token = f"{uuid.uuid4()}&{code}&{generate_key(20)}"
        shifr = code_decoder(token, l=3)

        otp = Otp.objects.create(key=shifr, mobile=mobile)

        return Response({
            "otp_token": otp.key
        })


class ResendCode(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        token = request.data.get("token")

        if None in [phone, token]:
            return Response({"error": "phone and token required"}, status=400)

        otp = Otp.objects.filter(key=token).first()
        if not otp:
            return Response({"error": "Wrong Token"}, status=400)

        if otp.mobile != phone:
            return Response({"error": "wrong phone number"}, status=400)

        if otp.is_expired or otp.is_confirmed:
            return Response({"error": "unusable token"}, status=400)
        otp.is_expired = True
        otp.save()

        # token deshifr
        shifr = code_decoder(token, l=3, decode=True).split("&")[1]
        message = f"Otp kod: {shifr}\n bu kodni hech kimga bermang"
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={user_id}&text={message}&parse_mode=HTML'
        requests.get(url)

        token = code_decoder(f"{generate_key(20)}&{shifr}&{uuid.uuid4()}", l=3)
        otp = Otp.objects.create(key=token, mobile=phone)
        return Response({
            "otp_token": otp.key
        })


class StepTwo(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if "otp" not in request.data or "otp_token" not in request.data:
            return Response({"error": "Ma'lumotlar to'lliq emas!"}, status=HTTP_400_BAD_REQUEST)
        token = Otp.objects.filter(key=request.data['otp_token']).first()
        if not token:
            return Response({"error": "Bunday token mavjud emas!"}, status=HTTP_400_BAD_REQUEST)

        if token.is_expired or token.is_confirmed:
            return Response({"error": "Token eskirkan!"}, status=HTTP_400_BAD_REQUEST)

        if not token.check_time():
            token.is_expired = True
            token.save()
            return Response({"error": "Token Uchun ajratilgan vaqt tugadi"})

        shifr = code_decoder(request.data['otp_token'], l=3, decode=True).split("&")[1]
        if str(shifr) != str(request.data['otp']):
            token.tries += 1
            token.save()
            return Response({"error": f"Xato Kod. {3 - token.tries} ta urunish qoldi"})

        token.is_confirmed = True
        token.is_expired = True
        token.save()

        user = User.objects.filter(phone=token.mobile).first()  # None
        return Response({
            "is_registered": user is not None
        })


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if "phone" not in data or "password" not in data:
            return Response({"error": "Ma'lumotlar to'lliq emas!"})

        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            return Response({"error": "User or Password incorrect"})

        if not user.check_password(str(data['password'])):
            return Response({"error": "User or Password incorrect"})

        token = Token.objects.get_or_create(user=user)

        return Response({
            "access_token": token[0].key
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        password = request.data.get("password")
        username = request.data.get("username")
        if None in [username, password, token]:
            return Response({"error": "password, token, username are required"})

        otp = Otp.objects.filter(key=token).first()
        if not otp:
            return Response({"error": "Bunday token mavjud emas!"}, status=HTTP_400_BAD_REQUEST)

        if not otp.is_confirmed:
            return Response({"error": "Ishonchsiz token"})

        user = User.objects.create_user(
            phone=otp.mobile,
            password=password,
            fullname=request.data.get("full_name"),
            username=request.data.get("username")
        )
        access_token = Token.objects.create(user=user)

        return Response({
            "access_token": access_token.key
           })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerAuth]

    def post(self, request):
        try:
            Token.objects.get(user=request.user).delete()
        except: ...
        return Response({"success": "User Logged out"})







