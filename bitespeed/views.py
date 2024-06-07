from rest_framework.decorators import api_view
from .serializers import ContactSeriazlizer
from rest_framework.response import Response
from rest_framework import status
from .services import ContactService
from django.http import JsonResponse

# Create your views here.
@api_view(['GET', 'POST'])
def identify(request):
    if request.method == 'GET':
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            print(request.META)
            return JsonResponse({'error': 'Method Not Allowed'})
        else:
            return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = ContactSeriazlizer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    instance = serializer.save()
    return Response(ContactService.get_all_connected_contacts(instance), status=status.HTTP_200_OK)


