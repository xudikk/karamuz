from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from core.models import Category
from .forms import CtgForm


def list(request):
    ctgs = Category.objects.all().order_by('-id')

    paginator = Paginator(ctgs, 3)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)

    ctx = {
        "status": "list",
        "ctgs": result,
        "page": int(page),
        "paginator": paginator
    }

    added = request.session.get("added", None)
    error = request.session.get("error", None)
    deleted = request.session.get("deleted", None)
    ctx['added'] = added
    ctx['error'] = error
    ctx['deleted'] = deleted
    try:
        del request.session['added']
    except: ...
    try:
        del request.session['error']
    except: ...
    try:
        del request.session['deleted']
    except: ...
    return render(request, "dashboard/ctg.html", ctx)


def add(request, pk=None):
    ctg = None
    if pk:
        ctg = Category.objects.filter(id=pk).first()
        if not ctg:
            request.session['error'] = "Bunaqa id lik kategoriya topilmadi!!"
            return redirect("ctg_list")

    if request.POST:
        form = CtgForm(request.POST, instance=ctg)
        if form.is_valid():
            form.save()
            request.session['added'] = True
        else:
            request.session['error'] = form.errors

    print("added", request.session.get('added'), "\n\nError:", request.session.get('error'))
    return redirect("ctg_list")


def delete(request, pk):
    try:
        ctg = Category.objects.filter(id=pk).first()
        request.session['deleted'] = f"{ctg.name} deleted successfully"
        ctg.delete()
    except: ...
    return redirect("ctg_list")















