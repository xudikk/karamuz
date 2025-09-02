from django.urls import path
from .views import *
from . import auth_views as auth

urlpatterns = [
    path("", index, name='home'),
    path("ctg/<slug>/", category, name='category'),
    path("contact/", contact, name='contact'),
    path("srch/", search, name='search'),
    path("view/<int:pk>/", view, name='view'),

    # auth
    path("registration/", auth.regis, name='regis'),
    path("login/", auth.login, name='login'),
    path("logot/", auth.logout, name='logout'),
    path("otp/", auth.step_one, name='step-one'),
]




