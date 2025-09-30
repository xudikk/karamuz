from rest_framework import serializers
from core.models import Category


class CtgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]



