# Create your views here.
import json
import requests
import time
import datetime
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from user_manage.models import Project, Result, Section, Device


# /map_page
def map_page(request):
    # print('+++++++++++', request.environ)
    return render(request, "map_page.html")

# /details_page
def details_page(request):
    # todo: 通过这个接口获取projectid
    pid = request.GET.get('projectid', None)
    print("Pid: %s" % pid)
    return render(request, "details.html", {"Pid": pid})

# /more_data
def more_data(request):
    # 指定section的id、device的sn，未指定id时缺省为None.
    sid = request.GET.get('sectionid', None)
    dsn = request.GET.get('devicesn', None)
    # 指定条数，缺省为所有记录
    num = request.GET.get('num', None)

    # 初始化列表
    lst_data = []
    # sid和dsn为必须参数
    if (not sid) | (not dsn):
        lst_data = []
    else:
        results = Result.objects \
            .filter(Q(section=sid) & Q(device_sn=dsn)) \
            .order_by("id") \
            .values()
        if results:
            if num == 4:
                results = results[4]
            for result in results:
                item = {'create_time': datetime.datetime.strftime(result["create_time"], "%Y-%m-%d-%H:%M:%S"),
                        'device_sn': result["device_sn"],
                        'timestamp': '3333',
                        'convergence': result["convergence"],
                        'sedimentation': result["sedimentation"],
                        'data6': '6666',
                        'data7': '7777',
                        }
                lst_data.append(item)
        print('more_data: ', lst_data)
    return render(request, "more_data.html", {"List": lst_data})








# api: /get_project_info
def get_project_info(request):
    # print('+++++++++++', request.environ)
    # 读取项目信息
    '''
    param: None
    return:
    [{"adress_detail":"四川成都温江",
      "lnglat":["103.837104", "30.690460"],
      "name":"隧道1左洞",
      "position":"315线",
      "company":"暂无",
      "link":"暂无"},
     {"adress_detail":"贵州贵阳白云区",
      "lnglat":["106.623007", "26.678562"],
      "name":"隧道2右洞",
      "position":"999国道",
      "company":"暂无",
      "link":"暂无"},
      ]
    '''
    dct_projects = []
    objs = Project.objects \
        .values()
    # .values("name", "province", "city", "district", "position")

    for obj in objs:
        # print(obj)
        # 整理project数据
        id = obj.get("id", None)
        province = obj.get("province", None)
        city = obj.get("city", None)
        district = obj.get("district", None)
        adress_detail = '%s%s%s' % (province, city, district)
        # 获取地理坐标
        lng = get_geo(adress_detail)
        a_project = {
            "id": id,
            "name": obj.get("name", None),
            "adress_detail": adress_detail,
            "lnglat": lng,
            "position": obj.get("position", None),
            "company": obj.get("owner_company", None),
            "link": "../details_page?projectid=%s" % id
        }
        dct_projects.append(a_project)
    dct_projects = json.dumps(dct_projects)
    print("项目信息: ", dct_projects)
    return HttpResponse(dct_projects)

