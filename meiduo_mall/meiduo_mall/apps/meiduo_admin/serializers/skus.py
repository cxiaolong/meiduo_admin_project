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

    def validate_sku_id(self, value):
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        return value

    def create(self, validated_data):
        # 调用父类ModelSerializer中的create方法
        sku_image = super().create(validated_data)
        # 默认图片判断: 是否需要设置默认图片
        sku = sku_image.sku
        if not sku.default_image:
            sku.default_image = sku_image.image
            sku.save()

        return sku_image


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""
    class Meta:
        model = SKU
        fields = ('id', 'name')














