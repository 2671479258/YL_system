'''
需求:
    登录时将cookie数据与redis数据进行同步

以redis为同步目标
    将redis数据拿出来赋值给cookie

以cookie为同步目标
    将cookie数据拿出来添加到redis

看产品经理

目前项目采用的方式
    以cookie为主

    简单

    如果未登录
        将cookie数据拿出来 当用户登录时做数据新增
        如果cookie数据与redis数据重复 不动

后端:
    业务逻辑:
        将cookie数据合并到redis中

        读取cookie
            初始化一个字典用于保存sku_id: count
            初始化列表用于保存selected 两个列表分别存储
                保存选中商品
                保存未选中商品
            遍历cookie数据
            将字典数据 列表数据添加到redis中
            删除cookie

将cookie数据转为redis数据
'''
import pickle
import base64
from django_redis import get_redis_connection


# 合并购物车
def merge_cookie_to_redis(request, response):
    # 获取cookie数据
    cookie_carts = request.COOKIES.get('carts')
    # 判断当前cookie数据是否存在
    if cookie_carts is not None:
        # 解码
        carts = pickle.loads(base64.b64decode(cookie_carts))
        # 初始化字典 用于保存sku_id: count
        cookie_dict = {}
        # 初始化两个列表 分别保存选中状态和未选中状态
        selected_ids = []
        unselected_ids = []

        # 遍历cookie数据
        '''
        1: {
            count: 10,
            selected: True
        }
        '''
        for sku_id, count_selected_dict in carts.items():
            # 获取所有商品的数量
            cookie_dict[sku_id] = count_selected_dict['count']

            # 获取商品选中状态 是否为选中
            if count_selected_dict['selected']:
                selected_ids.append(sku_id)
            else:
                unselected_ids.append(sku_id)

        # 将组织到的数据添加到redis中
        # 连接redis
        redis_cli = get_redis_connection('carts')
        # 使用管道提交数据
        pipeline = redis_cli.pipeline()
        # 将字典数据添加到redis中 可能有多个字典
        pipeline.hmset('carts_%s' % request.user.id, cookie_dict)
        # 添加列表数据 因为当前的ids为列表 需要添加 * 作为解包
        if len(selected_ids) > 0:
            pipeline.sadd('selected_%s' % request.user.id, *selected_ids)
        if len(unselected_ids) > 0:
            pipeline.srem('selected_%s' % request.user.id, *unselected_ids)

        # 管道提交
        pipeline.execute()

        # 删除cookie
        response.delete_cookie('carts')

        # 把登录视图中的response返回给登录视图
        return response
    else:
        return response
