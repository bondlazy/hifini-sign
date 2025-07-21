import json
import os
import random
import re
import time
from urllib.parse import urlencode

import requests


def bark(device_key, title, content, bark_icon):
    if not device_key:
        return 2

    url = "https://api.day.app/push"
    headers = {
        "content-type": "application/json",
        "charset": "utf-8"
    }
    data = {
        "title": title,
        "body": content,
        "device_key": device_key
    }

    if not bark_icon:
        bark_icon = ''
    if len(bark_icon) > 0:
        url += '?icon=' + bark_icon
        print('拼接icon')
    else:
        print('不拼接icon')

    resp = requests.post(url, headers=headers, data=json.dumps(data))
    resp_json = resp.json()
    if resp_json["code"] == 200:
        print(f"[Bark]Send message to Bark successfully.")
    if resp_json["code"] != 200:
        print(f"[Bark][Send Message Response]{resp.text}")
        return -1
    return 0


def signV1(cookie):
    url = "https://www.hifini.com.cn/sg_sign.htm"
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers)

    print(response.text)

    return response.text


def signV2(cookie, sign):
    dynamicKey = generateDynamicKey()
    encryptedSign = simpleEncrypt(sign, dynamicKey)

    url = "https://hifini.com.cn/sg_sign.htm"
    params = {'sign': encryptedSign}
    payload = urlencode(params)
    headers = {
        'authority': 'hifini.com.cn',
        'accept': 'text/plain, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'origin': 'https://hifini.com.cn',
        'referer': 'https://hifini.com.cn/sg_sign.htm',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return response.text

def signV3(cookie, sign):
    url = "https://hifini.com.cn/sg_sign.htm"
    params = {'sign': sign}
    payload = urlencode(params)
    headers = {
        'authority': 'hifini.com.cn',
        'accept': 'text/plain, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'origin': 'https://hifini.com.cn',
        'referer': 'https://hifini.com.cn/sg_sign.htm',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return response.text

def generateDynamicKey():
    current_time = int(time.time() * 1000)
    key_index = (current_time // (5 * 60 * 1000)) % 5
    keys = ['HIFINI', 'HIFINI_COM', 'HIFINI.COM', 'HIFINI-COM', 'HIFINICOM']
    return keys[key_index]


def simpleEncrypt(input, key):
    result = ''
    for i in range(len(input)):
        result += chr(ord(input[i]) ^ ord(key[i % len(key)]))
    return result


def getMessage(text):
    message = ''

    if "成功签到" in text:
        message = '成功签到'
    elif "今天已经签过啦" in text:
        message = '今天已经签过啦'
    elif "操作存在风险" in text:
        message = '未签到，操作存在风险'
    elif "维护中" in text:
        message = '未签到，服务器正在维护'
    elif "请完成验证" in text:
        message = '未签到，需要手动滑块验证'
    elif "行为存在风险" in text:
        message = '未签到，极验geetest页面滑块验证'
    elif "正在进行人机识别" in text:
        message = '未签到，页面需要renji.js跳转验证'
    else:
        message = '签到结果解析错误'

    return message


def sign(cookie, no):
    pre = '第' + str(no) + '个，'
    if not cookie:
        cookie = ''

    if len(cookie) > 0:
        print('有cookie，需要执行签到')

        text = signV1(cookie)

        message = ''

        if "操作存在风险" in text and "encryptedSign" in text:
            print('V2，再次签到')
            pattern = r"var sign = \"([a-f0-9]+)\";"
            match = re.search(pattern, text)
            if match:
                sign = match.group(1)
                if len(sign) > 0:
                    sm = random.randint(3, 6)
                    time.sleep(sm)

                    text2 = signV2(cookie, sign)
                    message = getMessage(text2)
                else:
                    message = '未签到，操作存在风险且未能解析出sign'
            else:
                message = '未签到，操作存在风险且sign匹配失败'
        elif "操作存在风险，请稍后重试。" in text and "$.xpost(xn.url('sg_sign'), {'sign':  sign}" in text:
            print('V3，再次签到')
            pattern = r"var sign = \"([a-f0-9]+)\";"
            match = re.search(pattern, text)
            if match:
                sign = match.group(1)
                if len(sign) > 0:
                    sm = random.randint(3, 6)
                    time.sleep(sm)

                    text2 = signV3(cookie, sign)
                    message = getMessage(text2)
                else:
                    message = '未签到，操作存在风险且未能解析出sign'
            else:
                message = '未签到，操作存在风险且sign匹配失败'
        else:
            message = getMessage(text)

        return pre + message

    else:
        print('不执行签到')
        return ''


def main():
    bark_device_key = os.environ.get('BARK_DEVICEKEY')
    bark_icon = os.environ.get('BARK_ICON')

    wait = random.randint(3, 110)
    time.sleep(wait)

    message_all = []
    title = 'HiFiNi-签到结果'
    message = ''
    for i in range(1, 4):
        cookie = os.environ.get('COOKIE' + str(i))
        msg = sign(cookie, i)
        if not msg:
            msg = ''
        if len(msg) > 0:
            message_all.append(msg)

        sm = random.randint(19, 97)
        time.sleep(sm)

    if not message_all:
        message = '暂无执行结果'
    else:
        message_all = '\n'.join(message_all)
        message_all = re.sub('\n+', '\n', message_all).rstrip('\n')
        message = message_all

    bark(bark_device_key, title, message, bark_icon)

    print('finish')


if __name__ == '__main__':
    main()
