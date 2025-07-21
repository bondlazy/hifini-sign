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

    if bark_icon:
        url += "?icon=" + bark_icon

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        resp_json = resp.json()
    except Exception as e:
        print(f"[Bark] 推送失败: {e}")
        return -1

    if resp_json.get("code") == 200:
        print("[Bark] 推送成功")
        return 0
    else:
        print(f"[Bark] 推送返回: {resp.text}")
        return -1


def signV1(cookie):
    url = "https://www.hifini.com.cn/sg_sign.htm"
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    try:
        response = requests.post(url, headers=headers, timeout=10)
        print(response.text)
        return response.text
    except Exception as e:
        print(f"[signV1] 请求失败: {e}")
        return "未签到，网络异常"


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
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        return response.text
    except Exception as e:
        print(f"[signV2] 请求失败: {e}")
        return "未签到，网络异常"


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
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        return response.text
    except Exception as e:
        print(f"[signV3] 请求失败: {e}")
        return "未签到，网络异常"


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
    if "成功签到" in text:
        return '成功签到'
    if "今天已经签过啦" in text:
        return '今天已经签过啦'
    if "操作存在风险" in text:
        return '未签到，操作存在风险'
    if "维护中" in text:
        return '未签到，服务器正在维护'
    if "请完成验证" in text:
        return '未签到，需要手动滑块验证'
    if "行为存在风险" in text:
        return '未签到，极验geetest页面滑块验证'
    if "正在进行人机识别" in text:
        return '未签到，页面需要renji.js跳转验证'
    return '签到结果解析错误'


def sign(cookie, no):
    pre = f'第{no}个，'
    if not cookie:
        return ''

    print('有cookie，开始签到...')
    text = signV1(cookie)
    message = getMessage(text)

    # V2 加密逻辑
    if "操作存在风险" in text and "encryptedSign" in text:
        print('触发 V2 加密签到...')
        match = re.search(r'var sign = "([a-f0-9]+)";', text)
        if match:
            sign_value = match.group(1)
            time.sleep(random.randint(3, 6))
            text = signV2(cookie, sign_value)
            message = getMessage(text)
        else:
            message = '未签到，未能提取 sign'

    # V3 明文 sign 逻辑
    elif "操作存在风险，请稍后重试。" in text and "sign" in text:
        print('触发 V3 明文签到...')
        match = re.search(r'var sign = "([a-f0-9]+)";', text)
        if match:
            sign_value = match.group(1)
            time.sleep(random.randint(3, 6))
            text = signV3(cookie, sign_value)
            message = getMessage(text)
        else:
            message = '未签到，未能提取 sign'

    return pre + message


def main():
    bark_device_key = os.getenv('BARK_DEVICEKEY')
    bark_icon = os.getenv('BARK_ICON')

    time.sleep(random.randint(3, 110))

    messages = []
    for i in range(1, 4):
        cookie = os.getenv(f'COOKIE{i}')
        msg = sign(cookie, i)
        if msg:
            messages.append(msg)
        time.sleep(random.randint(19, 97))

    message = '\n'.join(messages) if messages else '暂无执行结果'
    bark(bark_device_key, 'HiFiNi-签到结果', message, bark_icon)
    print('finish')


if __name__ == '__main__':
    main()
