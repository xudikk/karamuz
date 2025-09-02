# bu bizd global ctx lar jamlanmasi!!!
from core.models import Category, New


def valyuta():
    import requests
    # response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
    response = [
        {
            "Ccy": "USD",
            "Rate": 12591.71
        },
        {
            "Ccy": "RUB",
            "Rate": 160.18
        },
        {
            "Ccy": "EUR",
            "Rate": 14821.70
        },
    ]
    return response


def main(request):
    menu_ctgs = Category.objects.filter(is_menu=True)
    svejiy = New.objects.all().order_by("-created")

    return {
        "valyutalar": valyuta(),
        "menu_ctgs": menu_ctgs,
        "svejiy": svejiy
    }






