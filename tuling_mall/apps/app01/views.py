import pymysql
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
import re
from app01.models import AdminsInfo
import json
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from users.models import User
from django import forms
from django.views.decorators.csrf import csrf_exempt





class AdLogin(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            # 查询数据库中是否存在匹配的用户
            user = AdminsInfo.objects.get(username=username)
        except AdminsInfo.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        # 直接比较密码
        if user.password != password:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        # 成功匹配，登录用户
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', username, max_age=3600 * 24 * 15)
        return response




