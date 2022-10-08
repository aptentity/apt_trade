# coding: utf-8
import requests
import json


# 发送钉钉消息
def send_dingtalk_message(url, content):
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
def send_normal_buy(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=c39f229f015c093c32ecdc9f2fe7f186ce2ffd2dda8a5b44b76f9af5b504bbdd'
    send_dingtalk_message(access_token, msg+"\n--gulliver")


def send_short_over_sell(msg):
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=1b2570b482bc750749dc2733bca5f9c820c5df7a6fc597ca4954f195834d4c7a'
    send_dingtalk_message(access_token, msg+"\n--gulliver")


if __name__ == "__main__":
    # 获取dingtalk token url
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=c39f229f015c093c32ecdc9f2fe7f186ce2ffd2dda8a5b44b76f9af5b504bbdd'
    # 钉钉消息内容，注意test是自定义的关键字，需要在钉钉机器人设置中添加，这样才能接收到消息
    content = 'test,测试消息\n--gulliver'
    # 要@的人的手机号，可以是多个，注意：钉钉机器人设置中需要添加这些人，否则不会接收到消息
    mobile_list = ['173xxxxxx']
    # 发送钉钉消息
    send_dingtalk_message(access_token, content)
