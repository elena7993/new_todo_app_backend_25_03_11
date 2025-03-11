from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import UserSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    # Me역시 로그인되어야만 볼 수 있게 해야함

    def get(self, req):
        user = req.user

        serializer = UserSerializer(user)

        return Response(serializer.data)
