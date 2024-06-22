from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from appaccounts.models import AccountModel, AccountSerializer, LogModel, LogSerializer, DanmuModel, DanmuSerializer
from yanbao_api import settings
log = settings.log 


# Create your views here.
class AccountView(APIView):
    def get(self, request):
        models = AccountModel.objects.all() 
        if "isvalid" in request.GET:
            models = models.filter(isvalid=request.GET["isvalid"])
        else:
            models = models.filter(isvalid=1)
        if "username" in request.GET:
            models = models.filter(username=request.GET["username"])
        if "password" in request.GET:
            models = models.filter(password=request.GET["password"])
        if "phone" in request.GET:
            models = models.filter(phone=request.GET["phone"])
        serializer = AccountSerializer(models, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username is None or username == "" or password is None or password == "":
            return Response({"msg": "用户名/密码不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, password=password)
            Token.objects.create(user=user)
        except Exception as e:
            return Response({"msg": f"user创建失败{e}"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountViewDetail(APIView):
    def put(self, request, id):
        try:
            account = AccountModel.objects.get(id=id)
        except Exception as e:
            return Response({"msg": f"account{id}查询失败{e}"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            username = request.data.get("username", None)
            password = request.data.get("password", None)
            if username is None or username == "" or password is None or password == "":
                return Response({"msg": "用户名/密码不能为空"}, status=status.HTTP_400_BAD_REQUEST)
            isvalid = request.data.get("isvalid", 1)
            if isvalid == 0: #删除账户
                user = User.objects.get(username=username)
                user.delete()
                log.debug(f'删除用户 {username}')
            else:
                if password != account.password:  #修改密码
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    log.debug(f'修改密码 {username}')
            # 保存用户全部字段
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": f"serializer不可用 {serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class LogView(APIView):
    def get(self, request):
        models = LogModel.objects.all() 
        if "event" in request.GET:
            models = models.filter(event=request.GET["event"])
        if "begin_date" not in request.GET or "end_date" not in request.GET:
            return Response({"msg": "请设置起止日期/begin_date/end_date"}, status=status.HTTP_400_BAD_REQUEST)
        models = models.filter(createtime__range=(request.GET["begin_date"], request.GET["end_date"]))
        serializer = LogSerializer(models, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LogSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print("--post save--")
            serializer.save()
            print("--post saved--")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DanmuView(APIView):
    def get(self, request):
        models = DanmuModel.objects.all() 
        if "username" in request.GET:
            models = models.filter(username=request.GET["username"])
        if "plat" in request.GET:
            models = models.filter(plat=request.GET["plat"])
        if "type" in request.GET:
            models = models.filter(type__in=request.GET["type"].split(","))
        if "liveid" in request.GET:
            models = models.filter(liveid__in=request.GET["liveid"].split(","))
        if "begin_time" not in request.GET or "end_time" not in request.GET:
            return Response({"msg": "请设置起止日期/begin_time/end_time"}, status=status.HTTP_400_BAD_REQUEST)
        models = models.filter(createtime__range=(request.GET["begin_time"], request.GET["end_time"]))
        serializer = DanmuSerializer(models, many=True)
        return Response(serializer.data)

    def post(self, request):
        many = True if isinstance(request.data, list) else False
        serializer = DanmuSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
