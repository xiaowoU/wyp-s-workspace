from django.contrib import admin
from user_manage.models import Device, DevicePid, MeasureArea, ZeroOffset, UnifyParam
from utils.utils_code import *
from utils.cmd_pub import CmdPub
import datetime
# Register your models here.

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('section', 'type', 'name', 'device_sn', 'soft_ver', 'firm_ver', 'to_softver', 'control', 'upfile', 'status',)
    search_fields = ('status',)
    list_filter = ('section', 'type',)

    actions = ['get_all_info', 'set_start_stop', 'get_version', 'get_ver_update', 'set_start_update']

    def get_all_info(self, request, queryset):
        print("获取-设备all信息: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.type,
                "cmd": CMD_GET_ALLINFO,
                "device_sn": obj.device_sn,
                "data": {
                    "reserve": 0  # 保留字段
                }
            }
            CmdPub.send_cmd(dct_msg)
    get_all_info.short_description = '获取-设备all信息'
    get_all_info.style = 'background:green;color:white;'

    def set_start_stop(self, request, queryset):
        print("设置-设备启停: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.type,
                "cmd": CMD_SET_START_STOP,
                "device_sn": obj.device_sn,
                "data": {
                    "status": obj.status,    # 启动/停止/暂停
                }
            }
            CmdPub.send_cmd(dct_msg)
    set_start_stop.short_description = '设置-设备启停'
    set_start_stop.style = 'background:green;color:white;'

    def get_version(self, request, queryset):
        print("获取-软硬版本: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.type,
                "cmd": CMD_GET_VERSION,
                "device_sn": obj.device_sn,
                "data": {
                    "reserve": 0  # 保留字段
                }
            }
            CmdPub.send_cmd(dct_msg)
    get_version.short_description = '获取-软硬版本'
    get_version.style = 'background:green;color:white;'

    def get_ver_update(self, request, queryset):
        print("询问-x版本是否支持升级: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.type,
                "cmd": CMD_ENABLE_UPDATE,
                "device_sn": obj.device_sn,
                "data": {
                    "softver": obj.soft_ver,  # 要升级的软件版本
                }
            }
            CmdPub.send_cmd(dct_msg)
    get_ver_update.short_description = '询问-x版本是否支持升级'
    get_ver_update.style = 'background:green;color:white;'

    def set_start_update(self, request, queryset):
        print("传输-升级版本文件: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.type,
                "cmd": CMD_UPDATE_FILE,
                "device_sn": obj.device_sn,
                "data": {
                    "reserve": 0  # 保留字段
                }
            }
            CmdPub.send_cmd(dct_msg)
    set_start_update.short_description = '传输-升级版本文件'
    set_start_update.style = 'background:green;color:white;'

@admin.register(DevicePid)
class DevicePidAdmin(admin.ModelAdmin):
    list_display = ('device', 'angle_p', 'angle_i', 'speed_p', 'speed_i', 'max_acc', 'max_speed', 'max_angle', 'angle_err')
    search_fields = ('device',)
    list_filter = ('device',)

    actions = ['set_pid', ]

    def set_pid(self, request, queryset):
        print("设置-pid参数: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.device.type,
                "cmd": CMD_SET_PID,
                "device_sn": obj.device.device_sn,
                "data": {
                    "angle_p": obj.angle_p,  # Angle_P角度比例值
                    "angle_i": obj.angle_i,  # Angle_I角度积分值
                    "speed_p": obj.speed_p,  # Speed_P速度比例值
                    "speed_i": obj.speed_i,  # Speed_I速度积分值
                    "max_acc": obj.max_acc,  # Max_Accel最大加速度值
                    "max_speed": obj.max_speed,  # Max_Speed最大速度值
                    "max_angle": obj.max_angle,  # Max_Angle最大旋转角度值
                    "angle_err": obj.angle_err,  # Angle_Erro角度最大误差阈值
                }
            }
            CmdPub.send_cmd(dct_msg)
    set_pid.short_description = '设置-pid参数'
    set_pid.style = 'background:green;color:white;'


