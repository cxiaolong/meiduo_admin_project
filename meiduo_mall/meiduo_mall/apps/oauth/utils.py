from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings

def generate_access_token(openid):
    '''把openid加密为access_token'''


    # 用导入的类创建对象
    # obj = TimedJSONWebSignatureSerializer(秘钥, 有效期)
    obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=3600)

    dict = {
        'openid':openid
    }
    # 调用对象的方法 ---> 把数据变为token
    token_bytes = obj.dumps(dict)

    # 返回token
    return token_bytes.decode()


def check_access_token(access_token):
    '''把access_token解密为openid'''

    # 用导入的类创建对象
    # obj = TimedJSONWebSignatureSerializer(秘钥, 有效期)
    obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=3600)

    data = obj.loads(access_token)

    return data.get('openid')