# -*- coding: utf-8 -*-
from flask import make_response, jsonify, request
from app.api import api
from app.models import getHomepageData
import requests
import logging
import json
import re
@api.route('/v1.0/homePage/', methods=['GET', 'POST'])
def homepage():
    """
     上面 /v1.0/homePage/ 定义的url最后带上"/"：
     1、如果接收到的请求url没有带"/"，则会自动补上，同时响应视图函数
     2、如果/v1.0/homePage/这条路由的结尾没有带"/"，则接收到的请求里也不能以"/"结尾，否则无法响应
    """
    response = jsonify(code=200,
                       msg="success",
                       data=getHomepageData())

    return response
    # 也可以使用 make_response 生成指定状态码的响应
    # return make_response(response, 200)




@api.route('/v1.0/videoUrl/', methods=['GET', 'POST'])
def video_url():

    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    link = request.args.get("link") # 获取  get  参数
    types = request.args.get("type") # 获取  get  参数
    video_url = ""
    if types == 'douyin':
        video_url = get_dou_yin(user_agent, link)
    if types == 'kuaishou':
        video_url = get_kuai_shou(user_agent, link)

    data ={
        'video_link': video_url
    }

    result = jsonify(code=200,
                       msg="success",
                       data=data)

    return result


def get_dou_yin(user_agent, link):

    headers = {'User-Agent': user_agent}
    r = requests.get(link, headers=headers)
    redirect_url = r.url
    # 获取视频ID
    redirect_url = redirect_url.split("/")
    video_id = redirect_url[5]
    logging.info('获取到视频ID:' + video_id)

    # 通过这个接口获取视频信息，其中包括带有水印的链接
    watermark_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + video_id
    watermark_info = requests.get(watermark_url, headers=headers)

    res = watermark_info.text
    info = json.loads(res)
    vid = info['item_list'][0]['video']['vid']
    # 自行拼接成无水印的链接
    video_link = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + vid + "&ratio=720p&line=0"

    video_content = requests.get(video_link, headers=headers)
    video_url = video_content.url

    return video_url

def get_kuai_shou(link):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    # 禁止重定向获取cookie
    r = requests.get(link, headers=headers,allow_redirects=False)
    # 获取重定向后的url
    res = requests.get(link, headers=headers)
    redirect_url = res.url
    cookies = r.cookies.items()
    cookie = ""
    for name, value in cookies:
        cookie += '{0}={1};'.format(name, value)

    headers['Cookie'] = cookie

    watermark_info = requests.get(redirect_url, headers=headers)
    content = watermark_info.text
    # pattern = '<img[^>]*/>'
    pattern = 'srcNoMark:(.*?)'

    result = re.findall(pattern, content)
    print(result)
    return result


    # 获取视频ID
    # redirect_url = redirect_url.split("/")
    # video_id = redirect_url[5]
    # logging.info('获取到视频ID:' + video_id)
    #
    # # 通过这个接口获取视频信息，其中包括带有水印的链接
    # watermark_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + video_id
    # watermark_info = requests.get(watermark_url, headers=headers)
    #
    # res = watermark_info.text
    # info = json.loads(res)
    # vid = info['item_list'][0]['video']['vid']
    # # 自行拼接成无水印的链接
    # video_link = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + vid + "&ratio=720p&line=0"
    #
    # video_content = requests.get(video_link, headers=headers)
    # video_url = video_content.url
    #
    # return video_url
    return ""
