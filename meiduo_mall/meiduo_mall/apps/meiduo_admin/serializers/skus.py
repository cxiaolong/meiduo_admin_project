from goods.models import SKU
from goods.models import SKUImage
from rest_framework import serializers


class SKUImageSerializer(serializers.ModelSerializer):
    """图片序列化器类"""
    sku_id = serializers.IntegerField(label='SKU商品id')
    sku = serializers.StringRelatedField(label='SKU商品')

    class Meta:
        model = SKUImage
        fields = ('id', 'sku', 'sku_id', 'image')


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""
    class Meta:
        model = SKU
        fields = ('id', 'name')














