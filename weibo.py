import json
import requests

headers = {
    'cookie': "替换自己的cookie",
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}
# 获取关注列表
#key为超话名，value为超话id
map = {}
list_url = "https://weibo.com/ajax/profile/topicContent?tabid=231093_-_chaohua"
list_data = "tabid=231093_-_chaohua"
response = requests.get(list_url, data=list_data, headers=headers)
# print(response.text)
json_data = json.loads(response.text)

# 提取需要的信息
topics = json_data.get('data', {}).get('list', [])

# 遍历并打印每个超话的信息
for topic in topics:
    title = topic.get('title', 'N/A')
    link = topic.get('link', 'N/A')

    # 找到最后一个斜杠的位置
    last_slash_index = link.rfind("/")

    # 获取最后一个斜杠之后的所有字符
    id = link[last_slash_index + 1:] if last_slash_index != -1 else link
    map[title] = id

#签到方法
def sign(key,value):
    sign_url = "https://weibo.com/p/aj/general/button?ajwvr=6&api=http://i.huati.weibo.com/aj/super/checkin&texta=%E7%AD%BE%E5%88%B0&textb=%E5%B7%B2%E7%AD%BE%E5%88%B0&status=0&id={}&location=page_100808_super_index&timezone=GMT+0800&lang=zh-cn&plat=Win32&ua=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/126.0.0.0%20Safari/537.36%20Edg/126.0.0.0&screen=2048*1152&__rnd=1720793419490".format(value)
    data = {
        'ajwvr': '6',
        'api': "http://i.huati.weibo.com/aj/super/checkin",
        'texta': "签到",
        'textb': "已签到",
        'status': '0',
        'id': value,
        'location': "page_100808_super_index",
        'timezone': "GMT 0800",
        'lang': "zh-cn",
        'plat': "Win32",
        'ua': " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        'screen': "2048*1152",
        '__rnd': "1720793419490",
    }
    response = requests.get(sign_url, data=data, headers=headers)
    rep=response.text.encode("utf-8")
    rep=json.loads(rep)
    if rep.get('msg')=="今天已签到(382004)":
        print(key+"签到失败")
        return 0
    else :
        print(key + "签到成功")
        return 1
success=0
fail=0
for key in map:
    if sign(key,map[key]):
        success=success+1
    else:
        fail=fail+1
print("===========分割线===========")
print("共{}个超话，签到成功{}个，失败{}个".format(len(map),success,fail))
