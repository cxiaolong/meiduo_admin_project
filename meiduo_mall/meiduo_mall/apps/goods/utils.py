from collections import OrderedDict

from goods.models import GoodsChannel, GoodsCategory


def get_breadcrumb(category):
    '''根据category判断类别,从而返回dict'''
    # 1.定义一个dict
    breadcrumb = {
        'cat1':'',
        'cat2':'',
        'cat3':''
    }
    # 2.判断category类别
    if category.parent is None:
        # 3.如果category是一级类别, 往dict中添加一级类别的标题
        breadcrumb['cat1'] = category.name
    elif category.parent.parent is None:
        # 4.如果category是二级类别, 往dict中添加一级和二级类别的标题
        breadcrumb['cat2'] = category.name
        breadcrumb['cat1'] = category.parent.name
    else:
        # 5.如果category是三级类别, 往dict中添加一级和二级&三级类别的标题
        breadcrumb['cat3'] = category.name
        breadcrumb['cat2'] = category.parent.name
        breadcrumb['cat1'] = category.parent.parent.name

    # 6.返回
    return breadcrumb


def get_categories():
    '''返回各个页面需要的商品分类数据'''
    # 1.定义一个有序字典
    dict = OrderedDict()

    # 2.从GoodsChannel表中获取所有的频道, 排序(group_id & sequence)
    try:
        channels = GoodsChannel.objects.all().order_by('group_id', 'sequence')

        # 3.遍历, 拿取每一个频道
        for channel in channels:

            # 4.获取频道组的id
            group_id = channel.group_id

            # 5.判断该id是否在有序字典中, 如果不在,添加
            if group_id not in dict:
                dict[group_id] = {
                    'channels': [],
                    'sub_cats': []
                }

            # 6.根据频道, 获取对应的一级分类
            cat1 = channel.category

            # 7.拼接数据 id&name&url===> {} ===> []

            dict.get(group_id).get('channels').append({
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url
            })

            # 8.根据一级分类, 获取所有的二级分类
            cat2s = GoodsCategory.objects.filter(parent=cat1)

            # 9.遍历所有的二级分类, 拿到每一个二级分类
            for cat2 in cat2s:

                # 10.给每一个二级分类添加一个 k&v
                cat2.sub_cats = []

                # 11.根据二级分类, 获取所有的三级分类
                cat3s = GoodsCategory.objects.filter(parent=cat2)

                # 12.遍历所有的三级分类, 拿到每一个三级分类
                for cat3 in cat3s:
                    # 13.把三级分类, 添加到二级分类的[]中去
                    cat2.sub_cats.append(cat3)

                # 14.把二级分类添加到sub_cats对应的列表中去.
                dict.get(group_id).get('sub_cats').append(cat2)
    except Exception as e:
        raise Exception('数据库获取失败')
    else:
        return dict

# 导入:
from django import http
from collections import OrderedDict
from goods.models import GoodsCategory
from goods.models import GoodsChannel, SKU
from goods.models import SKUImage, SKUSpecification
from goods.models import SPUSpecification, SpecificationOption


def get_goods_and_spec(sku_id):

    # ======== 获取该商品和该商品对应的规格选项id ========
    try:
        # 根据 sku_id 获取该商品(sku)
        sku = SKU.objects.get(id=sku_id)
        # 获取该商品的图片
        sku.images = SKUImage.objects.filter(sku=sku)
    except Exception as e:
        return http.JsonResponse({'code':400,
                                  'errmsg':'获取数据失败'})

    # 获取该商品的所有规格: [颜色, 内存大小, ...]
    sku_specs = SKUSpecification.objects.filter(sku=sku).order_by('spec_id')

    sku_key = []
    # 获取该商品的所有规格后,遍历,拿取一个规格

    for spec in sku_specs:
        # 规格 ----> 规格选项 ----> 选项id  ---> 保存到[]
        sku_key.append(spec.option.id)

    # ======== 获取类别下所有商品对应的规格选项id ========
    # 根据sku对象,获取对应的类别
    spu = sku.spu

    # 获取该类别下面的所有商品
    skus = SKU.objects.filter(spu=spu)

    dict = {}
    for temp_sku in skus:
        # 获取每一个商品(temp_sku)的规格参数
        s_specs = SKUSpecification.objects.filter(sku=temp_sku).order_by('spec_id')

        key = []
        for spec in s_specs:
            # 规格 ---> 规格选项 ---> 规格选项id ----> 保存到[]
            key.append(spec.option.id)

        # 把 list 转为 () 拼接成 k : v 保存到dict中:
        dict[tuple(key)] = temp_sku.id

    # ======== 在每个选项上绑定对应的sku_id值 ========
    specs = SPUSpecification.objects.filter(spu=spu).order_by('id')

    for index, spec in enumerate(specs):
        # 复制当前sku的规格键
        key = sku_key[:]
        # 该规格的选项
        spec_options = SpecificationOption.objects.filter(spec=spec)

        for option in spec_options:
            # 在规格参数sku字典中查找符合当前规格的sku
            key[index] = option.id
            option.sku_id = dict.get(tuple(key))

        spec.spec_options = spec_options

    return spu, specs, sku