from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .models import Category, New, Comment
import random


# Create your views here.


def index(request):
    news = New.objects.all().order_by("-created")

    random_news = [news[random.randint(0, len(news) - 1)], news[random.randint(0, len(news) - 1)]]
    most_viewed = news.order_by("-view")
    ctx = {
        "news": news,
        "random_news": random_news,
        "most_viewed": most_viewed
    }
    return render(request, "site/index.html", ctx)


def category(request, slug):
    ctx = {}
    ctg = Category.objects.filter(slug=slug).first()
    if not ctg:
        ctx['error'] = 404
        ctx['error_content'] = "Bunaqa Categoriya Mavjud emas"

    news = New.objects.filter(ctg=ctg)
    if not news:
        ctx['error'] = 404
        ctx['error_content'] = "Bu Categoryga Oid Yangilik Mavjud emas"
    ctx['ctg'] = ctg
    ctx['news'] = news

    return render(request, "site/category.html", ctx)


def contact(request):
    ctx = {

    }
    return render(request, "site/contact.html", ctx)


def view(request, pk):
    new = New.objects.filter(pk=pk).first()
    if not new:
        return render(request, "site/view.html", {"error": 404})

    if request.POST:
        sub = request.POST.get('sub', None)

        Comment.objects.create(
            user=request.POST['user'],
            message=request.POST['message'],
            new_id=new.id,
            sub_comment_id=sub,
            is_sub=bool(sub)
        )

        return redirect('view', pk=pk)

    new.view += 1
    new.save()
    comments = Comment.objects.filter(new=new, is_sub=False).order_by('-date')

    ctx = {
        "new": new,
        "comment_cnt": len(comments),
        "comments": comments,
    }
    return render(request, "site/view.html", ctx)


def search(request):
    key = request.GET.get('search', None)
    if not key:
        return redirect("home")

    filterlar = New.objects.filter(Q(title__icontains=key) | Q(description__icontains=key) |
                                   Q(short_desc__icontains=key) | Q(ctg__name__icontains=key))

    paginator = Paginator(filterlar, settings.LIST_PER_PAGE)
    page = request.GET.get("page", 1)
    result = paginator.get_page(page)

    ctx = {
        'key': key,
        "cnt": len(filterlar),
        "result": result,
        "paginator": paginator,
        "page": int(page)
    }
    return render(request, "site/search.html", ctx)
