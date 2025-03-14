from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework import status
from .serializer import UserSerializer

# import할때는 장고를 최상단에 그 다음에 rest_framework


class Me(APIView):
    permission_classes = [IsAuthenticated]

    # Me역시 로그인되어야만 볼 수 있게 해야함

    def get(self, req):
        user = req.user

        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, req):
        user = req.user

        serializer = UserSerializer(
            user,
            data=req.data,
            partial=True,
            # 부분수정
        )

        if serializer.is_valid():
            user = serializer.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 유저가 입력한 정보 가져와서
        # 유효성 검사하고 -> 리턴함
        #


class Signup(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")

        if not username or not password:
            raise ParseError("아이디 및 패스워드는 필수입니다!")

        # "유저가 입력한 데이터를 가져와서 유효성 검사 후
        # 데이터베이스에 유저 정보를 저장 한뒤
        # 응답을 회원가입 되었습니다." -> 우리가 해야할 일

        # 패스워드를 캐시화 해야함(암호화)

        try:
            validate_password(password)
            # 패스워드 유효검사
        except Exception as e:
            raise ParseError(e)

        serializer = UserSerializer(data=req.data)

        if serializer.is_valid():
            user = serializer.save()
            # 아직 로그인한 유저가 없기때문에 빈칸으로()
            user.set_password(password)
            # -> 캐시처리
            user.save()
            # ->캐시처리 했기 때문에 한번 더 저장
            serializer = UserSerializer(user)
            return Response({"ok": "회원가입 되었습니다!"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")

        if not username or not password:
            raise ParseError("아이디 및 패스워드는 필수입력 사항입니다!")

        user = authenticate(
            req,
            username=username,
            password=password,
            # 데이터베이스에 있는 유저네임과 비번 = 유저가 입력한 유저네임과 비번
        )

        if user:
            login(req, user)
            return Response({"ok": "로그인 되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "로그인에 실패하였습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        logout(req)
        return Response(
            {"ok": "로그아웃 되었습니다."},
            status=status.HTTP_200_OK,
        )


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, req):
        user = req.user
        current_password = req.data.get("current_password")
        new_password = req.data.get("new_password")

        if not current_password or not new_password:
            raise ParseError("빈 값은 허용되지 않습니다.")

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(
                {"ok": "패스워드를 변경했습니다."},
                status=status.HTTP_200_OK,
            )
        else:
            raise ParseError("패스워드를 다시 확인해주세요.")

    # -> 유저가 입력한 정보를 가져와서
    # -> 빈값인지 아닌지 유효성 검사하고
    # -> 새로운 비번 캐시처리하여 새로운 비번 저장하고
    # -> 비번이 변경되었다고 응답
    # -> 문제발생 하면 예외처리
