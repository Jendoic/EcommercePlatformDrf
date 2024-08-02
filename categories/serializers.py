from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = "__all__"
        
    def get_detail_url(self, obj):
        return obj.get_absolute_url()