from rest_framework import serializers
from .models import Contact
from .services import ContactService

class ContactSeriazlizer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'phoneNumber']

    def validate(self, data):
        if not data['email'] and not data['phoneNumber']:
            raise serializers.ValidationError("At least email or phoneNumber has to be provided")
        return data

    def create(self, validated_data):
        return ContactService.create_contact(validated_data)