from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        pass
        # email = request.data['email']
        # password = request.data['password']
        # user = User.objects.filter(email=email).first()
        # if user is not None and user.check_password(password):
        # return Response({'error': 'wrong password'}, status=400)


class LogoutView(APIView):
    pass
