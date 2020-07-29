from django.db import models

# Create your models here.
from meiduo_mall.utils.BaseModel import BaseModel


class GoodsCategory(BaseModel):
    """
    商品分类表对应的内容, 自关联
    """
    # 分类的名称
    name = models.CharField(max_length=10, verbose_name='名称')
    # 分类的上级id (分类一共有三级)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               related_name="subs",
                               on_delete=models.CASCADE,
                               verbose_name='父类别')

    # 设置分类表的属性
    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    # 返回分类名称
    def __str__(self):
        return self.name


class GoodsChannel(BaseModel):
    """
    商品频道表展示的内容
    """
    # 当前商品频道属于哪个组
    group_id = models.IntegerField(verbose_name='组号')
    # 频道对应的一级分类id
    category = models.ForeignKey(GoodsCategory,
                                 on_delete=models.CASCADE,
                                 verbose_name='顶级商品类别')
    # 当前频道点击后跳转的链接地址
    url = models.CharField(max_length=50,
                           verbose_name='频道页面链接')
    # 这组频道的先后顺序
    sequence = models.IntegerField(verbose_name='组内顺序')

    class Meta:
        db_table = 'tb_goods_channel'
        verbose_name = '商品频道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name


class Brand(BaseModel):
    """
    品牌
    """
    # 品牌名称
    name = models.CharField(max_length=20,
                            verbose_name='名称')
    # 品牌logo
    logo = models.ImageField(verbose_name='Logo图片')
    # 品牌首字母
    first_letter = models.CharField(max_length=1,
                                    verbose_name='品牌首字母')

    class Meta:
        db_table = 'tb_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SPU(BaseModel):
    """
    商品SPU表对应的内容: SPU: 代表一组商品
    """
    # 这组商品的名称
    name = models.CharField(max_length=50, verbose_name='名称')
    # 这组商品的品牌
    brand = models.ForeignKey(Brand,
                              on_delete=models.PROTECT,
                              verbose_name='品牌')
    # 这组商品的一级分类
    category1 = models.ForeignKey(GoodsCategory,
                                  on_delete=models.PROTECT,
                                  related_name='cat1_spu',
                                  verbose_name='一级类别')
    # 这组商品的二级分类
    category2 = models.ForeignKey(GoodsCategory,
                                  on_delete=models.PROTECT,
                                  related_name='cat2_spu',
                                  verbose_name='二级类别')
    # 这组商品的三级分类
    category3 = models.ForeignKey(GoodsCategory,
                                  on_delete=models.PROTECT,
                                  related_name='cat3_spu',
                                  verbose_name='三级类别')
    # 这组商品的销量数
    sales = models.IntegerField(default=0,
                                verbose_name='销量')
    # 这组商品的评价数
    comments = models.IntegerField(default=0,
                                   verbose_name='评价数')
    desc_detail = models.TextField(default='',
                                   verbose_name='详细介绍')
    desc_pack = models.TextField(default='',
                                 verbose_name='包装信息')
    desc_service = models.TextField(default='',
                                    verbose_name='售后服务')

    class Meta:
        db_table = 'tb_spu'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SPUSpecification(BaseModel):
    """
    商品规格
    """
    # 这个商品规格属于哪个商品
    spu = models.ForeignKey(SPU,
                            related_name='specs',
                            on_delete=models.CASCADE,
                            verbose_name='商品')
    # 这组规格的名称
    name = models.CharField(max_length=20,
                            verbose_name='规格名称')

    class Meta:
        db_table = 'tb_spu_specification'
        verbose_name = '商品规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.spu.name, self.name)


class SpecificationOption(BaseModel):
    """
    规格具体选项表
    """
    # 这个规格选项表对应上面的哪个商品规格
    spec = models.ForeignKey(SPUSpecification,
                             related_name='options',
                             on_delete=models.CASCADE,
                             verbose_name='规格')
    # 规格选项的内容
    value = models.CharField(max_length=20,
                             verbose_name='选项值')

    class Meta:
        db_table = 'tb_specification_option'
        verbose_name = '规格选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s - %s' % (self.spec, self.value)


class SKU(BaseModel):
    """
    商品SKU表对应的内容:   SKU: 具体的某个商品
    """
    # 这个商品的名称
    name = models.CharField(max_length=50,
                            verbose_name='名称')
    # 这个商品的副标题
    caption = models.CharField(max_length=100,
                               verbose_name='副标题')
    # 这个商品对应 spu 表中的那个字段
    spu = models.ForeignKey(SPU,
                            related_name='skus',
                            on_delete=models.CASCADE,
                            verbose_name='商品')
    # 这个商品的类别
    category = models.ForeignKey(GoodsCategory,
                                 on_delete=models.PROTECT,
                                 verbose_name='从属类别')
    # 这个商品的价格
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='单价')
    # 这个商品的进价
    cost_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     verbose_name='进价')
    # 此商品的市场价
    market_price = models.DecimalField(max_digits=10,
                                       decimal_places=2,
                                       verbose_name='市场价')
    # 此商品的库存
    stock = models.IntegerField(default=0,
                                verbose_name='库存')
    # 此商品的销量
    sales = models.IntegerField(default=0,
                                verbose_name='销量')
    # 此商品的评价个数
    comments = models.IntegerField(default=0,
                                   verbose_name='评价数')
    # 此商品是否上架(是否在售)
    is_launched = models.BooleanField(default=True,
                                      verbose_name='是否上架销售')
    # 此商品对应的图片
    default_image = models.ImageField(max_length=200,
                                      default='',
                                      null=True,
                                      blank=True,
                                      verbose_name='默认图片')

    class Meta:
        db_table = 'tb_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class SKUImage(BaseModel):
    """
    SKU图片
    """
    # 这个图片对应哪个 SKU 商品类
    sku = models.ForeignKey(SKU,
                            on_delete=models.CASCADE,
                            verbose_name='sku')
    # 图片
    image = models.ImageField(verbose_name='图片')

    class Meta:
        db_table = 'tb_sku_image'
        verbose_name = 'SKU图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.sku.name, self.id)


class SKUSpecification(BaseModel):
    """
    SKU具体规格
    """
    # 对应的SKU值
    sku = models.ForeignKey(SKU,
                            related_name='specs',
                            on_delete=models.CASCADE,
                            verbose_name='sku')
    # 对应哪一个规格
    spec = models.ForeignKey(SPUSpecification,
                             on_delete=models.PROTECT,
                             verbose_name='规格名称')
    # 规格的具体内容
    option = models.ForeignKey(SpecificationOption,
                               on_delete=models.PROTECT,
                               verbose_name='规格值')

    class Meta:
        db_table = 'tb_sku_specification'
        verbose_name = 'SKU规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s - %s' % (self.sku, self.spec.name, self.option.value)