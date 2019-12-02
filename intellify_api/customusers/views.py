from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from customusers.serializers import CustomUserSerializer
from customusers.models import CustomUser
from customusers.functions import check_password


@api_view(['GET'])
@csrf_exempt
def users_list(request, format=None):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@csrf_exempt
def signup(request, format=None):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CustomUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED,
                            )

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST,
                        )
    else:
        context = dict()
        context['method'] = 'POST'
        context['required_params'] = ['name', 'email', 'phone', 'password', 'user_name']
        context['example'] = {
            'name': 'test user',
            'email': 'test@gmail.com',
            'phone': '1234567890',
            'password': 'min_8_characters',
            'user_name': 'only_alphabets&nums',
        }
        return Response(context, status=status.HTTP_200_OK, )


@api_view(['GET', 'POST'])
@csrf_exempt
def login(request, format=None):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_name = data['user_name']
        password = data['password']

        try:
            user = CustomUser.objects.get(user_name=user_name)
        except ObjectDoesNotExist:
            return Response({"success": False, "error": "Invalid user_name"}, status=status.HTTP_400_BAD_REQUEST,
                            )

        password_hash = user.password

        if not check_password(password, password_hash):
            return Response({"success": False, "error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST,
                            )
        else:
            serializer = CustomUserSerializer(user)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK,
                            )

    elif request.method == 'GET':
        context = dict()
        context['method'] = 'POST'
        context['required_params'] = ['user_name', 'password']
        return Response(context, status=status.HTTP_200_OK, )


@api_view(['GET'])
@csrf_exempt
def home(request, format=None):
    if request.method == 'GET':
        signup_context = dict()
        signup_context['url'] = 'http://' + request.get_host() + '/users/signup'
        signup_context['required_params'] = ['name', 'email', 'phone', 'password', 'user_name']

        login_context = dict()
        login_context['url'] = 'http://' + request.get_host() + '/users/login'
        login_context['required_params'] = ['user_name', 'password']

        return Response({'signup': signup_context, 'login': login_context}, status=status.HTTP_200_OK,
                        )