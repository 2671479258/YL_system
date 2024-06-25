from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from article.models import article

class new_article(View):
    def get(self,request):
        article_records = article.objects.all().order_by('-release_data')[:3]
        article_records_list=[]

        for record in article_records:
            # 创建一个字典
            article_dict = dict(
                id=record.id,
                title=record.title,
                introd=record.introd,
                release_data=record.release_data,


            )
            article_records_list.append(article_dict)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'records': article_records_list})

class article_content(View):
    def get(self,request,article_id):
        art=article.objects.get(id=article_id)
        title=art.title
        content=art.content
        author=art.doctor.doctorname
        release_data=art.release_data
        context={
            'title':title,
            'content':content,
            'author':author,
            'release_data':release_data

        }
        return render(request,'article_content.html',context)


class yangsheng_article(View):
    def get(self,request):
        yangsheng_records=article.objects.filter(category=3).all().order_by('-release_data')[:3]
        yangsheng_records_list=[]

        for record in yangsheng_records:
            # 创建一个字典
            article_dict = dict(
                id=record.id,
                title=record.title,
                introd=record.introd,
                release_data=record.release_data,


            )
            yangsheng_records_list.append(article_dict)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'Ysrecords': yangsheng_records_list})


class kepu_article(View):
    def get(self,request):
        kepu_records=article.objects.filter(category=2).all().order_by('-release_data')[:3]
        kepu_records_list=[]

        for record in kepu_records:
            # 创建一个字典
            article_dict = dict(
                id=record.id,
                title=record.title,
                introd=record.introd,
                release_data=record.release_data,


            )
            kepu_records_list.append(article_dict)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'KPrecords': kepu_records_list})


class huli_article(View):
    def get(self,request):
        huli_records=article.objects.filter(category=1).all().order_by('-release_data')[:3]
        huli_records_list=[]

        for record in huli_records:
            # 创建一个字典
            article_dict = dict(
                id=record.id,
                title=record.title,
                introd=record.introd,
                release_data=record.release_data,


            )
            huli_records_list.append(article_dict)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'HLrecords': huli_records_list})


from django.shortcuts import render


class ALL_YS_article(View):
    def get(self, request):
        ALL_YS_records = article.objects.filter(category=3).all()
        ALL_YS_records_list = []

        for record in ALL_YS_records:
            # 创建一个字典
            article_dict = dict(
                id=record.id,
                title=record.title,
                introd=record.introd,
                release_data=record.release_data,
            )
            ALL_YS_records_list.append(article_dict)
            print(ALL_YS_records_list)

        # 将列表放入字典中
        context = {'ALL_YS_records_list': ALL_YS_records_list}

        # 使用字典作为上下文数据传递给render函数
        return render(request, 'YS_article.html', context)


class ALL_KP_article(View):
    def get(self, request):
        ALL_KP_records = article.objects.filter(category=2).all()
        ALL_KP_records_list = []

        for record in ALL_KP_records:
            # 创建一个字典
            article_dict = dict(
                id=record.id,
                title=record.title,
                introd=record.introd,
                release_data=record.release_data,
            )
            ALL_KP_records_list.append(article_dict)


        # 将列表放入字典中
        context = {'ALL_KP_records_list': ALL_KP_records_list}

        # 使用字典作为上下文数据传递给render函数
        return render(request, 'KP_article.html', context)

class ALL_HL_article(View):
    def get(self, request):
        ALL_HL_records = article.objects.filter(category=1).all()
        ALL_HL_records_list = []

        for record in ALL_HL_records:
            # 创建一个字典
            article_dict = dict(
                id=record.id,
                title=record.title,
                introd=record.introd,
                release_data=record.release_data,
            )
            ALL_HL_records_list.append(article_dict)


        # 将列表放入字典中
        context = {'ALL_HL_records_list': ALL_HL_records_list}

        # 使用字典作为上下文数据传递给render函数
        return render(request, 'HL_article.html', context)


class UserSearchArticle(View):
    def get(self, request):
        # 1. 接收参数 排序规则 分页数量 当前页数

        page_size = request.GET.get('page_size')  # 默认每页数量为 6
        page = request.GET.get('page')  # 默认当前页数为 1
        q = request.GET.get('q')


        from article.models import article
        # 2. 查询数据
        articles = article.objects.filter(title__contains=q)


        # 分页
        from django.core.paginator import Paginator

        # 每页的数据量
        paginator = Paginator(articles, per_page=page_size)
        # 获取指定页面的数据
        page_skus = paginator.page(page)

        # 4. 将获取到的查询数据集转成列表数据
        article_list = []
        for article in page_skus.object_list:

            article_list.append({
                'id': article.id,
                'title': article.title,
                'introd': article.introd,
                'release_data': article.release_data
            })



        # 5. 获取总页数
        total_num = paginator.num_pages

        # 6. 返回响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'list': article_list,
            'count': total_num,
            'q':q

        })
