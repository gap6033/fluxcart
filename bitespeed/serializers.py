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

    def validate(self, data):
        if not 'email' in data or not 'phoneNumber' in data:
            raise serializers.ValidationError("email and/or phoneNumber missing as input")
        if not data['email'] and not data['phoneNumber']:
            raise serializers.ValidationError("Both email and phoneNumber values cannot be empty")
        return data

    def create(self, validated_data):
        return ContactService.create_contact(validated_data)