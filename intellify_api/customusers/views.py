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
    """
    This view provides the data of all the users registered with the API.
    **This view is meant to be used, only to test the working of the API**
    """
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@csrf_exempt
def signup(request, format=None):
    """
    This view registers new users with the API.

    To register a new user, make a POST request to this view using the following format:

    ```
    {
        "name": "test user",
        "email": "test@gmail.com",
        "phone": "1234567890",
        "user_name": "test1",
        "password": "password"
    }
    ```


    1. name:
        * max length 40
        * min length 3
        * should contain only alphabets and spaces
    2. email: should be a valid email.
    3. phone:
        * should be a string of exactly 10 digits.
    4. user_name:
        * max length 15
        * min length 4
        * should contain only alphabets and digits
        * should contain at least 1 alphabet
    5. password:
        * max length 15
        * min length 8

    > ***All passwords are stored in Hashed format. Unlike encoded passwords, these hashes
    cannot be misused to recover user passwords.***

    users can also make POST requests using the form available at the bottom of the page.

    On successful signup a success message is shown.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CustomUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
        return Response(context, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@csrf_exempt
def login(request, format=None):
    """
    This view logs in users, who are registered with the API.

    For login, make a POST request to this view using the following format:

    ```
    {
        "user_name": "test1",
        "password": "password1"
    }
    ```

    users can also make POST requests using the form available at the bottom of the page.

    On successful login, details of the requested user will be returned. ex:

    ```
    {
        "name": "test user",
        "email": "test@gmail.com",
        "phone": "1234567890",
        "user_name": "test1",
        "created_on": "YYYY-MM-DD"
    }
    ```
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_name = data['user_name']
        password = data['password']

        try:
            user = CustomUser.objects.get(user_name=user_name)
        except ObjectDoesNotExist:
            return Response({"success": False, "error": "Invalid user_name"}, status=status.HTTP_400_BAD_REQUEST)

        password_hash = user.password

        if not check_password(password, password_hash):
            return Response({"success": False, "error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CustomUserSerializer(user)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        context = dict()
        context['method'] = 'POST'
        context['required_params'] = ['user_name', 'password']
        return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def home(request, format=None):
    """
    This API has 5 views:

    1. **Home:** This view provides a basic introduction to the user.
    2. **Signup:** Using this view end users can register themselves with the API. For more info
    go to [Signup](https://intellify-user-api.herokuapp.com/users/signup).
    3. **Login:** Using this view, registered users can log in to their accounts. For more info
    go to [Login](https://intellify-user-api.herokuapp.com/users/login).
    4. **All users:** This view is meant for **developer use only**, it provides the info about all
    users registered with the API. This view is to be used to verify the functioning of the API.
    For more info, go to [All users](https://intellify-user-api.herokuapp.com/users/all).
    5. **Ping:** This view is provided to check server status, for more info see,
    [Ping](https://intellify-user-api.herokuapp.com/ping)


    Each of the four views can be accessed either in this BrowsableAPI format or JSON format
    (use `?format=json` at the end of any url).

    """
    if request.method == 'GET':
        signup_context = dict()
        signup_context['description'] = 'registers new users'
        signup_context['url'] = 'http://' + request.get_host() + '/users/signup'
        signup_context['required_params'] = ['name', 'email', 'phone', 'password', 'user_name']

        login_context = dict()
        login_context['description'] = 'logs in registered users'
        login_context['url'] = 'http://' + request.get_host() + '/users/login'
        login_context['required_params'] = ['user_name', 'password']

        return Response({'signup': signup_context, 'login': login_context}, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def ping(request, format=None):
    """
    This view is implemented to check server status, a GET request at this view will return:

    ```
    {
        "status": "OK"
    }
    ```
    """
    if request.method == 'GET':
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)
