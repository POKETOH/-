import requests
from bs4 import BeautifulSoup

cookie = r"""BAIDUID_BFESS=9D08E1F0C10E0D486D3F8AA11DE0F452:FG=1; __bid_n=1901ad690ee5344fbba0be; BAIDU_WISE_UID=wapp_1719737409920_132; ZFY=THA0QGdJTYyLJ7xvh5u17OTwD3WgF2oTX:B1RHjqhnUY:C; USER_JUMP=-1; st_key_id=17; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1719737409,1720779575; HMACCOUNT=EFD44E776A16C92D; arialoadData=false; BDUSS=EzN1VIQTBVLWRyU3ZwV21tODVWZ1Zta0VXd1RRbG9MdGRubkwxRVJiNW5rTGhtRVFBQUFBJCQAAAAAAAAAAAEAAACSv1BcwfevdwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGcDkWZnA5FmQV; BDUSS_BFESS=EzN1VIQTBVLWRyU3ZwV21tODVWZ1Zta0VXd1RRbG9MdGRubkwxRVJiNW5rTGhtRVFBQUFBJCQAAAAAAAAAAAEAAACSv1BcwfevdwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGcDkWZnA5FmQV; STOKEN=36735c07a7e4f2921e9012eaa8e878cf34b0c9e5db656f8c72f63e180c12dbc3; ariawapForceOldFixed=false; tb_as_data=88f36b05a251f738397ed3d8afe2fa100495bc59923bd994a5cf5ac045846fc65ec46aa9dbdb2af8aaf98a1a41955c456b1bcf815248ad6b3742fef5fbb04d3273b858ddc2662f722ea1aef91ad821db2dda50e412f5a97997632c5276826fc2; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1720779747; 1548795794_FRSVideoUploadTip=1; video_bubble1548795794=1; XFI=a3980550-4038-11ef-9ccf-d50aab6e2cfe; BA_HECTOR=2l8ka40425252l84042g2k0k0ukt1k1j920v41u; ab_sr=1.0.1_ZjVlZWE3ODE2OTlhODZmZjdjNTMwMTJlODgxNWZiOTE2NDU0MWUxYmU4ZGI3ODJiYzIxYjY0OTA3ZTNjNzAyMjA5MDc5NDI4NzRmZmRhODIzOGQwOGQ1ZDkwMjljNTNjMjAzOTQ3ZmJkN2U1MjYwMWI4OTE5NzdlMTE3YTE0ODhiYTUyMTY5NTU0ZmVhZjk0NDllMGI0ODMyYTM3ZWY1MjgxZTJmYjhjYjdjMWRkOWRjMmM0ODdlNjU0YzJkODA5; st_data=b47b21fbb06a01edae888e2bc05241c06dbb90298c8a010e6f97317469502c9581cb7c0ae571d294d1bce9c868d8c7ebce1c19ce9663209ade91c809ae95fdfc383235c798797deb66abfb782384d0a1698c06d95ff68f7ece3ceeafbc02f79ac81d1450995fc709944bb2a30127302ed402e98fc11c12f1fac7c5a9cc05b467; st_sign=4e90c205; XFCS=1F274521FED9E7031EF57729FA6831EE373C06B429E7985AA30CB2A135B26E0E; XFT=JO7eZENGWUDm6U6PkKFFkozjpaq2RLWQo7qeaTbKKeA=; showCardBeforeSign=1; RT="z=1&dm=baidu.com&si=5ae767f8-852c-47ef-8b75-7f355f3c203e&ss=lyijq746&sl=9&tt=9u7&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=3ull&nu=15dbbhpwe&cl=4cag""" + "\""
signUrl = 'https://tieba.baidu.com/sign/add'

# 请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    'cookie': cookie
}


# 查找页数
def search_all_page():
    url = "https://tieba.baidu.com/f/like/mylike?v=1720786625680&pn=1"
    get_html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(get_html, 'html.parser')
    return len(soup.select('.pagination>a'))


page_num = search_all_page() - 1

# 查找关注的吧
def search_like(page):
    like_list = []
    url = "https://tieba.baidu.com/f/like/mylike?v=1720787781194&pn="
    for i in range(page):
        html = requests.get(url + str(i + 1), headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.select('.forum_main>.forum_table>table>tr>td>a'):
            title = item.attrs.get('title')
            if title and title.find("级会员")==-1:
                like_list.append(title)
    return like_list
like_list = search_like(page_num)


print("开始签到")

# 具体签到方法
def sign(title):
    data = {
        'ie': 'utf-8',
        'kw': title,  # 吧名
    }
    response = requests.post(signUrl, data=data, headers=headers)
    if response.text == r"""{"no":1101,"error":"\u4eb2\uff0c\u4f60\u4e4b\u524d\u5df2\u7ecf\u7b7e\u8fc7\u4e86","data":""}""":
        print(title + "签到失败")
        return 0
    else:
        print(title + "签到成功")
        return 1

success=0
fail=0
for item in like_list:
    if sign(item):
        success=success+1
    else:
        fail=fail+1
print("===================================")
print("签到完成，共有{}吧，签到成功{}个，失败{}个".format(len(like_list),success,fail))