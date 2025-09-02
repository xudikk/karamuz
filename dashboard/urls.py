from django.urls import path
from . import views
from . import category as ctg, news



urlpatterns = [
    path("", views.index, name='dashboard-home'),

    # crud: ctg
    path("ctg/list/", ctg.list, name='ctg_list'),
    path("ctg/add/", ctg.add, name='ctg_add'),
    path("ctg/edit/<int:pk>/", ctg.add, name='ctg_edit'),
    path("ctg/delete/<int:pk>/", ctg.delete, name='ctg_del'),

    # crud: news
    path("news/list/", news.list, name='news-list'),
    path("news/info/<int:pk>/", news.list, name='news-info'),
    path("news/delete/<int:pk>/", news.delete, name='news-delete'),
    path("news/add/", news.form, name='news-add'),
    path("news/edit/<int:pk>/", news.form, name='news-edit'),




]




