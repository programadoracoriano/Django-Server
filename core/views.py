from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth.models import User
from .models import *
from .serializers import *
import stripe
from decimal import Decimal
from django.conf import settings
# Create your views here.




@api_view(['POST'])
@authentication_classes([])
def Signup(request):
    if request.method == 'POST':
        msg = {}
        username = request.data['username']
        email    = request.data['email']
        password = request.data['password']
        getUsers = User.objects.filter(username=username)
        getEmail = User.objects.filter(email=email)
        if getUsers.count() > 0:
            msg = {'msg':'Utilizador já existe. Por favor escolhe outro nome de utilizador.', 'success':False}
        elif getEmail.count() > 0:
            msg = {'msg':'E-mail já está registrado. Por favor, escolhe outro e-mail.', 'success':False}
        elif ' ' in username == True:
            msg = {'msg': 'O nome de utilizador não pode conter espaços.', 'success': False}
        elif len(username) < 6 or len(username)> 20:
            msg = {'msg': 'The username needs to have 6 to 20 characters.', 'success':False}
        elif len(password) < 8 or len(password)>16:
            msg = {'msg': 'Your password need to have 8 to 16 characters.', 'success':False}
        else:
            qs = User.objects.create_user(username=username, email=email, password=password,
            last_login=timezone.now())
            msg = {'msg': 'User created successfully!', 'success':True}
        return Response(msg)
@api_view(['POST'])
@authentication_classes([])
def login(request):            # <-- And here
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        content = {}
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            content = {'token': str(token[0]), 'msg':'Succesfully logged in.', 'success':True}
        else:
            content = {'msg':'Username or password are incorrect.', 'success':False}
        return Response(content)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def getUserData(request):
    if request.method == 'GET':
        qs          = Profile.objects.get(user=request.user)
        serializer  = ProfileSerializer(qs, many=False)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def secret(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET
        res         = {}
        qs          = Profile.objects.get(user=request.user)
        try:
            amount      = float(request.data['amount'])
            if amount > 5:
                res = {"msg": "O valor minimo é 5€.", "success": False}
            else:
                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency="eur",
                    automatic_payment_methods={"enabled": True}, )
                amount += qs.funds
                qs.funds(amount)
                qs.save()
                serializer = ProfileSerializer(qs, many=False)
                res = {"msg": serializer.data, "success": False, "client_secret": intent.client_secret}
        except:
            res = {"msg":"Só podes inserir montantes numerários.", "success":False}
        return Response(res)