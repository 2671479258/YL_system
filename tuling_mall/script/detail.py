# 添加 django 环境
import os, sys
import django

# 1. 找到当前项目的上一级目录
sys.path.insert(0, '../')
# 2. 在项目根目录中找到settings配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuling_mall.settings')
# 3. 该文件交给django运行
django.setup()

from medicine.models import SKU
from utils.goods import get_categories, get_breadcrumb, get_goods_specs


def generic_detail_html(sku):
    # 1. 分类数据
    categories = get_categories()
    # 2. 面包屑
    breadcrumb = get_breadcrumb(sku.category)
    # 3. 规格信息
    goods_specs = get_goods_specs(sku)

    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs,

    }

    # 1. 加载模板
    from django.template import loader
    detail_template = loader.get_template('detail.html')
    # 2. 模板渲染
    detail_html_data = detail_template.render(context)
    # 3. 写入文件
    import os
    from tuling_mall import settings

    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/goods/%s.html' % sku.id)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(detail_html_data)
        print(sku.id)


# 1. 要进入到数据库查询所有的商品数据
skus = SKU.objects.all()
for sku in skus:
    generic_detail_html(sku)

