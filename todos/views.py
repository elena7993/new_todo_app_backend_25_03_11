from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializer import TodoSerializer

# Create your views here.


class Todos(APIView):
    permission_classes = [IsAuthenticated]
    # 로그인 되었을 때만 투두리스트를를 볼 수 있음

    def get(self, req):
        # todos = Todo.objects.all()
        todos = Todo.objects.filter(user=req.user)
        # 로그인한 유저(요청한 유저)의 투두만 가져옴

        serializer = TodoSerializer(
            todos,
            many=True,
        )

        return Response(serializer.data)

    # many=True : QuerySet을 리스트 형태로 변환(serializer)함
