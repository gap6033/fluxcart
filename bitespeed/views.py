from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import ContactSeriazlizer

# Create your views here.
@api_view(['POST'])
def identify(request):
    pass
