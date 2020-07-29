import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')

from celery import Celery

# 创建一个对象:
celery_app = Celery('meiduo')

# 让对象知道有一个配置文件:
celery_app.config_from_object('celery_tasks.config')

# 让对象自动发现任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email', 'celery_tasks.html'])