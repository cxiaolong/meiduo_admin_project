import sys
sys.path.insert(0, '../')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')

# 初始化django
import django
django.setup()

from django.template import loader
from django.conf import settings

from goods.models import SKU
from goods.utils import get_categories, get_goods_and_spec


def generate_detail_html(sku_id):
    """
    根据接收的sku_id生成对应的详情页面
    """
    # 获取的是商品分类部分的数据:
    dict = get_categories()

    goods, specs, sku = get_goods_and_spec(sku_id)

    # 渲染模板，生成静态html文件
    context = {
        'categories': dict,
        'goods': goods,
        'specs': specs,
        'sku': sku
    }

    # 加载 loader 的 get_template 函数, 获取对应的 detail 模板
    template = loader.get_template('detail.html')
    # 拿到模板, 将上面添加好的数据渲染进去.
    html_text = template.render(context)
    # 拼接模板要生成文件的位置:
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'goods/'+str(sku_id)+'.html')
    # 写入
    with open(file_path, 'w') as f:
        f.write(html_text)


if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        print(sku.id)
        generate_detail_html(sku.id)