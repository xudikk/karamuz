from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url='login')
def index(request):
    if not request.user.is_staff or not request.user.is_superuser or request.user.user_type != 2:
        return redirect("home")

    return render(request, "dashboard/index.html")



