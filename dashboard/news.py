from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from core.models import New
from dashboard.forms import NewsForm


def list(request, pk=None):
    if pk:
        new = New.objects.filter(id=pk).first()
        if not new:
            request.session['error'] = "Bunaqa yangilik mavjud emas"
            return redirect("news-list")

        ctx = {
            "status": "profile",
            "new": new
        }
    else:
        news = New.objects.all().order_by('-pk')

        paginator = Paginator(news, 5)
        page = request.GET.get('page', 1)
        result = paginator.get_page(page)

        ctx = {
            "status": "list",
            "news": result,
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
        except:
            ...
        try:
            del request.session['error']
        except:
            ...
        try:
            del request.session['deleted']
        except:
            ...

    return render(request, "dashboard/news.html", ctx)


def form(request, pk=None):    # edit va add
    obj = None
    if pk:
        obj = New.objects.filter(pk=pk).first()

    form = NewsForm(request.POST or None, request.FILES or None, instance=obj)
    if request.POST and form.is_valid():
        print("\n\nshu yerga keldi. form valittt")
        form.save()
        request.session['added'] = "Yangilik Muaffaqiyatli qo'shildi"
        return redirect("news-list")
    print("\n\nform validmas", form.errors)
    ctx = {
        "obj": obj,
        "form": form,
        "status": "form"
    }
    return render(request, "dashboard/news.html", ctx)


def delete(request, pk):
    try:
        obj = New.objects.filter(id=pk).first()
        request.session['deleted'] = f"{obj.title} deleted successfully"
        obj.delete()
    except:
        ...
    return redirect("news-list")
