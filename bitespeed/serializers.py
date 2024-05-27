from rest_framework import serializers
from .models import Contact
from .services import ContactService

class ContactSeriazlizer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'phoneNumber']

    def to_internal_value(self, data):
        data = {key: value.strip() if isinstance(value, str) else value for key, value in data.items()}
        return super().to_internal_value(data)

    def validate(self, attrs):
        email = attrs.get('email')
        phoneNumber = attrs.get('phoneNumber')
        if not email and not phoneNumber:
            raise serializers.ValidationError("Both email and phoneNumber cannot be missing/null as input")
        return attrs

    def create(self, validated_data):
        return ContactService.create_contact(validated_data)