# api: /get_details_info
def get_details_info(request):
    '''
    param: projectid, sectionid, deviceid
    return:
    {
    "ProjectList":[{"id":1, "name":"隧道1左洞"},],
    "SectionList":[{"id":1, "name":"断面名1"},],
    "DeviceList":[{"id":1, "name":"device1"},],
    "ProjectAttr":{
        "id":1,
        "name":"隧道1左洞",
        "owner_company":"单位1",
        "manage_company":"单位1",
        "province":"四川",
        "city":"成都",
        "district":"温江",
        "position":"315线"},
    "SectionAttr":{
        "id":1,
        "name":"断面名1",
        "tunnel_name":"隧道1-左幅",
        "mileage":"12"},
    "DeviceAttr":{
        "id":1,
        "name":"device1",
        "device_sn":"sn_ASD",
        "firmware_version":"1",
        "type":1,
        "model":"e1",
        "ip":"1e2",
        "mac":"2e:11:23:11:22:34"},
    "List":[{
            "data1":"1111",
            "data2":"2222",
            "data3":"3333",
            "data4":"4444",
            "data5":"5555",
            "data6":"6666",
            "data7":"7777"},]
    }
    '''
    # print("00000000000000")
    # 指定project、section、device的id时用指定id,未指定id时缺省为None.
    pid = request.GET.get('projectid', None)
    sid = request.GET.get('sectionid', None)
    did = request.GET.get('deviceid', None)

    # 指定时用指定id,并且转id为int类型
    pid = int(pid) if pid else None
    sid = int(sid) if sid else None
    did = int(did) if did else None
    dsn = None
    print('get_details_info param: ', pid, sid, did)

    # 数据初始化
    lst_projects = []
    lst_sections = []
    lst_devices = []
    attr_project = {}
    attr_section = {}
    attr_device = {}
    lst_data = []

    # xxx工程档案
    projects = Project.objects \
        .values()   # .values("name", "owner_company", "manage_company", "province", "city", "district", "position")

    if projects:
        for project in projects:
            lst_projects.append({"id": project["id"], "name": project["name"]})
            if pid and project["id"] == pid:
                attr_project.update({
                    "id": project["id"],
                    "name": project["name"],
                    "owner_company": project["owner_company"],
                    "manage_company": project["manage_company"],
                    "province": project["province"],
                    "city": project["city"],
                    "district": project["district"],
                    "position": project["position"]
                })
        if not pid:
            pid = projects[0]["id"]
        if not attr_project:
            attr_project.update({
                "id": projects[0]["id"],
                "name": projects[0]["name"],
                "owner_company": projects[0]["owner_company"],
                "manage_company": projects[0]["manage_company"],
                "province": projects[0]["province"],
                "city": projects[0]["city"],
                "district": projects[0]["district"],
                "position": projects[0]["position"]
            })

    # xxx工程的断面信息
    sections = Section.objects \
        .filter(project__exact=pid) \
        .values()

    if sections:
        for section in sections:
            lst_sections.append({"id": section["id"], "name": section["name"]})
            if sid and section["id"] == sid:
                attr_section.update({
                    "id": section["id"],
                    "name": section["name"],
                    "tunnel_name": section["tunnel_name"],
                    "mileage": section["mileage"]
                })

        if not sid:
            sid = sections[0]["id"]
        if not attr_section:
            attr_section.update({
                "id": sections[0]["id"],
                "name": sections[0]["name"],
                "tunnel_name": section["tunnel_name"],
                "mileage": sections[0]["mileage"]
            })

    # xxx断面的设备信息
    devices = Device.objects \
        .filter(section__exact=sid) \
        .values()
    if devices:
        for device in devices:
            lst_devices.append({"id": device["id"], "name": device["name"]})
            if did and device["id"] == did:
                dsn = device["device_sn"]
                attr_device.update({
                    "id": device["id"],
                    "name": device["name"],
                    "type": device["type"],
                    "device_sn": device["device_sn"],
                    "soft_ver": device["soft_ver"],
                    "firm_ver": device["firm_ver"],
                    "status": device["status"]
                })
        if not did:
            dsn = devices[0]["device_sn"]
            # print(dsn)
        if not attr_device:
            attr_device.update({
                "id": devices[0]["id"],
                "name": devices[0]["name"],
                "type": devices[0]["type"],
                "device_sn": devices[0]["device_sn"],
                "soft_ver": devices[0]["soft_ver"],
                "firm_ver": devices[0]["firm_ver"],
                "status": devices[0]["status"]
            })
        # create_time = datetime.datetime.strftime(device["create_time"], "%Y-%m-%d-%H:%M:%S")
    # print("=======", lst_projects, lst_sections, lst_devices)

    # todo: xx隧道xx指标检测
    results = Result.objects \
        .filter(device_sn=dsn)\
        .order_by("id") \
        .values()
    # print(results)
    if results:
        # 只展示前四个记录
        for result in results[:4]:
            item = {'create_time': datetime.datetime.strftime(result["create_time"], "%Y-%m-%d-%H:%M:%S"),
                    'device_sn': result["device_sn"],
                    'timestamp': '3333',
                    'convergence': result["convergence"],
                    'sedimentation': result["sedimentation"],
                    'data6': '6666',
                    'data7': '7777',
                    }
            lst_data.append(item)


    ret = {"ProjectList": lst_projects,
            "SectionList": lst_sections,
            "DeviceList": lst_devices,
            "ProjectAttr": attr_project,
            "SectionAttr": attr_section,
            "DeviceAttr": attr_device,
            "List": lst_data}
    print("get_details_info ret: ", ret)

    return HttpResponse(json.dumps(ret))





# 公共方法
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



# # /details
# def details(request):
#     # print('+++++++++++', request.environ)
#     return render(request, 'details.html')

