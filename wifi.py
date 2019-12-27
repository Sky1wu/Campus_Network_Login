import requests
import os
import pickle
import json
import getpass
from time import sleep
import win32api
import win32con

file_name = 'campus_network_data'


def exit_program():
    os.system("pause")
    exit()


print('校园网一键认证')
if not os.path.exists(file_name):
    print('首次运行请输入登录信息')
    username = input('账号：')
    password = getpass.getpass('密码（输入不显示）：')

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
    try:
        login_response = requests.post(
            login_url, headers=login_header, data=data)
        login_response = json.loads(login_response.content.decode('utf-8'))

        try:
            access_token = login_response['access_token']
            break
        except KeyError:
            print('帐号或密码错误')
            username = input('帐号：')
            password = getpass.getpass('密码（输入不显示）：')

            win32api.SetFileAttributes(
                file_name, win32con.FILE_ATTRIBUTE_NORMAL)
            file = open(file_name, 'wb')
            pickle.dump([username, password], file)
            file.close()
            win32api.SetFileAttributes(
                file_name, win32con.FILE_ATTRIBUTE_HIDDEN)
    except:
        print('无法连接至校园网')
        exit_program()


access_token = login_response['access_token']
status_url = 'http://172.16.251.172:8081/portal/wifi/status'

# 认证 header
auth_header = {
    'Authorization': 'bearer '+access_token
}

try:
    status_response = requests.post(status_url, headers=auth_header)
    status_response = json.loads(status_response.content.decode('utf-8'))
    code = status_response['code']
    message = status_response['message']

except:
    print('状态获取失败')
    exit_program()

online_code = '12001'

if code != online_code:
    url = 'http://172.16.251.172:8081/portal/wifi/login'
    try:
        auth_response = requests.post(url, headers=auth_header)
        auth_response = json.loads(auth_response.content.decode('utf-8'))
        code = auth_response['code']

        if(code == online_code):
            print('认证成功')
            sleep(1)
        else:
            print('认证失败')
            print(auth_response)
            exit_program()
    except:
        print('认证失败')
        print(auth_response)
        exit_program()

else:
    print("当前在线")
    sleep(1)
