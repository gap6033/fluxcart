from rest_framework import serializers
from .models import Contact

class ContactSeriazlizer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'phone']