from rest_framework import serializers
from core.models import VumaRequest


class VumaRequestSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = VumaRequest
        fields = '__all__'
        read_only_fields = ('id','created_at', 'modified_at', 'user')
