import datetime

from django.db import models

# Create your models here.
from django.utils.text import slugify
from .auth_models import User


class Category(models.Model):
    name = models.CharField(max_length=56)
    slug = models.SlugField(max_length=56, null=True, blank=True, unique=True)
    is_menu = models.BooleanField(default=False)

    def response(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "is_menu": self.get_is_menu()
        }

    def get_is_menu(self):
        return "Menuda Chiqadi✅" if self.is_menu else "Menuda Chiqmaydi ❌"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class New(models.Model):
    title = models.CharField(max_length=256)

    short_desc = models.TextField()
    description = models.TextField()

    image1 = models.ImageField(upload_to="news")
    image2 = models.ImageField(upload_to="news", null=True, blank=True)

    view = models.PositiveIntegerField(default=0, editable=False)
    tags = models.CharField(max_length=128)

    ctg = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if "#" not in self.tags:
            self.tags = "#" + "#".join(self.tags.lower().split())

        return super(New, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_tags(self):
        return self.tags.lstrip("#").split("#")

    def get_full_desc(self):
        return self.description.split("\n")

    def get_date(self):
        obj = self
        now = datetime.datetime.now()
        if now.date() == obj.created.date():
            if (now - obj.created).total_seconds() <= 3600:
                return f"{int((now - obj.created).total_seconds() // 60)} minut oldin"

            return obj.created.strftime("%H:%M:%S")

        return obj.created.strftime("%d %B %Y")

    def get_date_up(self):
        obj = self
        now = datetime.datetime.now()
        if now.date() == obj.updated.date():
            if (now - obj.updated).total_seconds() <= 3600:
                return f"{int((now - obj.updated).total_seconds() // 60)} minut oldin"

            return obj.updated.strftime("%H:%M:%S")

        return obj.updated.strftime("%d %B %Y")


    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "1. Yangiliklar"


class Subscribe(models.Model):
    email = models.EmailField(unique=True, primary_key=True)
    is_trash = models.BooleanField(default=False)


class Contact(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    is_trash = models.BooleanField(default=False)


class Comment(models.Model):
    sub_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='subs')
    user = models.CharField(max_length=128)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name='comments')
    is_sub = models.BooleanField(default=False)

    def get_date(self):
        obj = self
        now = datetime.datetime.now()
        if now.date() == obj.date.date():
            if (now - obj.date).total_seconds() <= 3600:

                calc = int((now - obj.date).total_seconds() // 60)
                return "Hozir" if calc == 0 else  f"{calc} minut oldin"

            return obj.date.strftime("%H:%M:%S")

        return obj.date.strftime("%d %B %Y")






