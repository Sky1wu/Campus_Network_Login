import requests
import os
import pickle

dirs = os.path.abspath('.')

file_path = dirs+'/campus_network_data'

if not os.path.exists(file_path):
    print('首次运行')
    username = input('账号：')
    password = input('密码：')
else:
    file = open(file_path, 'rb')
    username, password = pickle.load(file)
    file.close()

while True:
    data = {'username': username, 'password': password}  # 帐号密码
    login_url = 'http://172.16.251.172:8081/authentication/form'  # 登录地址

    # 登录 header
    login_header = {
        'Authorization': 'Basic eGlhb2RlOnhpYW9kZTEyMw=='
    }

    # 登录
    login_response = eval(requests.post(
        login_url, headers=login_header, data=data).content.decode('utf-8'))

    if 'content' in login_response.keys():
        print('帐号或密码错误')
        username = input('帐号：')
        password = input('密码：')

    else:
        break


# 认证 token
access_token = login_response['access_token']

# 状态检查
status_url = 'http://172.16.251.172:8081/portal/wifi/status'

# 认证 header
auth_header = {
    'Authorization': 'bearer '+access_token
}

status_response = eval(requests.post(
    status_url, headers=auth_header).content.decode('utf-8'))

code = status_response['code']
message = status_response['message']

online_code = '12001'

if code != online_code:
    url = 'http://172.16.251.172:8081/portal/wifi/login'
    auth_response = eval(requests.post(
        url, headers=auth_header).content.decode('utf-8'))

    # 重新检查认证状态
    status_response = eval(requests.post(
        status_url, headers=auth_header).content.decode('utf-8'))
    code = status_response['code']
    message = status_response['message']

    print('认证状态：'+message, 'Code: '+code)

else:
    print("当前在线")


file = open(file_path, 'wb')
pickle.dump([username, password], file)
file.close()
