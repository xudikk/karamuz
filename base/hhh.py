from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [

    ],
}








schema_view = get_schema_view(
    openapi.Info(
        title="Books API",
        default_version='v1',
        description="Kitoblar uchun oddiy REST API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



# path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
# path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),






# @swagger_auto_schema(operation_description="Barcha kitoblarni ro'yxatlash yoki yangi kitob qo'shish")




