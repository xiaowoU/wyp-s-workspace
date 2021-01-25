'''==================================================
@IDE: PyCharm
@Time : 2020/12/23 15:17 
@Author : wyp
@File : proxy.py 
=================================================='''
from pyecharts.charts import Bar
from pyecharts import options as opts

from user_manage.models import Project, Result
from pyecharts import options as opts
from pyecharts.charts import Geo, Line
from pyecharts.globals import ChartType, SymbolType
import datetime

class ReadGeoInfo(object):
    def __init__(self):
        self.dct_position = {}
        self.dct_map_point = {}

    def read_geoinfo(self):
        '''
        dct_position = {'315线': ['隧道1右洞', '隧道2左洞'],
              '999国道': ['隧道3333左洞', '隧道3333右洞']}
        dct_map_point = {'隧道1右洞': ('四川', '成都', '温江区', '315线'),
              '隧道2左洞': ('四川', '成都', '郫都区', '315线'),
              '隧道3333左洞': ('贵州', '贵阳', '白云区', '999国道'),
              '隧道3333右洞': ('贵州', '贵阳', '白云区', '999国道')}
        '''
        objs = Project.objects\
            .values("name", "province", "city", "district", "position")

        for obj in objs:
            # 整理隧道navigation
            positon = obj.get("position", None)
            name = obj.get("name", None)
            if positon in self.dct_position:
                lst_name = self.dct_position[positon]
                lst_name.append(name)
                self.dct_position[positon] = lst_name
            else:
                self.dct_position[positon] = [name, ]
            # 整理隧道地图位置
            province = obj.get("province", None)
            city = obj.get("city", None)
            district = obj.get("district", None)
            self.dct_map_point[name] = [province, city, district, positon]

    # 绘制geo对象
    @classmethod
    def geo_object(cls, x_data, y_data) -> Geo:
        aa = [list(z) for z in zip(x_data, y_data)]
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
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False, #设置是否显示标签数据
                                                       ))
            .set_global_opts(
                    # visualmap_opts=opts.VisualMapOpts(max_=400),    #设置legend显示的最大值
                    title_opts=opts.TitleOpts(title="Geo-项目分布图"),   #左上角标题
            )
        )
        return c

    def generate_geo(self):
        # 查询数据库得到当前项目分布信息
        self.read_geoinfo()
        # 将信息转化为图表数据
        dct_tmp = {}
        address, value = [], []
        # '隧道1右洞': ('四川', '成都', '温江区', '315线'),
        for k, v in self.dct_map_point.items():
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
        # 生成geo对象
        geoobj = self.geo_object(address, value)
        return geoobj
        # geoobj.render(path="test_heatmap.html")

class ReadDataInfo(object):
    def __init__(self):
        self.device_status = {}

    def read_lineinfo(self):
        '''
        device_status = {"sn_001": [{timestamp: [convergence, sedimentation]},
                                    {timestamp: [convergence, sedimentation]},]
                        "sn_002": [{timestamp: [convergence, sedimentation]},
                                    {timestamp: [convergence, sedimentation]},]
                        }
        '''
        objs = Result.objects\
            .values("device_sn", "timestamp", "convergence", "sedimentation", "section")
        if objs:
            for obj in objs:
                device_sn = obj.get("device_sn")
                timestamp = obj.get("timestamp")
                dt = datetime.datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
                convergence = obj.get("convergence")
                sedimentation = obj.get("sedimentation")
                data = {dt: [convergence, sedimentation]}
                if device_sn in self.device_status:
                    lst_data = self.device_status[device_sn]
                    lst_data.append(data)
                    self.device_status[device_sn] = lst_data
                else:
                    self.device_status[device_sn] = [data, ]

    # 绘制line对象
    @classmethod
    def line_object(cls, device_sn, device_info) -> Geo:
        x_data = []
        y_data1, y_data2 = [], []
        if device_info:
            for a_info in device_info:
                # {timestamp: [convergence, sedimentation]}
                for timestamp, lst_result in a_info.items():
                    x_data.append(timestamp)
                    y_data1.append(lst_result[0])
                    y_data2.append(lst_result[1])

        line = (
            Line()
                .set_global_opts(
                title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle=device_sn),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
                .add_xaxis(xaxis_data=x_data)
                .add_yaxis(
                series_name="收敛图",
                y_axis=y_data1,
                symbol="emptyCircle",   # 坐标点形状
                is_symbol_show=True,    # 显示坐标点
                symbol_size=8,          # 坐标点大小
                label_opts=opts.LabelOpts(is_show=False),   # 显示y轴数值
            )
                .add_yaxis(
                series_name="沉降图",
                y_axis=y_data2,
                symbol="emptyCircle",
                is_symbol_show=True,
                symbol_size=8,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )
        return line


    def generate_line(self, device_sn):
        self.read_lineinfo()
        if self.device_status:
            device_info = self.device_status.get(device_sn, '')
            lineobj = self.line_object(device_sn, device_info)
        return lineobj







if __name__ == '__main__':

    pass