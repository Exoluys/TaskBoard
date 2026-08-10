from knox.models import AuthToken
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import CustomUser
from accounts.serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterApi (CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginApi(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, req):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token = AuthToken.objects.create(user)[1]
        return Response({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": UserSerializer(user).data
        }, status=200)



class MeApi(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutApi(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        req.auth.delete()
        return Response({
            "success": True,
            "message": "Logout successful"
        })