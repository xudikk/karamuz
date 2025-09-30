from django.urls import path
from .services.ctg import CtgView
from .services.auth import LoginView, StepOne, StepTwo, ResendCode, RegisterView, LogoutView


urlpatterns = [
    path("ctg/", CtgView.as_view()),
    path("ctg/<int:pk>/", CtgView.as_view()),

    # auth
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("logout/", LogoutView.as_view()),

    path("step/one/", StepOne.as_view()),
    path("step/two/", StepTwo.as_view()),
    path("resent/code/", ResendCode.as_view()),

]







