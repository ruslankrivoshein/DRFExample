from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)

from account.api.serializers import RegistrationSerializer
from account.models import Account
from rest_framework.authtoken.models import Token


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    if request.method == 'POST':
        data = {}
        phone = request.data.get('phone', '0')
        if validate_phone(phone) is not None:
            data['error_message'] = 'The phone is already in use'

            return Response(data)

        username = request.data.get('username', '0')
        if validate_username(username) is not None:
            data['error_message'] = 'The username is already in use'

            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            data['phone'] = account.phone
            data['username'] = account.username
            data['pk'] = account.pk
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors

        return Response(data)


def validate_phone(phone):
    account = None
    try:
        account = Account.objects.get(phone=phone)
    except Account.DoesNotExist:
        return None
    if account is not None:
        return phone


def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account is not None:
        return username


class GetAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        phone = request.POST.get('phone')
        password = request.POST.get('password')
        account = authenticate(phone=phone, password=password)

        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['token'] = token.key
        else:
            context['error_message'] = 'Invalid credentials'

        return Response(context)
