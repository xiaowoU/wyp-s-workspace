from pyecharts.charts import Bar
from pyecharts import options as opts

from user_manage.models import Project
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType


def read_geoinfo():
    # objs = Project.objects.all().values_list()
    # objs = Project.objects.all().values("name", "province", "city", "district", "position", "create_time")
    objs = Project.objects\
        .values("name", "province", "city", "district", "position",
                                                       "create_time")
    dct_position = {}
    dct_map_point = {}
    for obj in objs:
        # 整理隧道navigation
        positon = obj.get("position", None)
        name = obj.get("name", None)
        if positon in dct_position:
            lst_name = dct_position[positon]
            lst_name.append(name)
            dct_position[positon] = lst_name
        else:
            dct_position[positon] = [name, ]

        # 整理隧道地图位置
        province = obj.get("province", None)
        city = obj.get("city", None)
        district = obj.get("district", None)
        dct_map_point[name] = [province, city, district, positon]
    return dct_position, dct_map_point

# geo图
def geo_scatter(address, value) -> Geo:
    aa = [list(z) for z in zip(address, value)]
    # print(aa)
    c = (
        Geo()
        .add_schema(maptype="china")
        .add(
            series_name="项目分布",    #图题
            data_pair=aa,
            type_=ChartType.EFFECT_SCATTER,   #地图类型
            is_selected=True,
        )
        .add_coordinate("衡阳", 112.37, 26.53)    # 新增一个坐标点
        # coordinate = c.get_coordinate("衡阳")   # 查询坐标
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  #设置是否显示标签
        .set_global_opts(
                # visualmap_opts=opts.VisualMapOpts(max_=400),    #设置legend显示的最大值
                title_opts=opts.TitleOpts(title="Geo-项目分布图"),   #左上角标题
        )
    )
    return c

def generate_map():
    # 查询数据库得到当前项目分布信息
    dct_position, dct_map_point = read_geoinfo()
    # 将信息转化为图表数据
    dct_tmp = {}
    address, value = [], []
    # '隧道1右洞': ('四川', '成都', '温江区', '315线'),
    for k, v in dct_map_point.items():
        point_value = '-'.join(v) + "--%s" % k
        if v[1] in dct_tmp:
            locate = v.pop(1)
            lst_project = dct_tmp[locate]
            lst_project.append(point_value)
            dct_tmp[locate] = lst_project
        else:
            dct_tmp[v.pop(1)] = [point_value, ]
    print(dct_tmp)
    for k, v in dct_tmp.items():
        address.append(k)
        value.append(v)
    # 生成项目分布热力图
    heatmap = geo_scatter(address, value)
    return heatmap
    # heatmap.render(path="test_heatmap.html")





if __name__ == '__main__':
    '''
    dct_position = {'315线': ['隧道1右洞', '隧道2左洞'],
          '999国道': ['隧道3333左洞', '隧道3333右洞']}
    dct_map_point = {'隧道1右洞': ('四川', '成都', '温江区', '315线'),
          '隧道2左洞': ('四川', '成都', '郫都区', '315线'),
          '隧道3333左洞': ('贵州', '贵阳', '白云区', '999国道'),
          '隧道3333右洞': ('贵州', '贵阳', '白云区', '999国道')}
    '''

    pass