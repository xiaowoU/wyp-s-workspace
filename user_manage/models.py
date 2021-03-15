from django.db import models

# Create your models here.
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from utils.base_model import BaseModel, DataModel
from utils.utils_code import WARN, TYPE, STATUS, CHARGE_STATUS, MEAS_RANGE
import uuid

class Company(BaseModel):
    # id = models.AutoField(primary_key=True)
    # company_id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(verbose_name='单位名', max_length=64)
    address = models.CharField(verbose_name='地址', max_length=64, null=True, blank=True)
    key_person = models.CharField(verbose_name='关键人物', max_length=64, null=True, blank=True)
    contacts = models.CharField(verbose_name='联系人', max_length=64, null=True, blank=True)
    manager = models.CharField(verbose_name='负责人', max_length=64, null=True, blank=True)
    contract_number = models.CharField(verbose_name='合同编号', max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_company'
        verbose_name = u'单位表'
        verbose_name_plural = verbose_name
        app_label = 'user_manage'

# # AUTH_USER_MODEL = 'user_manage.User'  # 在设置中声明
class User(AbstractUser, BaseModel):
    # help_text="xx", validators=[validators.RegexValidator(regex=r"^1111$", message="xxx！")], error_messages={"unique": "已存在！", "required": "非空！"}
    tel = models.CharField(verbose_name='联系电话', max_length=64, blank=True, null=True)
    wechat = models.CharField(verbose_name='微信', max_length=64, blank=True, null=True)
    company = models.ForeignKey('user_manage.Company', verbose_name='所属单位', to_field='id', on_delete=models.DO_NOTHING, blank=True, null=True, default='')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_user'
        verbose_name = u'用户表'
        verbose_name_plural = verbose_name
        app_label = 'user_manage'

class Project(BaseModel):
    name = models.CharField(verbose_name='隧道名', max_length=128)
    owner_company = models.CharField(verbose_name='业主单位', max_length=128, null=True, blank=True)
    manage_company = models.CharField(verbose_name='运营单位', max_length=128, null=True, blank=True)
    province = models.CharField(verbose_name='所属省', max_length=32)
    city = models.CharField(verbose_name='所属市', max_length=32)
    district = models.CharField(verbose_name='所属区/县', max_length=32)
    position = models.CharField(verbose_name='位置详情', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_project'
        verbose_name = u'项目表'
        verbose_name_plural = verbose_name
        app_label = 'user_manage'

class OperateCompany(BaseModel):
    manage_company = models.CharField(verbose_name='运营单位', max_length=128)
    superior_company = models.CharField(verbose_name='上级', max_length=128, null=True, blank=True)
    contacts = models.CharField(verbose_name='联系人', max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.manage_company

    class Meta:
        db_table = 't_operate_company'
        verbose_name = u'运营单位表'
        verbose_name_plural = verbose_name
        app_label = 'user_manage'

class Section(BaseModel):
    name = models.CharField(verbose_name='断面名称', max_length=64)
    tunnel_name = models.CharField(verbose_name='隧道边幅名称', max_length=64)
    mileage = models.CharField(verbose_name='里程', max_length=64)
    project = models.ForeignKey('user_manage.Project', verbose_name='所属工程', to_field='id', on_delete=models.DO_NOTHING, blank=True, null=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_section'
        verbose_name = u'断面表'
        verbose_name_plural = verbose_name
        app_label = 'user_manage'

class Position(BaseModel):
    # todo: circular arc position
    device_sn = models.CharField(verbose_name='设备编号', max_length=128)
    position = models.CharField(verbose_name='安装位置', max_length=128)

    def __unicode__(self):
        return self.device_sn

    class Meta:
        db_table = 't_position'
        verbose_name = u'设备位置表'
        verbose_name_plural = verbose_name
        app_label = 'user_manage'


class Warning(BaseModel):
    name = models.CharField(verbose_name='预警名', max_length=128)
    # Ⅳ级（一般）、Ⅲ级（较重）、Ⅱ级（严重）、Ⅰ级（特别严重）
    level = models.IntegerField(verbose_name='预警级别', choices=WARN, default=4)
    notify_obj = models.CharField(verbose_name='通知对象', max_length=128)
    desc = models.CharField(verbose_name='预警信息描述', max_length=256)
    project = models.ForeignKey('user_manage.Project', verbose_name='所属工程', to_field='id', on_delete=models.DO_NOTHING, blank=True, null=True, default='')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_warning'
        verbose_name = u'预警信息表'
        verbose_name_plural = verbose_name
        app_label = 'warning_manage'






class Device(BaseModel):
    section = models.ForeignKey('user_manage.Section', verbose_name='所属断面', on_delete=models.DO_NOTHING, blank=True, null=True)
    type = models.IntegerField(verbose_name='设备类型', blank=True, null=True, choices=TYPE)
    name = models.CharField(verbose_name='设备名称', max_length=128, blank=True, null=True)
    device_sn = models.CharField(verbose_name='设备编号', max_length=128)
    soft_ver = models.CharField(verbose_name='软件版本', max_length=32, blank=True, null=True)
    firm_ver = models.CharField(verbose_name='固件版本', max_length=32, blank=True, null=True)
    to_softver = models.CharField(verbose_name='升级到版本', max_length=32, blank=True, null=True)
    control = models.IntegerField(verbose_name='控制测量启停', blank=True, null=True, choices=STATUS)
    upfile = models.FileField(verbose_name='上传升级文件', max_length=100, blank=True, null=True)
    status = models.BooleanField(verbose_name='在线状态', )

    def __str__(self):
        ret = None
        if self.type:
            for i in TYPE:
                if self.type == i[0]:
                    type_name = i[1]
                    ret = f'{type_name}-{self.device_sn}'
        else:
            ret = f'None-%s' % self.device_sn
        return ret

    class Meta:
        # managed = False
        db_table = 't_device'
        verbose_name = u'管理-设备列表'
        verbose_name_plural = verbose_name
        app_label = 'test_install'


class DevicePid(BaseModel):
    device = models.OneToOneField('test_install.Device', verbose_name='所属设备', on_delete=models.CASCADE, blank=True, null=True)
    angle_p = models.CharField(verbose_name='角度比例值', max_length=32, blank=True, null=True)
    angle_i = models.CharField(verbose_name='角度积分值', max_length=32, blank=True, null=True)
    speed_p = models.CharField(verbose_name='速度比例值', max_length=32, blank=True, null=True)
    speed_i = models.CharField(verbose_name='速度积分值', max_length=32, blank=True, null=True)
    max_acc = models.CharField(verbose_name='最大加速度值', max_length=32, blank=True, null=True)
    max_speed = models.CharField(verbose_name='最大速度值', max_length=32, blank=True, null=True)
    max_angle = models.CharField(verbose_name='最大旋转角度值', max_length=32, blank=True, null=True)
    angle_err = models.CharField(verbose_name='角度最大误差阈值', max_length=32, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_device_pid'
        verbose_name = u'设置-pid参数'
        verbose_name_plural = verbose_name
        app_label = 'test_install'

class MeasureArea(BaseModel):
    device = models.ForeignKey('test_install.Device', verbose_name='所属设备', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(verbose_name='区段名', max_length=128)
    re_times = models.CharField(verbose_name='单点重复测量次数', max_length=64)
    scan_resolution = models.CharField(verbose_name='扫面分辨率', max_length=64)
    start_angle = models.CharField(verbose_name='起始角度', max_length=64)
    end_angle = models.CharField(verbose_name='终止角度', max_length=64)
    turns_flag = models.CharField(verbose_name='圈数标志', max_length=64, blank=True, null=True)
    cycle = models.CharField(verbose_name='采集周期', max_length=64, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_measure_area'
        verbose_name = u'设置-测量区段'
        verbose_name_plural = verbose_name
        app_label = 'test_install'


class ZeroOffset(BaseModel):
    device = models.OneToOneField('test_install.Device',  verbose_name='所属设备', on_delete=models.CASCADE, blank=True, null=True)
    zero_offset = models.CharField(verbose_name='零偏参数', max_length=32, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_zero_offset'
        verbose_name = u'设置-零偏参数'
        verbose_name_plural = verbose_name
        app_label = 'test_install'

class UnifyParam(BaseModel):
    device = models.OneToOneField('test_install.Device', verbose_name='所属设备', on_delete=models.CASCADE, blank=True, null=True)
    meas_intvl = models.CharField(verbose_name='测量(采集)频率', max_length=32, blank=True, null=True)
    up_intvl = models.CharField(verbose_name='上传频率', max_length=32, blank=True, null=True)
    meas_mode = models.CharField(verbose_name='测量值模式', max_length=32, blank=True, null=True)
    range = models.CharField(verbose_name='测距量程', max_length=32, blank=True, null=True,  choices=MEAS_RANGE)
    server_ip = models.CharField(verbose_name='服务器', max_length=32, blank=True, null=True)
    server_bak_ip = models.CharField(verbose_name='备用服务器', max_length=32, blank=True, null=True)
    server_port = models.CharField(verbose_name='服务器端口', max_length=32, blank=True, null=True)
    server_bak_port = models.CharField(verbose_name='备用服务器端口', max_length=32, blank=True, null=True)
    bak_use_date = models.DateTimeField(verbose_name='备用服务器启用日期', blank=True, null=True)
    server_bak_switch = models.BooleanField(verbose_name='服务器B开关', )
    network_status = models.CharField(verbose_name='网络工作状态', max_length=32, blank=True, null=True)
    meas_num = models.CharField(verbose_name='测量点数', max_length=32, blank=True, null=True)

    reserve = models.CharField(verbose_name='留用', max_length=32, blank=True, null=True)
    # 只读数据
    addr_storage = models.CharField(verbose_name='记录存储地址', max_length=32, blank=True, null=True)
    addr_upload = models.CharField(verbose_name='记录上传地址', max_length=32, blank=True, null=True)
    init_val = models.CharField(verbose_name='测量相对值的初值', max_length=32, blank=True, null=True)
    firm_ver = models.CharField(verbose_name='硬件版本', max_length=32, blank=True, null=True)
    soft_ver = models.CharField(verbose_name='软件版本', max_length=32, blank=True, null=True)
    power_type = models.CharField(verbose_name='系统运行的电源类型', max_length=32, blank=True, null=True)
    charge_state = models.CharField(verbose_name='电池充电状态', max_length=32, blank=True, null=True, choices=CHARGE_STATUS)
    battery_volt = models.CharField(verbose_name='电池电压', max_length=32, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_unify_param'
        verbose_name = u'设置-一体化参数'
        verbose_name_plural = verbose_name
        app_label = 'test_install'



class CollectRaw(DataModel):
    device_sn = models.CharField(verbose_name='设备编号', max_length=128, blank=True, null=True)
    # scan_time = models.CharField(verbose_name='扫描时间', max_length=32, blank=True, null=True)
    # scan_points = models.CharField(verbose_name='本帧扫描点数', max_length=32, blank=True, null=True)
    # start_angle = models.CharField(verbose_name='本帧起始角度', max_length=32, blank=True, null=True)
    # step = models.CharField(verbose_name='本帧分辨率', max_length=32, blank=True, null=True)
    angle = models.CharField(verbose_name='当前点角度', max_length=32, blank=True, null=True)
    range = models.CharField(verbose_name='当前点距离', max_length=32, blank=True, null=True)
    # turns_flag = models.IntegerField(verbose_name='圈数标志', )
    # times = models.IntegerField(verbose_name='次数编号', )
    # timestamp = models.DateTimeField(verbose_name='数据接收时间', )

    class Meta:
        # managed = False
        db_table = 't_collect_raw'
        verbose_name = u'轮廓数据'
        verbose_name_plural = verbose_name
        app_label = 'data_display'

class Result(DataModel):
    device_sn = models.CharField(verbose_name='设备编号', max_length=128)
    convergence = models.CharField(verbose_name='收敛值', max_length=64, blank=True, null=True)
    sedimentation = models.CharField(verbose_name='沉降值', max_length=64, blank=True, null=True)
    # timestamp = models.DateTimeField(verbose_name='计算时间')

    def __unicode__(self):
        return self.device_sn

    class Meta:
        db_table = 't_result'
        verbose_name = u'数据处理结果'
        verbose_name_plural = verbose_name
        app_label = 'data_display'

class UnifyDataRaw(DataModel):
    device_sn = models.CharField(verbose_name='设备编号', max_length=128, blank=True, null=True)
    meas_time = models.DateTimeField(verbose_name='当前第一点时间', blank=True, null=True)
    index = models.CharField(verbose_name='上传流水号', max_length=64, blank=True, null=True)
    value = models.CharField(verbose_name='测量值(0.01mm)', max_length=64, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_unify_data_raw'
        verbose_name = u'一体化数据'
        verbose_name_plural = verbose_name
        app_label = 'data_display'








