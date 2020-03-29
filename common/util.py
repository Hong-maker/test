# encoding: utf-8

import requests
import time
import hmac
import hashlib
import json

# 获取账号2.0登录token
def login_token_v2(host, identity, password, pid='unknown'):
    data = {
        "identity": identity,
        "password": password,
        "pid": pid
    }
    res = requests.post(host+'/tiger/accounts/login', json=data)
    if res.status_code == 200 and 'application/json' in res.headers['Content-Type']:
        bearer_token = 'Bearer '+ res.json()['token']
        return bearer_token

# 获取账号3.0发送图形验证码的ticket
def get_captcha_ticket_account_v3(host):
    res = requests.get(host+'/tiger/captcha/graph/ticket')
    if res.status_code == 200:
        return res.json()['ticket']
    else:
        print('账号3.0获取发送图形验证码的ticket失败，状态码：%s' % res.status_code)

# 获取某具体时间的时间戳
def get_timeslot(time_date):
    return int(time.mktime(time.strptime(str(time_date), '%Y-%m-%d')))

# 返回当前时间戳的后3分钟，用于测试删除作品业务标志位
def timestamp_3minutes():
    return int(time.time()+180)

# 判断两个值是否相等
def eval_equal(source, target):
    return source == target

# 测试国家数字教育资源接入：获取ticket
# www.codemao.cn?ticket={ticket}即可登录对应账号
def get_eduyun_ticket(account='test_account', password='123456'):
    host = 'http://system.eduyun.cn/bmp-web'
    user = {
        'account': account,
        'password': password
    }
    res = requests.post(host+'/debugTool/createTicket', data=user)
    ticket = ''
    if res.status_code == 200 and 'application/json' in res.headers['Content-Type']:
        # 注意返回的res.json()['data']['data']，格式为str，需要转为dict
        ticket = json.loads(res.json()['data']['data'])['data']['ticket']
    else:
        print('获取国家数字教育资源账号的ticket失败，状态码：%s' % res.status_code)
    return ticket

# 登录文轩智慧校园平台
# 登录需要验证码，暂时不实现自动化
def login_wenxuan(username, password):
    pass

# 获取文轩智慧校园token
def get_wenxuan_token():
    # 获取当前时间毫秒极时间戳
    timestamp_ms = int(time.time() * 1000)
    APPID, APPKEY = '68c94f4affa97e4974d8e927183a91a1', '9ce2dac77c2e0e4ec6cac11c538ff174'
    uid = 'F8A2A8AB40B204C18ED6E03E4499795F'
    cookies_wenxuan = login_wexuan()
    url = "http://smart.winshareyun.cn/winshare-web-portal/portal/getToken?appKey={}&info={}_{}".format(APPKEY, APPID, timestamp_ms)
    res1 = requests.get(url, headers={"Cookie": cookies_wenxuan})
    if res1.status_code == 200 and res.headers['Content-Type'] == 'application/json':
        token = res1.json()['data']

if __name__ == '__main__':
    print(get_eduyun_ticket())