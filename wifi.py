import requests
import os
import pickle
import win32api
import win32con

file_name = 'campus_network_data'

print('校园网一键认证')
if not os.path.exists(file_name):
    print('首次运行请输入登录信息')
    username = input('账号：')
    password = input('密码：')

    file = open(file_name, 'wb')
    pickle.dump([username, password], file)
    file.close()
    win32api.SetFileAttributes(file_name, win32con.FILE_ATTRIBUTE_HIDDEN)

else:
    win32api.SetFileAttributes(file_name, win32con.FILE_ATTRIBUTE_NORMAL)
    file = open(file_name, 'rb')
    username, password = pickle.load(file)
    file.close()
    win32api.SetFileAttributes(file_name, win32con.FILE_ATTRIBUTE_HIDDEN)

while True:
    login_url = 'http://172.16.251.172:8081/authentication/form'  # 登录地址

    # 帐号密码
    data = {
        'username': username,
        'password': password
    }

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

        win32api.SetFileAttributes(file_name, win32con.FILE_ATTRIBUTE_NORMAL)
        file = open(file_name, 'wb')
        pickle.dump([username, password], file)
        file.close()
        win32api.SetFileAttributes(file_name, win32con.FILE_ATTRIBUTE_HIDDEN)

    else:
        break

access_token = login_response['access_token']
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

os.system("pause")
