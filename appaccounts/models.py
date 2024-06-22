from django.db import models
from rest_framework import serializers

# Create your models here.
class AccountModel(models.Model):
    """沿宝用户模型"""
    id = models.AutoField(primary_key=True, verbose_name="ID")
    username = models.CharField(null=False, max_length=50, verbose_name="用户名")
    password = models.CharField(null=False, max_length=50, verbose_name="密码")
    email = models.CharField(null=True, max_length=100, verbose_name="邮箱")
    phone = models.CharField(null=True, max_length=50, verbose_name="手机号")
    begin = models.DateField(null=True, verbose_name="授权起始日期")
    end = models.DateField(null=True, verbose_name="授权终止日期")
    modelkey = models.CharField(null=True, max_length=2048, verbose_name="大模型key")
    isvalid = models.SmallIntegerField(default=1, verbose_name="是否有效")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "account"
        verbose_name_plural = verbose_name
        ordering = ('id', )

    def __str__(self):
        return self.id
    
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = ('id', 'username', 'password', 'email', 'phone', 'begin', 'end', 'modelkey', 'isvalid', 'createtime', 'updatetime')

class LogModel(models.Model):
    """操作日志模型"""
    id = models.AutoField(primary_key=True, verbose_name="ID")
    username = models.CharField(null=False, max_length=50, verbose_name="用户名")
    app = models.CharField(null=True, max_length=50, verbose_name="应用名")
    event = models.CharField(null=True, max_length=50, verbose_name="事件")
    msg = models.CharField(null=True, max_length=200, verbose_name="详情")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "log"
        verbose_name_plural = verbose_name
        ordering = ('id', )

    def __str__(self):
        return self.id
    
class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogModel
        fields = ('id', 'username', 'app', 'event', 'msg', 'createtime')


class DanmuModel(models.Model):
    """直播弹幕数据"""
    id = models.AutoField(primary_key=True, verbose_name="ID")
    username = models.CharField(null=False, max_length=50, verbose_name="用户名")
    danmuid = models.CharField(null=False, max_length=50, verbose_name="弹幕ID")
    plat = models.CharField(null=True, max_length=20, verbose_name="平台")  #抖音/B站/
    type = models.CharField(null=True, max_length=20, verbose_name="类型")  #评论/礼物/加入/点赞
    liveid = models.CharField(null=True, max_length=30, verbose_name="直播间ID")  #
    danmu_userid = models.CharField(null=True, max_length=30, verbose_name="弹幕用户ID")  #
    danmu_usernick = models.CharField(null=True, max_length=30, verbose_name="弹幕用户昵称")  #
    danmu_usergender = models.CharField(null=True, max_length=10, verbose_name="弹幕用户性别")  #
    content = models.CharField(null=True, max_length=50, verbose_name="弹幕")  #
    reply = models.CharField(null=True, max_length=50, verbose_name="回复弹幕")  #
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "danmu"
        verbose_name_plural = verbose_name
        ordering = ('id', )

    def __str__(self):
        return self.id
    
class DanmuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanmuModel
        fields = ('id', 'username', 'danmuid', 'plat', 'type', 'liveid', 'danmu_userid', 'danmu_usernick', 'danmu_usergender', 'content', 'reply', 'createtime')