@admin.register(MeasureArea)
class MeasureAreaAdmin(admin.ModelAdmin):
    list_display = ('device', 'name', 're_times', 'start_angle', 'end_angle', 'cycle')    # 'turns_flag',
    search_fields = ('device',)
    list_filter = ('device',)

    actions = ['set_area', 'get_area']

    def set_area(self, request, queryset):
        print("设置-测量区段: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.device.type,
                "cmd": CMD_SET_MEASURE_AREA,
                "device_sn": obj.device.device_sn,
                "data": {
                    "repeat_times": obj.re_times,      # 区段测点重测次数
                    "precision": obj.scan_resolution,  # 区段测量精度
                    "start_angle": obj.start_angle,    # 区段起始角度
                    "end_angle": obj.end_angle,        # 区段结束角度
                }
            }
            CmdPub.send_cmd(dct_msg)
    set_area.short_description = '设置-测量区段'
    set_area.style = 'background:green;color:white;'

    def get_area(self, request, queryset):
        print("获取-测量区段: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.device.type,
                "cmd": CMD_GET_MEASURE_AREA,
                "device_sn": obj.device.device_sn,
                "data": {
                    "reserve": 0  # 保留字段
                }
            }
            CmdPub.send_cmd(dct_msg)
    get_area.short_description = '获取-测量区段'
    get_area.style = 'background:green;color:white;'


@admin.register(ZeroOffset)
class ZeroOffsetAdmin(admin.ModelAdmin):
    list_display = ('device', 'zero_offset',)
    search_fields = ('device',)
    list_filter = ('device',)

    actions = ['set_zero_offset', 'get_zero_offset']

    def set_zero_offset(self, request, queryset):
        print("设置-零偏参数: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.device.type,
                "cmd": CMD_SET_ZERO_OFFSET,
                "device_sn": obj.device.device_sn,
                "data": {
                    "zero_offset": obj.zero_offset  # 零偏参数
                }
            }
            CmdPub.send_cmd(dct_msg)
    set_zero_offset.short_description = '设置-零偏参数'
    set_zero_offset.style = 'background:green;color:white;'

    def get_zero_offset(self, request, queryset):
        print("获取-零偏参数: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.device.type,
                "cmd": CMD_GET_ZERO_OFFSET,
                "device_sn": obj.device.device_sn,
                "data": {
                    "reserve": 0  # 保留字段
                }
            }
            CmdPub.send_cmd(dct_msg)
    get_zero_offset.short_description = '获取-零偏参数'
    get_zero_offset.style = 'background:green;color:white;'


@admin.register(UnifyParam)
class UnifyParamAdmin(admin.ModelAdmin):
    list_display = ('device', 'meas_intvl', 'up_intvl', 'meas_mode', 'range',
                    'server_ip', 'server_bak_ip', 'server_port', 'server_bak_port',
                    'bak_use_date', 'server_bak_switch', 'network_status', 'meas_num',
                    'reserve',
                    'addr_storage', 'addr_upload', 'init_val', 'firm_ver',
                    'soft_ver', 'power_type', 'charge_state', 'battery_volt',)
    fields = ('device', 'meas_intvl', 'up_intvl', 'meas_mode', 'range',
              'server_ip', 'server_bak_ip', 'server_port', 'server_bak_port',
              'bak_use_date', 'server_bak_switch', 'network_status', 'meas_num',)
    search_fields = ('device',)
    list_filter = ('device',)

    actions = ['set_param', 'get_param']

    def set_param(self, request, queryset):
        print("设置-一体化参数: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.device.type,
                "cmd": CMD_SET_UNIFY_PARAM,
                "device_sn": obj.device.device_sn,
                "data": {
                    "cur_time": str(datetime.datetime.now()),         # 当前时间8B
                    "meas_intvl": obj.meas_intvl,              # 测量(采集)频率4B
                    "up_intvl": obj.up_intvl,                  # 上传频率4B
                    "meas_mode": obj.meas_mode,                # 测量值模式1B
                    "range": obj.range,                    # 测距量程1B
                    "server_ip": obj.server_ip,                # 服务器 - IP4B
                    "server_bak_ip": obj.server_bak_ip,        # 服务器备用 - IP4B
                    "server_port": obj.server_port,            # 服务器 - IP对应的端口2B
                    "server_bak_port": obj.server_bak_port,    # 服务器备用 - IP对应的端口2B
                    "bak_use_date": str(obj.bak_use_date),            # 服务器备用 - IP启用日期4B
                    "server_bak_switch": obj.server_bak_switch,# 服务器B开关1B
                    "network_status": obj.network_status,      # 网络工作状态1B
                    "meas_num": obj.meas_num,               # 测量(采集)点数(1B)
                }
            }
            CmdPub.send_cmd(dct_msg)
    set_param.short_description = '设置-一体化参数'
    set_param.style = 'background:green;color:white;'

    def get_param(self, request, queryset):
        print("获取-一体化参数: ", len(queryset))
        for obj in queryset:
            dct_msg = {
                "type": obj.device.type,
                "cmd": CMD_GET_UNIFY_PARAM,
                "device_sn": obj.device.device_sn,
                "data": {
                    "reserve": 0  # 保留字段
                }
            }
            CmdPub.send_cmd(dct_msg)
    get_param.short_description = '获取-一体化参数'
    get_param.style = 'background:green;color:white;'

