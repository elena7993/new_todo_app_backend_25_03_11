# from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Todo
from .serializer import TodoSerializer

# Create your views here.

# User = get_user_model()


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

    def post(self, req):
        serializer = TodoSerializer(data=req.data)
        # print(req.data)
        # return Response({"ok": True})
        if serializer.is_valid():
            todo = serializer.save(user=req.user)
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 유저가 입력한 데이터중에 필수항목이 없다면 알려줌

        # 1.등록하면 -> 유저가 작성한 내용을 가져와야함 req.data
        # 2.가져온 유저의 json을 -> python코드로 변환과정이 필요함 serializer
        # 3.유효성검사 ok -> 저장!
        # 4.파이썬 코드를 -> json으로 변환 -> serializer


class TodoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        # print(pk)
        except Todo.DoesNotExist:
            raise NotFound
        # 오류를 강제로 일으킴

        # 함수로 뺀거임

    def get(self, req, pk):
        todo = self.get_object(pk)

        if todo.user != req.user:
            raise PermissionDenied
        # 다른 유저가 투두를 보려면 권한없음으로 나오게함

        serializer = TodoSerializer(todo)

        return Response(serializer.data)

    def put(self, req, pk):
        todo = self.get_object(pk)

        serializer = TodoSerializer(
            todo,
            data=req.data,
            partial=True,
            # 부분 수정이 가능하게 함
        )

        if serializer.is_valid():
            todo = serializer.save(user=req.user)
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, req, pk):
        todo = self.get_object(pk)

        if todo.user != req.user:
            raise PermissionDenied

        todo.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
