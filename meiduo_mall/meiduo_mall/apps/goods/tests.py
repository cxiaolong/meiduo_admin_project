from django.test import TestCase
import pickle, base64

# Create your tests here.
if __name__ == '__main__':

    dict = {
        'name':'zs',
        'age':12
    }

    result1 = pickle.dumps(dict)
    print(result1)  # bytes ====> 二进制(0,1)  ====> 在控制台展示会以16进行的形式展示

    # result2 = pickle.loads(result1)
    # print(result2)   # bytes反向转回  ===> python数据类型(dict)


    # 目标: 在控制台展示会以64位的数据格式展示
    result3 = base64.b64encode(result1)
    print(result3)  # 64位的bytes类型

    resul4 = result3.decode()
    print(resul4)  # 64位的str


    # 合并的使用:
    # 加密:
    str_64 = base64.b64encode(pickle.dumps(dict)).decode()
    # 解密:
    data = pickle.loads(base64.b64decode(str_64.encode()))
    data1 = pickle.loads(base64.b64decode(str_64))
    print(data)
    print(data1)
