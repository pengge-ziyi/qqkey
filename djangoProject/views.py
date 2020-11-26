# -*- coding: utf-8 -*-
# @Time     :2020/11/24
# @Author    :鹏哥
import re
import json
from random import random
import requests
from django.http import HttpResponse
from django.shortcuts import render
import base64
import warnings
warnings.filterwarnings("ignore")

ss = requests.session()

def hash33(t):
    e = 0
    for i in range(len(t)):
        e += (e << 5) + ord(t[i])
    return 2147483647 & e


def getGTK(p_skey):
    hashes = 5381
    for letter in p_skey:
        hashes += (hashes << 5) + ord(letter)
    return hashes & 0x7fffffff


def index(request):
    return render(request, 'a.html')


def login(request):
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=' + str(
        '0.' + str(int(random() * 10000000000000000)))
    h = ss.get(url, verify=False)
    tp = base64.b64encode(h.content)
    tp = str(tp, encoding='utf-8')
    cookie = h.cookies
    headers = requests.utils.dict_from_cookiejar(cookie)
    qrsig = headers['qrsig']
    fh = {
        'tp': tp,
        'qrsig': qrsig
    }
    return HttpResponse(json.dumps(fh))


def zt(request):
    qrsig = request.GET['qrsig']
    url = f'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.Html' \
          f'%3Fpara%3Dizone%26from%3Diqq&ptqr' \
          f'token={hash33(qrsig)}&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0' \
          f'-1542784335061&js_ver=10289&js_type=1&login_sig=hn6ZiMZRPT8LWFsFG3MrScznzLVrdbwS9EIo-ihAmeD' \
          f'*YmOfqP3uoI6JytVVQYw2&pt_uistyle=40&aid=549000912&daid=5& '
    html = ss.get(url=url)
    type = re.findall('[\u4e00-\u9fa5]+', html.text)[0]
    uin = ''
    skey = ''
    p_skey = ''
    gtk = ''
    if type == '登录成功':
        url3 = re.findall("'0','0','(.*?)','0','登录成功！", html.text)
        url3 = url3[0]
        h2 = ss.get(url3, allow_redirects=False)
        cookie = h2.cookies
        dict = requests.utils.dict_from_cookiejar(cookie)
        uin = dict['uin']
        skey= dict['skey']
        p_skey= dict['p_skey']
        gtk = getGTK(p_skey)

    fh = {
        'type': type,
        'uin': uin,
        'gtk': gtk,
        'p_skey': p_skey,
        'skey': skey
    }

    return HttpResponse(json.dumps(fh))
