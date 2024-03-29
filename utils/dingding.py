# coding: utf-8
import requests
import json


# 发送钉钉消息
def send_dingtalk_message(url, content):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0b5c5489-8959-412f-9c30-3d4b9cc62043'
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            # 要发送的内容【支持markdown】【！注意：content内容要包含机器人自定义关键字，不然消息不会发送出去，这个案例中是test字段】
            "content": content
        },
        "at": {
            # 要@的人
            # "atMobiles": mobile_list,
            # 是否@所有人
            "isAtAll": True
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.text)
    return r.text


# 普通买入消息
def trend_bull(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=a18ed48ce5689243f3dfcff9eccf78654e38f3e3306b9080f4224794d5872925'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def trend_bear(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=d5bbc36f0545270456bf4a6be93195d7c579acc8e6584cc2c7fecdcb6ac0ebff'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def send_short_bear(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=1b2570b482bc750749dc2733bca5f9c820c5df7a6fc597ca4954f195834d4c7a'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def send_short_bull(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=edb9bc14e04cff680ccc65b1c1fcb148dbf82ed89a44ffb8a4671bcaaec05be0'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def send_day_bull(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=bc271058e2e64cc88e8b8ce6842e290cc94d917e6d09362cad3f9187bde31b15'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def send_day_bear(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=88f7a41ed014e867fb59ebea1b8a01f31b1a4ca3f20695f9aae5b0a8139149bf'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def send_week_bull(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=8aac3da1d291c9acd2be47b9306f153fa8e91caad8d26a20669821c825677ced'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def send_week_bear(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=4bd62f55525d77c8553254ef730f42471bc73699519c5ca011f8362423bc48a3'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def duy_notice(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=98c7dd2d0c5ac59a8fc14b8f03b39063e256616c8cd87e92a482217fb8180121'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def sell_notice(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=24180f92aa1c91597fcc5590f0bfeba3162b7d4c57d8b45620768bbdbd5325fd'
    send_dingtalk_message(access_token, msg + "\n--gulliver")


def send_wechat_message(url, content):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            # 要发送的内容【支持markdown】【！注意：content内容要包含机器人自定义关键字，不然消息不会发送出去，这个案例中是test字段】
            "content": content
        },
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print('-----------------')
    print(r.text)
    return r.text


def send_notice(msg):
    token = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0b5c5489-8959-412f-9c30-3d4b9cc62043'
    send_wechat_message(token, msg)


if __name__ == "__main__":
    # 获取dingtalk token url
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=c39f229f015c093c32ecdc9f2fe7f186ce2ffd2dda8a5b44b76f9af5b504bbdd'
    # 钉钉消息内容，注意test是自定义的关键字，需要在钉钉机器人设置中添加，这样才能接收到消息
    content = 'test,测试消息\n--gulliver'
    # 要@的人的手机号，可以是多个，注意：钉钉机器人设置中需要添加这些人，否则不会接收到消息
    mobile_list = ['173xxxxxx']
    # 发送钉钉消息
    send_dingtalk_message(access_token, content)

# send_notice('1111111111111')
