import os

from django.shortcuts import render
from utils.goods import get_goods_specs
# Create your views here.

from django.views import View
from utils.goods import get_categories
from contents.models import ContentCategory


class IndexView(View):
    def get(self, request):
        # 1. 获取商品分类的数据
        categories = get_categories()


        contents = {}

        contents_categories = ContentCategory.objects.all()
        for cat in contents_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 我们之前所用的前端页面做了数据页面静态化
        # 用自己的模板做测试
        # 将数据组织完成之后进行返回
        context = {
            'categories': categories,
            'contents': contents
        }

        return render(request, 'index.html', context)


'''
列表页面展示

用的不是模板  使用的是前端文件

需求：
    根据首页中的分类去获取分类数据

前端：
    前端会根据用户点击分类数据之后 发送一个ajax(axios)请求
    id 通过路由进行传递
    分页的页码
    每页多少条数据
    排序数据也会传递



后端：
    请求
        接收参数
            page: 1   第几页
            page_size: 5 一页多少条数据
            ordering: -create_time 排序规则 倒序


    业务逻辑
        根据需求查询数据 将对象数据转成字典数据  前后端分离的

    路由：
        GET
        http://127.0.0.1:8000/list/<category_id>/skus/


    步骤：
        1. 接收参数
        2. 获取分类id
        3. 根据分类id进行分类i数据的查询验证
        4. 获取面包屑数据
        5. 查询分类数据对应的sku 数据 排序规则 分页功能
        6. 返回响应
'''
from medicine.models import GoodsCategory
from django.http import JsonResponse
from utils.goods import get_breadcrumb
from medicine.models import SKU


class ListView(View):
    def get(self, request, category_id):
        # 1. 接收参数 排序规则 分页数量 当前页数
        ordering = request.GET.get('ordering')
        page_size = request.GET.get('page_size')
        page = request.GET.get('page')

        # 2. 获取分类id
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '当前数据不存在'})

        # 3. 获取面包屑
        breadcrumb = get_breadcrumb(category)
        # 4. 查询分类数据对应的sku商品数据
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(ordering)

        # 分页
        from django.core.paginator import Paginator

        # 每页的数据量
        paginator = Paginator(skus, per_page=page_size)
        # 获取指定页面的数据
        page_skus = paginator.page(page)

        # 需要将获取到的查询数据集转成列表数据
        sku_list = []
        for sku in page_skus.object_list:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })

        # 获取总页数
        total_num = paginator.num_pages

        # 返回响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'breadcrumb': breadcrumb,
            'list': sku_list,
            'count': total_num
        })


'''
商品热销数据展示
'''


class HotGoodsView(View):
    def get(self, request, category_id):
        # 通过模型查询当前的商品数据
        # order.by默认是升序  销量需要倒叙展示
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        hot_skus = []

        for sku in skus:
            hot_skus.append({
                'id': sku.id,
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': sku.price
            })

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'hot_skus': hot_skus})


#
# from haystack.views import SearchView
# from django.http import JsonResponse
#
#
# from haystack.views import SearchView
# from django.http import JsonResponse
#
#
# class SKUSearchView(SearchView):
#     def create_response(self):
#         # 获取搜索结果
#         context = self.get_context()
#         data_list = []
#         for sku in context['page'].object_list:
#             data_list.append({
#                 'id': sku.object.id,
#                 'name': sku.object.name,
#                 'price': sku.object.price,
#                 'default_image_url': sku.object.default_image.url,
#                 'searchkey': context.get('query'),
#                 'page_size': context['page'].paginator.num_pages,
#                 'count': context['page'].paginator.count
#             })
#         # 拼接参数, 返回
#         return JsonResponse(data_list, safe=False)
#
#
#


class DetailView(View):
    def get(self,request,sku_id):

        sku=SKU.objects.get(id=sku_id)


        categories=get_categories()
        breadcrumb=get_breadcrumb(sku.category)
        goods_specs=get_goods_specs(sku)
        context={
            'categories':categories,
            'breadcrumb':breadcrumb,
            'sku':sku,
            'goods_specs':goods_specs
         }
        return render(request,'detail.html',context)




def generate_static_index_html():
    # 获取商品频道和分类
    categories = get_categories()
    # 广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
    # 渲染模板
    context = {
        'categories': categories,
        'contents': contents
    }
    # 获取首页模板文件
    from django.template import loader
    template = loader.get_template('index.html')

    html_text = template.render(context)

    from tuling_mall import settings
    file_path =os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)


class SearchView(View):
    def get(self, request):
        # 1. 接收参数 排序规则 分页数量 当前页数

        page_size = request.GET.get('page_size')  # 默认每页数量为 6
        page = request.GET.get('page')  # 默认当前页数为 1
        q = request.GET.get('q')
        print(q)

        # 2. 查询数据
        skus = SKU.objects.filter(name__contains=q, is_launched=True).order_by('price')
        print(len(skus))

        # 分页
        from django.core.paginator import Paginator

        # 每页的数据量
        paginator = Paginator(skus, per_page=page_size)
        # 获取指定页面的数据
        page_skus = paginator.page(page)

        # 4. 将获取到的查询数据集转成列表数据
        sku_list = []
        for sku in page_skus.object_list:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })

        print(sku_list)
        # 5. 获取总页数
        total_num = paginator.num_pages

        # 6. 返回响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'list': sku_list,
            'count': total_num
        })