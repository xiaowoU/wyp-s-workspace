from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from user_manage.models import Project, Result
import json

# /map_page
def map_page(request):
    return render(request, "dev_map_page.html")


# /get_project_info
def get_project_info(request):
    # print('+++++++++++', request.environ)
    # 读取项目信息
    '''
    dct_projects:
     [{'adress_detail': '四川成都温江', '项目名字': '隧道1左洞', '位置': '315线', '管理单位': '暂无', '数据链接': '暂无'},
     {'adress_detail': '江苏苏州姑苏区', '项目名字': '隧道3左洞', '位置': '233国道', '管理单位': '暂无', '数据链接': '暂无'}]
    '''
    dct_projects = []
    objs = Project.objects \
        .exclude(is_delete=1) \
        .values("name", "province", "city", "district", "position")
    # .values("name", "province", "city", "district", "position")

    for obj in objs:
        # print(obj)
        # 整理隧道navigation
        name = obj.get("name", None)
        province = obj.get("province", None)
        city = obj.get("city", None)
        district = obj.get("district", None)
        position = obj.get("position", None)
        adress_detail = '%s%s%s' % (province, city, district)
        a_project = {
            "adress_detail": adress_detail,
            "项目名字": name,
            "位置": position,
            "管理单位": "暂无",
            "数据链接": "暂无"
        }
        dct_projects.append(a_project)
    dct_projects = json.dumps(dct_projects)
    print("项目信息: ", dct_projects)
    return HttpResponse(dct_projects)
    # return render(request, "dev_map_page.html", dct_city)


# # /details
# def details(request):
#     # print('+++++++++++', request.environ)
#     return render(request, 'details.html')

