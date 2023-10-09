from rest_framework import serializers
from .models import Cancillaria, Supplier


class CancillariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancillaria
        fields = ['name', 'description', 'price', 'exist', 'supplier']
