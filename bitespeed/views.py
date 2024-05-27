from rest_framework.decorators import api_view
from .serializers import ContactSeriazlizer
from rest_framework.response import Response
from rest_framework import status
from .services import ContactService

# Create your views here.
@api_view(['POST'])
def identify(request):
    serializer = ContactSeriazlizer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    instance = serializer.save()
    return Response(ContactService.get_all_connected_contacts(instance), status=status.HTTP_200_OK)


