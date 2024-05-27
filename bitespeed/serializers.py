from rest_framework import serializers
from .models import Contact
from .services import ContactService

class ContactSeriazlizer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'phoneNumber']

    def create(self, validated_data):
        return ContactService.create_contact(validated_data)