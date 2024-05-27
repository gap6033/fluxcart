# Create your models here.
from django.db import models

# Create your models here.
class Contact(models.Model):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'

    CONTACT_TYPE = [
        (PRIMARY, 'primary'),
        (SECONDARY, 'secondary')
    ]

    email = models.EmailField(blank=True, null=True, db_index=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    linkedId = models.IntegerField(null=True)
    linkPrecedence = models.CharField(max_length=256, choices=CONTACT_TYPE, default=PRIMARY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now_add=True, null=True)