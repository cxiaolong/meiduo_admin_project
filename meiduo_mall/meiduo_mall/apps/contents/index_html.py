import os
from django.conf import settings
from django.template import loader
from contents.models import ContentCategory, Content
from goods.utils import get_categories


def generate_index_html():
    """把首页的静态文件生成"""
    dict = get_categories()

    # 1. 获取所有的广告类别
    try:
        cats = ContentCategory.objects.all()

        new_dict = {}

        # 2.遍历所有的广告类别, 获取每一个
        for cat in cats:
            content = Content.objects.filter(category=cat,
                                             status=True).order_by('sequence')

            # 3.定义一个dict, 然后把类别的key和内容作为数据放到dict中
            new_dict[cat.key] = content

    except Exception as e:
        raise Exception('广告数据获取失败')

    # 第二部分: 模板渲染部分:
    # 把上面两部分获取的有序字典和字典作为变量,拼接新的字典 context
    context = {
        'categories': dict,
        'contents': new_dict
    }

    # =====================获取模板,把数据添加进去生成页面====================
    # 根据导入的 loader 获取 'index.html' 模板
    template = loader.get_template('index.html')

    # 拿到模板, 然后将 context 渲染到模板中, 生成渲染过的模板
    html_text = template.render(context)

    # 我们拼接新的 index.html 模板将要生成的所在地地址:
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')

    # 以写的权限,将渲染过的模板重新生成, 写入到文件中.
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)


if __name__ == '__main__':
    generate_index_html()