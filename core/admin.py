import datetime

from django.contrib import admin
from .models import Category, New, Comment, Contact, Subscribe, User


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "is_menu"]
    list_display_links = ["name"]
    search_fields = ["name", "slug"]


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ["show_title", "ctg", "view", "qoshilgan", "ozgargan"]
    ordering = ["view"]
    search_fields = ["title", "description"]
    list_filter = ["view", "created"]
    # list_editable = ["ctg"]
    readonly_fields = ["view", "updated", "created"]

    @admin.display
    def show_title(self, obj):
        return " ".join(obj.title.split()[:3])
    show_title.short_description = "Yangilik"

    @admin.display
    def qoshilgan(self, obj):
        now = datetime.datetime.now()
        if now.date() == obj.created.date():
            if (now - obj.created).total_seconds() <= 3600:
                return f"{int((now - obj.created).total_seconds() // 60)} minut oldin"

            return obj.created.strftime("%H:%M:%S")

        return obj.created.strftime("%d %B %Y")

    @admin.display
    def ozgargan(self, obj):
        now = datetime.datetime.now()
        if now.date() == obj.updated.date():
            if (now - obj.updated).total_seconds() <= 3600:
                return f"{int((now - obj.updated).total_seconds() // 60)} minut oldin"

            return obj.updated.strftime("%H:%M:%S")

        return obj.updated.strftime("%d %B %Y")


admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Subscribe)
admin.site.register(User)
