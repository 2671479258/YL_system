from django.shortcuts import render
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse

# Create your views here.
'''
前端：
    拼接了一个url 地址 img标签请求该地址
    url: 127.0.0.1:8000/image_codes/<uuid>/


后端：
    接收请求
        uuid

    处理业务逻辑
        生成图片验证码与图片二进制
        redis 进行图片验证码的保存

    返回响应
        返回图片二进制数据

    路由：
        get

    第三方包
        captcha
'''


class ImageCodeView(View):
    def get(self, request,uuid):
        '''

        :param request:
        :param uuid:
        :return:
        text: 验证码内容
        image： 图片
        '''
        text, image = captcha.captcha.generate_captcha()
        # 将验证码保存到redis
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 100, text)
        return HttpResponse(image, content_type='image/jpeg')

