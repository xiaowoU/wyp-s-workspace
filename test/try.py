import jwt
import base64


secret_key = 'wyp'
class jwtToken():
    def __init__(self):
        pass
    def encoded_jwt(self, payload):
        # {'username': '运维咖啡吧', 'site': 'https://ops-coffee.cn'}, # 第一部分是一个 Json 对象，称为 Payload，主要用来存放有效的信息，例如用户名，过期时间等等所有你想要传递的信息
        # secret_key,    # 第二部分是一个秘钥字串，用于 Signature 签名，服务端用来校验 Token 合法性，这个秘钥只有服务端知道，不能泄露
        # algorithm='HS256')    # 第三部分指定了 Signature 签名的算法
        encoded_jwt = jwt.encode(payload, secret_key, algorithm='HS256')
        '''
        点分割成的三部分:Header.Payload.Signature
        其中Header和Payload只是对原始输入的信息转成了 base64 编码，第三部分 Signature 是用 header+payload+secret_key 进行加密的结果
        '''
        return encoded_jwt
    def decoded_jwt(self, encoded_jwt):
        # encoded_jwt = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ilx1OGZkMFx1N2VmNFx1NTQ5Nlx1NTU2MVx1NTQyNyIsInNpdGUiOiJodHRwczovL29wcy1jb2ZmZWUuY24ifQ.fIpSXy476r9F9i7GhdYFNkd-2Ndz8uKLgJPcd84BkJ4'
        header, payload, signature = encoded_jwt.split('.')
        header_raw = base64.b64decode(header)
        payload_raw = base64.b64decode('%s==' % payload)    # 不是2的对象，参数后加==
        signature = jwt.decode(encoded_jwt, secret_key, algorithms=['HS256'])
        '''
        b'{"typ":"JWT","alg":"HS256"}'
        b'{"username":"\\u8fd0\\u7ef4\\u5496\\u5561\\u5427","site":"https://ops-coffee.cn"}'
        {'username': '运维咖啡吧', 'site': 'https://ops-coffee.cn'}
        '''




from pyecharts import options as opts
from pyecharts.charts import Geo, BMap, Map
from pyecharts.globals import ChartType, SymbolType
from pyecharts.faker import Faker


def area_map() -> Map:
    data = [('湖北', 9074), ('浙江', 661),
            ('广东', 632), ('湖南', 463),
            ('四川', 231), ('贵州', 38)]

    area_map = (
        Map()
            # .add(series_name="设备数量", data_pair=data, maptype="china", zoom=1, center=[105, 38])
            .add(series_name="设备数量",
                 data_pair=data,  # 坐标点名称，坐标点值
                 maptype="china",
                 zoom=1, center=[105, 38])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国地图"),
            visualmap_opts=opts.VisualMapOpts(max_=9999, is_piecewise=True,
                                              pieces=[{"max": 9, "min": 0, "label": "0-9", "color": "#FFE4E1"},
                                                      {"max": 99, "min": 10, "label": "10-99", "color": "#FF7F50"},
                                                      {"max": 499, "min": 100, "label": "100-499", "color": "#F08080"},
                                                      {"max": 999, "min": 500, "label": "500-999", "color": "#CD5C5C"},
                                                      {"max": 9999, "min": 1000, "label": ">=1000", "color": "#8B0000"}]
                                              )
        )
    )
    return area_map

def scatter_map() -> Geo:
    address, value = Faker.provinces, Faker.values()
    data = [list(z) for z in zip(address, value)]
    c = (
        Geo()
        .add_schema(maptype="china",
                    # is_roam=True,
                    )
        .add(
            series_name="设备分布",    #图题
            data_pair=data,
            type_=ChartType.EFFECT_SCATTER,
            is_selected=True
        )
        .add_coordinate("衡阳", 112.37, 26.53)    # 新增一个坐标点
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  #设置是否显示标签
        .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=200),    #设置legend显示的最大值
                title_opts=opts.TitleOpts(title="Geo-设备分布图"),   #左上角标题
        )
    )
    return c

def baidu_map() -> BMap:
    baiduAK = "lqa7E19BuMACUHqXf9u3ogZIO6wBTYN"
    bd_map = (
        BMap()
        .add_schema(
            baidu_ak=baiduAK,
            center=[104.07332, 30.57775],
            # zoom=8
        )
        .add(
            series_name='bmap',
            data_pair=[list(z) for z in zip(Faker.provinces, Faker.values())],
            label_opts=opts.LabelOpts(formatter="{b}")
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=200),  # 设置legend显示的最大值
            title_opts=opts.TitleOpts(title="bMap-设备分布图"),  # 左上角标题
        )

    )
    return bd_map



def run():
    a_map = area_map()
    a_map.render(path="area_map.html")
    province_heat = scatter_map()
    province_heat.render(path="scatter_map.html")
    b_map = baidu_map()
    b_map.render(path="baidu_map.html")


import requests
import json
import time

def get_geo(address):
    '''
    {
	"status": "1",
	"info": "OK",
	"infocode": "10000",
	"count": "1",
	"geocodes": [{
		"formatted_address": "四川省成都市温江区",
		"country": "中国",
		"province": "四川省",
		"citycode": "028",
		"city": "成都市",
		"district": "温江区",
		"township": [],
		"neighborhood": {
			"name": [],
			"type": []
		},
		"building": {
			"name": [],
			"type": []
		},
		"adcode": "510115",
		"street": [],
		"number": [],
		"location": "103.837104,30.690460",
		"level": "区县"
	}]
}
    '''
    url = 'https://restapi.amap.com/v3/geocode/geo?key=864c853f3ad0f0a878d7ad7670a8019c&address=%s' % address
    res = requests.get(url)
    try:
        while True:
            if(200 == res.status_code):
                # bytes
                content = json.loads(res.content)
                # print(content)
                geocodes = content.get("geocodes", None)
                if geocodes:
                    location = geocodes[0]["location"]
                    location = location.split(',')
                    # ['103.837104', '30.690460']
                    return location
            else:
                print("Try geturl again")
                time.sleep(2)
    except:
        print("Exception!")


if __name__ == '__main__':
    # run()
    # res = get_geo("四川成都温江")
    # print(res)
    pid = None
    if pid:
        print(1111)
    else:
        print(2222)

    pass
