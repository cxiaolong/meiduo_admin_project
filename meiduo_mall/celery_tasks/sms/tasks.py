
from celery_tasks.main import celery_app
from celery_tasks.yuntongxun.ccp_sms import CCP


@celery_app.task(name='send_sms_code_func')
def send_sms_code_func(mobile, sms_code):
    '''发送短信'''

    result = CCP().send_template_sms(mobile, [sms_code, 5], 1)

    print(result)

    return result # 0: 成功 -1:失败