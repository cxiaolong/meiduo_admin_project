# 设置Django运行所依赖环境环境
import os
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

# 初始化
import django
django.setup()

from django.core.files import File
from goods.models import SKUImage


if __name__ == "__main__":
    # 模拟获取客户端上传文件对象
    file = open('/Users/smart/Desktop/images/1.jpg', 'rb')
    file = File(file)

    # 保存文件
    # SKUImage.objects.create(image=file, sku_id=1)

    # 更新
    sku_image = SKUImage.objects.get(id=44)
    sku_image.image = file
    sku_image.save()
