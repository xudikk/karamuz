from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from base.helper import BearerAuth
from core.models import Category
from core.v1.serializers import CtgSerializer


class CtgView(GenericAPIView):
    """
    Bu class Categoriya uchun CRUD sistemasining classi
    """
    permission_classes = [IsAuthenticated]   # Shu api ishlatishga dostup
    serializer_class = CtgSerializer
    authentication_classes = [BearerAuth]

    def get_object(self, pk):
        obj = Category.objects.filter(id=pk).first()
        if not obj:
            raise Http404("Bunday categoriyaa Yo'q!")
        return obj

    @swagger_auto_schema(operation_description="Bu barcha ctglar listini oberadi")
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            obj = self.get_object(pk)
            natija = obj.response()
        else:
            ctg = Category.objects.all()   # QuerySet |  dict va list
            natija = [x.response() for x in ctg]

        return Response({
            "natija": natija
        })

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        ctx = {
            "result": serializer.data
        }
        return Response(ctx, status=HTTP_201_CREATED)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer_class(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"result": serializer.data})

    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"result": serializer.data})

    def delete(self, request, pk):
        self.get_object(pk=pk).delete()
        return Response({"result": "Deleted Successfully"}, status=HTTP_200_OK)


class CategoriyaView(ListCreateAPIView):
    """
       Bunisi bo'lsa prosta
    """
    permission_classes = (AllowAny, )
    serializer_class = CtgSerializer
    queryset = Category.objects.all()
